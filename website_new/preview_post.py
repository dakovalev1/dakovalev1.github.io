import sys
import livereload
import jinja2
import threading
import webbrowser
import markdown
import frontmatter
import dateparser


def build(post_path: str):
    file_loader = jinja2.FileSystemLoader("")
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template("posts/template/template_post.html")

    post = frontmatter.load(post_path + "/index.md")

    # print(post.metadata)
    # print(post.content)
    html = markdown.markdown(
        post.content,
        extensions=["toc"],
        extension_configs={"toc": {"baselevel": 2}},
    )

    output = template.render(
        title=post.metadata["title"],
        date=dateparser.parse(str(post.metadata["date"])).strftime("%B %d, %Y"),
        html=html,
    )
    open(post_path + "/index.html", "w").write(output)


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
