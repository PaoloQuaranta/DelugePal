"""Trova la dimensione massima di blocco che il Deluge accetta per `read`.

La documentazione dice 1024 byte per operazione, ma con l'impacchettamento 7/8
un blocco da 1024 diventa ~1170 byte piu' il JSON, e il dispositivo non risponde.
Questo script prova le dimensioni una per una e riporta quali funzionano.

Uso: .venv\\Scripts\\python.exe tools/sysex_blocksize.py --in "Deluge 0" --out "Deluge 1"
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
    ap.add_argument('--timeout', type=float, default=2.0)
    a = ap.parse_args()

    with mido.open_input(a.inp) as inp, mido.open_output(a.outp) as out:
        dev = Deluge(inp, out, a.timeout)
        s = dev.open_session()
        print(f'sessione sid={s["sid"]}\n')

        reply, _, _ = dev.request({'open': {'path': PATH}})
        val = reply_value(reply, 'open')
        if not val or val.get('err'):
            sys.exit(f'open fallita: {reply}')
        fid, size = val['fid'], val['size']
        print(f'{PATH}: fid={fid}, {size} byte\n')

        print(f'{"blocco":>8} {"esito":<14} {"byte resi":>10} {"ms":>7} {"kB/s":>8}')
        print('-' * 52)
        best = 0
        try:
            for n in (64, 128, 192, 256, 320, 384, 448, 512, 640, 768, 1024):
                if n > size:
                    break
                t0 = time.time()
                reply, blob, _ = dev.request(
                    {'read': {'fid': fid, 'addr': 0, 'size': n}})
                dt = time.time() - t0
                if reply is None:
                    print(f'{n:>8} {"nessuna risposta":<14} {"":>10} '
                          f'{dt*1000:>7.0f}')
                    continue
                v = reply_value(reply, 'read') or {}
                err = v.get('err')
                got = len(blob)
                rate = (got / 1024) / dt if dt else 0
                status = 'ok' if (err == 0 and got >= n) else f'err={err} '
                if err == 0 and got >= n:
                    best = max(best, n)
                print(f'{n:>8} {status:<14} {got:>10} {dt*1000:>7.0f} '
                      f'{rate:>8.1f}')
        finally:
            dev.request({'close': {'fid': fid}})

        print(f'\nblocco massimo funzionante: {best} byte')
        if best:
            print(f'stima per una song da 270 kB: '
                  f'{270*1024/best:.0f} richieste')


if __name__ == '__main__':
    sys.exit(main())
