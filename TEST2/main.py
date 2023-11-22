import bibtexparser
import bibtexparser.middlewares
import bibtexparser.middlewares.latex_encoding

# import json
import re
import jinja2
from collections import defaultdict


class Paper:
    def __init__(self, title, authors, venue, year) -> None:
        self.title = title
        self.authors = authors
        self.venue = venue
        self.year = int(year)

    def __lt__(a, b):
        return (
            a.year > b.year
            or (a.year == b.year and a.venue < b.venue)
            or (a.year == b.year and a.venue == b.venue and a.title < b.title)
        )


b = bibtexparser.parse_file(
    "papers.bib",
    append_middleware=[
        bibtexparser.middlewares.LatexDecodingMiddleware(
            decoder=bibtexparser.middlewares.latex_encoding.LatexNodes2Text()
        ),
        bibtexparser.middlewares.SeparateCoAuthors(True),
        bibtexparser.middlewares.SplitNameParts(True),
        bibtexparser.middlewares.MergeNameParts(True),
    ],
)


# author_json = json.load(open("authors.json"))

publication_list = []
preprint_list = []


for entry in b.entries:
    fields = entry.fields_dict
    venue = ""
    if "journal" in fields.keys():
        venue = fields["journal"].value
    elif "booktitle" in fields.keys():
        venue = fields["booktitle"].value
    else:
        raise KeyError("no venue", fields)

    title = ""
    if "url" not in fields.keys():
        title = fields["title"].value
        # raise KeyError("no url", fields)
    else:
        title = "<a href='{}'>{}</a>".format(fields["url"].value, fields["title"].value)

    authors = fields["author"].value
    # for index, a in enumerate(authors):
    #     if a in author_json:
    #         authors[index] = "<a href='{}'>{}</a>".format(author_json[a], a)

    paper = Paper(title, ", ".join(authors), venue, fields["year"].value)

    if re.fullmatch("arXiv.*", venue):
        preprint_list.append(paper)
    else:
        publication_list.append(paper)


# publication_list.sort()
# preprint_list.sort()


def split_by_year(paper_list):
    pd = defaultdict(list)
    for paper in paper_list:
        pd[paper.year].append(paper)
    result = [(k, v) for k, v in pd.items()]
    result.sort(reverse=True)
    return result


publication_list = split_by_year(publication_list)
preprint_list = split_by_year(preprint_list)


file_loader = jinja2.FileSystemLoader("")
env = jinja2.Environment(loader=file_loader)
template = env.get_template("template_index.html")

output = template.render(
    publications=publication_list,
    preprints=preprint_list,
)
open("index.html", "w").write(output)
