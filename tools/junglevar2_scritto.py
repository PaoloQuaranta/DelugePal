"""JUNGLEVAR02 -- revisione ritmica senza lo slicer Scorpio.

Parte sempre dalla JUNGLEVAR01 appena riscaricata dal Deluge. Le quattro clip
972 dell'utente restano intatte e suonano per intero; da quel vocabolario
nascono tre groove programmati e tre fill. I parameter lock vivono sulle
singole righe del kit (step automation), non sui kitParams globali.

Forma ritmica della revisione:

    8-39   le quattro clip 972 originali, una dopo l'altra
    40-47  MOTOR, poi FILL-A
    48-51  MIROIR armonico senza batteria principale
    52-55  MIRROR, poi FILL-B
    56-63  FRACTURE, poi FILL-C
    64-71  MOTOR -> FRACTURE -> FILL-A

Nessun nuovo campione viene affettato e lo strumento SCORPIO viene rimosso.
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

B = MU.TICK_PER_BATTUTA
P = MU.TICK_PER_MOVIMENTO // 4
S32 = P // 2
SOURCE = RADICE / 'out' / 'JUNGLEVAR01_fresh.XML'


def strumento(doc, nome: str):
    """Lo strumento della song identificato dal nome umano."""
    from delugexml import song as S                           # noqa: PLC0415
    for inst in S.instruments(doc):
        if inst.get('presetName') == nome or inst.get('name') == nome:
            return inst
    raise ValueError(f'nessuno strumento {nome!r} nella song')


def _nota(pos: int, *, durata: int = P, velocity: int = 96):
    from delugexml.notes import Note                          # noqa: PLC0415
    return Note(pos=pos, length=durata, velocity=velocity)


def _duplica(doc, clip, *, section: str, name: str, length: int):
    from delugexml import song as S                           # noqa: PLC0415
    indice = next(i for i, (_, c) in enumerate(S.clips(doc)) if c is clip)
    copia = S.duplicate_clip(doc, indice, section=section, name=name)
    S.set_clip_length(copia, length)
    return copia


def _pulisci_clip(doc, clip) -> None:
    """Toglie note e automazioni ereditate, conservando le righe del kit."""
    from delugexml import automation as AU, song as S         # noqa: PLC0415
    from delugexml import sound as SND                        # noqa: PLC0415
    for riga in S.note_rows(clip):
        MU.togli(doc, riga)
        cont = SND.container(riga)
        if cont is None:
            continue
        for param, valore in list(cont.attrs):
            if AU.is_automation(valore):
                testa, _ = AU.decode(valore)
                SND.set_raw(riga, param, f'0x{testa:08X}')


def _scrivi(doc, clip, parte: dict[str, list]) -> None:
    for drum, note in parte.items():
        if note:
            MU.scrivi(doc, clip, note, dove=drum)


def _a_bar(bar: int, step: int = 0, sub: int = 0) -> int:
    return bar * B + step * P + sub * S32


def _motor() -> dict[str, list]:
    """Fondamento continuo: half-time leggibile, bordi rapidi e ghost."""
    parte = {'6': [], '7': [], '13': [], '14': [], '16': []}
    for bar in range(4):
        parte['6'] += [_nota(_a_bar(bar, 0), velocity=116),
                       _nota(_a_bar(bar, 10 if bar % 2 == 0 else 6), velocity=91)]
        parte['7'] += [_nota(_a_bar(bar, 8), velocity=121),
                       _nota(_a_bar(bar, 7), durata=S32, velocity=48)]
        parte['14'] += [_nota(_a_bar(bar, s), durata=S32,
                              velocity=74 if s % 4 else 92)
                        for s in range(0, 16, 2)]
    parte['13'] += [_nota(_a_bar(0, 3), durata=S32, velocity=63),
                    _nota(_a_bar(1, 13), durata=S32, velocity=72),
                    _nota(_a_bar(2, 5), durata=S32, velocity=58),
                    _nota(_a_bar(3, 14), durata=S32, velocity=79)]
    parte['16'] += [_nota(_a_bar(1, 15), durata=S32, velocity=82),
                    _nota(_a_bar(3, 15), durata=S32, velocity=99)]
    return parte


def _fracture() -> dict[str, list]:
    """Stesso peso half-time, ma con buchi, spostamenti e burst a 1/32."""
    parte = {'6': [], '7': [], '11': [], '13': [], '15': [], '16': []}
    casse = ((0, 0), (0, 11), (1, 3), (1, 14), (2, 0), (2, 6), (3, 2), (3, 13))
    parte['6'] = [_nota(_a_bar(b, s), velocity=112 if s < 4 else 88)
                  for b, s in casse]
    parte['7'] = [_nota(_a_bar(0, 8), velocity=119),
                  _nota(_a_bar(1, 9), velocity=113),
                  _nota(_a_bar(2, 7), velocity=116),
                  _nota(_a_bar(3, 8), velocity=124)]
    parte['11'] = [_nota(_a_bar(0, 5), durata=S32, velocity=61),
                   _nota(_a_bar(2, 12), durata=S32, velocity=70)]
    parte['13'] = [_nota(_a_bar(b, s), durata=S32, velocity=55 + 5 * b)
                   for b, s in ((0, 2), (1, 6), (2, 10), (3, 14))]
    for bar, step in ((0, 14), (1, 7), (2, 14), (3, 12)):
        parte['15'] += [_nota(_a_bar(bar, step, k), durata=S32,
                              velocity=104 - 9 * k) for k in range(2)]
    parte['16'] = [_nota(_a_bar(1, 15), durata=S32, velocity=88),
                   _nota(_a_bar(3, 15), durata=S32, velocity=106)]
    return parte


def _mirror() -> dict[str, list]:
    """Figura rarefatta: risposte filtrate e spazio prima del secondo drop."""
    return {
        '6': [_nota(_a_bar(0, 0), velocity=108),
              _nota(_a_bar(1, 12), velocity=84),
              _nota(_a_bar(2, 0), velocity=110),
              _nota(_a_bar(3, 10), velocity=87)],
        '7': [_nota(_a_bar(0, 8), velocity=116),
              _nota(_a_bar(2, 8), velocity=120)],
        '13': [_nota(_a_bar(0, 3), durata=S32, velocity=56),
               _nota(_a_bar(1, 7), durata=S32, velocity=61),
               _nota(_a_bar(2, 11), durata=S32, velocity=67),
               _nota(_a_bar(3, 15), durata=S32, velocity=74)],
        '14': [_nota(_a_bar(b, s), durata=S32, velocity=60 + 4 * b)
               for b, s in ((0, 6), (1, 2), (2, 14), (3, 4))],
        '16': [_nota(_a_bar(3, 14), durata=S32, velocity=91)],
    }


def _fill_a() -> dict[str, list]:
    return {
        '7': [_nota(0, velocity=116)],
        '14': [_nota(8 * P + k * S32, durata=S32,
                     velocity=72 + 6 * k) for k in range(8)],
        '16': [_nota(15 * P, durata=S32, velocity=118)],
    }


def _fill_b() -> dict[str, list]:
    return {
        '11': [_nota(6 * P, durata=S32, velocity=83),
               _nota(9 * P, durata=S32, velocity=90)],
        '13': [_nota(10 * P + k * P, durata=S32, velocity=88 + 5 * k)
               for k in range(3)],
        '15': [_nota(13 * P + k * S32, durata=S32, velocity=107 - 7 * k)
               for k in range(4)],
    }


def _fill_c() -> dict[str, list]:
    return {
        '6': [_nota(0, velocity=119), _nota(7 * P, velocity=94)],
        '7': [_nota(8 * P, velocity=123)],
        '13': [_nota(11 * P, durata=S32, velocity=72)],
        '14': [_nota(12 * P + k * S32, durata=S32,
                     velocity=82 + 7 * k) for k in range(6)],
        '16': [_nota(15 * P, durata=S32, velocity=121)],
    }


def _blocchi(doc, clip, nome: str) -> None:
    """Scrive una tavolozza diversa di lock su ogni groove lungo."""
    if nome == '972-MOTOR':
        MU.blocca_passi(doc, clip, '14', 'lpfFrequency',
                        [(0, 18), (4 * P, 31), (8 * P, 22), (12 * P, 39),
                         (B, 25), (2 * B, 34), (3 * B, 20)])
        MU.blocca_passi(doc, clip, '7', 'lpfResonance',
                        [(8 * P, 18), (B + 8 * P, 34),
                         (2 * B + 8 * P, 22), (3 * B + 8 * P, 40)])
        MU.blocca_passi(doc, clip, '13', 'pan',
                        [(3 * P, 8), (B + 13 * P, 42),
                         (2 * B + 5 * P, 14), (3 * B + 14 * P, 38)])
    elif nome == '972-FRACTURE':
        MU.blocca_passi(doc, clip, '15', 'sampleRateReduction',
                        [(14 * P, 9), (B + 7 * P, 27),
                         (2 * B + 14 * P, 16), (3 * B + 12 * P, 38)])
        MU.blocca_passi(doc, clip, '15', 'bitCrush',
                        [(14 * P, 5), (B + 7 * P, 18),
                         (2 * B + 14 * P, 11), (3 * B + 12 * P, 31)])
        MU.blocca_passi(doc, clip, '7', 'delayRate',
                        [(8 * P, 14), (B + 9 * P, 36),
                         (2 * B + 7 * P, 21), (3 * B + 8 * P, 43)])
        MU.blocca_passi(doc, clip, '13', 'delayFeedback',
                        [(2 * P, 16), (B + 6 * P, 31),
                         (2 * B + 10 * P, 28), (3 * B + 14 * P, 20)])
    elif nome == '972-MIRROR':
        MU.blocca_passi(doc, clip, '13', 'reverbAmount',
                        [(3 * P, 36), (B + 7 * P, 43),
                         (2 * B + 11 * P, 32), (3 * B + 15 * P, 47)])
        MU.blocca_passi(doc, clip, '14', 'pan',
                        [(6 * P, 6), (B + 2 * P, 44),
                         (2 * B + 14 * P, 11), (3 * B + 4 * P, 39)])
        MU.blocca_passi(doc, clip, '6', 'lpfFrequency',
                        [(0, 17), (B + 12 * P, 29),
                         (2 * B, 21), (3 * B + 10 * P, 35)])


def costruisci(source: Path | str = SOURCE) -> tuple[object, dict]:
    """Rimuove lo slicer dalla JUNGLEVAR01 e sviluppa il kit 972."""
    from delugexml import arranger as A, parse_file, song as S  # noqa: PLC0415

    doc = parse_file(str(source))

    rimossi = []
    for nome in ('SCORPIO', 'GLITCH'):
        try:
            inst = strumento(doc, nome)
        except ValueError:
            continue
        rimossi.append(nome)
        MU.togli(doc, inst)

    i972 = strumento(doc, '972')
    originali = sorted(
        [c for _, c in S.clips(doc)
         if S.instrument_of(doc, c) is i972
         and c.has('section')
         and not (c.get('clipName') or '').startswith('972-')],
        key=lambda c: int(c.get('section')))
    if len(originali) != 4:
        raise ValueError(f'attese quattro clip 972 originali, trovate {len(originali)}')

    specifiche = [
        ('972-MOTOR', '4', 4 * B, _motor()),
        ('972-FRACTURE', '5', 4 * B, _fracture()),
        ('972-MIRROR', '6', 4 * B, _mirror()),
        ('972-FILL-A', '7', B, _fill_a()),
        ('972-FILL-B', '8', B, _fill_b()),
        ('972-FILL-C', '9', B, _fill_c()),
    ]
    nuove = {}
    for nome, sezione, durata, parte in specifiche:
        clip = _duplica(doc, originali[-1], section=sezione,
                        name=nome, length=durata)
        _pulisci_clip(doc, clip)
        _scrivi(doc, clip, parte)
        if 'FILL' not in nome:
            _blocchi(doc, clip, nome)
        nuove[nome] = clip

    def bar(n: int) -> int:
        return n * B

    # Nessuna sovrapposizione sullo stesso kit: le quattro originali restano
    # intere a 8-40; lo sviluppo comincia subito dopo.
    A.place(doc, i972, nuove['972-MOTOR'], bar(40), bar(7))
    A.place(doc, i972, nuove['972-FILL-A'], bar(47), bar(1))
    A.place(doc, i972, nuove['972-MIRROR'], bar(52), bar(3))
    A.place(doc, i972, nuove['972-FILL-B'], bar(55), bar(1))
    A.place(doc, i972, nuove['972-FRACTURE'], bar(56), bar(7))
    A.place(doc, i972, nuove['972-FILL-C'], bar(63), bar(1))
    A.place(doc, i972, nuove['972-MOTOR'], bar(64), bar(4))
    A.place(doc, i972, nuove['972-FRACTURE'], bar(68), bar(3))
    A.place(doc, i972, nuove['972-FILL-A'], bar(71), bar(1))

    A.fit_view(doc)
    A.open_in_arranger(doc)
    return doc, {'variazioni': nuove, 'rimossi': rimossi,
                 'originali_972': originali}


if __name__ == '__main__':
    from delugexml import arranger as A

    doc, meta = costruisci()
    print('rimossi:', ', '.join(meta['rimossi']))
    print('nuove clip:', ', '.join(meta['variazioni']))
    print('arco:', A.extent(doc))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
