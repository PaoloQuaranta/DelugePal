"""delugexml — lettura/scrittura degli XML del Synthstrom Deluge.

Il firmware NON scrive XML strettamente well-formed (vedi docs/FINDINGS.md):
non escapa '&' e in alcuni casi duplica attributi. Questo package usa quindi
un parser tollerante scritto su misura, non xml.etree.
"""
from .parser import Node, Document, parse, parse_file, ParseProblem
from .writer import FormatTable, serialize, write_file
from .notes import Note
from . import song, notes, arranger, midicv, audio, musica

__all__ = ['Node', 'Document', 'parse', 'parse_file', 'ParseProblem',
           'FormatTable', 'serialize', 'write_file', 'Note', 'song', 'notes',
           'arranger', 'midicv', 'audio', 'musica']
