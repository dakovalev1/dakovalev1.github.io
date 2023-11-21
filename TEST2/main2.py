import bibtexparser
import bibtexparser.middlewares
import bibtexparser.middlewares.latex_encoding
import bibtexparser.library
import bibtexparser.entrypoint
import bibtexparser.model
import bibtexparser.middlewares.names

import jinja2


class Paper:
    def __init__(self, title, authors) -> None:
        self.title = title
        self.authors = authors
                                    

b = bibtexparser.parse_file('papers.bib', append_middleware=[
    bibtexparser.middlewares.LatexDecodingMiddleware(decoder=bibtexparser.middlewares.latex_encoding.LatexNodes2Text()),
    bibtexparser.middlewares.SeparateCoAuthors(True),
    bibtexparser.middlewares.SplitNameParts(True),
    bibtexparser.middlewares.MergeNameParts(True),
    bibtexparser.middlewares.MergeCoAuthors(),
    bibtexparser.middlewares.SortFieldsAlphabeticallyMiddleware()
])


print('START')

paper_list = []


print(b.entries[10].fields_dict['year'].value)

for entry in b.entries:
    fields = entry.fields_dict
    # print(fields['title'].value)
    # print('\t', fields['author'].value)
    paper_list.append(Paper(fields['title'].value, fields['author'].value))
    # for author in fields['author'].value:
    #     print('\t', author.merge_first_name_first)


file_loader = jinja2.FileSystemLoader('')
env = jinja2.Environment(loader=file_loader)
template = env.get_template('template_index.html')

output = template.render(papers = paper_list)
open('index.html', 'w').write(output)


# a = d['author'].value[3]


# print(a.merge_first_name_first)