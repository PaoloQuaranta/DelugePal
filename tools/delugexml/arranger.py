"""L'arranger: quando ogni clip suona sulla linea del tempo.

La session view dice QUALI clip esistono; l'arranger dice QUANDO suonano. Ma
le clip d'arranger non portano nessuna posizione: cercarla addosso a loro non
porta da nessuna parte, ed e' un vicolo cieco in cui si finisce facilmente,
perche' <arrangementOnlyTracks> esiste e sembra il posto giusto.

Le posizioni stanno altrove e in un'altra forma: un ATTRIBUTO sul nodo dello
STRUMENTO, cioe' letto dal lato di chi suona, non di cosa viene suonato.

    <sound presetName="ADDITIVE" clipInstances="0x00000C00 00004F80 00000000 …">

E' il TERZO membro della famiglia di blob esadecimali del formato, dopo le
note e le automazioni: parole da 32 bit maiuscole senza separatori. Qui in
TERNE.

FORMATO
-------
Da `src/deluge/model/output.cpp`, branch `community` — non dedotto. Scrittura:

    writer.writeTagNameAndSeperator("clipInstances");
    writer.write("\\"0x");
    per ogni ClipInstance:  intToHex(pos);
                            intToHex(length);
                            intToHex(clipCode);

    uint32_t clipCode;
    if (!thisInstance->clip) clipCode = 0xFFFFFFFF;
    else {
        clipCode = thisInstance->clip->indexForSaving;
        if (thisInstance->clip->section == 255) clipCode |= (1 << 31);
    }

Lettura (`song.cpp`, `Song::readFromFile`), che e' quella che dice il senso:

    uint32_t lookingForIndex = clipCode & ~((uint32_t)1 << 31);
    bool isArrangementClip   = clipCode >> 31;
    ClipArray* clips = isArrangementClip ? &arrangementOnlyClips : &sessionClips;

Quindi `clipCode` NON e' un identificatore: e' un **indice ordinale** in una
delle due liste di clip, e il bit 31 sceglie la lista. Il che significa che
rimuovere o riordinare una clip invalida silenziosamente ogni istanza che
punta a quella posizione o oltre — vedi `check()`.

    bit 31 = 0  ->  indice in <sessionClips>
    bit 31 = 1  ->  indice in <arrangementOnlyTracks>
    0xFFFFFFFF  ->  nessuna clip (buco nell'arrangiamento)

`pos` e `length` sono in tick, come le note e le posizioni delle automazioni.
`length` e' quello dell'ISTANZA, non della clip: una clip da una battuta
piazzata per otto battute e' UNA istanza con length otto volte la clip.

VERIFICATO
----------
Su tutte le 2116 istanze delle 24 song del corpus che hanno un arrangiamento:
2115 risolte piu' una sentinella, zero indici fuori range, e — la prova che
conta — zero istanze che puntino a una clip di uno strumento diverso da
quello che le ospita. Una decodifica sbagliata dell'indice avrebbe rotto
proprio quel legame.

[OSS] La sola LETTURA e' verificata. Cosa il dispositivo tocchi ANCHE quando
piazzi una clip nell'arranger — stato di vista, scroll, sezioni — non e'
ancora stato misurato su una coppia controllata. E' la stessa classe di
domanda di `yScrollSongView` e `beingEdited`, che sono costati caro entrambi:
finche' non e' misurata, scrivere un arrangiamento da zero non e' garantito
che si veda.
"""
from __future__ import annotations

from typing import NamedTuple

from .parser import Document, Node

PAROLA = 8                      # cifre esadecimali per parola da 32 bit
TERNA = PAROLA * 3

BIT_ARRANGER = 1 << 31
NESSUNA = 0xFFFFFFFF            # sentinella: istanza senza clip

#: L'attributo moderno e quello storico. Il firmware legge entrambi ma scrive
#: solo il primo; qui si conserva quello che il file usava gia'.
ATTRIBUTI = ('clipInstances', 'trackInstances')

#: I due contenitori indicizzati da `clipCode`, nell'ordine dei due valori del
#: bit 31. `arrangementClips` non compare nel corpus ma il parser lo prevede.
CONTENITORI = ('sessionClips', 'arrangementOnlyTracks')


class Istanza(NamedTuple):
    """Una clip piazzata sulla linea del tempo di uno strumento."""
    pos: int                    # tick d'inizio
    length: int                 # durata dell'istanza in tick, non della clip
    code: int                   # indice + bit 31, oppure NESSUNA

    @property
    def vuota(self) -> bool:
        return self.code == NESSUNA

    @property
    def da_arranger(self) -> bool:
        """La clip sta in <arrangementOnlyTracks> invece che in <sessionClips>."""
        return not self.vuota and bool(self.code >> 31)

    @property
    def indice(self) -> int | None:
        """La posizione ordinale nella lista scelta da `da_arranger`."""
        return None if self.vuota else self.code & ~BIT_ARRANGER

    @property
    def fine(self) -> int:
        return self.pos + self.length


def codice(indice: int, da_arranger: bool = False) -> int:
    """Il `clipCode` per una clip in una data posizione ordinale."""
    if indice < 0 or indice >= BIT_ARRANGER:
        raise ValueError(f'indice fuori scala: {indice}')
    return indice | BIT_ARRANGER if da_arranger else indice


def decode(value: str) -> list[Istanza]:
    """Le istanze contenute in un attributo `clipInstances`."""
    if not (isinstance(value, str) and value.startswith('0x')):
        raise ValueError(f'{str(value)[:24]}… non e un blob di istanze')
    corpo = value[2:]
    if len(corpo) % TERNA:
        raise ValueError(f'{len(corpo)} cifre non sono terne intere '
                         f'({TERNA} cifre ciascuna)')
    out = []
    for i in range(0, len(corpo), TERNA):
        t = corpo[i:i + TERNA]
        out.append(Istanza(pos=int(t[0:8], 16),
                           length=int(t[8:16], 16),
                           code=int(t[16:24], 16)))
    return out


def encode(istanze) -> str:
    """L'attributo per queste istanze.

    Vengono riordinate per posizione: il firmware le tiene ordinate e le cerca
    per posizione, quindi una sequenza disordinata non e' un formato valido
    anche se si rilegge senza errori.
    """
    parole = []
    for i in sorted(istanze, key=lambda x: x.pos):
        if i.length <= 0:
            raise ValueError(f'istanza di durata {i.length} a tick {i.pos}')
        parole += [i.pos, i.length, i.code]
    return '0x' + ''.join(f'{w:08X}' for w in parole)


# ------------------------------------------------------------- lettura da song

def attr_of(strumento: Node) -> str | None:
    """Quale dei due nomi d'attributo usa questo strumento, se ne usa uno."""
    for a in ATTRIBUTI:
        if strumento.get(a) is not None:
            return a
    return None


def instances(strumento: Node) -> list[Istanza]:
    """Le istanze d'arranger di uno strumento; lista vuota se non ne ha."""
    a = attr_of(strumento)
    if a is None:
        return []
    v = strumento.get(a)
    return decode(v) if len(v) > 2 else []


def set_instances(strumento: Node, istanze) -> str:
    """Riscrive le istanze, conservando il nome d'attributo gia' in uso.

    Senza istanze l'attributo viene TOLTO, non scritto vuoto. Nel corpus, su
    203 strumenti, 92 non hanno l'attributo e ZERO ce l'hanno vuoto (`0x`):
    l'assenza e' la forma con cui il dispositivo scrive "nessuna istanza", e
    `0x` non e' mai stato osservato. Serve da quando esiste la rimozione, che
    e' l'unica operazione capace di svuotare una traccia d'arranger.
    """
    a = attr_of(strumento) or ATTRIBUTI[0]
    if not list(istanze):
        if strumento.has(a):
            strumento.remove(a)
        return ''
    v = encode(istanze)
    strumento.set(a, v)
    return v


def clip_list(doc: Document, da_arranger: bool) -> list[Node]:
    """La lista di clip che `clipCode` indicizza, nell'ordine del file."""
    if not da_arranger:
        node = doc.root.find(CONTENITORI[0])
        return node.children if node else []
    for nome in (CONTENITORI[1], 'arrangementClips'):
        node = doc.root.find(nome)
        if node is not None:
            return node.children
    return []


def clip_of(doc: Document, istanza: Istanza) -> Node | None:
    """La clip che l'istanza fa suonare, o None se vuota o non risolvibile."""
    if istanza.vuota:
        return None
    lista = clip_list(doc, istanza.da_arranger)
    i = istanza.indice
    return lista[i] if i < len(lista) else None


def arrangement(doc: Document) -> list[tuple[Node, Istanza, Node | None]]:
    """(strumento, istanza, clip) per tutto l'arrangiamento, ordinato nel tempo."""
    out = []
    from . import song as S                               # import locale: ciclo
    for strumento in S.instruments(doc):
        for ist in instances(strumento):
            out.append((strumento, ist, clip_of(doc, ist)))
    out.sort(key=lambda r: (r[1].pos, r[1].length))
    return out


def has_arrangement(doc: Document) -> bool:
    from . import song as S                               # import locale: ciclo
    return any(instances(i) for i in S.instruments(doc))


def nome_di(strumento: Node) -> str:
    return (strumento.get('presetName') or strumento.get('name')
            or f'<{strumento.tag}>')


def remove_instances_in(strumento: Node, da: int, a: int) -> dict[str, object]:
    """Toglie dalla traccia di `strumento` le istanze nel tratto [da, a).

    E' cio' che serve per «leva quel pattern nella seconda meta'»: la clip
    resta, lanciabile in song view, e sparisce solo quel tratto della linea
    del tempo. Non tocca nessun `clipCode`, perche' non cambia nessuna lista.

    Vengono tolte le istanze CONTENUTE nel tratto. Una che lo ATTRAVERSA porta
    anche materiale fuori, e toglierla farebbe tacere musica che nessuno ha
    chiesto di togliere: resta, e il rapporto la dichiara in `a_cavallo`, cosi'
    chi ha chiesto puo' sapere che qualcosa e' rimasto e decidere.
    """
    if a <= da:
        raise ValueError(f'tratto vuoto o rovesciato: [{da}, {a})')
    ists = instances(strumento)
    # per POSIZIONE nella lista, non per valore: `Istanza` e' una NamedTuple e
    # due istanze identiche si cancellerebbero a vicenda con un `in`
    dentro = {k for k, i in enumerate(ists) if i.pos >= da and i.fine <= a}
    cavallo = sum(1 for k, i in enumerate(ists)
                  if k not in dentro and i.pos < a and i.fine > da)
    if dentro:
        set_instances(strumento,
                      [i for k, i in enumerate(ists) if k not in dentro])
    return {'strumento': nome_di(strumento), 'tolte': len(dentro),
            'a_cavallo': cavallo}


def renumber_after_removal(doc: Document, indice: int,
                           da_arranger: bool) -> dict[str, int]:
    """Aggiorna i `clipCode` dopo che la clip in quella posizione e' sparita.

    Le istanze che puntavano PROPRIO a lei spariscono; quelle che puntavano
    piu' in la' scalano di uno. `clipCode` e' una POSIZIONE ORDINALE, non un
    identificatore: senza questo passaggio ogni istanza oltre il buco suona la
    clip sbagliata, e il file resta perfettamente valido -- il difetto non si
    vede da nessuna parte tranne che dal Deluge, suonando.

    Le DUE LISTE hanno numerazioni indipendenti, scelte dal bit 31: togliere da
    `<sessionClips>` non deve toccare un solo indice di
    `<arrangementOnlyTracks>`. E' il punto in cui si sbaglia.

    Uno strumento le cui istanze non cambiano non viene toccato affatto, cosi'
    il suo attributo resta i byte originali e il round-trip chirurgico regge.
    """
    from . import song as S                               # import locale: ciclo

    tolte = scalate = 0
    for strumento in S.instruments(doc):
        ists = instances(strumento)
        if not ists:
            continue
        nuove, cambiato = [], False
        for ist in ists:
            if ist.vuota or ist.da_arranger != da_arranger:
                nuove.append(ist)
                continue
            if ist.indice == indice:
                tolte += 1
                cambiato = True
            elif ist.indice > indice:
                nuove.append(ist._replace(
                    code=codice(ist.indice - 1, da_arranger)))
                scalate += 1
                cambiato = True
            else:
                nuove.append(ist)
        if cambiato:
            set_instances(strumento, nuove)
    return {'istanze_tolte': tolte, 'istanze_rinumerate': scalate}


def index_of(doc: Document, clip: Node) -> tuple[int, bool] | None:
    """(indice, da_arranger) della clip, cioe' cosa mettere in `clipCode`."""
    for da_arr in (False, True):
        lista = clip_list(doc, da_arr)
        for i, c in enumerate(lista):
            if c is clip:
                return i, da_arr
    return None


# ------------------------------------------------------- scrittura e visibilita'

#: Colonne della griglia sull'asse dei tempi. Come le 8 righe di
#: `SONG_VIEW_ROWS`, e' la geometria fisica del display.
ARRANGER_COLS = 16

#: I livelli di zoom osservati, in tick per colonna: 48 x 2^n. `384` e' una
#: battuta per colonna, quindi `192` mostra otto battute sullo schermo.
ZOOM_LIVELLI = (48, 96, 192, 384, 768, 1536, 3072, 6144)


def place(doc: Document, strumento: Node, clip: Node, pos: int,
          length: int | None = None) -> Istanza:
    """Piazza `clip` sulla traccia di `strumento` a `pos` tick.

    `length` di default e' la lunghezza della clip: e' una singola ripetizione.
    Per stenderla, passare un multiplo — il dispositivo usa UNA istanza lunga,
    non tante istanze corte.

    Non tocca la vista: `fit_view()` va chiamata dopo, e sono due cose diverse
    perche' si puo' voler piazzare molte clip e sistemare la vista una volta
    sola alla fine.
    """
    from . import song as S                               # import locale: ciclo

    trovato = index_of(doc, clip)
    if trovato is None:
        raise ValueError(f'la clip {S.clip_label(clip)!r} non sta in nessuno '
                         f'dei due contenitori indicizzabili')
    idx, da_arr = trovato

    atteso = S.instrument_of(doc, clip)
    if atteso is not None and atteso is not strumento:
        raise ValueError(
            f'la clip {S.clip_label(clip)!r} appartiene a '
            f'{nome_di(atteso)!r}, non a {nome_di(strumento)!r}: una traccia '
            f'puo suonare solo le proprie clip')

    if length is None:
        length = int(clip.get('length') or 0)
    if length <= 0:
        raise ValueError(f'lunghezza non valida: {length}')
    if pos < 0:
        raise ValueError(f'posizione negativa: {pos}')

    nuova = Istanza(pos=pos, length=length, code=codice(idx, da_arr))
    ists = instances(strumento)
    for i in ists:
        if i.pos < nuova.fine and i.fine > nuova.pos:
            raise ValueError(
                f'si sovrappone all istanza a tick {i.pos} lunga {i.length}: '
                f'una traccia suona una clip per volta')
    ists.append(nuova)
    set_instances(strumento, ists)
    return nuova


def is_white(clip: Node) -> bool:
    """La clip e' "bianca", cioe' non appartiene a nessuna scena.

    Il criterio e' l'ASSENZA di `section`, non `section="255"`: nel corpus le
    54 clip d'arranger non hanno l'attributo affatto, e tutte e 1127 le clip
    di sessione ce l'hanno. Il 255 e' la rappresentazione in memoria, che il
    firmware impone al caricamento in base al contenitore:

        // Ensure all arranger-only Clips have their section as 255
        for (…arrangementOnlyClips…) { clip->section = 255; }
    """
    return clip.get('section') is None


def _contenitore_arranger(doc: Document) -> Node:
    """`<arrangementOnlyTracks>`, creandolo se manca.

    Va subito dopo `<sessionClips>`: nel corpus e' cosi' in tutte e 8 le song
    che ce l'hanno.
    """
    for nome in (CONTENITORI[1], 'arrangementClips'):
        n = doc.root.find(nome)
        if n is not None:
            return n
    nodo = Node(tag=CONTENITORI[1], attrs=[], text=None,
                self_closing=False, span=None, dirty=True)
    figli = doc.root.children
    dopo = next((i for i, c in enumerate(figli)
                 if c.tag == CONTENITORI[0]), len(figli) - 1)
    doc.root.insert(dopo + 1, nodo)
    return nodo


#: Attributi che una copia non deve portarsi dietro nell'arranger. `section`
#: e' quello che DEFINISCE la clip bianca; gli altri due sono stati di vista
#: che riferiscono la session view e che il dispositivo non lascia mai su una
#: clip d'arranger.
NON_EREDITATI = ('section', 'beingEdited', 'selected')


def place_unique(doc: Document, strumento: Node, sorgente: Node, pos: int,
                 length: int | None = None) -> tuple[Node, Istanza]:
    """La clip "bianca": una copia INDIPENDENTE piazzata solo in quel punto.

    E' il gesto che rende l'arranger uno strumento di arrangiamento e non solo
    una lista di lanci. Si prende una clip che appartiene a una scena, la si
    piazza sulla timeline come copia scollegata, e da li' la si puo' modificare
    — aggiungere un fill, togliere un colpo — senza toccare l'originale ne'
    nessun'altra ripetizione.

    La copia non eredita `section`, ed e' esattamente questo a renderla bianca:
    non appartenendo a nessuna scena non compare in session view, e vive solo
    dove sta sulla timeline.

    Usa `copy_detached()` e non `copy()`: i nodi copiati portano con se' gli
    span del documento di origine, e riusarli altrove produce XML troncato che
    si scrive senza errori e fallisce solo alla rilettura. E' gia' successo.
    """
    from . import song as S                               # import locale: ciclo

    atteso = S.instrument_of(doc, sorgente)
    if atteso is not None and atteso is not strumento:
        raise ValueError(
            f'la clip {S.clip_label(sorgente)!r} appartiene a '
            f'{nome_di(atteso)!r}, non a {nome_di(strumento)!r}')

    copia = sorgente.copy_detached()
    for a in NON_EREDITATI:
        if copia.has(a):
            copia.remove(a)

    cont = _contenitore_arranger(doc)
    cont.append(copia)
    try:
        ist = place(doc, strumento, copia, pos, length)
    except ValueError:
        cont.children.remove(copia)      # non lasciare una clip orfana
        raise
    return copia, ist


def extent(doc: Document) -> tuple[int, int] | None:
    """(primo tick, ultimo tick) dell'arrangiamento, o None se e' vuoto."""
    ists = [i for _, i, _ in arrangement(doc)]
    if not ists:
        return None
    return min(i.pos for i in ists), max(i.fine for i in ists)


def fit_view(doc: Document, apri: bool = True) -> dict[str, str]:
    """Fa in modo che l'arrangiamento appena scritto si VEDA.

    Tre assi, e servono tutti e tre:

    1. le righe sono gli strumenti -> `yScrollArrangementView`, che e' la
       stessa aritmetica della song view e sta gia' in `song.py`
    2. le colonne sono il tempo -> `xScrollArrangementView` piu'
       `xZoomArrangementView`: la finestra visibile e'
       `[xScroll, xScroll + 16*xZoom)`, e un arrangiamento che comincia oltre
       quel bordo si apre su uno schermo vuoto
    3. `inArrangementView` decide su quale schermata si apre la song

    Il punto 2 non e' teorico: nel corpus `Junglevar.XML` ha la finestra a
    `[0,1536)` e la prima istanza a 14014, cioe' si apre davvero sul vuoto.

    `xScrollSongView`/`xZoomSongView` NON sono lo scroll dell'arranger — dal
    sorgente sono lo stato a cui TORNARE uscendone — ma il firmware li scrive
    sempre insieme a `inArrangementView`, quindi si scrivono anche qui per
    somigliare a cio' che scrive il dispositivo.
    """
    from . import song as S                               # import locale: ciclo

    scritti: dict[str, str] = {}
    est = extent(doc)
    if est is None:
        return scritti
    primo, ultimo = est

    # riga: lo strumento piu' in basso che ha istanze
    ultima_riga = max((n for n, st in enumerate(S.instruments(doc))
                       if instances(st)), default=None)
    if ultima_riga is not None:
        v = S.scroll_arrangement_view_to(doc, ultima_riga)
        if v is not None:
            scritti['yScrollArrangementView'] = v

    # colonne: zoom abbastanza largo da contenere l'arrangiamento, poi scroll
    zoom = doc.root.get('xZoomArrangementView')
    zoom = int(zoom) if zoom and zoom.isdigit() else ZOOM_LIVELLI[2]
    durata = max(ultimo - primo, 1)
    while zoom * ARRANGER_COLS < durata and zoom < ZOOM_LIVELLI[-1]:
        zoom = next(z for z in ZOOM_LIVELLI if z > zoom)
    if str(zoom) != doc.root.get('xZoomArrangementView'):
        doc.root.set('xZoomArrangementView', str(zoom))
        scritti['xZoomArrangementView'] = str(zoom)

    xs = doc.root.get('xScrollArrangementView')
    xs = int(xs) if xs and xs.lstrip('-').isdigit() else 0
    if not (xs <= primo < xs + zoom * ARRANGER_COLS):
        xs = (primo // zoom) * zoom          # allinea alla colonna, come il device
        doc.root.set('xScrollArrangementView', str(xs))
        scritti['xScrollArrangementView'] = str(xs)

    if apri:
        scritti.update(open_in_arranger(doc))
    return scritti


def open_in_arranger(doc: Document) -> dict[str, str]:
    """La song si apre in arranger view invece che in session view.

    Dal sorgente (`song.cpp`), i tre attributi sono scritti insieme:

        if (getRootUI() == &arrangerView) {
            writer.writeAttribute("inArrangementView", 1);
            goto weAreInArrangementEditorOrInClipInstance;
        }
        …
        weAreInArrangementEditorOrInClipInstance:
            writer.writeAttribute("xScrollSongView", xScrollForReturnToSongView);
            writer.writeAttribute("xZoomSongView",   xZoomForReturnToSongView);

    Nel corpus compaiono in 0 song su 114 senza arrangiamento, quindi la loro
    assenza e' il caso normale di una song salvata in session view.

    Toglie inoltre `beingEdited` da tutte le clip e lo trasforma in `selected`.
    Non e' cosmesi: nel corpus `inArrangementView="1"` e `beingEdited` non
    convivono MAI, 20 casi su 20 — e ha senso, perche' `beingEdited` vuol dire
    che una clip e' aperta in clip view, che non puo' essere vero se la
    schermata aperta e' l'arranger. E' la stessa famiglia di `yScrollSongView`:
    contenuto giusto, attributo di stato che lo contraddice.

    `selected` invece e' indipendente dalla vista — compare anche in session
    view, e in 7 song su 20 in arranger view non c'e' affatto — quindi viene
    solo spostato dove stava `beingEdited`, non inventato.
    """
    scritti = {'inArrangementView': '1'}
    doc.root.set('inArrangementView', '1')
    for da, a in (('xScroll', 'xScrollSongView'), ('xZoom', 'xZoomSongView')):
        if not doc.root.has(a):
            v = doc.root.get(da) or '0'
            doc.root.set(a, v)
            scritti[a] = v

    for cont in CONTENITORI:
        n = doc.root.find(cont)
        if n is None:
            continue
        for c in n.children:
            if c.get('beingEdited') == '1':
                c.remove('beingEdited')
                c.set('selected', '1')
                scritti['beingEdited->selected'] = S_label(c)
    return scritti


def S_label(clip: Node) -> str:
    from . import song as S                               # import locale: ciclo
    return S.clip_label(clip)


def check(doc: Document) -> list[str]:
    """I problemi dell'arrangiamento, uno per riga; lista vuota se e' sano.

    Tre categorie, tutte conseguenza del fatto che `clipCode` e' un indice
    ordinale e non un identificatore:

    - indice oltre la fine della lista: la clip non esiste piu'
    - clip di un altro strumento: gli indici sono scalati, tipicamente perche'
      una clip e' stata rimossa senza rinumerare
    - istanze sovrapposte sullo stesso strumento: una traccia non puo' suonare
      due clip insieme
    """
    from . import song as S                               # import locale: ciclo

    problemi = []
    for strumento in S.instruments(doc):
        ists = instances(strumento)
        nome = nome_di(strumento)
        for ist in ists:
            if ist.vuota:
                continue
            lista = clip_list(doc, ist.da_arranger)
            dove = CONTENITORI[1] if ist.da_arranger else CONTENITORI[0]
            if ist.indice >= len(lista):
                problemi.append(
                    f'{nome}: tick {ist.pos} punta a {dove}[{ist.indice}] '
                    f'ma ce ne sono {len(lista)}')
                continue
            clip = lista[ist.indice]
            atteso = S.instrument_of(doc, clip)
            if atteso is not None and atteso is not strumento:
                altro = atteso.get('presetName') or atteso.get('name')
                problemi.append(
                    f'{nome}: tick {ist.pos} punta a {dove}[{ist.indice}] '
                    f'che appartiene a {altro!r}')
        ordinate = sorted((i for i in ists), key=lambda x: x.pos)
        for a, b in zip(ordinate, ordinate[1:]):
            if a.fine > b.pos:
                problemi.append(
                    f'{nome}: istanza a tick {a.pos} lunga {a.length} '
                    f'si sovrappone a quella a tick {b.pos}')
    return problemi
