import jinja2
import markdown
import frontmatter
import dateparser
import pathlib


def build(post_path: pathlib.Path):

    file_loader = jinja2.FileSystemLoader("")
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template(str(post_path.parent / "template_post.html"))

    post = frontmatter.load(post_path / "index.md")

    macros = ""
    if "macros" in post.metadata:
        macros = (post_path / str(post["macros"])).read_text(encoding="utf-8")

    extensions = [
        "toc",
        "pymdownx.arithmatex",
        "admonition",
    ]

    extension_configs = {
        "toc": {"baselevel": 2},
        "pymdownx.arithmatex": {"generic": True},
    }

    if "bibliography" in post.metadata:
        extensions.append("la.cite")
        extension_configs["la.cite"] = {
            "file": str(post_path / str(post["bibliography"])),
            "style": "alpha",
            "hyperlinks": "both",
            "ignore_missing_file": False,
        }

    html = markdown.markdown(
        post.content,
        extensions=extensions,
        extension_configs=extension_configs,
    )

    output = template.render(
        title=post["title"],
        date=dateparser.parse(str(post["date"])).strftime("%B %d, %Y"),
        html=html,
        macros=macros,
    )

    open(post_path.parent / "{}.html".format(post_path.name), "w").write(output)
