"""La tabella dei parametri automatizzabili: ID, tipo, nome nel file.

A COSA SERVE
------------
`lastSelectedParamID` sulla clip dice quale parametro l'automazione riguarda.
Senza, la vista automazione si apre su un altro parametro e la curva scritta
non si vede (vedi `automation.mark_view`).

DA DOVE VENGONO GLI ID
----------------------
Dall'ordine dell'enum in `src/deluge/modulation/params/param.h`, branch
`community` — **non da misure sul dispositivo**. Le voci `FIRST_*` sono
marcatori e condividono il valore della voce seguente, quindi non consumano un
numero. Con questa regola `LOCAL_LPF_FREQ` vale **24**, che e' esattamente il
`lastSelectedParamID` osservato in un'automazione fatta a mano sul cutoff.
E' l'unico ancoraggio verificato.

`Kind` viene dallo stesso file: NONE=0, **PATCHED=1**, UNPATCHED_SOUND=2,
UNPATCHED_GLOBAL=3, STATIC=4, MIDI=5, PATCH_CABLE=6, EXPRESSION=7. Il valore
osservato per il cutoff e' 1, coerente.

QUANTO E' AFFIDABILE
--------------------
Gli ID sono aritmetica su un enum: o sono giusti tutti, o c'e' uno scarto
costante che l'ancoraggio a 24 escluderebbe. I NOMI sono un'altra cosa: la
mappa `paramNameForFileConst()` del firmware non e' stata letta per intero, e
quelli qui sotto sono ricavati dall'enum e **verificati contro i nomi che
compaiono davvero nel corpus**. Dove la corrispondenza non e' certa, il campo
vale None e le funzioni si rifiutano di indovinare.

⚠ Solo `lpfFrequency` e' stato verificato sul dispositivo. Prima di fidarsi
degli altri, automatizzarne un paio a mano e confrontare `lastSelectedParamID`.
"""
from __future__ import annotations

from typing import NamedTuple


class Parametro(NamedTuple):
    id: int
    enum: str
    nome: str | None        # attributo nel file, None se non risolto
    kind: int               # 1 = PATCHED


KIND_PATCHED = 1

#: enum Local in ordine; i marcatori FIRST_* sono alias e non consumano valori
_LOCAL = [
    'LOCAL_OSC_A_VOLUME', 'LOCAL_OSC_B_VOLUME', 'LOCAL_VOLUME',
    'LOCAL_NOISE_VOLUME', 'LOCAL_MODULATOR_0_VOLUME',
    'LOCAL_MODULATOR_1_VOLUME', 'LOCAL_FOLD',
    'LOCAL_MODULATOR_0_FEEDBACK', 'LOCAL_MODULATOR_1_FEEDBACK',
    'LOCAL_CARRIER_0_FEEDBACK', 'LOCAL_CARRIER_1_FEEDBACK',
    'LOCAL_LPF_RESONANCE', 'LOCAL_HPF_RESONANCE',
    'LOCAL_ENV_0_SUSTAIN', 'LOCAL_ENV_1_SUSTAIN',
    'LOCAL_ENV_2_SUSTAIN', 'LOCAL_ENV_3_SUSTAIN',
    'LOCAL_LPF_MORPH', 'LOCAL_HPF_MORPH',
    'LOCAL_OSC_A_PHASE_WIDTH', 'LOCAL_OSC_B_PHASE_WIDTH',
    'LOCAL_OSC_A_WAVE_INDEX', 'LOCAL_OSC_B_WAVE_INDEX', 'LOCAL_PAN',
    'LOCAL_LPF_FREQ', 'LOCAL_PITCH_ADJUST',
    'LOCAL_OSC_A_PITCH_ADJUST', 'LOCAL_OSC_B_PITCH_ADJUST',
    'LOCAL_MODULATOR_0_PITCH_ADJUST', 'LOCAL_MODULATOR_1_PITCH_ADJUST',
    'LOCAL_HPF_FREQ', 'LOCAL_LFO_LOCAL_FREQ_1', 'LOCAL_LFO_LOCAL_FREQ_2',
    'LOCAL_ENV_0_ATTACK', 'LOCAL_ENV_1_ATTACK',
    'LOCAL_ENV_2_ATTACK', 'LOCAL_ENV_3_ATTACK',
    'LOCAL_ENV_0_DECAY', 'LOCAL_ENV_1_DECAY',
    'LOCAL_ENV_2_DECAY', 'LOCAL_ENV_3_DECAY',
    'LOCAL_ENV_0_RELEASE', 'LOCAL_ENV_1_RELEASE',
    'LOCAL_ENV_2_RELEASE', 'LOCAL_ENV_3_RELEASE',
]
_GLOBAL = [
    'GLOBAL_VOLUME_POST_FX', 'GLOBAL_VOLUME_POST_REVERB_SEND',
    'GLOBAL_REVERB_AMOUNT', 'GLOBAL_MOD_FX_DEPTH', 'GLOBAL_DELAY_FEEDBACK',
    'GLOBAL_DELAY_RATE', 'GLOBAL_MOD_FX_RATE',
    'GLOBAL_LFO_FREQ_1', 'GLOBAL_LFO_FREQ_2', 'GLOBAL_ARP_RATE',
]

#: Nomi che l'enum non permette di indovinare, presi dalla mappa
#: `paramNameForFileConst()` del firmware oppure dal corpus. Gli inviluppi
#: NON compaiono qui: nel file sono nodi figli <envelope1..4> con attributi
#: attack/decay/sustain/release, non attributi di <soundParams>.
_NOMI = {
    'LOCAL_OSC_A_VOLUME': 'oscAVolume', 'LOCAL_OSC_B_VOLUME': 'oscBVolume',
    'LOCAL_VOLUME': 'volume', 'LOCAL_NOISE_VOLUME': 'noiseVolume',
    'LOCAL_MODULATOR_0_VOLUME': 'modulator1Amount',
    'LOCAL_MODULATOR_1_VOLUME': 'modulator2Amount',
    'LOCAL_FOLD': 'waveFold',
    'LOCAL_MODULATOR_0_FEEDBACK': 'modulator1Feedback',
    'LOCAL_MODULATOR_1_FEEDBACK': 'modulator2Feedback',
    'LOCAL_CARRIER_0_FEEDBACK': 'carrier1Feedback',
    'LOCAL_CARRIER_1_FEEDBACK': 'carrier2Feedback',
    'LOCAL_LPF_RESONANCE': 'lpfResonance',
    'LOCAL_HPF_RESONANCE': 'hpfResonance',
    'LOCAL_LPF_MORPH': 'lpfMorph', 'LOCAL_HPF_MORPH': 'hpfMorph',
    'LOCAL_OSC_A_PHASE_WIDTH': 'oscAPulseWidth',
    'LOCAL_OSC_B_PHASE_WIDTH': 'oscBPulseWidth',
    'LOCAL_OSC_A_WAVE_INDEX': 'oscAWavetablePosition',
    'LOCAL_OSC_B_WAVE_INDEX': 'oscBWavetablePosition',
    'LOCAL_PAN': 'pan',
    'LOCAL_LPF_FREQ': 'lpfFrequency', 'LOCAL_HPF_FREQ': 'hpfFrequency',
    'LOCAL_PITCH_ADJUST': 'pitch',
    'LOCAL_LFO_LOCAL_FREQ_1': 'lfo3Rate',
    'LOCAL_LFO_LOCAL_FREQ_2': 'lfo4Rate',
    'GLOBAL_VOLUME_POST_FX': 'volumePostFX',
    'GLOBAL_VOLUME_POST_REVERB_SEND': 'volumePostReverbSend',
    'GLOBAL_REVERB_AMOUNT': 'reverbAmount',
    'GLOBAL_MOD_FX_DEPTH': 'modFXDepth',
    'GLOBAL_DELAY_FEEDBACK': 'delayFeedback',
    'GLOBAL_DELAY_RATE': 'delayRate',
    'GLOBAL_MOD_FX_RATE': 'modFXRate',
    'GLOBAL_LFO_FREQ_1': 'lfo1Rate', 'GLOBAL_LFO_FREQ_2': 'lfo2Rate',
    'GLOBAL_ARP_RATE': 'arpeggiatorRate',
}

#: Verificati SUL DISPOSITIVO, generando un'automazione e ascoltando quale
#: parametro si muove:
#:   lpfFrequency (24) — dal file di un'automazione fatta a mano
#:   pan (23)          — LOCAL a meta' enum
#:   reverbAmount (47) — GLOBAL, cioe' oltre la giunzione LOCAL_LAST = 45,
#:                       che e' il punto dove un errore di +-1 sarebbe emerso
#: Con un LOCAL e un GLOBAL corretti, uno scarto costante e' escluso in
#: entrambe le meta' della tabella.
#:   arpeggiatorGate (11, kind 2) — primo UNPATCHED dopo un marcatore, quindi
#:                       scioglie insieme la questione dei marcatori e quella
#:                       dell'offset UNPATCHED_START
VERIFICATI_SUL_DISPOSITIVO = {'lpfFrequency', 'pan', 'reverbAmount',
                              'arpeggiatorGate', 'stutterRate'}

KIND_UNPATCHED_SOUND = 2
KIND_UNPATCHED_GLOBAL = 3

#: enum UnpatchedShared, in ordine. UNPATCHED_FIRST_ARP_PARAM e
#: UNPATCHED_LAST_ARP_PARAM sono marcatori.
_UNPATCHED_SHARED = [
    'UNPATCHED_STUTTER_RATE', 'UNPATCHED_BASS', 'UNPATCHED_TREBLE',
    'UNPATCHED_BASS_FREQ', 'UNPATCHED_TREBLE_FREQ',
    'UNPATCHED_SAMPLE_RATE_REDUCTION', 'UNPATCHED_BITCRUSHING',
    'UNPATCHED_MOD_FX_OFFSET', 'UNPATCHED_MOD_FX_FEEDBACK',
    'UNPATCHED_SIDECHAIN_SHAPE', 'UNPATCHED_COMPRESSOR_THRESHOLD',
    'UNPATCHED_ARP_GATE', 'UNPATCHED_ARP_RHYTHM',
    'UNPATCHED_ARP_SEQUENCE_LENGTH', 'UNPATCHED_ARP_CHORD_POLYPHONY',
    'UNPATCHED_ARP_RATCHET_AMOUNT', 'UNPATCHED_NOTE_PROBABILITY',
    'UNPATCHED_REVERSE_PROBABILITY', 'UNPATCHED_ARP_BASS_PROBABILITY',
    'UNPATCHED_ARP_SWAP_PROBABILITY', 'UNPATCHED_ARP_GLIDE_PROBABILITY',
    'UNPATCHED_ARP_CHORD_PROBABILITY', 'UNPATCHED_ARP_RATCHET_PROBABILITY',
    'UNPATCHED_ARP_SPREAD_GATE', 'UNPATCHED_ARP_SPREAD_OCTAVE',
    'UNPATCHED_SPREAD_VELOCITY',
]

_NOMI_UNPATCHED = {
    'UNPATCHED_STUTTER_RATE': 'stutterRate', 'UNPATCHED_BASS': 'bass',
    'UNPATCHED_TREBLE': 'treble', 'UNPATCHED_BASS_FREQ': 'bassFrequency',
    'UNPATCHED_TREBLE_FREQ': 'trebleFrequency',
    'UNPATCHED_SAMPLE_RATE_REDUCTION': 'sampleRateReduction',
    'UNPATCHED_BITCRUSHING': 'bitCrush',
    'UNPATCHED_MOD_FX_OFFSET': 'modFXOffset',
    'UNPATCHED_MOD_FX_FEEDBACK': 'modFXFeedback',
    'UNPATCHED_SIDECHAIN_SHAPE': 'sidechainCompressorShape',
    'UNPATCHED_COMPRESSOR_THRESHOLD': 'compressorThreshold',
    'UNPATCHED_ARP_GATE': 'arpeggiatorGate', 'UNPATCHED_ARP_RHYTHM': 'rhythm',
    'UNPATCHED_ARP_SEQUENCE_LENGTH': 'sequenceLength',
    'UNPATCHED_ARP_CHORD_POLYPHONY': 'chordPolyphony',
    'UNPATCHED_ARP_RATCHET_AMOUNT': 'ratchetAmount',
    'UNPATCHED_NOTE_PROBABILITY': 'noteProbability',
    'UNPATCHED_REVERSE_PROBABILITY': 'reverseProbability',
    'UNPATCHED_ARP_BASS_PROBABILITY': 'bassProbability',
    'UNPATCHED_ARP_SWAP_PROBABILITY': 'swapProbability',
    'UNPATCHED_ARP_GLIDE_PROBABILITY': 'glideProbability',
    'UNPATCHED_ARP_CHORD_PROBABILITY': 'chordProbability',
    'UNPATCHED_ARP_RATCHET_PROBABILITY': 'ratchetProbability',
    'UNPATCHED_ARP_SPREAD_GATE': 'spreadGate',
    'UNPATCHED_ARP_SPREAD_OCTAVE': 'spreadOctave',
    'UNPATCHED_SPREAD_VELOCITY': 'spreadVelocity',
    'UNPATCHED_PORTAMENTO': 'portamento',
    'UNPATCHED_TEMPO': 'tempo',
}

#: RISOLTO SUL DISPOSITIVO. Automatizzando a mano `arpeggiatorGate` su una
#: clip di synth, il firmware ha scritto `lastSelectedParamID="11"` e
#: `lastSelectedParamKind="2"`. Da li':
#:
#: 1. **11 e non 12**: i marcatori `UNPATCHED_FIRST_/LAST_ARP_PARAM` sono
#:    alias e non consumano un valore, come nell'enum patched;
#: 2. **11 e non 101**: `UNPATCHED_START = 90` NON entra in
#:    `lastSelectedParamID` — e' un offset interno agli array compressi;
#: 3. e una cosa che non avevo previsto: il **Kind e' 2 (UNPATCHED_SOUND)**,
#:    non 3. Su una clip di synth gli unpatched shared sono parametri del
#:    suono. Il Kind dipende dal CONTESTO in cui il parametro e' usato, non
#:    dal parametro in se': lo stesso `stutterRate` in arranger sarebbe
#:    presumibilmente UNPATCHED_GLOBAL. [OSS] quel caso non e' verificato.
UNPATCHED_INCERTI = False


PARAMETRI: list[Parametro] = []
for _i, _e in enumerate(_LOCAL):
    PARAMETRI.append(Parametro(_i, _e, _NOMI.get(_e), KIND_PATCHED))
_base = len(_LOCAL)
for _i, _e in enumerate(_GLOBAL):
    PARAMETRI.append(Parametro(_base + _i, _e, _NOMI.get(_e), KIND_PATCHED))

# Gli unpatched: numerazione propria che riparte da zero, e Kind 2 su una
# clip di suono — verificato leggendo cosa scrive il dispositivo.
for _i, _e in enumerate(_UNPATCHED_SHARED):
    PARAMETRI.append(Parametro(_i, _e, _NOMI_UNPATCHED.get(_e),
                               KIND_UNPATCHED_SOUND))
_n_shared = len(_UNPATCHED_SHARED)
PARAMETRI.append(Parametro(_n_shared, 'UNPATCHED_PORTAMENTO',
                           'portamento', KIND_UNPATCHED_SOUND))
# `tempo` vive solo a livello di song/arranger, quindi resta GLOBAL
PARAMETRI.append(Parametro(_n_shared + 16, 'UNPATCHED_TEMPO',
                           'tempo', KIND_UNPATCHED_GLOBAL))

_PER_NOME = {p.nome: p for p in PARAMETRI if p.nome}


def by_name(nome: str) -> Parametro:
    """Il parametro che nel file si chiama `nome`."""
    p = _PER_NOME.get(nome)
    if p is None:
        risolti = ', '.join(sorted(_PER_NOME))
        raise ValueError(
            f'"{nome}" non e nella tabella dei parametri automatizzabili. '
            f'Risolti: {risolti}')
    return p


def by_id(pid: int) -> Parametro:
    for p in PARAMETRI:
        if p.id == pid:
            return p
    raise ValueError(f'nessun parametro con id {pid}')


def is_verified(nome: str) -> bool:
    """Il legame nome -> ID e' stato confermato sul dispositivo?"""
    return nome in VERIFICATI_SUL_DISPOSITIVO
