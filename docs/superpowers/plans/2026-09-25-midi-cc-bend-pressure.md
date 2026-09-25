# MIDI CC, Bend and Pressure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add safe, round-trippable MIDI CC, pitch-bend and channel-pressure automation to MIDI clips.

**Architecture:** Keep the AutoParam codec in `automation.py` and add the MIDI-specific value scales and XML placement to `midicv.py`. Expose typed read/write functions, keep CC ramps discrete, and use native interpolation only for expression data.

**Tech Stack:** Python 3 standard library, `delugexml` tolerant parser/writer, custom `tests/test_all.py` runner.

**Spec:** `docs/superpowers/specs/2026-09-25-midi-cc-bend-pressure-design.md`

## Global Constraints

- Target beta 20260925, firmware commit `b76ed39`.
- Never interpolate MIDI CC; materialize requested ramps as step nodes.
- Pitch bend range is -8192..8191; pressure and CC range is 0..127, with CC numbers limited to 0..119.
- Validate all input before mutating the document.
- Do not depend on unpublished corpus fixtures.
- Generate and upload probe XML only through the library and `musica.destinazione()`.

## Review Focus

- `bool` values masquerading as integers must be rejected without mutation; Task 1 tests it.
- Duplicate or decreasing ticks must be rejected without mutation; Task 1 tests it.
- Rewriting one CC must not duplicate its `<param>` or disturb another CC; Task 1 tests it.
- Maximum/minimum numeric values must survive serialize/parse exactly; Task 1 tests all endpoints.
- A dense CC ramp with more points than available ticks must fail before mutation; Task 2 tests it.

---

### Task 1: MIDI automation codec and XML placement

**Files:**
- Modify: `tools/delugexml/midicv.py`
- Modify: `tests/test_all.py`

**Interfaces:**
- Consumes: `automation.Punto`, `automation.encode`, `automation.decode`, `parser.Node`.
- Produces: `MIDIValuePoint`, `set_cc_automation`, `read_cc_automation`, `set_pitch_bend`, `read_pitch_bend`, `set_channel_pressure`, `read_channel_pressure`.

- [ ] **Step 1: Write the failing test**

Add `test_midi_automation()` beside `test_midi_cv()`. Build a minimal song,
call `add_midi_track(..., length=192)`, then assert these independent literals:

```python
M.set_cc_automation(clip, 74, [(0, 0), (48, 64), (96, 127)])
M.set_pitch_bend(clip, [(0, -8192), (48, 0), (96, 8191)])
M.set_channel_pressure(clip, [(0, 0), (48, 64), (96, 127)])

assert raw_cc == [0x80000000, 0x00000000, 0x7E000000]
assert raw_bend == [0x80000000, 0x00000000, 0x7FFC0000]
assert raw_pressure == [0x00000000, 0x40000000, 0x7F000000]
```

Use `check()` rather than bare assertions. Verify CC flags are all false,
expression flags true, child order is
`midiParams, arpeggiator, expressionData, bendRange, bendRangeMPE,
columnControls`, and serialize/parse preserves all public read results.
Snapshot `serialize(doc)` and prove invalid CC number/value, bend, pressure,
tick order, duplicate tick, out-of-clip tick and boolean value leave it equal.
Rewrite CC 74, add CC 1, and prove exactly two `<param>` children remain.

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'tests'); import test_all; test_all.test_midi_automation()"
```

Expected: failure because `set_cc_automation` does not exist.

- [ ] **Step 3: Implement the minimal codec and writers**

In `midicv.py`, add the named tuple, private signed/unsigned conversion
helpers, a preflight validator, relative-child insertion helpers, and the six
public read/write functions. Build new nodes with `Node`; update existing text
with `touch()` and attributes with `set()`. CC nodes are always
`interp=False`; expression nodes use the requested global flag.

- [ ] **Step 4: Run the focused test and verify GREEN**

Run the command from Step 2. Expected: every check printed by
`test_midi_automation` is `PASS`, with no `FAIL`.

- [ ] **Step 5: Commit**

```powershell
git add tools/delugexml/midicv.py tests/test_all.py
git commit -m "feat: add MIDI CC bend and pressure automation"
```

---

### Task 2: Discrete CC ramps and capability documentation

**Files:**
- Modify: `tools/delugexml/midicv.py`
- Modify: `tests/test_all.py`
- Modify: `docs/COPERTURA_DELUGE.md`
- Modify: `.agents/skills/deluge-pal/SKILL.md`

**Interfaces:**
- Consumes: Task 1 `set_cc_automation` and `read_cc_automation`.
- Produces: `ramp_cc`; public usage guidance and an updated capability row.

- [ ] **Step 1: Write the failing ramp test**

Extend `test_midi_automation()`:

```python
M.ramp_cc(clip, 1, 0, 127, 0, 96, steps=5)
```

Expect positions `[0, 24, 48, 72, 96]`, values `[0, 32, 64, 95, 127]`,
and five false interpolation flags. Snapshot the document and verify
`steps=1`, reversed/equal tick bounds, and `steps > end_tick-start_tick+1`
raise `ValueError` without mutation.

- [ ] **Step 2: Run the focused test and verify RED**

Run the focused command from Task 1. Expected: failure because `ramp_cc` does
not exist.

- [ ] **Step 3: Implement `ramp_cc`**

Validate `steps` and bounds first, compute positions and values with Python
`round`, then delegate once to `set_cc_automation`. Return its report extended
with `start`, `end` and `steps`.

- [ ] **Step 4: Update user-facing documentation**

Update the firmware target in `docs/COPERTURA_DELUGE.md`; promote `midi-cc`
reading/writing to complete but leave Device absent until user confirmation.
Add the four public writing calls and the CC/interpolation distinction to the
Deluge Pal skill table.

- [ ] **Step 5: Run focused and full verification**

Run the focused test, then:

```powershell
.venv\Scripts\python.exe tests\test_all.py
```

Expected: new checks green; full suite has no new failures compared with the
baseline single failure `ogni riga punta a evidenze locali esistenti` caused
by absent private fixtures.

- [ ] **Step 6: Commit**

```powershell
git add tools/delugexml/midicv.py tests/test_all.py docs/COPERTURA_DELUGE.md .agents/skills/deluge-pal/SKILL.md
git commit -m "docs: describe MIDI automation support"
```

---

### Task 3: Device acceptance probe

**Files:**
- Create ignored local artifact: `out/build_midi_automation_probe.py`
- Create ignored local artifact: `out/MIDIAUTO01.XML`

**Interfaces:**
- Consumes: Task 1 and 2 public APIs, `musica.verifica`, `musica.avvertenze`, `musica.destinazione`, `write_file`.
- Produces: `/SONGS/DelugePal/MIDIAUTO01.XML` for physical-device inspection.

- [ ] **Step 1: Build using library calls only**

Load the local blank-song fixture, add a playing MIDI clip on channel 1, add
CC1 steps, a CC74 discrete ramp, interpolated bend and pressure, and a short
note pattern. Write with the learned format table.

- [ ] **Step 2: Validate and narrate**

Require `musica.verifica(doc) == []`; record `musica.avvertenze(doc)` and
`musica.racconta_clip(doc, clip)`. Abort upload if verification is non-empty.

- [ ] **Step 3: Upload without overwrite**

Resolve the remote path only with `musica.destinazione('midiauto', 1)` and run
`dsysex.py put`, which rereads and compares the hash. If version 1 exists,
increment the version rather than forcing overwrite.

- [ ] **Step 4: Record the boundary honestly**

Upload/hash proves transfer only. Leave Device `assente` until the user opens
the song and confirms CC steps plus smooth bend/pressure on the beta firmware.

