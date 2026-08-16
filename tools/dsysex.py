"""dsysex - client SysEx per il filesystem del Deluge.

Protocollo, da documentazione community + sorgente `smsysex.cpp`:

    richiesta  F0 00 21 7B 01 06 <seq> <JSON ASCII> F7
    risposta   F0 00 21 7B 01 07 <seq> <JSON ASCII> [00 <binario packed 7/8>] F7

Il JSON viaggia in ASCII, non impacchettato. Solo il contenuto dei file usa
l'impacchettamento 7 su 8 (ogni 8 byte trasmessi portano 7 byte di dati; il
primo contiene i bit alti dei successivi). La chiave della risposta e' quella
della richiesta con un '^' davanti.

La scrittura funziona dalla nightly `1.3.0-beta build 2d7cdf8` (12 agosto
2026): prima era rotta dalla perdita di pacchetti USB in ricezione, corretta
dal PR #4633 del firmware. Vedi docs/SYSEX.md §5.

`put` non sovrascrive mai: se il percorso remoto esiste gia', si ferma. E
rilegge sempre il file per confrontare gli hash — su un canale che puo'
perdere messaggi, un trasferimento non si da' per buono senza riprova.
Attenzione a scrivere sulla SD mentre il Deluge la usa: limitarsi a nomi
nuovi, e mai alla song correntemente caricata.

Comandi:
    ports                          elenca le porte MIDI
    ping                           verifica che il servizio risponda
    dir <path> [--lines N]         elenca una cartella
    get <remoto> <locale>          scarica un file
    put <locale> <remoto>          deposita un file (non sovrascrive)
    raw '<json>'                   invia un JSON arbitrario (per esplorare)

Opzioni comuni: --in PORTA --out PORTA --timeout SEC --verbose
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

try:
    import mido
except ImportError:
    sys.exit('serve mido. Installa con:\n'
             '  .venv\\Scripts\\python.exe -m pip install mido python-rtmidi')

HDR = [0x00, 0x21, 0x7B, 0x01]      # manufacturer Synthstrom + product id

# Numeri di comando presi dall'enum del firmware (src/deluge/io/midi/sysex.h):
#     Ping=0, Popup=1, HID=2, Debug=3, Json=4, JsonReply=5, Pong=0x7F
# La documentazione community indica 0x06/0x07: e' sbagliata, o descrive una
# numerazione precedente. Con 0x06 il dispositivo non risponde, con 0x04 si'.
CMD_JSON = 0x04
CMD_JSON_REPLY = 0x05
# Osservato sul dispositivo: la risposta a ping arriva con 0x05, quella ad
# assignSession con 0x04 e sequence 0 (la sessione non esiste ancora quando
# viene costruita la risposta). Accettiamo entrambi piu' il valore che indica
# la documentazione, e ci fidiamo del corpo JSON per capire cosa e'.
REPLY_CMDS = {0x04, 0x05, 0x07}


# ------------------------------------------------------- impacchettamento 7/8

def unpack_7to8(packed: bytes) -> bytes:
    """Ogni gruppo di 8 byte trasmessi porta 7 byte di dati.

    Il primo byte del gruppo contiene i bit alti dei 7 successivi, uno per bit.
    """
    out = bytearray()
    for i in range(0, len(packed), 8):
        group = packed[i:i + 8]
        if not group:
            break
        hi = group[0]
        for k, b in enumerate(group[1:]):
            out.append((b & 0x7F) | (((hi >> k) & 1) << 7))
    return bytes(out)


def pack_8to7(data: bytes) -> bytes:
    """Inverso di unpack_7to8. Non usato finche' non si scrive sul dispositivo."""
    out = bytearray()
    for i in range(0, len(data), 7):
        chunk = data[i:i + 7]
        hi = 0
        for k, b in enumerate(chunk):
            if b & 0x80:
                hi |= 1 << k
        out.append(hi)
        out += bytes(b & 0x7F for b in chunk)
    return bytes(out)


# ------------------------------------------------------------------- trasporto

class Deluge:
    def __init__(self, inport, outport, timeout=3.0, verbose=False):
        self.inp = inport
        self.out = outport
        self.timeout = timeout
        self.verbose = verbose
        self.sid = None
        # senza sessione si usa 1..7; con la sessione l'intervallo lo detta il
        # dispositivo (midMin..midMax, cioe' (sid << 3) | 1..7)
        self.mid_min, self.mid_max = 1, 7
        self.seq = 0
        self.timeouts = 0        # richieste senza risposta
        self.retried = 0         # ritentativi andati a buon fine

    def _next_seq(self) -> int:
        span = self.mid_max - self.mid_min + 1
        self.seq = (self.seq + 1) % span
        return self.mid_min + self.seq

    def open_session(self, tag='dsysex') -> dict:
        """Le operazioni su file richiedono una sessione; il ping no.

        La risposta indica l'intervallo di message id da usare da qui in poi:
        midBase = sid << 3, e i sequence validi vanno da midMin a midMax.
        """
        reply, _, _ = self.request({'session': {'tag': tag}})
        if reply is None:
            raise RuntimeError('nessuna risposta a assignSession')
        val = reply_value(reply, 'session')
        if not isinstance(val, dict) or 'sid' not in val:
            raise RuntimeError(f'assignSession fallita: {json.dumps(reply)}')
        self.sid = val['sid']
        self.mid_min = val.get('midMin', (self.sid << 3) | 1)
        self.mid_max = val.get('midMax', (self.sid << 3) | 7)
        self.seq = 0
        if self.verbose:
            print(f'     sessione sid={self.sid} '
                  f'sequence {self.mid_min}..{self.mid_max}')
        return val

    def request(self, obj: dict, retries: int = 0,
                blob: bytes = b'') -> tuple[dict | None, bytes, list]:
        """Invia un JSON e attende la risposta, con ritentativi opzionali.

        Serve ritentare perche' il firmware, quando sta gia' accedendo alla SD,
        esce dal gestore SysEx senza rispondere (`if (currentlyAccessingCard
        != 0) return;`). Il risultato e' un silenzio, non un errore. Misurato:
        le risposte che arrivano sono sempre integre, non ci sono mai
        troncamenti — quindi ritentare e' sicuro e sufficiente.

        Ritorna (json_risposta, dati_binari, messaggi_grezzi_scartati).
        """
        for attempt in range(retries + 1):
            r = self._request_once(obj, blob)
            if r[0] is not None:
                if attempt and self.verbose:
                    print(f'     (riuscito al tentativo {attempt + 1})')
                self.retried += attempt
                return r
            self.timeouts += 1
        return r

    def _request_once(self, obj: dict,
                      blob: bytes = b'') -> tuple[dict | None, bytes, list]:
        seq = self._next_seq()
        payload = json.dumps(obj, separators=(',', ':')).encode('ascii')
        if any(b > 0x7F for b in payload):
            raise ValueError('il JSON contiene byte non ASCII')
        data = HDR + [CMD_JSON, seq] + list(payload)
        if blob:
            # stessa struttura della risposta: separatore 00 e poi il binario
            # impacchettato 7 su 8
            data += [0x00] + list(pack_8to7(blob))
        if self.verbose:
            print(f'  -> F0 {" ".join(f"{b:02X}" for b in data)} F7')
            print(f'     {payload.decode()}')

        # svuota eventuali messaggi pendenti
        while self.inp.poll():
            pass
        self.out.send(mido.Message('sysex', data=data))

        other = []
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            msg = self.inp.poll()
            if msg is None:
                time.sleep(0.002)
                continue
            if msg.type != 'sysex':
                continue
            d = bytes(msg.data)
            if self.verbose:
                head = ' '.join(f'{b:02X}' for b in d[:16])
                print(f'  <- F0 {head}{"…" if len(d) > 16 else ""} F7  ({len(d)} byte)')
            if d[:4] != bytes(HDR) or len(d) < 6:
                other.append(d)
                continue
            if d[4] not in REPLY_CMDS:
                other.append(d)
                continue
            # La sequence DEVE corrispondere. Con una perdita del 70% capita
            # spesso che la risposta di un tentativo precedente arrivi mentre
            # si sta gia' aspettando quella del tentativo successivo:
            # accettarla significa credere riuscita un'operazione che non lo
            # e'. In lettura si nota subito (dati sbagliati), in scrittura no
            # — ed e' cosi' che il primo file scritto e' uscito corrotto.
            # La risposta a `session` fa eccezione: arriva con sequence 0,
            # perche' la sessione non esiste ancora quando viene costruita.
            if d[5] != seq and not (d[5] == 0 and 'session' in obj):
                if self.verbose:
                    print(f'     (scartata: sequence {d[5]:02X}, '
                          f'attesa {seq:02X})')
                other.append(d)
                continue
            body = d[6:]
            # il binario, se c'e', e' preceduto da un byte 00
            cut = body.find(0x00)
            if cut < 0:
                jtxt, blob = body, b''
            else:
                jtxt, blob = body[:cut], unpack_7to8(body[cut + 1:])
            try:
                return json.loads(jtxt.decode('ascii', 'replace')), blob, other
            except json.JSONDecodeError as e:
                raise RuntimeError(
                    f'risposta non JSON: {jtxt[:200]!r} ({e})') from e
        return None, b'', other


def reply_value(reply: dict, key: str):
    """Il Deluge risponde con la chiave della richiesta preceduta da '^'."""
    for k in (f'^{key}', key):
        if k in reply:
            return reply[k]
    return None


# -------------------------------------------------------------------- comandi

def pick_ports(a):
    ins, outs = mido.get_input_names(), mido.get_output_names()

    def choose(name, avail, what):
        if name:
            exact = [p for p in avail if p == name]
            part = [p for p in avail if name.lower() in p.lower()]
            if exact:
                return exact[0]
            if len(part) == 1:
                return part[0]
            sys.exit(f'porta {what} "{name}" ambigua o assente. Disponibili: {avail}')
        cands = [p for p in avail if 'deluge' in p.lower()]
        if len(cands) == 1:
            return cands[0]
        if not avail:
            sys.exit(f'nessuna porta MIDI {what}. Il Deluge e collegato e acceso?')
        sys.exit(f'non riesco a scegliere la porta {what}. '
                 f'Usa --{"in" if what == "ingresso" else "out"}. Disponibili: {avail}')

    return choose(a.inp, ins, 'ingresso'), choose(a.outp, outs, 'uscita')


def cmd_ports(a):
    ins, outs = mido.get_input_names(), mido.get_output_names()
    print('ingressi MIDI:')
    for p in ins or ['  (nessuno)']:
        mark = '  <- probabile Deluge' if 'deluge' in p.lower() else ''
        print(f'  {p}{mark}')
    print('uscite MIDI:')
    for p in outs or ['  (nessuna)']:
        mark = '  <- probabile Deluge' if 'deluge' in p.lower() else ''
        print(f'  {p}{mark}')
    if not ins:
        print('\nNessun ingresso MIDI. Collega il Deluge via USB e accendilo.')


def with_device(a, fn):
    ip, op = pick_ports(a)
    print(f'ingresso: {ip}\nuscita  : {op}\n')
    with mido.open_input(ip) as inp, mido.open_output(op) as out:
        return fn(Deluge(inp, out, a.timeout, a.verbose))


def cmd_ping(a):
    def go(dev):
        t0 = time.time()
        reply, blob, other = dev.request({'ping': {}})
        dt = (time.time() - t0) * 1000
        if reply is None:
            print(f'NESSUNA RISPOSTA entro {a.timeout}s')
            if other:
                print(f'  ({len(other)} sysex ricevuti ma non riconosciuti; '
                      'riprova con --verbose)')
            print('\nDa controllare, in ordine:')
            print('  - la porta di uscita e quella giusta')
            print('  - SETTINGS > COMMUNITY FEATURES > devSysexAllowed sul Deluge')
            print('  - il Deluge non sta accedendo alla SD in questo momento')
            return 1
        print(f'RISPOSTA in {dt:.0f} ms: {json.dumps(reply)}')
        return 0
    return with_device(a, go)


def cmd_dir(a):
    def go(dev):
        dev.open_session()
        offset, total = 0, 0
        while True:
            prev, dev.timeout = dev.timeout, 0.25
            reply, _, _ = dev.request({'dir': {'path': a.path,
                                               'offset': offset,
                                               'lines': a.lines}},
                                      retries=25)
            dev.timeout = prev
            if reply is None:
                print(f'nessuna risposta a offset {offset}')
                return 1
            val = reply_value(reply, 'dir')
            if val is None:
                print(f'risposta inattesa: {json.dumps(reply)}')
                return 1
            entries = val.get('list', val) if isinstance(val, dict) else val
            if not isinstance(entries, list) or not entries:
                break
            for e in entries:
                if isinstance(e, dict):
                    name = e.get('name', '?')
                    size = e.get('size', '')
                    attr = e.get('attr', '')
                    print(f'  {str(size):>10}  {attr:>4}  {name}')
                else:
                    print(f'  {e}')
            total += len(entries)
            offset += len(entries)
            if len(entries) < a.lines:
                break
        print(f'\n{total} voci in {a.path}')
        return 0
    return with_device(a, go)


def _open(dev, path, retries):
    reply, _, _ = dev.request({'open': {'path': path}}, retries=retries)
    if reply is None:
        return None, 0
    val = reply_value(reply, 'open')
    if not isinstance(val, dict) or 'fid' not in val or val.get('err'):
        return None, 0
    return val['fid'], val.get('size', 0)


def cmd_get(a):
    def go(dev):
        dev.open_session()
        fid, size = _open(dev, a.remote, a.retries)
        if fid is None:
            print(f'open fallita per {a.remote}')
            return 1
        print(f'aperto fid={fid} size={size}')

        buf, addr, reopens = bytearray(), 0, 0
        t0 = time.time()
        try:
            while addr < size:
                n = min(a.block, size - addr)
                # timeout corto: una risposta buona torna in 3-5 ms, quindi
                # aspettarne 800 costa 200 volte troppo. Vedi docs/SYSEX.md.
                prev, dev.timeout = dev.timeout, a.read_timeout
                reply, blob, _ = dev.request(
                    {'read': {'fid': fid, 'addr': addr, 'size': n}},
                    retries=a.retries)
                dev.timeout = prev
                if reply is not None and blob:
                    buf += blob[:n]
                    addr += len(blob[:n])
                    print(f'\r  {addr}/{size} byte ({100*addr/size:.0f}%)'
                          f'{f"  riaperture {reopens}" if reopens else ""}',
                          end='', flush=True)
                    continue

                # Osservato: dopo un certo numero di letture il firmware smette
                # di rispondere a `read`, mentre `close` risponde ancora subito.
                # Il descrittore va rinfrescato: chiudere e riaprire riprende
                # da dove si era arrivati.
                if reopens >= a.max_reopens:
                    print(f'\nlettura interrotta a {addr}/{size} dopo '
                          f'{reopens} riaperture')
                    return 1
                reopens += 1
                dev.request({'close': {'fid': fid}}, retries=a.retries)
                fid, _ = _open(dev, a.remote, a.retries)
                if fid is None:
                    print(f'\nriapertura fallita a {addr}/{size}')
                    return 1
        finally:
            if fid is not None:
                dev.request({'close': {'fid': fid}}, retries=a.retries)
        dt = time.time() - t0
        print(f'\n  {len(buf)/1024/dt:.1f} kB/s — {dev.timeouts} timeout, '
              f'{reopens} riaperture')
        Path(a.local).write_bytes(bytes(buf))
        print(f'scritto {a.local} ({len(buf)} byte)')
        return 0
    return with_device(a, go)


def _read_all(dev, path, block, retries, read_timeout):
    """Rilegge un file dal dispositivo. Usato per verificare cosa si e' scritto."""
    fid, size = _open(dev, path, retries)
    if fid is None:
        return None
    buf, addr = bytearray(), 0
    try:
        while addr < size:
            n = min(block, size - addr)
            prev, dev.timeout = dev.timeout, read_timeout
            reply, blob, _ = dev.request(
                {'read': {'fid': fid, 'addr': addr, 'size': n}}, retries=retries)
            dev.timeout = prev
            if reply is None or not blob:
                return None
            buf += blob[:n]
            addr += len(blob[:n])
    finally:
        dev.request({'close': {'fid': fid}}, retries=retries)
    return bytes(buf)


def cmd_put(a):
    """Scrive un file sulla SD del Deluge e ne verifica il contenuto.

    Rifiuta di sovrascrivere: se il percorso remoto esiste gia', si ferma.
    Dopo la scrittura rilegge sempre il file e confronta gli hash — un
    trasferimento su un canale che perde messaggi non va mai dato per buono
    senza riprova.
    """
    src = Path(a.local)
    if not src.is_file():
        print(f'{src} non esiste')
        return 1
    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    print(f'sorgente : {src} ({len(data)} byte)')
    print(f'sha256   : {digest}')
    print(f'destinaz.: {a.remote}\n')

    def go(dev):
        dev.open_session()

        # --- nessuna sovrascrittura ---
        fid, size = _open(dev, a.remote, 25)
        if fid is not None:
            dev.request({'close': {'fid': fid}}, retries=25)
            print(f'ATTENZIONE: {a.remote} esiste gia ({size} byte). '
                  'Non lo sovrascrivo.')
            print('Scegli un nome diverso.')
            return 1

        reply, _, _ = dev.request(
            {'open': {'path': a.remote, 'write': 1, 'date': 0, 'time': 0}},
            retries=25)
        val = reply_value(reply, 'open') if reply else None
        if not val or 'fid' not in val or val.get('err'):
            print(f'open in scrittura fallita: {json.dumps(reply)}')
            return 1
        fid = val['fid']
        print(f'creato fid={fid}')

        addr, short, reopens = 0, 0, 0
        t0 = time.time()
        ok = True
        try:
            while addr < len(data):
                chunk = data[addr:addr + a.block]
                prev, dev.timeout = dev.timeout, a.write_timeout
                reply, _, _ = dev.request(
                    {'write': {'fid': fid, 'addr': addr, 'size': len(chunk)}},
                    retries=a.retries, blob=chunk)
                dev.timeout = prev
                v = reply_value(reply, 'write') if reply else None
                if not v or v.get('err'):
                    print(f'\nscrittura fallita a {addr}: {json.dumps(reply)}')
                    ok = False
                    break
                # Il firmware riporta quanti byte ha SCRITTO davvero, che puo'
                # essere meno di quanti gliene abbiamo mandati. Avanzare della
                # lunghezza richiesta invece che di quella confermata lascia
                # buchi silenziosi nel file: e' cosi' che i primi tentativi
                # producevano file piu' corti dell'originale.
                wrote = v.get('size', len(chunk))
                if wrote != len(chunk):
                    short += 1
                    if short <= 3:
                        print(f'\n  ! a {addr}: chiesti {len(chunk)}, '
                              f'scritti {wrote}')
                if wrote <= 0:
                    # Stesso rimedio che sblocca le letture: il descrittore
                    # smette di accettare dati, ma chiudendolo e riaprendolo
                    # in append (write=2) si riprende da dove si era arrivati.
                    if reopens >= a.max_reopens:
                        print(f'\nfermo a {addr}/{len(data)} dopo '
                              f'{reopens} riaperture')
                        ok = False
                        break
                    reopens += 1
                    dev.request({'close': {'fid': fid}}, retries=25)
                    r2, _, _ = dev.request(
                        {'open': {'path': a.remote, 'write': 2,
                                  'date': 0, 'time': 0}}, retries=25)
                    v2 = reply_value(r2, 'open') if r2 else None
                    if not v2 or 'fid' not in v2 or v2.get('err'):
                        print(f'\nriapertura in append fallita a {addr}: '
                              f'{json.dumps(r2)}')
                        ok = False
                        break
                    fid = v2['fid']
                    continue
                addr += wrote
                print(f'\r  {addr}/{len(data)} byte '
                      f'({100*addr/len(data):.0f}%)', end='', flush=True)
        finally:
            dev.request({'close': {'fid': fid}}, retries=25)
        dt = time.time() - t0
        if not ok:
            return 1
        print(f'\n  {len(data)/1024/dt:.1f} kB/s, {dev.timeouts} timeout, '
              f'{short} blocchi parziali, {reopens} riaperture\n')

        print('verifica per rilettura…')
        back = _read_all(dev, a.remote, a.block, 25, a.read_timeout)
        if back is None:
            print('  rilettura fallita: NON posso confermare la scrittura')
            return 1
        got = hashlib.sha256(back).hexdigest()
        print(f'  riletti  : {len(back)} byte')
        print(f'  sha256   : {got}')
        if got == digest and len(back) == len(data):
            print('\n  IDENTICO — la scrittura e verificata')
            return 0
        print(f'\n  DIVERSO dall originale ({len(data)} byte, {digest})')
        return 1

    return with_device(a, go)


def cmd_raw(a):
    def go(dev):
        if a.session:
            print(f'sessione: {json.dumps(dev.open_session())}\n')
        rc = 0
        for j in a.json:
            print(f'--- {j}')
            reply, blob, other = dev.request(json.loads(j))
            print(f'risposta: {json.dumps(reply) if reply else "NESSUNA"}')
            if blob:
                print(f'binario : {len(blob)} byte, primi 80: {blob[:80]!r}')
            for d in other:
                print(f'altro sysex: {" ".join(f"{b:02X}" for b in d[:24])}'
                      f' ({len(d)} byte)')
            if reply is None:
                rc = 1
            print()
        return rc
    return with_device(a, go)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--in', dest='inp', help='porta MIDI di ingresso')
    ap.add_argument('--out', dest='outp', help='porta MIDI di uscita')
    ap.add_argument('--timeout', type=float, default=3.0)
    ap.add_argument('-v', '--verbose', action='store_true')
    sub = ap.add_subparsers(dest='cmd', required=True)

    sub.add_parser('ports').set_defaults(fn=cmd_ports)
    sub.add_parser('ping').set_defaults(fn=cmd_ping)

    p = sub.add_parser('dir')
    p.add_argument('path', nargs='?', default='/')
    p.add_argument('--lines', type=int, default=20)
    p.set_defaults(fn=cmd_dir)

    p = sub.add_parser('get')
    p.add_argument('remote'); p.add_argument('local')
    # 768 e' il massimo che il dispositivo accetta (a 1024 non risponde mai) ed
    # e' anche il piu' veloce. Misurato end-to-end su Perche.XML, hash sempre
    # verificato: 96 -> 52 s, 256 -> 18 s, 384 -> 14 s, 512 -> 13 s, 768 -> 7 s.
    # Le sonde brevi sulla percentuale di successo dicono il contrario e sono
    # fuorvianti: la perdita compare sotto carico prolungato. L'unica misura
    # che conta e' il trasferimento di un file vero, cronometrato e con hash.
    p.add_argument('--block', type=int, default=768)
    p.add_argument('--read-timeout', type=float, default=0.06,
                   help='timeout per singola read; le risposte buone '
                        'arrivano in 3-5 ms')
    p.add_argument('--retries', type=int, default=25)
    p.add_argument('--max-reopens', type=int, default=200)
    p.set_defaults(fn=cmd_get)

    p = sub.add_parser('put')
    p.add_argument('local'); p.add_argument('remote')
    p.add_argument('--block', type=int, default=768)
    p.add_argument('--write-timeout', type=float, default=0.06)
    p.add_argument('--read-timeout', type=float, default=0.06)
    p.add_argument('--retries', type=int, default=25)
    p.add_argument('--max-reopens', type=int, default=400)
    p.set_defaults(fn=cmd_put)

    p = sub.add_parser('raw')
    p.add_argument('json', nargs='+', help='una o piu richieste JSON, in sequenza')
    p.add_argument('--session', action='store_true',
                   help='apre prima una sessione (serve per le operazioni su file)')
    p.set_defaults(fn=cmd_raw)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == '__main__':
    sys.exit(main())
