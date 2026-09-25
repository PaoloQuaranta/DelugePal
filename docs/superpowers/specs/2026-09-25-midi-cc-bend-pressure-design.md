# MIDI CC, pitch bend e channel pressure

## Obiettivo

DelugePal deve leggere e scrivere automazione su una clip MIDI per:

- Control Change 0-119, sempre a gradini;
- pitch bend MIDI 14 bit, -8192..8191;
- channel pressure MIDI 7 bit, 0..127.

Il target e' la beta 20260925, commit firmware `b76ed39`. Questa build include
il fix `685b4fb` per gli incrementi di interpolazione e il clamp dei dati di
expression, e il fix `a23d06e` per la conservazione dell'expression automation.

## Formato autorevole

Dal writer del firmware corrente:

- i CC sono figli di `<midiParams>` come `<param><cc>...</cc><value>...</value>`;
- bend e pressure sono attributi `pitchBend` e `pressure` di
  `<expressionData>`;
- `midiParams` viene prima di `arpeggiator`;
- `expressionData` viene prima di `bendRange`;
- tutti i valori usano il codec `AutoParam` gia' modellato da
  `delugexml.automation`.

Scale intere, inverse esatte del playback firmware:

- CC: `raw_signed = (value - 64) << 25`;
- bend: `raw_signed = value << 18`;
- pressure: `raw = value << 24`.

## API

In `delugexml.midicv`:

```python
MIDIValuePoint(pos: int, value: int, interp: bool)

set_cc_automation(clip, cc, points) -> dict
ramp_cc(clip, cc, start, end, start_tick, end_tick, *, steps=9) -> dict
read_cc_automation(clip, cc) -> list[MIDIValuePoint]

set_pitch_bend(clip, points, *, interpolated=True) -> dict
read_pitch_bend(clip) -> list[MIDIValuePoint]

set_channel_pressure(clip, points, *, interpolated=True) -> dict
read_channel_pressure(clip) -> list[MIDIValuePoint]
```

`points` e' una lista di coppie `(tick, value)`. Le posizioni devono essere
intere, crescenti, distinte e interne alla clip. I valori devono essere interi
nei rispettivi intervalli; `bool` non e' accettato come intero.

Un CC non porta mai il bit di interpolazione. `ramp_cc` materializza la retta
in `steps` nodi discreti. Bend e pressure impostano il bit di interpolazione
per default; `interpolated=False` conserva l'alternativa a gradini.

Ogni mutazione fa prima il preflight completo: un input invalido non crea nodi
e non modifica automazioni esistenti. Una seconda scrittura dello stesso CC o
della stessa expression dimension aggiorna il dato senza duplicarlo.

## Verifica e accettazione

- Test senza fixture private: struttura, scale letterali, ordine figli,
  round-trip, aggiornamento e atomicita' degli errori.
- Suite completa: resta ammesso il solo rosso di baseline dovuto alle due
  evidenze private assenti dal checkout.
- Probe costruito esclusivamente con la libreria, `musica.verifica(doc)` vuota,
  destinazione ottenuta con `musica.destinazione`, upload con rilettura hash.
- Accettazione Device completata il 25 settembre 2026: l'utente ha aperto e
  verificato `MIDIAUTO02` sulla beta 20260925, confermando il comportamento
  musicale di CC a gradini e bend/pressure interpolati.
