"""DX7 voice authoring and single-file wavetable assignment.

Firmware b76ed39: processing/sound/sound.cpp writes 156 unpacked bytes
as dx7patch (no 0x prefix). contrib/dx7/sysex-format.txt specifies the
field order. Operator arguments use musician numbering 1..6; the payload
stores 6..1. Algorithm arguments use 1..32, payload uses 0..31.
No bank dependency: the complete DX7 voice is embedded in the preset.
"""
from dataclasses import dataclass
from pathlib import PurePosixPath
from .parser import Node
from . import sound as V, structure as ST


def _ints(values, maxima):
    if len(values) != len(maxima):
        raise ValueError('wrong number of DX7 parameters')
    for value, high in zip(values, maxima):
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= high:
            raise ValueError(f'DX7 value {value!r} outside 0..{high}')
    return list(values)


@dataclass(frozen=True)
class DX7Operator:
    rates: tuple = (99, 65, 35, 65)
    levels: tuple = (99, 75, 0, 0)
    breakpoint: int = 39
    left_depth: int = 0
    right_depth: int = 0
    left_curve: int = 0
    right_curve: int = 0
    rate_scaling: int = 0
    amp_mod: int = 0
    velocity: int = 2
    level: int = 85
    mode: int = 0
    coarse: int = 1
    fine: int = 0
    detune: int = 7

    def encode(self):
        return bytes(_ints(self.rates, [99]*4) + _ints(self.levels, [99]*4)
                     + _ints((self.breakpoint, self.left_depth, self.right_depth,
                              self.left_curve, self.right_curve, self.rate_scaling,
                              self.amp_mod, self.velocity, self.level, self.mode,
                              self.coarse, self.fine, self.detune),
                             (99, 99, 99, 3, 3, 7, 3, 7, 99, 1, 31, 99, 14)))


@dataclass(frozen=True)
class DX7Patch:
    operators: tuple
    algorithm: int = 5
    feedback: int = 0
    osc_sync: int = 1
    pitch_rates: tuple = (99, 99, 99, 99)
    pitch_levels: tuple = (50, 50, 50, 50)
    lfo_speed: int = 25
    lfo_delay: int = 0
    lfo_pitch: int = 0
    lfo_amp: int = 0
    lfo_sync: int = 1
    lfo_wave: int = 4
    pitch_sensitivity: int = 0
    transpose: int = 24
    name: str = 'INIT'
    operator_mask: int = 63

    def encode(self):
        if len(self.operators) != 6:
            raise ValueError('DX7 needs exactly six operators, numbered 1..6')
        _ints((self.algorithm,), (32,))
        if self.algorithm == 0:
            raise ValueError('algorithm is 1..32')
        if not isinstance(self.name, str) or not 1 <= len(self.name) <= 10 or any(not 32 <= ord(c) <= 126 for c in self.name):
            raise ValueError('DX7 name must be 1..10 printable ASCII characters')
        data = b''.join(op.encode() for op in reversed(self.operators))
        data += bytes(_ints(self.pitch_rates, [99]*4) + _ints(self.pitch_levels, [99]*4))
        data += bytes(_ints((self.algorithm-1, self.feedback, self.osc_sync,
                             self.lfo_speed, self.lfo_delay, self.lfo_pitch,
                             self.lfo_amp, self.lfo_sync, self.lfo_wave,
                             self.pitch_sensitivity, self.transpose),
                            (31, 7, 1, 99, 99, 99, 99, 1, 5, 7, 48)))
        data += self.name.ljust(10).encode('ascii')
        data += bytes(_ints((self.operator_mask,), (63,)))
        return data.hex().upper()

    @classmethod
    def decode(cls, payload):
        data = bytes.fromhex(payload)
        if len(data) != 156:
            raise ValueError('Deluge DX7 payload must have 156 bytes')
        ops = []
        for start in range(0, 126, 21):
            b = data[start:start+21]
            ops.append(DX7Operator(tuple(b[:4]), tuple(b[4:8]), *b[8:]))
        patch = cls(tuple(reversed(ops)), data[134]+1, data[135], data[136],
                    tuple(data[126:130]), tuple(data[130:134]),
                    *data[137:145], data[145:155].decode('ascii').rstrip(), data[155])
        patch.encode()  # validate all field ranges
        return patch


def _osc(owner, which):
    if owner.tag != 'sound' or which not in (1, 2):
        raise ValueError('a sound and oscillator 1 or 2 are required')
    osc = owner.find(f'osc{which}')
    if osc is None:
        raise ValueError('oscillator missing')
    return osc


def _clear_source(osc):
    for name in ('fileName', 'dx7patch', 'dx7randomdetune', 'dx7enginemode',
                 'loopMode', 'reversed', 'timeStretchEnable', 'timeStretchAmount'):
        osc.remove(name)
    osc.children = [node for node in osc.children
                    if node.tag not in ('zone', 'sampleRanges', 'wavetableRanges')]
    osc.touch()


def set_dx7(owner, patch: DX7Patch, *, params_node=None):
    """Assign a complete original voice; match firmware blank-DX7 envelope setup."""
    payload = patch.encode()  # fail before mutating anything
    osc = _osc(owner, 1)
    target = owner if params_node is None else params_node
    changes = {'oscBVolume': 0, 'envelope1.attack': 0,
               'envelope1.sustain': 50, 'envelope1.release': 50}
    if any(V.get_raw(target, name) is None for name in changes):
        raise ValueError('DX7 setup requires synth parameters')
    _clear_source(osc)
    ST.set_attr(owner, 'mode', 'subtractive')
    # Firmware-confirmed type; structure.py's historical corpus predates DX7.
    ST.set_osc(owner, 1, type='dx7', transpose=0, cents=0, force=True)
    osc.set('dx7patch', payload)
    for name, value in changes.items():
        V.set(target, name, value)
    V.remove_patch_cable(target, 'velocity', 'volume')


def update_dx7_patch(owner, patch: DX7Patch):
    """Edit an existing DX7 voice without resetting engine, routing or mix."""
    payload = patch.encode()
    osc = _osc(owner, 1)
    if osc.get('type') != 'dx7' or not osc.get('dx7patch'):
        raise ValueError('patch editing requires an existing DX7 oscillator')
    DX7Patch.decode(osc.get('dx7patch'))
    osc.set('dx7patch', payload)


def set_wavetable(owner, path: str, *, which=1):
    """Assign a single SD WAV table. Position/modulation use sound.py normally."""
    osc = _osc(owner, which)
    _check_wavetable_path(path)
    _clear_source(osc)
    ST.set_attr(owner, 'mode', 'subtractive')
    ST.set_osc(owner, which, type='wavetable', transpose=0, cents=0)
    osc.set('fileName', path)


def _check_wavetable_path(path):
    if (not isinstance(path, str) or '\\' in path
            or '..' in PurePosixPath(path).parts
            or not path.startswith('SAMPLES/')
            or PurePosixPath(path).suffix.lower() != '.wav'):
        raise ValueError('expected an SD-relative SAMPLES/...wav path')
    if any(ord(c) < 32 or c in '<>:"|?*' for c in path):
        raise ValueError('invalid SD path')


def set_wavetable_ranges(owner, ranges, *, which=1, experimental=False):
    """Assign WAV tables across note ranges: (inclusive top MIDI note, path).

    The final range has ``None`` as its top and extends to the highest note.
    For authoring on b76ed39, ``osc.fileName`` supplies the final table and
    explicit rows supply the lower ranges. The device rewrites this into a
    canonical ``wavetableRanges`` list on save. On b76ed39, browsing that
    resaved preset crashes the device. Explicit opt-in is required for
    diagnostic work until a safe device round-trip is demonstrated.
    Validation is atomic.
    """
    if not experimental:
        raise RuntimeError('multi-range wavetable write is experimental: '
                           'b76ed39 crashes when browsing a resaved preset')
    _osc(owner, which)
    if not isinstance(ranges, (list, tuple)) or len(ranges) < 2:
        raise ValueError('provide at least two wavetable note ranges')
    previous = -1
    for index, item in enumerate(ranges):
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise ValueError('each range must be (top note, WAV path)')
        top, path = item
        _check_wavetable_path(path)
        if index == len(ranges) - 1:
            if top is not None:
                raise ValueError('last range must end with top note None')
        elif (isinstance(top, bool) or not isinstance(top, int)
              or not previous < top < 127):
            raise ValueError('range tops must increase within MIDI notes 0..126')
        if top is not None:
            previous = top
    set_wavetable(owner, ranges[-1][1], which=which)
    osc = _osc(owner, which)
    group = osc.append(Node(tag='wavetableRanges'))
    for top, path in ranges[:-1]:
        attrs = [('rangeTopNote', str(top)), ('fileName', path)]
        group.append(Node(tag='wavetableRange', attrs=attrs, self_closing=True))


def wavetable_ranges(owner, *, which=1):
    """Read a single table or each note range as (top note, SD path)."""
    osc = _osc(owner, which)
    if osc.get('type') != 'wavetable':
        raise ValueError('oscillator is not a wavetable')
    group = osc.find('wavetableRanges')
    if group is None:
        path = osc.get('fileName')
        return [(None, path)] if path is not None else []
    rows = [(int(row.get('rangeTopNote')) if row.get('rangeTopNote') is not None else None,
             row.get('fileName')) for row in group.find_all('wavetableRange')]
    fallback = osc.get('fileName')
    if fallback is not None and (not rows or rows[-1][0] is not None):
        rows.append((None, fallback))
    return rows
