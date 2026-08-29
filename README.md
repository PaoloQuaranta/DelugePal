# DelugePal

Write music for the **Synthstrom Deluge** by describing it in words, and load it
onto the device over USB — no SD card shuffling.

```
prompt  →  library  →  XML  →  SysEx  →  you open it and listen
                                              ↓
        reload as        ←   edit   ←   "the bass is too static"
        a new version         ↑
                    RE-DOWNLOAD from the Deluge before touching it
```

Target firmware: **community 1.3.0-beta** (build `2d7cdf8`, 2026-08-12). It does
not support, and does not try to support, the official firmware.

> **Language.** This README is in English; the documentation and the library API
> are in **Italian**. See [Language](#language) for what that means in practice
> and for what is already bilingual.

---

## What actually works

Everything below has been **verified on the device**, not merely produced as a
file that parses. That distinction is the spine of this project: a Deluge song
can be flawless XML, round-trip byte-for-byte, and still fail to load — or load
and be invisible.

| | |
|---|---|
| **Read and rewrite** | byte-exact round-trip, both surgically and by rebuilding from learned format rules |
| **Tempo, notes, clips** | changing the tempo of an 8577-line song touches exactly 2 lines |
| **Writing over USB** | songs deposited into `SONGS/` with the Deluge powered on, ~60 kB/s, hash-verified by read-back |
| **Instruments from scratch** | a synth or kit instantiated from the device's *empty* preset, with oscillators, FM, filters, envelopes and modulation all designed programmatically |
| **Synthesised drum kits** | a kit drum *is* a full `<sound>` node, so drums can be built from oscillators and noise instead of samples |
| **Modulation** | patch cables — `lfo1 → lpfFrequency` for a wobble, `lfo1 → pitch` for a dub siren, `envelope2 → oscAPitch` for a kick's pitch drop |
| **Automation** | parameter curves, in the firmware's own packed format, decoded |
| **Arranger** | clip instances placed on instrument tracks, including "white" (detached) clips |
| **Removing and transforming** | delete a track or just a stretch of it; transpose chromatically or diatonically; half and double time |
| **MIDI import** | dependency-free Standard MIDI File reader, validated note-for-note against `mido` |

**284 tests pass** out of the box. Another **73 skip**, because they need a
corpus of Deluge songs this repository deliberately does not ship — see
[Bring your own corpus](#bring-your-own-corpus).

---

## The constraint that shaped everything

**The Deluge firmware does not write valid XML.** 255 songs out of 378 are
rejected by a conforming parser:

- `&` is never escaped — confirmed in the firmware source, where
  `writeAttribute` escapes nothing, ever
- duplicated attribute blocks on `<audioClip>`
- a legacy format with two root elements

So `xml.etree` is unusable, and this project has a **tolerant parser written for
the job** that keeps byte offsets into the source. Because of that an unmodified
node is re-emitted by **copying its original bytes**, which is what makes
surgical edits possible and provable.

The formatting table — which attributes go inline and which get their own line —
is **learned from a corpus** rather than derived from rules. That is not a
shortcut: the firmware source shows formatting is a boolean decided at each
individual call site, so there is no rule to find.

---

## The method

Three levels, and confusing them is how this project has repeatedly hurt itself:

> **Documentation says what should be true. Files say how it is written. Only
> the device says whether it works.**

There is a second ordering, for *where to look first*, and it runs the other way:

```
1. community docs  →  2. official guidebook  →  3. firmware source  →  4. local files
```

Local files are the **last** place to look, not the first. Starting there is
reverse engineering without a model, and it has produced — all documented in
`docs/` — statistical analysis of things explained in one sentence of the
manual, four consecutive wrong models of clip-view scrolling that every test
agreed with, and a demolished hypothesis about MIDI rows inside kits.

**Search top-down. Decide bottom-up.**

A corollary learned the hard way: **a corpus of songs is not a specification.**
A feature absent from someone's songs is usually absent because they never used
it, not because the firmware lacks it. The firmware's own parameter enum lists
56 modulation destinations; the corpus that taught this project used 37.

---

## Quick start

Python 3.13. The library itself has no dependencies.

```bash
python tests/test_all.py
```

Describe a song in musical terms:

```bash
python tools/dsong.py info yoursong.XML
```

`tools/delugexml/musica.py` is the layer a language model is meant to call. It
never writes XML itself — it calls library functions that are covered by tests:

```python
from delugexml import parse_file, musica as MU

doc = parse_file('yoursong.XML')
print(MU.racconta(doc))                       # describe it in words

MU.scrivi(doc, clip, MU.passi('x...x...x...x...'), dove='KICK')
MU.scrivi(doc, clip, MU.melodia('re2 fa2 la2', durata='1/8'))
MU.trasponi(doc, clip, gradi=1)
MU.togli(doc, strumento)

assert not MU.verifica(doc)     # the gate: nothing is uploaded if this fails
```

`verifica()` **blocks**; `avvertenze()` **informs**. Nothing reaches the device
while `verifica()` is non-empty. It has already stopped files the Deluge
rejected, one of them with a crash.

Talking to the device needs `mido` and `python-rtmidi` in a virtualenv:

```bash
python -m venv .venv
```

```bash
.venv/bin/python tools/dsysex.py --in "Deluge 0" --out "Deluge 1" get /SONGS/YOURSONG.XML out/YOURSONG.XML
```

`put` refuses to overwrite, and always verifies by reading back: on a channel
that loses messages, a transfer is not assumed good without proof.

---

## Bring your own corpus

`refs/` and `corpus_versions/` are **nearly empty here on purpose**. They held
around 130 songs written by the author's device, plus presets from paid sample
packs — neither is ours to publish. `out/format_table.json` is a derived
artefact and contains no musical content, so it ships.

This is not only a precaution. It is how the project is meant to work: the
format table is learned from *the corpus you have*, and the corpus that matters
is your own.

To populate it, copy from your SD card:

```
refs/songs/       songs written by your Deluge  — this is what most tests need
refs/kits/        kit presets
refs/synths/      synth presets
```

`refs/synths/TEMPL.XML` **is** included: it is the device's empty synth — two
square oscillators, filter wide open, effects at zero — which is firmware
defaults rather than anyone's sound design. It is the chassis every generated
instrument is built from.

Tests that need material you have not supplied print `SKIP` with the reason.
They are not failures.

---

## Language

The documentation and the API are Italian, and translation is not currently
planned. The prose alone is around 50 000 words, and the Python docstrings are
essays about *why* something is the way it is rather than descriptions of
arguments — that reasoning is the most valuable thing in the repository and the
most expensive to move.

What is **already bilingual** is the part you are most likely to touch: the
musical vocabulary. Note names work in either language, with sharps and flats.

```python
MU.altezza('re2')  == MU.altezza('D2')
MU.altezza('sib3') == MU.altezza('Bb3')
```

A glossary, if you want to read the source:

| Italian | English |
|---|---|
| `altezza` | pitch |
| `passi` | steps — a drum pattern, one character per sixteenth |
| `melodia`, `accordi` | melody, chords |
| `scrivi`, `togli` | write, remove |
| `trasponi`, `sposta` | transpose, shift in time |
| `verifica`, `avvertenze` | the gate (blocks), warnings (inform) |
| `racconta` | describe in words |
| `destinazione`, `origine` | where to save, where to read from |

---

## Layout

```
tools/delugexml/      the library
  parser.py           tolerant parser, keeps byte offsets into the source
  writer.py           serializer + format table learned from a corpus
  notes.py            note blob encoding
  song.py             tempo, clips, notes, scales, scroll geometry
  sound.py            sound parameters and patch cables
  structure.py        synthesis structure, rejecting values never observed
  automation.py       parameter automation codec
  kit.py              kits and drums
  arranger.py         clip instances on the timeline
  midi.py             Standard MIDI File reader, no dependencies
  musica.py           the natural-language layer
tools/dsong.py        CLI
tools/dsysex.py       SysEx client: ping, get, put
docs/                 the reasoning, with numbers and proofs
tests/test_all.py     regression suite
```

Reading order, all Italian:

1. `docs/ARCHITETTURA.md` — the conceptual model, from the official guidebook
2. `docs/FINDINGS.md` — the schema derived from real files, with counts
3. `docs/SYSEX.md` — the USB MIDI channel
4. `docs/MUSICA.md` — composition knowledge, by genre
5. `HANDOFF.md` — current state and what to do next

---

## Known limits

- **The corpus teaches only what it contains.** An element never seen falls back
  to a heuristic, which has always worked in leave-one-out testing but is not
  guaranteed.
- **`preview` is a cached thumbnail** and is not recomputed on load, so generated
  songs show the wrong picture in the file browser until the device re-saves.
- **Open questions remain**: what `inKeyScrollOffset` and `drumsScrollOffset`
  actually govern, the section colour table, and whether a note row's own
  `length` really produces the polyrhythm it appears to promise.
- **A green test suite is not a substitute for listening.** Four successive
  wrong models of clip-view geometry were each covered by passing tests, because
  a test written by someone holding a wrong idea confirms the wrong idea. They
  were only caught by looking at the device's screen.

---

## Licence

**GPL-3.0** — see [LICENSE](LICENSE).

## Credits

The Deluge is made by [Synthstrom Audible](https://synthstrom.com/). This project
is not affiliated with them and learns the community firmware's file format by
observation. Built with [Claude Code](https://claude.com/claude-code).

### Musical corpora

The measured musical knowledge in `docs/MUSICA.md` and `docs/repertori/` is
derived from two datasets. Neither is redistributed here — they live outside the
repository — but the numbers derived from them **are** published, which is what
the attribution is for. How each licence was read, and the one clause that
differs between them, is in [docs/FONTI.md](docs/FONTI.md).

**Groove MIDI Dataset** — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Source of the velocity scale and the groove templates.

> Jon Gillick, Adam Roberts, Jesse Engel, Douglas Eck, and David Bamman.
> "Learning to Groove with Inverse Sequence Transformations."
> *International Conference on Machine Learning (ICML)*, 2019.
> <https://magenta.tensorflow.org/datasets/groove>

**Weimar Jazz Database (WJazzD)** v2.1 — The Jazzomat Research Project (c)
2012-2017. Database under [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1.0/),
individual contents under [DbCL 1.0](https://opendatacommons.org/licenses/dbcl/1.0/).
Source of the measured swing and the harmonic grids.

> Pfleiderer, Martin; Frieler, Klaus; Abeßer, Jakob; Zaddach, Wolf-Georg;
> Burkhart, Benjamin (eds.) (2017): *Inside the Jazzomat — New Perspectives for
> Jazz Research*. Schott Campus.
> <https://jazzomat.hfm-weimar.de/>

