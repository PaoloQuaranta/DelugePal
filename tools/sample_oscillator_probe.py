"""P1 oscillatore sample: quattro synth nuovi con playback isolato.

Usa l'Amen break gia' verificato sulla SD. La prima sezione e' attiva; le
altre si lanciano una alla volta per confrontare loop, reverse e stretch.
"""

from pathlib import Path

from delugexml import Note, parse_file, write_file
from delugexml import create as C, kit as K, musica as MU, song as S
from delugexml.writer import FormatTable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/SAMPLEOSC01.XML'
SAMPLE = 'SAMPLES/sampleswap/advanced_operator_samplepack/drums/original AMEN.wav'
FRAMES = 268795
CASES = (
    ('ONCE', 'once', False, False),
    ('LOOP', 'loop', False, False),
    ('REVERSE', 'once', True, False),
    ('STRETCH', 'stretch', False, True),
)


def costruisci():
    doc = parse_file(ROOT / 'refs/songs/TEMPL0.XML')
    for inst in list(S.instruments(doc)):
        MU.togli(doc, inst)
    S.set_bpm(doc.root, 171)
    S.set_scale(doc, 'C', 'maggiore')
    length = S.ticks_per_bar(doc.root) * 8
    for index, (name, loop, reverse, stretch) in enumerate(CASES):
        inst, clip = C.add_track(
            doc, ROOT / 'refs/synths/TEMPL.XML', name=name, folder='SYNTHS',
            length=length, section=str(index), playing=index == 0,
        )
        clip.set('clipName', name)
        K.set_sample(inst, SAMPLE, start=0, end=FRAMES)
        K.set_sample_playback(inst, loop=loop, reverse=reverse, stretch=stretch)
        S.write_notes(S.note_row(clip, 60, create=True),
                      [Note(pos=0, length=length - 1, velocity=100)],
                      create=True)
        S.fit_clip_scroll_to_notes(doc, clip)
    return doc


def scrivi(path=OUT):
    doc = costruisci()
    errors = MU.verifica(doc)
    if errors:
        raise ValueError(errors)
    write_file(doc, path, FormatTable.load(ROOT / 'out/format_table.json'))
    reread = parse_file(path)
    if MU.verifica(reread) or MU.avvertenze(reread):
        raise ValueError('la rilettura del probe ha errori o avvertenze')
    return path


if __name__ == '__main__':
    doc = costruisci()
    print(MU.racconta(doc))
    print('verifica:', MU.verifica(doc))
    print('avvertenze:', MU.avvertenze(doc))
    print('scritto:', scrivi())
    print('destinazione:', MU.destinazione('sampleosc', 1, 'SONGS'))
