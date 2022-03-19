import jinja2
import os
import markdown
import dateparser
import json
import datetime
import lxml.html
import lxml.html.builder
import json

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

        self.date = self._date.strftime("%d %b %Y")

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

print('Papers:')
for paper in paper_list:
    print(paper.title)
    for author in paper.authors:
        print('\t', author.title, author.href)
