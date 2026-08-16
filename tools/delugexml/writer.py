"""Serializzazione nello stile esatto del writer del firmware Deluge.

Due modalita':

  serialize(doc, table, rebuild=False)   [default, "chirurgica"]
      I sottoalberi non modificati vengono ricopiati byte per byte dal
      sorgente originale. Solo i nodi toccati (o creati) vengono riscritti
      usando le regole di formato. Il round-trip e' byte-esatto per
      costruzione e il rischio di formattazione resta confinato a cio' che
      abbiamo effettivamente cambiato.

  serialize(doc, table, rebuild=True)    ["rebuild"]
      Ogni nodo viene riscritto dalle regole. E' il test che dimostra che le
      regole sono corrette: se il rebuild di un file reale e' byte-identico
      all'originale, possiamo generare nodi nuovi con fiducia.

MODELLO DI FORMATO (osservato, non ipotizzato)
----------------------------------------------
La scelta fra "attributi su una riga" e "un attributo per riga" non dipende
dal numero di attributi ne' dalla lunghezza della riga: e' una proprieta'
fissa del punto del codice del firmware che scrive quell'elemento.

Il parametro appreso e' `inline_prefix`: quanti attributi finiscono sulla
stessa riga di `<tag`. I valori osservati sono tre:

    inline_prefix = n_attributi   ->  <tag a="1" b="2" />
    inline_prefix = 0             ->  <tag
                                          a="1"
                                          b="2" />
    0 < inline_prefix < n         ->  <tag a="1" b="2"        (ibrido)
                                          c="3" />
                                      (osservato su <midiKnob>: il firmware
                                       scrive channel e ccNumber inline e poi
                                       delega il resto alla classe base)

La forma dipende anche dall'insieme di attributi presenti: <device port="…">
e' inline, <device name=… vendorId=… productId=…> e' multiline. La tabella e'
quindi indicizzata su (percorso, firma degli attributi) con ripiego su
percorso e poi su tag.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

INDENT = '\t'
_ATTR = re.compile(r'([\w.:-]+)\s*=\s*"([^"]*)"')


class FormatTable:
    """Mappa (percorso, firma attributi) -> inline_prefix, appresa dal corpus."""

    def __init__(self):
        self.by_sig: dict[str, int] = {}      # "path|a,b,c" -> inline_prefix
        self.by_tag_sig: dict[str, int] = {}  # "tag|a,b,c"  -> inline_prefix
        self.by_path: dict[str, int] = {}     # "path"       -> inline_prefix
        self.by_tag: dict[str, int] = {}      # "tag"        -> inline_prefix
        self.conflicts: dict[str, dict] = {}
        self.default = 0                      # multiline

    # ------------------------------------------------------------ learning
    def learn(self, docs) -> 'FormatTable':
        sig_votes = defaultdict(Counter)
        tag_sig_votes = defaultdict(Counter)
        path_votes = defaultdict(Counter)
        tag_votes = defaultdict(Counter)

        for doc in docs:
            for path, node in doc.path_iter():
                if not node.attrs or node.span is None:
                    continue
                pref = observed_inline_prefix(doc.raw, node)
                if pref is None:
                    continue
                s = sig_of(node)
                sig_votes[f'{path}|{s}'][pref] += 1
                tag_sig_votes[f'{node.tag}|{s}'][pref] += 1
                path_votes[path][pref] += 1
                tag_votes[node.tag][pref] += 1

        for key, votes in sig_votes.items():
            self.by_sig[key] = votes.most_common(1)[0][0]
            if len(votes) > 1:
                self.conflicts[key] = dict(votes)
        for key, votes in tag_sig_votes.items():
            self.by_tag_sig[key] = votes.most_common(1)[0][0]
            if len(votes) > 1:
                self.conflicts['tag:' + key] = dict(votes)
        for key, votes in path_votes.items():
            self.by_path[key] = votes.most_common(1)[0][0]
        for key, votes in tag_votes.items():
            self.by_tag[key] = votes.most_common(1)[0][0]
        return self

    def inline_prefix(self, path: str, node) -> int:
        # dal piu' specifico al piu' generico. Il livello "tag|firma" e' quello
        # che generalizza fra tipi di file diversi (song/kit/synth), perche' nel
        # firmware l'elemento e' scritto sempre dalla stessa classe C++
        # indipendentemente da dove sia annidato.
        s = sig_of(node)
        for k, d in ((f'{path}|{s}', self.by_sig),
                     (f'{node.tag}|{s}', self.by_tag_sig),
                     (path, self.by_path),
                     (node.tag, self.by_tag)):
            if k in d:
                return d[k]
        return self.default

    # ------------------------------------------------------------------ io
    def save(self, path):
        Path(path).write_text(json.dumps({
            'by_sig': self.by_sig, 'by_tag_sig': self.by_tag_sig,
            'by_path': self.by_path, 'by_tag': self.by_tag,
            'conflicts': self.conflicts, 'default': self.default,
        }, indent=1, sort_keys=True), encoding='utf-8')

    @classmethod
    def load(cls, path) -> 'FormatTable':
        d = json.loads(Path(path).read_text(encoding='utf-8'))
        t = cls()
        t.by_sig = d.get('by_sig', {})
        t.by_tag_sig = d.get('by_tag_sig', {})
        t.by_path = d.get('by_path', {})
        t.by_tag = d.get('by_tag', {})
        t.conflicts = d.get('conflicts', {})
        t.default = d.get('default', 0)
        return t


def sig_of(node) -> str:
    return ','.join(k for k, _ in node.attrs)


def open_tag_text(raw: str, start: int) -> str:
    """Il tag di apertura completo a partire da `start`, quote-aware."""
    i, in_quotes = start, False
    while i < len(raw):
        c = raw[i]
        if c == '"':
            in_quotes = not in_quotes
        elif c == '>' and not in_quotes:
            return raw[start:i + 1]
        i += 1
    return raw[start:]


def observed_inline_prefix(raw: str, node) -> int | None:
    """Quanti attributi stanno sulla stessa riga di `<tag`, nel sorgente."""
    if node.span is None:
        return None
    txt = open_tag_text(raw, node.span[0])
    nl = txt.find('\n')
    if nl < 0:
        return len(node.attrs)
    # conta gli attributi che iniziano prima del primo a capo,
    # partendo dopo il nome del tag
    m = re.match(r'<[\w.:-]+', txt)
    start = m.end() if m else 1
    return sum(1 for a in _ATTR.finditer(txt, start) if a.start() < nl)


# --------------------------------------------------------------- serializing

def _subtree_dirty(node) -> bool:
    if node.dirty or node.span is None:
        return True
    return any(_subtree_dirty(c) for c in node.children)


def _emit(node, depth: int, path: str, table: FormatTable, raw: str,
          rebuild: bool, out: list) -> None:
    ind = INDENT * depth

    if not rebuild and not _subtree_dirty(node):
        s, e = node.span
        out.append(ind + raw[s:e].lstrip('\t\n '))
        return

    n = len(node.attrs)
    pref = min(table.inline_prefix(path, node), n) if n else 0
    has_kids = bool(node.children)
    has_text = bool(node.text) and not has_kids
    closes_empty = node.self_closing and not has_kids and not has_text

    head = f'{ind}<{node.tag}' + ''.join(
        f' {k}="{v}"' for k, v in node.attrs[:pref])

    # Elemento senza figli e senza testo ma con tag di chiusura esplicito.
    # La chiusura sta sulla stessa riga solo se anche gli attributi erano
    # inline: <setting name="…" value="1"></setting>. Se gli attributi sono
    # uno per riga il firmware manda a capo anche la chiusura:
    #     <osc2
    #         timeStretchAmount="0">
    #     </osc2>
    # (osservato rispettivamente in CommunityFeatures.XML e in Industrial.XML)
    empty_pair = not node.self_closing and not has_kids and not has_text

    if pref == n:                                   # tutto su una riga
        if closes_empty:
            out.append(head + ' />')
            return
        if has_text:
            out.append(f'{head}>{node.text}</{node.tag}>')
            return
        if empty_pair:
            out.append(f'{head}></{node.tag}>')
            return
        out.append(head + '>')
    else:                                           # resto uno per riga
        out.append(head)
        ai = INDENT * (depth + 1)
        rest = node.attrs[pref:]
        for k, (name, val) in enumerate(rest):
            line = f'{ai}{name}="{val}"'
            if k == len(rest) - 1:
                if closes_empty:
                    out.append(line + ' />')
                    return
                line += '>'
            out.append(line)
        if has_text:
            out[-1] += f'{node.text}</{node.tag}>'
            return

    for c in node.children:
        _emit(c, depth + 1, f'{path}/{c.tag}', table, raw, rebuild, out)
    out.append(f'{ind}</{node.tag}>')


def serialize(doc, table: FormatTable | None = None, rebuild: bool = False) -> str:
    table = table or FormatTable()
    out: list[str] = [doc.prolog]
    for r in doc.roots:
        _emit(r, 0, r.tag, table, doc.raw, rebuild, out)
    s = '\n'.join(out)
    return s + '\n' if doc.trailing_newline else s


def write_file(doc, path, table=None, rebuild=False) -> None:
    Path(path).write_bytes(
        serialize(doc, table, rebuild).encode('utf-8', 'surrogateescape'))
