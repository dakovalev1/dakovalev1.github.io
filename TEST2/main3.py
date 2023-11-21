import pybtex
import pybtex.database

base = pybtex.database.parse_file('papers.bib', bib_format='bibtex')

