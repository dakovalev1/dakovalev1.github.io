import bibtexparser
import bibtexparser.middlewares
import bibtexparser.middlewares.latex_encoding
import json
import re

import jinja2


class Paper:
    def __init__(self, title, authors, venue, year) -> None:
        self.title = title
        self.authors = authors
        self.venue = venue
        self.year = int(year)


b = bibtexparser.parse_file('papers.bib', append_middleware=[
    bibtexparser.middlewares.LatexDecodingMiddleware(decoder=bibtexparser.middlewares.latex_encoding.LatexNodes2Text()),
    bibtexparser.middlewares.SeparateCoAuthors(True),
    bibtexparser.middlewares.SplitNameParts(True),
    bibtexparser.middlewares.MergeNameParts(True),
    bibtexparser.middlewares.SortFieldsAlphabeticallyMiddleware()
])



author_json = json.load(open('authors.json'))

paper_list = []




for entry in b.entries:
    fields = entry.fields_dict
    venue = ''

    if 'journal' in fields.keys():
        venue = fields['journal'].value
    elif 'booktitle' in fields.keys():
        venue = fields['booktitle'].value
    else:
        raise KeyError('no venue', fields)
    
    authors = fields['author'].value

    for index, a in enumerate(authors):
        if a in author_json:
            authors[index] = '<a href={}>{}</a>'.format(author_json[a], a)
        

    paper_list.append(Paper(fields['title'].value, ', '.join(authors), venue, fields['year'].value))
    


file_loader = jinja2.FileSystemLoader('')
env = jinja2.Environment(loader=file_loader)
template = env.get_template('template_index.html')

output = template.render(publications = paper_list)
open('index.html', 'w').write(output)