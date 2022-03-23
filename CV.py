import jinja2
import os
import markdown
import dateparser
import json
import datetime
import lxml.html
import lxml.html.builder
import json

from unidecode import unidecode

author_list = json.load(open('authors.json'))


class Link:
    def __init__(self, title, href):
        self.title = title
        self.href = href


class Paper:
    def __init__(self, id, content):
        md = markdown.Markdown(extensions=['meta'])
        md.convert(content)
        meta = md.Meta

        self._id = id
        self._date = dateparser.parse(meta['date'][0])

        self.date = self._date.strftime("%B %Y")

        self.title = meta['title'][0]

        links = json.loads(meta['links'][0])
        self.links = []
        for key in links:
            self.links.append(Link(key, links[key]))

        self.authors = []
        for a in meta['authors']:
            if a in author_list:
                self.authors.append(Link(a, author_list[a]))
            else:
                self.authors.append(Link(a, ''))


class Talk:
    def __init__(self, id, content):
        md = markdown.Markdown(extensions=['meta'])
        md.convert(content)
        meta = md.Meta

        self._id = id
        self._date = dateparser.parse(meta['date'][0])

        self.date = self._date.strftime("%B %Y")

        self.title = meta['title'][0]
        self.venue = meta['venue'][0]
        self.location = meta['location'][0]

        # links = json.loads(meta['links'][0])
        # self.links = []
        # for key in links:
        #     self.links.append(Link(key, links[key]))

        # self.authors = []
        # for a in meta['authors']:
        #     if a in author_list:
        #         self.authors.append(Link(a, author_list[a]))
        #     else:
        #         self.authors.append(Link(a, ''))

# -----------
# LOAD PAPERS
# -----------


paper_list = []

for root, dirs, files in os.walk("papers"):
    for name in dirs:
        input = open(os.path.join(root, name, "index.md"), "r")
        paper_list.append(Paper(name, input.read()))
    break

paper_list.sort(key=lambda p: p._date, reverse=True)


# ----------
# LOAD TALKS
# ----------
talk_list = []

for root, dirs, files in os.walk("talks"):
    for name in dirs:
        input = open(os.path.join(root, name, "index.md"), "r")
        talk_list.append(Talk(name, input.read()))
    break

talk_list.sort(key=lambda t: t._date, reverse=True)


# conference_list = {
#     'NeurIPS 2021': 'huj',
#     'NeurIPS 2020': 'huj',
#     'NeurIPS 2019': 'huj',
#     'NeurIPS 2018': 'huj',
#     'ICML 2021': 'huj',
#     'ICML 2020': 'huj',
#     'AISTATS 2021': 'huj'}

def convert_venue(title):
    venue_list = {'CRM': 'Computer Research and Modeling'}
    if title in venue_list.keys():
        return venue_list[title]
    return title


file = open("CV2/papers.tex", "w")
# ------------------
# WRITE PUBLICATIONS
# ------------------
file.write("\\section{Publications}\n")
file.write('\\begin{enumerate}\n')
for paper in paper_list:
    if paper.links[1].title == 'arXiv':
        continue
    file.write('\\item \\textbf{{{}}}'.format(paper.title))
    file.write(' (')
    for author in paper.authors:
        file.write('\\href{{{}}}{{\\color{{linkcolour}}{}}}'.format(
            author.href, unidecode(author.title)))
        if author != paper.authors[-1]:
            file.write(', ')
    file.write('), ')
    file.write('{}'.format('\\href{{{}}}{{\\em \\color{{black}}{}}}'.format(
        paper.links[1].href, convert_venue(paper.links[1].title))))
    file.write('\n')
file.write('\\end{enumerate}\n')


# ---------------
# WRITE PREPRINTS
# ---------------
file.write("\\section{Preprints}\n")
file.write('\\begin{enumerate}\n')
for paper in paper_list:
    if paper.links[1].title != 'arXiv':
        continue
    file.write('\\item \\textbf{{{}}}'.format(paper.title))
    file.write(' (')
    for author in paper.authors:
        file.write('\\href{{{}}}{{\\color{{linkcolour}}{}}}'.format(
            author.href, unidecode(author.title)))
        if author != paper.authors[-1]:
            file.write(', ')
    file.write('), ')
    file.write('\\href{{{}}}{{\\em \\color{{black}}{} ({})}}'.format(
        paper.links[1].href, 'arXiv preprint', paper.date))
    file.write('\n')
file.write('\\end{enumerate}\n')
file.close()


# --------------
# WRITE DATETIME
# --------------
file = open("CV2/date.tex", "w")
file.write('\\begin{center}\n')
file.write('Last Updated on {}\n'.format(
    datetime.datetime.now().strftime('%B %d, %Y')))
file.write('\\end{center}\n')
file.close()


# -----------
# WRITE TALKS
# -----------
file = open("CV2/talks.tex", "w")
file.write('\\section{Conferences and Talks}\n')
file.write('\\begin{enumerate}\n')
for talk in talk_list:
    file.write('\\item {{\\bf {}}}, {{\\em {}}}, {} ({})\n'.format(
        talk.title, talk.venue, talk.location, talk.date))
file.write('\\end{enumerate}\n')
file.close()
