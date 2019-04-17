import jinja2

class Link:
    def __init__(self, title, href):
        self.title = title
        self.href = href

class Paper:
    def __init__(self):
        self.title = 'Paper Ttitle'
        self.authors = 'a1, a2 and a3'
        self.links = [Link("arxiv", "https://arxiv.org/")]

class Post:
    def __init__(self):
        self.title = 'Post Title'
        self.date = 'dd.mm.yyyy'
        self.links = [Link("slides", "https://arxiv.org/")]

file_loader = jinja2.FileSystemLoader('')
env = jinja2.Environment(loader=file_loader)
template = env.get_template('template_index.html')

output = template.render(papers=[Paper()] * 10, posts=[Post()] * 10)
open('index.html', 'w').write(output)