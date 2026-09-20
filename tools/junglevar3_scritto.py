"""JUNGLEVAR03 -- dinamica prudente, pad vivo, batteria e bassi piu incisivi.

La sorgente e sempre il file JUNGLEVAR02 appena riscaricato dal Deluge. I
livelli del SYMBOLIST PAD non vengono toccati: le nuove clip ne ereditano i
byte esatti e aggiungono soltanto curve lente. Il feedback ordinario resta a
25 o meno; due micro-accenti possono arrivare a 28 per un solo trentaduesimo.
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
SOURCE = RADICE / 'out' / 'JUNGLEVAR02_user.XML'


def carica_sorgente(source: Path | str = SOURCE):
    from delugexml import parse_file                         # noqa: PLC0415
    return parse_file(str(source))


def strumento(doc, nome: str):
    from delugexml import song as S                          # noqa: PLC0415
    for inst in S.instruments(doc):
        if inst.get('presetName') == nome or inst.get('name') == nome:
            return inst
    raise ValueError(f'nessuno strumento {nome!r} nella song')


def _nota(pos: int, durata: int = P, velocity: int = 96):
    from delugexml.notes import Note                         # noqa: PLC0415
    return Note(pos=pos, length=durata, velocity=velocity)


def _duplica(doc, clip, *, section: str, name: str):
    from delugexml import song as S                          # noqa: PLC0415
    indice = next(i for i, (_, c) in enumerate(S.clips(doc)) if c is clip)
    return S.duplicate_clip(doc, indice, section=section, name=name)


def _svuota_note(doc, clip) -> None:
    from delugexml import song as S                          # noqa: PLC0415
    for riga in list(S.note_rows(clip)):
        MU.togli(doc, riga)


def _scrivi_eventi(doc, clip, eventi: list[tuple[int, int, int, int]]) -> None:
    """Scrive (pitch, pos, durata, velocity) in una clip synth."""
    per_pitch = {}
    for pitch, pos, durata, velocity in eventi:
        per_pitch.setdefault(pitch, []).append(_nota(pos, durata, velocity))
    for pitch, note in per_pitch.items():
        MU.scrivi(doc, clip, sorted(note, key=lambda n: n.pos), dove=pitch)


def _aggiungi_fioritura(doc, clip, drum: str,
                        eventi: list[tuple[int, int]]) -> None:
    from delugexml import song as S                          # noqa: PLC0415
    riga = S.drum_row(doc, clip, drum, create=True)
    note = S.read_notes(riga)
    occupate = {n.pos for n in note}
    note.extend(_nota(pos, S32, vel) for pos, vel in eventi if pos not in occupate)
    S.write_notes(riga, sorted(note, key=lambda n: n.pos), create=True)


def _clip_per_nome(doc, inst, nome: str):
    from delugexml import song as S                          # noqa: PLC0415
    return next(c for _, c in S.clips(doc)
                if S.instrument_of(doc, c) is inst and c.get('clipName') == nome)


def _evolvi_pad(doc) -> dict[str, object]:
    from delugexml import arranger as A, song as S           # noqa: PLC0415

    pad = strumento(doc, 'SYMBOLIST PAD')
    clip = [c for _, c in S.clips(doc) if S.instrument_of(doc, c) is pad]
    principale = next(c for c in clip if not c.get('clipName'))
    ritorno = next(c for c in clip if c.get('clipName') == 'RITORNO')

    lungo = _duplica(doc, principale, section='7', name='PAD-EVOLVE')
    MU.repeat(doc, lungo, 3)
    coda = _duplica(doc, ritorno, section='8', name='RITORNO-EVOLVE')
    MU.repeat(doc, coda, 5)

    def curva(c, param, valori):
        fine = int(c.get('length')) - 1
        pos = [0, fine // 4, fine // 2, 3 * fine // 4, fine]
        MU.automatizza_punti(doc, c, param, list(zip(pos, valori)))

    # Movimenti larghi e loop-safe: niente cambi di volume.
    for param, valori in {
        'lpfFrequency': (34, 38, 42, 37, 34),
        'lpfResonance': (14, 16, 20, 17, 14),
        'pan': (23, 27, 25, 21, 23),
        'reverbAmount': (20, 23, 26, 22, 20),
    }.items():
        curva(lungo, param, valori)
    for param, valori in {
        'lpfFrequency': (35, 39, 43, 38, 35),
        'lpfResonance': (14, 17, 21, 16, 14),
        'pan': (22, 27, 25, 29, 22),
        'reverbAmount': (20, 24, 27, 23, 20),
    }.items():
        curva(coda, param, valori)

    A.remove_instances_in(pad, 0, 48 * B)
    A.remove_instances_in(pad, 52 * B, 72 * B)
    A.place(doc, pad, lungo, 0, 48 * B)
    A.place(doc, pad, coda, 52 * B, 20 * B)
    return {'PAD-EVOLVE': lungo, 'RITORNO-EVOLVE': coda}


def _sviluppa_kit(doc) -> dict[str, object]:
    kit = strumento(doc, '972')
    fill_a = _clip_per_nome(doc, kit, '972-FILL-A')
    fill_b = _clip_per_nome(doc, kit, '972-FILL-B')
    fill_c = _clip_per_nome(doc, kit, '972-FILL-C')
    motor = _clip_per_nome(doc, kit, '972-MOTOR')
    fracture = _clip_per_nome(doc, kit, '972-FRACTURE')
    mirror = _clip_per_nome(doc, kit, '972-MIRROR')

    _aggiungi_fioritura(doc, fill_a, '13',
                        [(9 * P, 66), (9 * P + S32, 74),
                         (10 * P, 82), (10 * P + S32, 91)])
    _aggiungi_fioritura(doc, fill_b, '14',
                        [(4 * P, 58), (4 * P + S32, 68),
                         (5 * P, 77), (5 * P + S32, 88)])
    _aggiungi_fioritura(doc, fill_c, '15',
                        [(9 * P, 64), (9 * P + S32, 73),
                         (10 * P, 86), (10 * P + S32, 98)])

    # Ratchet solo su accenti strutturali; il reset al 1/32 evita code.
    MU.blocca_passi(doc, motor, '14', 'ratchetAmount',
                    [(12 * P, 29), (12 * P + S32, 0),
                     (2 * B + 12 * P, 34), (2 * B + 12 * P + S32, 0)])
    MU.blocca_passi(doc, motor, '14', 'ratchetProbability',
                    [(12 * P, 37), (12 * P + S32, 0),
                     (2 * B + 12 * P, 41), (2 * B + 12 * P + S32, 0)])
    MU.blocca_passi(doc, fracture, '15', 'ratchetAmount',
                    [(14 * P, 32), (14 * P + S32, 0),
                     (3 * B + 12 * P, 38), (3 * B + 12 * P + S32, 0)])
    MU.blocca_passi(doc, fracture, '15', 'ratchetProbability',
                    [(14 * P, 40), (14 * P + S32, 0),
                     (3 * B + 12 * P, 44), (3 * B + 12 * P + S32, 0)])

    # Coppie accento/reset: vere modulazioni one-shot, non rampe lunghe.
    MU.blocca_passi(doc, fill_a, '13', 'pan',
                    [(9 * P, 8), (9 * P + S32, 25),
                     (10 * P, 43), (10 * P + S32, 25)])
    MU.blocca_passi(doc, fill_a, '14', 'envelope1.decay',
                    [(8 * P, 9), (8 * P + S32, 25),
                     (10 * P, 39), (10 * P + S32, 25)])
    MU.blocca_passi(doc, fill_b, '14', 'lpfFrequency',
                    [(4 * P, 13), (4 * P + S32, 25),
                     (5 * P, 41), (5 * P + S32, 25)])
    MU.blocca_passi(doc, fill_b, '15', 'bitCrush',
                    [(13 * P, 18), (13 * P + S32, 0),
                     (14 * P, 27), (14 * P + S32, 0)])
    MU.blocca_passi(doc, fill_c, '15', 'sampleRateReduction',
                    [(9 * P, 17), (9 * P + S32, 0),
                     (10 * P, 31), (10 * P + S32, 0)])
    MU.blocca_passi(doc, mirror, '13', 'envelope1.decay',
                    [(3 * P, 10), (3 * P + S32, 25),
                     (2 * B + 11 * P, 40), (2 * B + 11 * P + S32, 25)])

    # Due soli lampi oltre 25, entrambi lunghi un 1/32 e con ritorno a 14.
    MU.blocca_passi(doc, fill_c, '16', 'delayFeedback',
                    [(0, 14), (15 * P, 28), (15 * P + S32, 14)])
    MU.blocca_passi(doc, fill_a, '16', 'delayFeedback',
                    [(0, 14), (15 * P, 27), (15 * P + S32, 14)])
    return {'fill': (fill_a, fill_b, fill_c),
            'groove': (motor, fracture, mirror)}


def _sviluppa_bassi(doc) -> dict[str, object]:
    from delugexml import arranger as A, song as S           # noqa: PLC0415

    basso = strumento(doc, '31-BASS1')
    origine = next(c for _, c in S.clips(doc)
                   if S.instrument_of(doc, c) is basso and c.has('section'))
    push = _duplica(doc, origine, section='4', name='BASS-PUSH')
    climax = _duplica(doc, origine, section='5', name='BASS-CLIMAX')
    for c in (push, climax):
        _svuota_note(doc, c)
        S.set_clip_length(c, 4 * B)

    push_eventi = []
    climax_eventi = []
    for bar in range(4):
        base = bar * B
        # G con risposte D/A/B: note corte davanti al beat e appoggi lunghi.
        schema_push = [(31, 0, P * 2, 116), (38, 3 * P, P, 101),
                       (31, 6 * P, P, 108), (33, 9 * P, P, 96),
                       (35, 11 * P, P, 104), (38, 14 * P, P * 2, 113)]
        for pitch, pos, durata, vel in schema_push:
            push_eventi.append((pitch, base + pos, durata, vel))

        # Nel climax il pedale di G prende approcci cromatici Ab/F# e piu
        # sincopi; resta spazio fra i colpi per il raddoppio di Kaleidoscope.
        crom = 32 if bar in (1, 2) else 30
        schema_climax = [(31, 0, P, 121), (38, 2 * P, P, 108),
                         (31, 5 * P, P, 114), (crom, 7 * P, P, 88),
                         (33, 9 * P, P, 104), (35, 11 * P, P, 112),
                         (38, 14 * P, P, 118)]
        for pitch, pos, durata, vel in schema_climax:
            climax_eventi.append((pitch, base + pos, durata, vel))
    _scrivi_eventi(doc, push, push_eventi)
    _scrivi_eventi(doc, climax, climax_eventi)

    # Sostituisce soltanto il basso bianco del climax; le clip originali
    # restano nella song e le loro precedenti istanze restano intatte.
    A.remove_instances_in(basso, 56 * B, 72 * B)
    A.place(doc, basso, push, 40 * B, 8 * B)
    A.place(doc, basso, climax, 56 * B, 16 * B)

    kaleido = strumento(doc, 'Kaleidoscope')
    k_orig = next(c for _, c in S.clips(doc)
                  if S.instrument_of(doc, c) is kaleido and c.has('section'))
    doppio = _duplica(doc, k_orig, section='4', name='KALEIDO-DOUBLE')
    _svuota_note(doc, doppio)
    S.set_clip_length(doppio, 4 * B)
    selezionati = [e for i, e in enumerate(climax_eventi) if i % 3 == 0]
    _scrivi_eventi(doc, doppio,
                   [(pitch + 12, pos, durata, max(52, vel - 38))
                    for pitch, pos, durata, vel in selezionati])
    A.place(doc, kaleido, doppio, 56 * B, 16 * B)
    return {'BASS-PUSH': push, 'BASS-CLIMAX': climax,
            'KALEIDO-DOUBLE': doppio}


def costruisci(source: Path | str = SOURCE) -> tuple[object, dict]:
    from delugexml import arranger as A                     # noqa: PLC0415

    doc = carica_sorgente(source)
    limite = MU.limita_feedback_delay(doc, massimo=25, finale=14)
    pad = _evolvi_pad(doc)
    kit = _sviluppa_kit(doc)
    bassi = _sviluppa_bassi(doc)
    A.fit_view(doc)
    A.open_in_arranger(doc)
    return doc, {'pad': pad, 'kit': kit, 'bassi': bassi,
                 'feedback': limite, 'source': str(source)}


if __name__ == '__main__':
    from delugexml import arranger as A

    doc, meta = costruisci()
    print('sorgente:', meta['source'])
    print('feedback:', meta['feedback'])
    print('arco:', A.extent(doc))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
