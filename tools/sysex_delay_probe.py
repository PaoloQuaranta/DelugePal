"""Le perdite dipendono dal ritmo delle richieste?

Ipotesi da testare: non e' il Deluge a non rispondere, e' il backend MIDI del PC
(python-rtmidi su Windows MM) che perde messaggi SysEx sotto traffico continuo.
RtMidi su Windows usa un numero fisso di buffer per i SysEx in ingresso; se non
vengono riciclati abbastanza in fretta, i messaggi si perdono interi — il che
spiegherebbe perche' non si osservano mai troncamenti.

Se l'ipotesi regge, inserire una pausa fra una richiesta e l'altra deve ridurre
le perdite in modo netto. Se non cambia nulla, il problema e' altrove.

Uso: .venv\\Scripts\\python.exe tools/sysex_delay_probe.py --in "Deluge 0" --out "Deluge 1"
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import mido

sys.path.insert(0, str(Path(__file__).parent))
from dsysex import Deluge, reply_value          # noqa: E402

PATH = '/SONGS/Perche.XML'


def run(a, block, delay, reps):
    with mido.open_input(a.inp) as inp, mido.open_output(a.outp) as out:
        dev = Deluge(inp, out, a.timeout)
        dev.open_session()
        reply, _, _ = dev.request({'open': {'path': PATH}})
        val = reply_value(reply, 'open')
        if not val or val.get('err'):
            return None
        fid, size = val['fid'], val['size']
        ok = 0
        t0 = time.time()
        for k in range(reps):
            if delay:
                time.sleep(delay)
            addr = (k * block) % max(1, size - block)
            r, blob, _ = dev.request(
                {'read': {'fid': fid, 'addr': addr, 'size': block}})
            v = reply_value(r, 'read') if r else None
            if v and not v.get('err') and len(blob) >= block:
                ok += 1
        dt = time.time() - t0
        dev.request({'close': {'fid': fid}})
    return ok, reps, dt, (ok * block / 1024) / dt if dt else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='outp', required=True)
    ap.add_argument('--reps', type=int, default=30)
    ap.add_argument('--timeout', type=float, default=1.5)
    a = ap.parse_args()

    print(f'{"blocco":>7} {"pausa":>8} {"ok":>6}/{"tot":<5} {"kB/s":>7}')
    print('-' * 40)
    for block in (64, 768):
        for delay in (0, 0.005, 0.02, 0.05, 0.15):
            r = run(a, block, delay, a.reps)
            if r is None:
                print(f'{block:>7} {delay*1000:>7.0f}m  open fallita')
                continue
            ok, tot, dt, rate = r
            flag = '  <==' if ok == tot else ''
            print(f'{block:>7} {delay*1000:>7.0f}ms {ok:>6}/{tot:<5} '
                  f'{rate:>7.1f}{flag}')
        print()


if __name__ == '__main__':
    sys.exit(main())
