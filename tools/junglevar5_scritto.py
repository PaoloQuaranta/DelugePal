"""JUNGLEVAR05 -- BASS-PUSH diventa hook e il kit prende un feel jazz.

Parte dalla JUNGLEVAR04 appena riscaricata. Il groove deriva dalla singola
performance Groove MIDI Dataset ``drummer1/session1/77`` (jazz/mediumfast,
180 BPM): se ne usa il residuo microtimico, gia privato dello swing dalla
libreria, al 35%, e la dinamica al 30%. I trigger di loop ``Liqu`` restano
byte-esatti sulla griglia.
"""
from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

SOURCE = RADICE / 'out' / 'JUNGLEVAR04_user2.XML'
GROOVE_BASE = RADICE / 'to-read' / 'MIDI' / 'groove-v1.0.0-midionly' / 'groove'
GROOVE_ID = 'drummer1/session1/77'

# Ruolo musicale delle fette del kit 972, stabilito dalle parti gia scritte.
# Non e una mappa GM del nome numerico: dice quale gesto del batterista usare.
RUOLO = {
    '5': 'kick', '6': 'kick',
    '7': 'rullante', '8': 'rullante', '11': 'rullante', '13': 'rullante',
    '14': 'ride',
    '15': 'tom basso', '16': 'tom medio-alto',
}


def carica_sorgente(source: Path | str = SOURCE):
    from delugexml import parse_file                         # noqa: PLC0415
    return parse_file(str(source))


def strumento(doc, nome: str):
    from delugexml import song as S                          # noqa: PLC0415
    for inst in S.instruments(doc):
        if inst.get('presetName') == nome or inst.get('name') == nome:
            return inst
    raise ValueError(f'nessuno strumento {nome!r} nella song')


def _sposta_automazioni(riga, delta: dict[int, int], lunghezza: int,
                        finestra: int) -> int:
    """Fa seguire ai lock lo stesso piccolo scarto del colpo associato."""
    from delugexml import automation as AU, sound as SND     # noqa: PLC0415

    mosse = 0
    onset = sorted(delta)
    for param in SND.names(riga):
        raw = SND.get_raw(riga, param)
        if not raw or not AU.is_automation(raw):
            continue
        testa, punti = AU.decode(raw)
        nuovi = []
        for p in punti:
            scarto = delta.get(p.pos)
            if scarto is None:
                precedenti = [pos for pos in onset
                              if 0 < p.pos - pos <= finestra]
                scarto = delta[precedenti[-1]] if precedenti else 0
            nuova_pos = min(lunghezza - 1, max(0, p.pos + scarto))
            mosse += nuova_pos != p.pos
            nuovi.append(AU.Punto(pos=nuova_pos, raw=p.raw, interp=p.interp))
        # Il controllo esplicito impedisce di produrre un blob ambiguo se
        # due punti vicini collassano dopo il microtiming.
        if len({p.pos for p in nuovi}) != len(nuovi):
            raise ValueError(f'umanizzazione crea lock duplicati su {param}')
        SND.set_raw(riga, param, AU.encode(testa, nuovi))
    return mosse


def _umanizza_riga(doc, clip, riga, profilo, ruolo: str,
                   timing: float = 0.35, dinamica: float = 0.30) -> dict:
    """Miscela una riga col profilo senza sostituirne identita e accenti."""
    from delugexml import song as S                           # noqa: PLC0415

    originali = sorted(S.read_notes(riga), key=lambda n: n.pos)
    passo_song = S.ticks_per_bar(doc.root) // 16
    scala = MU.TICK_PER_PASSO / passo_song
    per_passo = {p.passo: p for p in profilo.passi[ruolo]}
    lunghezza = int(clip.get('length'))
    nuove = []
    delta = {}
    toccate = 0
    senza = set()
    for prima in originali:
        passo = (prima.pos // passo_song) % 16
        misura = per_passo.get(passo)
        if misura is None:
            scarto = 0
            velocity = prima.velocity
            senza.add(passo)
        else:
            scarto = max(-4, min(4, round(
                misura.scarto / scala * timing)))
            velocity = max(1, min(127, round(
                prima.velocity * (1 - dinamica)
                + misura.velocity * dinamica)))
            toccate += 1
        posizione = min(lunghezza - 1, max(0, prima.pos + scarto))
        nuove.append(replace(prima, pos=posizione, velocity=velocity))
        delta[prima.pos] = posizione - prima.pos
    if len({n.pos for n in nuove}) != len(nuove):
        raise ValueError(f'umanizzazione crea note duplicate nella riga {ruolo}')
    S.write_notes(riga, sorted(nuove, key=lambda n: n.pos), create=True)
    lock = _sposta_automazioni(riga, delta, lunghezza,
                               finestra=max(1, passo_song // 2))
    return {'ruolo': ruolo, 'note': len(nuove), 'toccate': toccate,
            'senza_appoggio': sorted(senza), 'lock_mossi': lock,
            'scarto_min': min(delta.values(), default=0),
            'scarto_max': max(delta.values(), default=0)}


def _anticipa_hook(doc) -> dict:
    from delugexml import arranger as A, song as S           # noqa: PLC0415

    basso = strumento(doc, '31-BASS1')
    tpb = S.ticks_per_bar(doc.root)
    clip = [c for _, c in S.clips(doc) if S.instrument_of(doc, c) is basso]
    originale = next(c for c in clip if c.has('section')
                     and not c.get('clipName'))
    hook = next(c for c in clip if c.get('clipName') == 'BASS-PUSH')

    # La vecchia istanza originale occupava 33-64. La prima meta diventa il
    # primo statement dell'hook; la seconda conserva un ciclo originale.
    tolte = A.remove_instances_in(basso, 32 * tpb, 64 * tpb)
    if tolte['tolte'] != 1 or tolte['a_cavallo']:
        raise ValueError(f'istanza basso 33-64 inattesa: {tolte}')
    A.place(doc, basso, hook, 32 * tpb, 16 * tpb)
    A.place(doc, basso, originale, 48 * tpb, 16 * tpb)
    return {'primo_hook': 33, 'ritorno_hook': 81,
            'contrasto_originale': 49}


def _umanizza_kit(doc, profilo) -> list[dict]:
    from delugexml import song as S                           # noqa: PLC0415

    kit = strumento(doc, '972')
    rapporti = []
    for _, clip in S.clips(doc):
        if S.instrument_of(doc, clip) is not kit:
            continue
        nomi = S.drum_names(doc, clip)
        for riga in S.note_rows(clip):
            note = S.read_notes(riga)
            if not note:
                continue
            drum = nomi[int(riga.get('drumIndex'))]
            if drum == 'Liqu':
                continue
            ruolo = RUOLO.get(drum, 'rullante')
            rapporti.append(_umanizza_riga(doc, clip, riga, profilo, ruolo))
    return rapporti


def costruisci(source: Path | str = SOURCE) -> tuple[object, dict]:
    from delugexml import arranger as A, groove as GR         # noqa: PLC0415

    doc = carica_sorgente(source)
    profilo = GR.profilo(GROOVE_BASE, GROOVE_ID)
    hook = _anticipa_hook(doc)
    rapporti = _umanizza_kit(doc, profilo)
    A.fit_view(doc)
    A.open_in_arranger(doc)
    return doc, {
        'hook': hook,
        'groove_id': profilo.id,
        'groove_style': profilo.style,
        'groove_bpm': profilo.bpm,
        'groove_bur': profilo.bur,
        'timing_mix': 0.35,
        'velocity_mix': 0.30,
        'righe_umanizzate': rapporti,
        'source': str(source),
    }


if __name__ == '__main__':
    from delugexml import arranger as A

    doc, meta = costruisci()
    print('hook:', meta['hook'])
    print('groove:', meta['groove_id'], meta['groove_style'], meta['groove_bpm'],
          'BPM, BUR', round(meta['groove_bur'], 3))
    print('righe umanizzate:', len(meta['righe_umanizzate']))
    print('arco:', A.extent(doc))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
