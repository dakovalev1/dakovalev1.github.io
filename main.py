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
                self.authors.append(lxml.html.tostring(lxml.html.builder.A(a, href = author_list[a])).decode())
            else:
                self.authors.append(a)

class Post:
    def __init__(self, id, content):
        md = markdown.Markdown(extensions=['meta'])
        md.convert(content)
        meta = md.Meta

        self._id = id
        self._date = dateparser.parse(meta['date'][0])

        
        self.title = meta['title'][0]
        self.summary = markdown.markdown(meta['summary'][0])
        self.date = self._date.strftime("%d %b %Y, %H:%M")
        
        if 'links' in meta:
            links = json.loads(meta['links'][0])
            self.links = []
            for key in links:
                self.links.append(Link(key, links[key]))

#-----------
#LOAD PAPERS
#-----------

paper_list = []

for root, dirs, files in os.walk("papers"):
    for name in dirs:
        input = open(os.path.join(root, name, "index.md"), "r")
        paper_list.append(Paper(name, input.read()))
    break

paper_list.sort(key=lambda p: p._date, reverse=True)

#----------
#LOAD POSTS
#----------

post_list = []

for root, dirs, files in os.walk("posts"):
    for name in dirs:
        input = open(os.path.join(root, name, "index.md"), "r")
        post_list.append(Post(name, input.read()))
    break

post_list.sort(key=lambda p: p._date, reverse=True)



file_loader = jinja2.FileSystemLoader('')
env = jinja2.Environment(loader=file_loader)
template = env.get_template('template_index.html')

output = template.render(papers=paper_list, posts=post_list, year=str(datetime.datetime.now().year))
open('index.html', 'w').write(output)

