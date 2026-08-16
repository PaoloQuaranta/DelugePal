"""Parser tollerante per gli XML scritti dal firmware Deluge.

Perche' non xml.etree: il writer del firmware produce file che un parser XML
conforme rifiuta. Difetti osservati e riprodotti fedelmente qui:

  1. '&' non escapato dentro i valori di attributo, quando il nome di un
     sample o di un preset lo contiene (es. name="R&b3").
  2. Blocchi di attributi duplicati su <audioClip> (stesso nome, stesso
     valore, scritto due volte).
  3. Formato legacy (pre 3.0): <firmwareVersion> e <song> sono due elementi
     radice affiancati, quindi il documento ha piu' di un document element.

Il parser quindi:
  - non decodifica entita': i valori restano byte-per-byte come sul file;
  - conserva gli attributi come lista ordinata di coppie, non come dict;
  - accetta piu' di un elemento radice;
  - registra per ogni nodo l'intervallo (start, end) nel testo originale, il
    che permette una riserializzazione byte-esatta dei rami non modificati.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------- token

_NAME = r'[A-Za-z_][\w.:-]*'
_OPEN = re.compile(rf'<(?P<tag>{_NAME})')
_ATTR = re.compile(rf'\s*(?P<name>{_NAME})\s*=\s*"(?P<val>[^"]*)"')
_CLOSE_OPEN = re.compile(r'\s*(?P<slash>/?)>')
_CLOSE_TAG = re.compile(rf'</\s*(?P<tag>{_NAME})\s*>')
_PROLOG = re.compile(r'<\?.*?\?>', re.S)
_COMMENT = re.compile(r'<!--.*?-->', re.S)


@dataclass
class ParseProblem:
    """Anomalia incontrata durante il parsing. Non blocca la lettura."""
    kind: str
    line: int
    detail: str


@dataclass
class Node:
    tag: str
    # lista ordinata: conserva l'ordine di scrittura e gli eventuali duplicati
    attrs: list[tuple[str, str]] = field(default_factory=list)
    children: list['Node'] = field(default_factory=list)
    text: str = ''            # testo scalare, gia' strippato
    self_closing: bool = False
    # intervallo nel sorgente originale; None per i nodi creati a mano
    span: tuple[int, int] | None = None
    dirty: bool = False       # True => va riserializzato, non ricopiato

    # ---------------------------------------------------------- accesso comodo
    def get(self, name: str, default=None) -> str | None:
        """Primo valore per `name`. Se ci sono duplicati vince il primo."""
        for k, v in self.attrs:
            if k == name:
                return v
        return default

    def get_all(self, name: str) -> list[str]:
        return [v for k, v in self.attrs if k == name]

    def has(self, name: str) -> bool:
        return any(k == name for k, _ in self.attrs)

    def set(self, name: str, value: str) -> None:
        """Sostituisce TUTTE le occorrenze di `name` (e marca il nodo dirty)."""
        value = str(value)
        found = False
        out = []
        for k, v in self.attrs:
            if k == name:
                if not found:
                    out.append((k, value))
                    found = True
                # i duplicati successivi vengono scartati
            else:
                out.append((k, v))
        if not found:
            out.append((name, value))
        self.attrs = out
        self.touch()

    def remove(self, name: str) -> None:
        self.attrs = [(k, v) for k, v in self.attrs if k != name]
        self.touch()

    def touch(self) -> None:
        """Marca il nodo (e solo lui) come da riserializzare."""
        self.dirty = True

    # --------------------------------------------------------------- struttura
    def find(self, tag: str) -> 'Node | None':
        for c in self.children:
            if c.tag == tag:
                return c
        return None

    def find_all(self, tag: str) -> list['Node']:
        return [c for c in self.children if c.tag == tag]

    def iter(self):
        yield self
        for c in self.children:
            yield from c.iter()

    def path_iter(self, prefix: str = ''):
        p = f'{prefix}/{self.tag}' if prefix else self.tag
        yield p, self
        for c in self.children:
            yield from c.path_iter(p)

    def copy(self) -> 'Node':
        """Copia profonda che conserva gli span.

        Conservarli non e' un dettaglio: un nodo copiato e non modificato resta
        "pulito", quindi il serializzatore lo riemette copiando i byte
        originali invece di ricostruirlo dalle regole di formato. Duplicare una
        clip produce cosi' un gemello byte-identico, e solo gli attributi che
        cambiamo davvero passano dal writer.

        ATTENZIONE: vale DENTRO lo stesso documento. Per portare un nodo in un
        ALTRO documento usa `copy_detached()` — vedi li' il perche'.
        """
        n = Node(tag=self.tag, attrs=list(self.attrs), text=self.text,
                 self_closing=self.self_closing, span=self.span,
                 dirty=self.dirty)
        n.children = [c.copy() for c in self.children]
        return n

    def copy_detached(self) -> 'Node':
        """Copia profonda SENZA span, per portare il nodo in un altro documento.

        Gli span sono offset dentro il testo sorgente del documento di
        provenienza. Se un nodo copiato da un file A finisce in un file B
        restando "pulito", il serializzatore di B ricopia i byte a QUEGLI
        offset dal testo di B: esce spazzatura, e non un errore.

        Il sintomo osservato la prima volta che e' successo, istanziando un
        preset dentro una song:

            <modKnob controlsParam="modulato
            Volume" />

        cioe' testo troncato e ricucito, con tag non chiusi. Il file passava
        comunque la scrittura e falliva solo alla rilettura.

        Qui gli span vengono azzerati e tutto il sottoalbero marcato `dirty`,
        cosi' il writer lo ricostruisce dalle regole di formato.
        """
        n = Node(tag=self.tag, attrs=list(self.attrs), text=self.text,
                 self_closing=self.self_closing, span=None, dirty=True)
        n.children = [c.copy_detached() for c in self.children]
        return n

    def insert(self, index: int, child: 'Node') -> 'Node':
        self.children.insert(index, child)
        self.self_closing = False
        self.touch()
        return child

    def append(self, child: 'Node') -> 'Node':
        self.children.append(child)
        self.self_closing = False
        self.touch()
        return child

    def __repr__(self):
        a = ' '.join(f'{k}={v!r}' for k, v in self.attrs[:3])
        more = '…' if len(self.attrs) > 3 else ''
        return f'<Node {self.tag} {a}{more} children={len(self.children)}>'


@dataclass
class Document:
    """Un file Deluge: prologo + uno o piu' elementi radice."""
    prolog: str = '<?xml version="1.0" encoding="UTF-8"?>'
    roots: list[Node] = field(default_factory=list)
    raw: str = ''
    problems: list[ParseProblem] = field(default_factory=list)
    trailing_newline: bool = True

    @property
    def root(self) -> Node:
        """L'elemento principale: nel formato legacy e' il secondo."""
        for r in self.roots:
            if r.tag in ('song', 'kit', 'sound', 'defaults', 'midiDevices',
                         'runtimeFeatureSettings', 'favourites'):
                return r
        return self.roots[-1]

    def iter(self):
        for r in self.roots:
            yield from r.iter()

    def path_iter(self):
        for r in self.roots:
            yield from r.path_iter()


# -------------------------------------------------------------------- parsing

def _line_of(text: str, pos: int) -> int:
    return text.count('\n', 0, pos) + 1


def parse(text: str) -> Document:
    doc = Document(raw=text)
    n = len(text)
    i = 0
    stack: list[Node] = []
    text_start: int | None = None

    # prologo
    m = _PROLOG.match(text.lstrip('﻿'))
    if m:
        doc.prolog = m.group(0)
        i = text.index(m.group(0)) + len(m.group(0))

    while i < n:
        lt = text.find('<', i)
        if lt < 0:
            break

        # testo fra il '>' precedente e questo '<'
        if stack and text_start is not None:
            chunk = text[text_start:lt].strip()
            if chunk:
                stack[-1].text = chunk

        if text.startswith('<!--', lt):
            m = _COMMENT.match(text, lt)
            i = m.end() if m else lt + 4
            text_start = i
            continue
        if text.startswith('<?', lt):
            m = _PROLOG.match(text, lt)
            i = m.end() if m else lt + 2
            text_start = i
            continue

        m = _CLOSE_TAG.match(text, lt)
        if m:
            tag = m.group('tag')
            if stack:
                if stack[-1].tag != tag:
                    doc.problems.append(ParseProblem(
                        'mismatched_close', _line_of(text, lt),
                        f'</{tag}> chiude <{stack[-1].tag}>'))
                    # risalgo fino a trovare il tag giusto, se c'e'
                    for k in range(len(stack) - 1, -1, -1):
                        if stack[k].tag == tag:
                            for node in stack[k:]:
                                node.span = (node.span[0], m.end()) if node.span else None
                            del stack[k:]
                            break
                    else:
                        pass  # chiusura orfana: ignorata
                else:
                    node = stack.pop()
                    node.span = (node.span[0], m.end()) if node.span else None
            else:
                doc.problems.append(ParseProblem(
                    'orphan_close', _line_of(text, lt), f'</{tag}>'))
            i = m.end()
            text_start = i
            continue

        m = _OPEN.match(text, lt)
        if not m:
            # '<' che non apre un tag: lo lascio scorrere come testo
            i = lt + 1
            continue

        node = Node(tag=m.group('tag'), span=(lt, -1))
        j = m.end()
        seen: set[str] = set()
        while True:
            am = _ATTR.match(text, j)
            if not am:
                break
            name, val = am.group('name'), am.group('val')
            if name in seen:
                doc.problems.append(ParseProblem(
                    'duplicate_attr', _line_of(text, lt),
                    f'<{node.tag}> ripete {name}="{val}"'))
            seen.add(name)
            if '&' in val and not re.search(
                    r'&(?:amp|lt|gt|quot|apos|#\d+|#x[0-9A-Fa-f]+);', val):
                doc.problems.append(ParseProblem(
                    'unescaped_amp', _line_of(text, lt),
                    f'<{node.tag} {name}="{val}">'))
            node.attrs.append((name, val))
            j = am.end()

        cm = _CLOSE_OPEN.match(text, j)
        if not cm:
            doc.problems.append(ParseProblem(
                'unterminated_tag', _line_of(text, lt), f'<{node.tag}'))
            i = j + 1
            continue

        node.self_closing = cm.group('slash') == '/'
        end = cm.end()

        if stack:
            stack[-1].children.append(node)
        else:
            doc.roots.append(node)

        if node.self_closing:
            node.span = (lt, end)
        else:
            stack.append(node)

        i = end
        text_start = i

    for leftover in stack:
        doc.problems.append(ParseProblem(
            'unclosed', _line_of(text, leftover.span[0]), f'<{leftover.tag}>'))
        leftover.span = (leftover.span[0], n)

    doc.trailing_newline = text.endswith('\n')
    return doc


def parse_file(path) -> Document:
    raw = Path(path).read_bytes().decode('utf-8', 'surrogateescape')
    return parse(raw)
