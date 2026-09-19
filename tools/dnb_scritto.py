"""DnB / JUNGLE -- l'amen break affettato e ri-sequenziato, sub half-time, armonia
minore cinematica.

Primo genere della riga aggregata «elettronica · IDM · DnB · jungle». Non serve
una capacita' nuova: lo SLICING (kit.affetta) e' lo stesso gesto del vocal chop --
l'HANDOFF lo diceva («Ora lo slicing c'e', quindi DnB/jungle non aspettano piu' un
prerequisito»). Qui cambia il MATERIALE (un break di batteria, non una voce) e il
METODO del chop (ricostruire un groove, non romperlo).

Il cuore e' il BREAK:
- `original AMEN.wav` (SAMPLES/sampleswap/...) e' gia' stretchato a ~171 BPM, 4
  battute, 268795 frame. A song=171 una griglia di 1/16 combacia con la durata di
  una fetta da 1/16: le fette IN ORDINE ricostruiscono l'amen esatto (ONCE + zona,
  come lo Slicer nativo), RI-SEQUENZIATE danno il chop jungle.
- 64 fette (1/16 su 4 battute). Il ri-sequenziamento lavora per BEAT (4 fette
  contigue = un movimento coerente del batterista vero): rimescolare i beat suona
  «amen editato», non rumore. Le casse gravi (fette 0, 24, 56 -- [OSS] dall'analisi
  di energia stdlib) cadono sui movimenti forti. Due rullate (stutter di una fetta
  di rullante) chiudono le frasi.
- + un drum a parte, l'AMEN INTERO in one-shot (zona [0, FRAMES], ONCE): NON e'
  sequenziato, serve a sentire il break ORIGINALE innescandolo a mano sul dispositivo.

Sotto il break veloce, il FEEL half-time lo danno le parti lente:
- SUB (Square Saw Bass scurito): fondamentale grave tenuta sul 1 + spinta sul 4,
  segue le fondamentali del vamp. Rado: e' il break a correre, non il basso.
- ARMONIA (priorita' 1, [CALC]): il vamp minore cinematico Cm9 | Abmaj7 | Cm9 | G7b9
  -- i-bVI-i-V7b9 (il bVI caldo, la dominante alterata scura), lo stesso colore che
  l'utente ha approvato nel trip-hop, arrangiato per la jungle. Tal Rhodes tenuto,
  con un velo di riverbero. Chiuso col [CALC] (racconta_armonia).

La FORMA (32 battute): intro (break solo, il groove si enuncia) -> drop (tutto) ->
breakdown (sub + pad, il break ESCE: la tensione) -> drop.

⚠️ FEEL DRITTO (swing 50), e non e' una dimenticanza: il break e' una REGISTRAZIONE,
il suo micro-timing e' gia' nell'audio delle fette. Uno swing di song lo sposterebbe
una seconda volta (e sposterebbe anche sub e pad). Il groove umano lo porta il
disco, non set_swing.

⚠️ NIENTE CORPUS DnB/jungle in casa (Groove MIDI non ha l'etichetta): [LIB]+[DEC].
Il break e' [OSS] (l'audio di un'esecuzione vera, l'amen); l'analisi delle fette e'
[OSS] stdlib; l'armonia e' [CALC]. Il chop e' [DEC], da rifinire all'orecchio --
anche QUALI beat stanno bene insieme si decide sentendo (come il vocal chop).

Metodo: audio + arrangiamento = ascolto pieno dell'utente. Verdetto (19 settembre
2026): «va bene».
"""
from __future__ import annotations

import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from delugexml import musica as MU                            # noqa: E402

B = MU.TICK_PER_BATTUTA      # 384
MOV = MU.TICK_PER_MOVIMENTO  # 96
CROMA = MOV // 2             # 48
P = MOV // 4                 # 24, un sedicesimo

TEMPL = RADICE / 'refs' / 'songs' / 'TEMPL0.XML'
PRESET_RHODES = RADICE / 'refs' / 'synths' / 'Tal Rhodes.XML'
PRESET_BASSO = RADICE / 'refs' / 'synths' / 'Square Saw Bass.XML'
KIT = RADICE / 'refs' / 'kits' / '808 From Mars.XML'

# il break: gia' sulla SD, niente upload. FRAMES da audio.wav_frames (268795, 48000, 2).
SAMPLE = 'SAMPLES/sampleswap/advanced_operator_samplepack/drums/original AMEN.wav'
FRAMES = 268795
NFETTE = 64                                # 1/16 su 4 battute (16 fette/battuta)
NOME_INTERO = 'amen intero'                # il drum col LOOP intero in one-shot (lo suona l'utente)

BPM = 171                                  # DnB classico; il nativo dell'amen stretchato
SWING = 50                                 # DRITTO: il feel del break e' nell'audio
VAMP = ['Cm9', 'Abmaj7', 'Cm9', 'G7b9']    # i-bVI-i-V7b9, cinematico e scuro
BARS = len(VAMP)                           # 4
LUNG = BARS * B                            # una clip dura 4 battute e si ripete

# --- il chop: quale BEAT sorgente (0..15) suona in ciascuno dei 16 beat in uscita.
# Un beat = 4 fette contigue (un movimento coerente del batterista). Le casse gravi
# aprono i movimenti forti (out-beat 0,4,8,12 = i "1" delle 4 battute):
#   beat 0  parte con la fetta 0  (1.00, la cassa grave iconica dell'amen)
#   beat 6  parte con la fetta 24 (2.08, cassa grave)
#   beat 14 parte con la fetta 56 (4.08, cassa grave)
BEAT_ORDER = [
    0,  5,  2,  3,     # batt.1: cassa, poi si enuncia quasi dritto (riconoscibile)
    6,  9, 10,  7,     # batt.2: cassa grave (b6), poi rulla nel mezzo
    0,  1, 10, 11,     # batt.3: riprende l'attacco, poi sale
    14, 13, 12, 15,    # batt.4: cassa grave (b14), giro, chiusura
]
# rullate (jungle snare roll): out-beat -> fetta ripetuta 4x (un 1/16 per volta).
# fetta 61 = 4.13 (rullante broadband, [OSS]); chiude le due frasi da 2 battute.
STUTTER = {7: 61, 15: 61}


def chop(fette: list[str]) -> dict:
    """Il break ri-sequenziato. Ritorna {nome_fetta: [Note,...]}. In ordine le fette
    ricostruirebbero l'amen; qui i beat sono rimescolati (+ due rullate) = il chop.
    Ogni fetta e' innescata con length=P; con ONCE e' la ZONA a durare, la length e'
    cosmetica. [DEC], da rifinire all'orecchio."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voci: dict = {}

    def metti(fetta_idx: int, step: int) -> None:
        nome = fette[fetta_idx]
        voci.setdefault(nome, []).append(
            Note(pos=step * P, length=P, velocity=115))

    for out_beat in range(16):
        base = out_beat * 4                                   # step 1/16 del beat
        if out_beat in STUTTER:                               # una fetta 4x = rullata
            for k in range(4):
                metti(STUTTER[out_beat], base + k)
        else:                                                 # 4 fette contigue del beat
            src = BEAT_ORDER[out_beat] * 4
            for k in range(4):
                metti(src + k, base + k)
    return voci


def _grave(pc: int, rif: int, lo: int = 26, hi: int = 38) -> int:
    """La nota di classe `pc` piu' vicina a `rif`, nel registro grave del sub."""
    best = None
    for y in range(lo, hi + 1):
        if y % 12 == pc and (best is None or abs(y - rif) < abs(best - rif)):
            best = y
    return best


def sub() -> dict:
    """Il sub half-time: fondamentale grave TENUTA sul 1 (3 movimenti) + una spinta
    corta sul 4, per battuta, sulle fondamentali del vamp. Rado -- e' il break a
    correre. Da' il feel dimezzato sotto la batteria veloce."""
    from delugexml.notes import Note                          # noqa: PLC0415
    voce: dict = {}
    rif = 33
    for bar, sig in enumerate(VAMP):
        da = bar * B
        root = _grave(MU.sigla(sig).fondamentale, rif)
        rif = root
        voce.setdefault(root, []).append(Note(pos=da, length=3 * MOV, velocity=104))
        voce.setdefault(root, []).append(Note(pos=da + 3 * MOV, length=MOV, velocity=86))
    return voce


def pad() -> dict:
    """Il vamp minore cinematico, tenuto e rootless sul Rhodes -- condotto
    (voice-leading). L'armonia e' chiusa col [CALC]; qui la si posa."""
    return MU.armonia(' | '.join(VAMP), voicing='senza-fondamentale',
                      registro='do3', durata='1/1', velocity=58,
                      articolazione='legato')


def strumento(doc, nome: str):
    """Lo strumento della song che si chiama `nome` (presetName)."""
    from delugexml import song as S                           # noqa: PLC0415
    for inst in S.instruments(doc):
        if inst.get('presetName') == nome or inst.get('name') == nome:
            return inst
    raise ValueError(f'nessuno strumento "{nome}" nella song')


def costruisci() -> tuple[object, dict]:
    """Il pezzo dell'ascolto. Ritorna (doc, {}). Solleva FileNotFoundError se manca
    una fixture (un preset di refs/)."""
    import warnings                                           # noqa: PLC0415
    from delugexml import parse_file, song as S              # noqa: PLC0415
    from delugexml import create as C, arranger as A         # noqa: PLC0415
    from delugexml import kit as K, sound as SND             # noqa: PLC0415

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        doc = parse_file(str(TEMPL))
        S.set_bpm(doc.root, BPM)
        S.set_swing(doc, SWING, figura='1/8')      # 50 = dritto
        S.set_scale(doc, 'C', 'minore')            # Do minore
        for inst in list(S.instruments(doc)):
            MU.togli(doc, inst)

        # il break: l'amen in 64 fette (kit 808 come telaio del drum, poi affettato)
        iBreak, cBreak = C.add_track(doc, str(KIT), name='AMEN', folder='KITS',
                                     length=LUNG, colour_offset='32', playing=True)
        fette = K.affetta(doc, iBreak, SAMPLE, FRAMES, n=NFETTE)
        for nome, note in chop(fette).items():
            if note:
                MU.scrivi(doc, cBreak, note, dove=nome)

        # + l'AMEN INTERO in one-shot: un drum in fondo al kit con la zona = tutto il
        # file [0, FRAMES] e REPEAT MODE ONCE (come lo Slicer, la zona delimita). NON
        # e' sequenziato -- serve a sentire il break ORIGINALE innescandolo a mano sul
        # dispositivo (richiesta dell'utente: «aggiungi solo il campione, poi lo suono io»).
        K.add_drum(doc, iBreak, K.copy_drum(iBreak, 0), name=NOME_INTERO)
        intero = S.drums(iBreak)[-1]
        K.set_sample(intero, SAMPLE, start=0, end=FRAMES)
        osc = intero.find('osc1')
        if osc is not None:
            osc.set('loopMode', str(K.LOOP_MODE['once']))

        # il sub half-time
        iSub, cSub = C.add_track(doc, str(PRESET_BASSO), name='SUB', folder='SYNTHS',
                                 length=LUNG, colour_offset='16', playing=True)
        try:
            MU.applica_verbo(doc, iSub, 'piu scuro')      # sub grave e pieno
        except Exception:                                 # noqa: BLE001
            pass
        MU.scrivi(doc, cSub, sub())

        # l'armonia: il pad minore cinematico + un velo di riverbero
        iPad, cPad = C.add_track(doc, str(PRESET_RHODES), name='PAD',
                                 folder='SYNTHS', length=LUNG, playing=True)
        MU.scrivi(doc, cPad, pad())
        try:
            SND.set(cPad, 'reverbAmount', 24)
        except Exception:                                 # noqa: BLE001
            pass

        # la forma: intro (break solo) -> drop (tutto) -> breakdown (break FUORI) -> drop
        sezioni = {
            'intro': [cBreak],
            'drop':  [cBreak, cSub, cPad],
            'break': [cSub, cPad],
        }
        MU.forma(doc, 'intro drop break drop', sezioni,
                 battute_per={'intro': 8, 'drop': 8, 'break': 8})
        A.open_in_arranger(doc)
    return doc, {}


if __name__ == '__main__':
    doc, _ = costruisci()
    from delugexml import arranger as A
    print(MU.racconta_armonia(' | '.join(VAMP), voicing='senza-fondamentale',
                              registro='do3'))
    print('fette:', NFETTE, '  campione:', SAMPLE)
    print('chop (out-beat -> beat sorgente):', BEAT_ORDER, ' rullate su', sorted(STUTTER))
    print('arco:', A.extent(doc), '(atteso (0, %d))' % (32 * B))
    print('verifica:', MU.verifica(doc) or 'vuota')
    print('avvertenze:', MU.avvertenze(doc) or 'nessuna')
