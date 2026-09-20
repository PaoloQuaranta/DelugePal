"""JUNGLEVAR -- jungle/IDM su materiale dell'utente, con armonia jazz e
un'ombra simbolista francese.

La song parte SEMPRE dalla copia riscaricata dal Deluge. Tutte le sette clip
originali compaiono integralmente almeno una volta; il materiale nuovo non le
sostituisce, ma le mette in prospettiva:

    0-15   BRUME: Kaleidoscope, pad, polimetri radi
    8-39   EXPOSE: le quattro clip 972 in successione; basso e poi break
    32-47  CONSTELLATION: la clip 097 intera, cromatica e smisurata
    48-55  MIROIR: sesta aumentata francese, Kaleidoscope trasposto
    56-71  SECOND DROP: Scorpio editato, basso abbassato, IDM 5/7/11

Il break e' ``Dennis Coffey - Scorpio (cd).wav``. Dura 8,051 s: come loop di
quattro battute e' ~119,2 BPM. Trasposto di +6 semitoni corre a ~168,6 BPM,
quindi la song sta a 169 BPM senza time-stretch esterno. Le fette restano ONCE:
la zona delimita ciascun sedicesimo, come lo Slicer nativo del Deluge.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

B = MU.TICK_PER_BATTUTA
MOV = MU.TICK_PER_MOVIMENTO
P = MOV // 4
S32 = P // 2

SOURCE = RADICE / 'out' / 'JUNGLEVAR_source.XML'
KIT = RADICE / 'refs' / 'kits' / '808 From Mars.XML'
PRESET_PAD = RADICE / 'refs' / 'synths' / 'TEMPL.XML'

SAMPLE = 'SAMPLES/01_DRUMS_Jungle Breaks/Dennis Coffey - Scorpio (cd).wav'
FRAMES = 355052
NFETTE = 64
TRASPOSIZIONE_BREAK = 6
BPM = 169
SWING = 50
TOT_BARS = 72

# Primo giro riconoscibile; il secondo riorganizza movimenti interi e usa due
# colpi forti misurati nel file (28 e 62) come stutter di chiusura.
BEAT_ORDER_B = [0, 1, 2, 3, 6, 5, 4, 7, 0, 9, 10, 7, 14, 13, 12, 15]
STUTTER_B = {7: 28, 15: 62}

ARMONIA_A = [
    'G13', 'G13', 'Bbmaj9/D', 'Bbmaj9/D',
    'Ebmaj7#11', 'Ebmaj7#11', 'D7alt', 'D7alt',
    'G13', 'Abmaj9/G', 'Bbmaj9/G', 'Bmaj7#11/G',
    'C13', 'Db7#11', 'D7alt', 'D7alt',
]
ARMONIA_RITORNO = ['D7alt', 'G13', 'Abmaj9/G', 'G13']


def strumento(doc, nome: str):
    """Lo strumento della song chiamato ``nome``."""
    from delugexml import song as S                           # noqa: PLC0415
    for inst in S.instruments(doc):
        if inst.get('presetName') == nome or inst.get('name') == nome:
            return inst
    raise ValueError(f'nessuno strumento {nome!r} nella song')


def _clip_di(doc, inst) -> list:
    from delugexml import song as S                           # noqa: PLC0415
    return [c for _, c in S.clips(doc) if S.instrument_of(doc, c) is inst]


def _nota(pos: int, *, durata: int = P, velocity: int = 96):
    from delugexml.notes import Note                          # noqa: PLC0415
    return Note(pos=pos, length=durata, velocity=velocity)


def _pattern_fette(fette: list[str], *, editato: bool) -> dict[str, list]:
    """Quattro battute di Scorpio. La A ricostruisce il loop; la B sposta beat
    interi e stuttera due attacchi, senza randomizzare singole fette."""
    voci: dict[str, list] = {}

    def metti(indice: int, passo: int, velocity: int = 114) -> None:
        voci.setdefault(fette[indice], []).append(
            _nota(passo * P, velocity=velocity))

    if not editato:
        for passo in range(64):
            metti(passo, passo)
        return voci

    for out_beat, src_beat in enumerate(BEAT_ORDER_B):
        base = out_beat * 4
        if out_beat in STUTTER_B:
            for k in range(4):
                metti(STUTTER_B[out_beat], base + k, 118 - 6 * k)
        else:
            for k in range(4):
                metti(src_beat * 4 + k, base + k)
    return voci


def _scrivi_kit(doc, clip, voci: dict[str, list]) -> None:
    for nome, note in voci.items():
        if note:
            MU.scrivi(doc, clip, note, dove=nome)


def _svuota_clip(doc, clip) -> None:
    from delugexml import song as S                           # noqa: PLC0415
    for riga in list(S.note_rows(clip)):
        MU.togli(doc, riga)


def _duplica(doc, clip, *, section: str, name: str):
    from delugexml import song as S                           # noqa: PLC0415
    indice = next(i for i, (_, c) in enumerate(S.clips(doc)) if c is clip)
    return S.duplicate_clip(doc, indice, section=section, name=name)


def _aggiungi_polimetri(doc):
    """Tre bordi percussivi coprimi: semplici da soli, mai riallineati nella
    finestra del brano. Sono punteggiatura attorno al break, non un secondo kit."""
    from delugexml import create as C, song as S              # noqa: PLC0415

    disegni = {
        'IDM5': (5, {
            'Rim Shot A 808': [_nota(0, velocity=106), _nota(3 * P, velocity=58)],
        }),
        'IDM7': (7, {
            'CH Combo 808': [_nota(P, durata=S32, velocity=68),
                             _nota(3 * P, durata=S32, velocity=54),
                             _nota(5 * P, durata=S32, velocity=72)],
        }),
        'IDM11': (11, {
            'Cowbell A 808': [_nota(0, velocity=92)],
            'Cym A 808 Decay C 01': [_nota(6 * P, durata=2 * P, velocity=66)],
        }),
    }
    risultato = {}
    for n, (nome, (periodo, voci)) in enumerate(disegni.items()):
        inst, clip = C.add_track(
            doc, str(KIT), name=nome, folder='KITS', length=periodo * P,
            colour_offset=str(8 + 16 * n), playing=True)
        _scrivi_kit(doc, clip, voci)
        S.set_clip_length(clip, periodo * P)
        risultato[nome] = (inst, clip)
    return risultato


def _aggiungi_glitch(doc):
    from delugexml import create as C                         # noqa: PLC0415
    inst, clip = C.add_track(doc, str(KIT), name='GLITCH', folder='KITS',
                             length=B, colour_offset='56', playing=True)
    rim = [_nota(2 * P + k * S32, durata=S32, velocity=104 - 7 * k)
           for k in range(6)]
    clave = [_nota(11 * P + k * S32, durata=S32, velocity=88 - 8 * k)
             for k in range(4)]
    _scrivi_kit(doc, clip, {'Rim Shot A 808': rim, 'Claves A 808': clave})
    return inst, clip


def _aggiungi_armonia(doc):
    """Pad continuo, voicing condotti e tre clip: il campo principale, la
    sesta francese scritta per note, il ritorno che non chiude del tutto."""
    from delugexml import create as C, song as S              # noqa: PLC0415
    from delugexml import sound as SND, structure as ST       # noqa: PLC0415

    inst, principale = C.add_track(
        doc, str(PRESET_PAD), name='SYMBOLIST PAD', folder='SYNTHS',
        length=16 * B, colour_offset='40', playing=True)
    ST.set_osc(inst, 1, type='triangle', transpose=0, cents=0)
    ST.set_osc(inst, 2, type='analogSaw', transpose=0, cents=-9)
    ST.set_unison(inst, num=2, detune=4, spread=12)
    SND.set(principale, 'oscAVolume', 28)
    SND.set(principale, 'oscBVolume', 14)
    SND.set(principale, 'envelope1.attack', 10)
    SND.set(principale, 'envelope1.sustain', 48)
    SND.set(principale, 'envelope1.release', 20)
    SND.set(principale, 'reverbAmount', 31)
    MU.scrivi(doc, principale, MU.armonia(
        ' | '.join(ARMONIA_A), voicing='senza-fondamentale', registro='do3',
        durata='1/1', velocity=50, articolazione='legato'))

    francese = _duplica(doc, principale, section='5', name='FRANCESE')
    _svuota_clip(doc, francese)
    S.set_clip_length(francese, B)
    MU.scrivi(doc, francese, MU.accordi(
        'mib3 sol3 la3 do#4', durata='1/1', velocity=56,
        articolazione='legato'))
    SND.set(francese, 'lpfFrequency', 34)
    SND.set(francese, 'lpfResonance', 18)

    ritorno = _duplica(doc, principale, section='6', name='RITORNO')
    _svuota_clip(doc, ritorno)
    S.set_clip_length(ritorno, 4 * B)
    MU.scrivi(doc, ritorno, MU.armonia(
        ' | '.join(ARMONIA_RITORNO), voicing='senza-fondamentale',
        registro='do3', durata='1/1', velocity=58, articolazione='legato'))
    MU.automatizza(doc, ritorno, 'lpfFrequency', 34, 46, 0, 4 * B, passi=9)
    MU.automatizza(doc, ritorno, 'lpfResonance', 14, 25, 0, 4 * B, passi=9)
    return inst, principale, francese, ritorno


def costruisci(source: Path | str = SOURCE) -> tuple[object, dict]:
    """Trasforma la JUNGLEVAR riscaricata dal Deluge nella prima versione
    completa. Il documento sorgente non viene mai sovrascritto."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    from delugexml import kit as K, structure as ST          # noqa: PLC0415

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(source))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, SWING, figura='1/8')

        # La timeline preesistente era uno schizzo a battuta 74/89. Le clip e
        # gli strumenti restano intatti; si tolgono soltanto le loro istanze.
        for inst in list(S.instruments(doc)):
            MU.togli(doc, inst, quando=(0, 1000 * B))

        iBass = strumento(doc, '31-BASS1')
        iLead = strumento(doc, '097')
        iKaleido = strumento(doc, 'Kaleidoscope')
        iKit = strumento(doc, '972')
        cBass = _clip_di(doc, iBass)[0]
        cLead = _clip_di(doc, iLead)[0]
        cKaleido = _clip_di(doc, iKaleido)[0]
        clipKit = sorted(_clip_di(doc, iKit), key=lambda c: int(c.get('section')))
        # La sorgente arrivava gia' con la clip del basso fuori dalla finestra
        # visibile. Le note non cambiano: si corregge soltanto la clip view.
        S.fit_clip_scroll_to_notes(doc, cBass)
        originali = {
            'Kaleidoscope': (iKaleido, cKaleido),
            '31-BASS1': (iBass, cBass),
            '097': (iLead, cLead),
            **{f'972/{n}': (iKit, c) for n, c in enumerate(clipKit)},
        }

        # Scorpio: 64 sedicesimi su quattro battute, +6 semitoni = ~168,6 BPM.
        iBreak, cBreakA = C.add_track(
            doc, str(KIT), name='SCORPIO', folder='KITS', length=4 * B,
            colour_offset='0', playing=True)
        fette = K.affetta(doc, iBreak, SAMPLE, FRAMES, n=NFETTE)
        for drum in S.drums(iBreak):
            ST.set_osc(drum, 1, transpose=TRASPOSIZIONE_BREAK)
        _scrivi_kit(doc, cBreakA, _pattern_fette(fette, editato=False))
        cBreakB = _duplica(doc, cBreakA, section='4', name='SCORPIO-B')
        _svuota_clip(doc, cBreakB)
        _scrivi_kit(doc, cBreakB, _pattern_fette(fette, editato=True))

        polimetri = _aggiungi_polimetri(doc)
        iGlitch, cGlitch = _aggiungi_glitch(doc)
        iPad, cPad, cFrancese, cRitorno = _aggiungi_armonia(doc)

        def bar(n: int) -> int:
            return n * B

        # Tutte le clip originali, intere almeno una volta.
        A.place(doc, iKaleido, cKaleido, bar(0), bar(16))
        A.place(doc, iKit, clipKit[0], bar(8), bar(8))
        A.place(doc, iBass, cBass, bar(16), bar(16))
        A.place(doc, iKit, clipKit[1], bar(16), bar(8))
        A.place(doc, iKit, clipKit[2], bar(24), bar(8))
        A.place(doc, iLead, cLead, bar(32), bar(16))
        A.place(doc, iKit, clipKit[3], bar(32), bar(8))

        # Il break emerge tardi nel primo arco, poi domina il secondo drop.
        A.place(doc, iBreak, cBreakA, bar(24), bar(4))
        A.place(doc, iBreak, cBreakB, bar(28), bar(4))
        A.place(doc, iBreak, cBreakB, bar(56), bar(16))

        # Il pad resta il filo continuo; a battuta 48 si congela nella sesta
        # francese, poi D7alt riapre il ritorno senza una chiusura piena.
        A.place(doc, iPad, cPad, bar(0), bar(48))
        A.place(doc, iPad, cFrancese, bar(48), bar(4))
        A.place(doc, iPad, cRitorno, bar(52), bar(20))

        # Nel miroir riappare Kaleidoscope come clip bianca indipendente.
        cMiroir, _ = A.place_unique(doc, iKaleido, cKaleido, bar(48), bar(8))
        MU.trasponi(doc, cMiroir, semitoni=5)

        # Nel secondo drop il basso originale diventa fondazione un'ottava sotto.
        cBassSub, _ = A.place_unique(doc, iBass, cBass, bar(56), bar(16))
        MU.trasponi(doc, cBassSub, semitoni=-12)
        S.fit_clip_scroll_to_notes(doc, cBassSub)

        # Accrezione IDM: entrate separate, vuoto nel miroir, tutti nel ritorno.
        A.place(doc, *polimetri['IDM5'], bar(0), bar(12))
        A.place(doc, *polimetri['IDM7'], bar(4), bar(12))
        A.place(doc, *polimetri['IDM11'], bar(24), bar(24))
        for nome in ('IDM5', 'IDM7', 'IDM11'):
            A.place(doc, *polimetri[nome], bar(56), bar(16))
        for n in (15, 31, 39, 47, 55, 63, 71):
            A.place(doc, iGlitch, cGlitch, bar(n), bar(1))

        A.fit_view(doc)
        A.open_in_arranger(doc)

    return doc, {
        'originali': originali,
        'francese': cFrancese,
        'break': (cBreakA, cBreakB),
    }


if __name__ == '__main__':
    from delugexml import arranger as A

    doc, meta = costruisci()
    print(MU.racconta_armonia(' | '.join(ARMONIA_A),
                              voicing='senza-fondamentale', registro='do3'))
    print('campione:', SAMPLE, 'frames:', FRAMES,
          'trasposizione:', TRASPOSIZIONE_BREAK)
    print('clip originali:', ', '.join(meta['originali']))
    print('arco:', A.extent(doc), '(atteso (0, %d))' % (TOT_BARS * B))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
