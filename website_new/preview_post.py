import sys
import livereload
import jinja2
import threading
import webbrowser
import markdown
import frontmatter
import dateparser
import pathlib


def build(post_path):
    post_path = pathlib.Path(post_path)

    file_loader = jinja2.FileSystemLoader("")
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template(str(post_path.parent / "template/template_post.html"))

    post = frontmatter.load(post_path / "index.md")

    macros = ""
    if "macros" in post.metadata:
        macros = (post_path / str(post["macros"])).read_text(encoding="utf-8")

    html = markdown.markdown(
        post.content,
        extensions=[
            "toc",
            "pymdownx.arithmatex",
        ],
        extension_configs={
            "toc": {"baselevel": 2},
            "pymdownx.arithmatex": {"generic": True},
        },
    )

    output = template.render(
        title=post["title"],
        date=dateparser.parse(str(post["date"])).strftime("%B %d, %Y"),
        html=html,
        macros=macros,
    )

    open(post_path / "index.html", "w").write(output)


def preview(post_path: str):
    build(post_path)

    # server = livereload.Server()

    # server.watch(post_path, lambda: build(post_path))

    # url = "http://localhost:8000/" + post_path
    # threading.Timer(1, lambda: webbrowser.open(url)).start()

    # server.serve(port=8000)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python build.py <metadata>")

    preview(sys.argv[1])
