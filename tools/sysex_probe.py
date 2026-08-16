"""Sonda: quale coppia di porte MIDI parla il protocollo SysEx del Deluge?

Invia il ping su ogni uscita, ascoltando contemporaneamente su TUTTI gli
ingressi. Prova anche le varianti di comando note, perche' il Deluge ha due
superfici SysEx distinte:

  - servizio filesystem JSON:  F0 00 21 7B 01 06 <seq> {"ping":{}} F7
  - comandi di sviluppo:       F0 7D 00 F7   (ping "storico", display, debug)

Se una delle due risponde e l'altra no, sappiamo esattamente cosa e' abilitato.

Uso: .venv\\Scripts\\python.exe tools/sysex_probe.py [--timeout 2]
"""
from __future__ import annotations

import argparse
import json
import sys
import time

import mido

HDR = [0x00, 0x21, 0x7B, 0x01]


def probes():
    p = json.dumps({'ping': {}}, separators=(',', ':')).encode('ascii')
    yield ('JSON ping (servizio filesystem)', HDR + [0x06, 0x01] + list(p))
    yield ('dev ping  F0 7D 00 F7', [0x7D, 0x00])
    yield ('dev richiesta versione F0 7D 03 00 F7', [0x7D, 0x03, 0x00])
    yield ('dev richiesta OLED F0 7D 02 00 01 F7', [0x7D, 0x02, 0x00, 0x01])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--timeout', type=float, default=2.0)
    a = ap.parse_args()

    ins = mido.get_input_names()
    outs = [p for p in mido.get_output_names() if 'wavetable' not in p.lower()]
    print(f'ingressi: {ins}')
    print(f'uscite  : {outs}\n')
    if not ins or not outs:
        sys.exit('servono almeno un ingresso e una uscita')

    open_ins = [(n, mido.open_input(n)) for n in ins]
    found = []
    try:
        for label, data in probes():
            print(f'=== {label} ===')
            for oname in outs:
                for _, port in open_ins:
                    while port.poll():
                        pass
                with mido.open_output(oname) as out:
                    out.send(mido.Message('sysex', data=data))
                    got = []
                    deadline = time.time() + a.timeout
                    while time.time() < deadline:
                        for iname, port in open_ins:
                            msg = port.poll()
                            if msg is not None and msg.type == 'sysex':
                                got.append((iname, bytes(msg.data)))
                        if got:
                            break
                        time.sleep(0.002)
                if got:
                    for iname, d in got:
                        head = ' '.join(f'{b:02X}' for b in d[:20])
                        print(f'  {oname:<22} -> RISPOSTA su {iname}: '
                              f'F0 {head}{"…" if len(d) > 20 else ""} F7 '
                              f'({len(d)} byte)')
                        try:
                            txt = bytes(d[6:]).split(b'\x00')[0].decode('ascii')
                            if txt.strip():
                                print(f'                          {txt[:120]}')
                        except (UnicodeDecodeError, IndexError):
                            pass
                    found.append((label, oname, got[0][0]))
                else:
                    print(f'  {oname:<22} -> niente')
            print()
    finally:
        for _, port in open_ins:
            port.close()

    print('=' * 60)
    if found:
        print('coppie funzionanti:')
        for label, o, i in found:
            print(f'  {label}\n      --out "{o}"  --in "{i}"')
    else:
        print('nessuna risposta su nessuna combinazione.')
        print('Il servizio SysEx non e attivo, oppure va abilitato sul dispositivo.')


if __name__ == '__main__':
    sys.exit(main())
