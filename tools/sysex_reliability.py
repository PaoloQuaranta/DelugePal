"""Quanto e' affidabile una dimensione di blocco su letture ripetute?

Un blocco che funziona una volta non dice nulla: il download di Perche.XML si
e' interrotto al terzo blocco da 768 pur avendo superato il test singolo. Qui si
fanno N letture consecutive per ogni dimensione e si conta quante ne passano.

Uso: .venv\\Scripts\\python.exe tools/sysex_reliability.py --in "Deluge 0" --out "Deluge 1"
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='outp', required=True)
    ap.add_argument('--reps', type=int, default=20)
    ap.add_argument('--timeout', type=float, default=2.0)
    ap.add_argument('--sizes', default='64,128,256,384,512,640,768')
    a = ap.parse_args()

    sizes = [int(x) for x in a.sizes.split(',')]

    print(f'{"blocco":>8} {"ok":>6}/{"tot":<5} {"byte errati":>12} '
          f'{"ms medi":>9} {"kB/s":>8}')
    print('-' * 56)
    results = []

    for n in sizes:
        # sessione nuova per ogni dimensione, cosi' un fallimento non
        # contamina la prova successiva
        with mido.open_input(a.inp) as inp, mido.open_output(a.outp) as out:
            dev = Deluge(inp, out, a.timeout)
            try:
                dev.open_session()
                reply, _, _ = dev.request({'open': {'path': PATH}})
                val = reply_value(reply, 'open')
                if not val or val.get('err'):
                    print(f'{n:>8}  open fallita: {reply}')
                    continue
                fid, size = val['fid'], val['size']

                ok = bad = wrong = 0
                t0 = time.time()
                for k in range(a.reps):
                    addr = (k * n) % max(1, size - n)
                    r, blob, _ = dev.request(
                        {'read': {'fid': fid, 'addr': addr, 'size': n}})
                    if r is None:
                        bad += 1
                        continue
                    v = reply_value(r, 'read') or {}
                    if v.get('err') or len(blob) < n:
                        bad += 1
                        wrong += abs(len(blob) - n)
                    else:
                        ok += 1
                dt = time.time() - t0
                dev.request({'close': {'fid': fid}})
            except Exception as e:                    # noqa: BLE001
                print(f'{n:>8}  eccezione: {type(e).__name__}: {e}')
                continue

        rate = (ok * n / 1024) / dt if dt else 0
        print(f'{n:>8} {ok:>6}/{a.reps:<5} {wrong:>12} '
              f'{dt/a.reps*1000:>9.0f} {rate:>8.1f}')
        results.append((n, ok, a.reps, rate))

    print()
    perfetti = [n for n, ok, tot, _ in results if ok == tot]
    if perfetti:
        best_n = max(perfetti)
        best_rate = max(r for n, ok, t, r in results if n == best_n)
        print(f'blocco piu grande con {a.reps}/{a.reps} successi: {best_n} byte '
              f'({best_rate:.0f} kB/s)')
        print(f'stima per una song da 270 kB: '
              f'{270/best_rate:.1f} s')
    else:
        print('nessuna dimensione e risultata affidabile: il problema non e '
              'la dimensione del blocco.')


if __name__ == '__main__':
    sys.exit(main())
