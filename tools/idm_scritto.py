"""ELETTRONICA / IDM astratto: polimetro, metallo e automazione lenta.

Pezzo originale nel territorio dell'IDM meccanica e non-lineare: non riprende
melodie, riff, pattern o firme sonore di un artista specifico. Il motore e'
l'interazione di quattro periodi coprimi (5/6/7/11 sedicesimi), non lo swing.

Forma, 40 battute, per accrezione e mutazione:
    0-3    THUD-A + CLICK + HAT
    4-19   + METAL + DRONE; THUD muta ogni otto battute
    20-27  interludio fratturato, mai ridotto alla sola cassa
    28-39  tutti gli strati, THUD variato e glitch distribuiti

Il drone Re-Lab e' volutamente cromatico: il tritono resta l'unico centro di
gravita' mentre cutoff e risonanza si aprono lentamente. Ritmo, timbri, forma e
livelli sono [DEC] e richiedono ascolto pieno sul dispositivo.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

B = MU.TICK_PER_BATTUTA      # 384
MOV = MU.TICK_PER_MOVIMENTO  # 96
P = MOV // 4                 # 24, un sedicesimo
S32 = P // 2                 # 12, un trentaduesimo

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
KIT = RADICE / 'refs' / 'kits' / '808 From Mars.XML'
PRESET_DRONE = RADICE / 'refs' / 'synths' / 'TEMPL.XML'

BD = 'BD B 808 Decay C 02'
RIM = 'Rim Shot A 808'
CLAVE = 'Claves A 808'
CH = 'CH Combo 808'
MARAC = 'Maracas B 808'
COWB = 'Cowbell A 808'
CYM = 'Cym A 808 Decay C 01'

BPM = 90
SWING = 50
TOT_BARS = 40
DRONE_BARS = 36

# Periodi primi fra loro, espressi in sedicesimi. Il riallineamento completo
# arriva dopo mcm(5, 6, 7, 11) = 2310 sedicesimi, molto oltre il pezzo.
PERIODI = {'THUD': 6, 'CLICK': 5, 'HAT': 7, 'METAL': 11}


def _nota(passo: int, *, durata: int = P, velocity: int = 100):
    from delugexml.notes import Note                          # noqa: PLC0415
    return Note(pos=passo * P, length=durata, velocity=velocity)


def thud() -> dict:
    """Cellula 6/16: due masse asimmetriche, la seconda piu' leggera."""
    return {BD: [_nota(0, velocity=118), _nota(3, velocity=94)]}


def thud_b() -> dict:
    """Seconda 6/16: un fantasma centrale spinge verso il colpo finale."""
    return {BD: [_nota(0, velocity=116), _nota(2, velocity=72),
                 _nota(5, velocity=98)]}


def thud_c() -> dict:
    """Terza 6/16: l'accento ruota e lascia vuoto il primo sedicesimo."""
    return {BD: [_nota(1, velocity=88), _nota(4, velocity=112)]}


def click() -> dict:
    """Cellula 5/16: rim in testa e clave fantasma al centro."""
    return {RIM: [_nota(0, velocity=112)], CLAVE: [_nota(2, velocity=84)]}


def hat() -> dict:
    """Cellula 7/16: trama sottile, con chiusura di maraca."""
    return {
        CH: [_nota(1, durata=S32, velocity=70),
             _nota(3, durata=S32, velocity=58),
             _nota(5, durata=S32, velocity=74)],
        MARAC: [_nota(6, durata=S32, velocity=52)],
    }


def metal() -> dict:
    """Cellula 11/16: due accenti metallici radi e sbilanciati."""
    return {
        COWB: [_nota(0, velocity=100)],
        CYM: [_nota(6, durata=2 * P, velocity=82)],
    }


def glitch() -> dict:
    """Una battuta con due burst a 1/32, abbastanza radi da restare eventi."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {RIM: [], CLAVE: []}
    for k in range(6):
        voci[RIM].append(
            Note(pos=2 * P + k * S32, length=S32, velocity=96 - 6 * k))
    for k in range(4):
        voci[CLAVE].append(
            Note(pos=10 * P + k * S32, length=S32, velocity=90 - 8 * k))
    return voci


def glitch_b() -> dict:
    """Gesto complementare: due sciami piu' corti e spostati."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci = {RIM: [], CLAVE: []}
    for k in range(4):
        voci[CLAVE].append(
            Note(pos=5 * P + k * S32, length=S32, velocity=88 - 7 * k))
    for k in range(5):
        voci[RIM].append(
            Note(pos=12 * P + k * S32, length=S32, velocity=100 - 6 * k))
    return voci


def drone() -> dict:
    """Re2 + Lab2, tenuti in blocchi fino a coprire 36 battute."""
    from delugexml.notes import Note                          # noqa: PLC0415
    re, lab = MU.altezza('re2'), MU.altezza('lab2')
    voci = {re: [], lab: []}
    for da_bar in range(0, DRONE_BARS, 8):
        durata = min(8, DRONE_BARS - da_bar) * B
        da = da_bar * B
        voci[re].append(Note(pos=da, length=durata, velocity=56))
        voci[lab].append(Note(pos=da, length=durata, velocity=50))
    return voci


def strumento(doc, nome: str):
    """Restituisce lo strumento col nome/preset richiesto."""
    from delugexml import song as S                           # noqa: PLC0415
    for inst in S.instruments(doc):
        if inst.get('presetName') == nome or inst.get('name') == nome:
            return inst
    raise ValueError(f'nessuno strumento "{nome}" nella song')


def costruisci() -> tuple[object, dict]:
    """Costruisce la song IDM pronta per verifica, scrittura e ascolto."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    from delugexml import sound as SND                       # noqa: PLC0415
    from delugexml import structure as ST                    # noqa: PLC0415

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPL))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, SWING, figura='1/8')
        S.set_scale(doc, 'D', 'minore')
        for inst in list(S.instruments(doc)):
            MU.togli(doc, inst)

        def strato_kit(nome: str, voci: dict, sedicesimi: int, colore: str):
            inst, clip = C.add_track(
                doc, str(KIT), name=nome, folder='KITS',
                length=sedicesimi * P, colour_offset=colore, playing=True)
            for drum, note in voci.items():
                if note:
                    MU.scrivi(doc, clip, note, dove=drum)
            S.set_clip_length(clip, sedicesimi * P)
            return inst, clip

        iThud, cThud = strato_kit('THUD', thud(), PERIODI['THUD'], '0')
        iClick, cClick = strato_kit('CLICK', click(), PERIODI['CLICK'], '16')
        iHat, cHat = strato_kit('HAT', hat(), PERIODI['HAT'], '32')
        iMetal, cMetal = strato_kit('METAL', metal(), PERIODI['METAL'], '48')

        iGlitch, cGlitch = C.add_track(
            doc, str(KIT), name='GLITCH', folder='KITS',
            length=B, colour_offset='24', playing=True)
        for drum, note in glitch().items():
            MU.scrivi(doc, cGlitch, note, dove=drum)

        def variazione_kit(sorgente, nome: str, sezione: str, voci: dict):
            indice = next(i for i, (_, c) in enumerate(S.clips(doc))
                          if c is sorgente)
            copia = S.duplicate_clip(doc, indice, section=sezione, name=nome)
            for riga in list(S.note_rows(copia)):
                MU.togli(doc, riga)
            for drum, note in voci.items():
                if note:
                    MU.scrivi(doc, copia, note, dove=drum)
            return copia

        cThudB = variazione_kit(cThud, 'THUD-B', '1', thud_b())
        cThudC = variazione_kit(cThud, 'THUD-C', '2', thud_c())
        cGlitchB = variazione_kit(cGlitch, 'GLITCH-B', '3', glitch_b())

        iDrone, cDrone = C.add_track(
            doc, str(PRESET_DRONE), name='DRONE', folder='SYNTHS',
            length=DRONE_BARS * B, playing=True)
        # Un drone deve nascere da una sorgente continua. Tal Rhodes usato
        # nelle versioni precedenti era un multisample one-shot: anche con
        # sustain alto, il campione decadeva come un piano elettrico.
        ST.set_osc(iDrone, 1, type='triangle', transpose=0, cents=0)
        ST.set_osc(iDrone, 2, type='analogSaw', transpose=0, cents=-7)
        ST.set_unison(iDrone, num=2, detune=5, spread=14)
        SND.set(cDrone, 'oscAVolume', 30)
        SND.set(cDrone, 'oscBVolume', 18)
        SND.set(cDrone, 'envelope1.attack', 12)
        SND.set(cDrone, 'envelope1.sustain', 50)
        SND.set(cDrone, 'envelope1.release', 24)
        MU.scrivi(doc, cDrone, drone())
        S.set_key_mode(cDrone, False)
        S.fit_clip_scroll_to_notes(doc, cDrone)
        # La rampa resta nella fascia aperta gia' approvata all'ascolto; ora
        # muove armoniche generate dal synth, non il decadimento di un sample.
        MU.automatizza(doc, cDrone, 'lpfFrequency', 40, 48,
                       0, DRONE_BARS * B, passi=16)
        MU.automatizza(doc, cDrone, 'lpfResonance', 12, 30,
                       0, DRONE_BARS * B, passi=16)
        SND.set(cDrone, 'reverbAmount', 30)

        def bar(n: int) -> int:
            return n * B

        A.place(doc, iThud, cThud, bar(0), bar(8))
        A.place(doc, iThud, cThudB, bar(8), bar(8))
        A.place(doc, iThud, cThudC, bar(16), bar(8))
        A.place(doc, iThud, cThudB, bar(24), bar(8))
        A.place(doc, iThud, cThudC, bar(32), bar(8))
        A.place(doc, iClick, cClick, bar(0), bar(24))
        A.place(doc, iClick, cClick, bar(28), bar(12))
        A.place(doc, iHat, cHat, bar(0), bar(12))
        A.place(doc, iHat, cHat, bar(16), bar(6))
        A.place(doc, iHat, cHat, bar(24), bar(16))
        A.place(doc, iMetal, cMetal, bar(4), bar(16))
        A.place(doc, iMetal, cMetal, bar(24), bar(16))
        A.place(doc, iDrone, cDrone, bar(4), bar(36))
        for n, clip in ((4, cGlitch), (9, cGlitchB),
                        (14, cGlitch), (18, cGlitchB),
                        (22, cGlitch), (27, cGlitchB),
                        (32, cGlitch), (37, cGlitchB)):
            A.place(doc, iGlitch, clip, bar(n), bar(1))

        A.fit_view(doc)
        A.open_in_arranger(doc)
    return doc, {}


if __name__ == '__main__':
    from math import lcm
    from delugexml import arranger as A

    doc, _ = costruisci()
    periodo = lcm(*PERIODI.values())
    print('polimetro:', list(PERIODI.values()), 'sedicesimi; riallineamento:',
          periodo, 'sedicesimi =', periodo / 16, 'battute')
    print('drone:', MU.nome_altezza(MU.altezza('re2')), '+',
          MU.nome_altezza(MU.altezza('lab2')))
    print('arco:', A.extent(doc), '(atteso (0, %d))' % (TOT_BARS * B))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
