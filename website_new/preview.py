import sys
import livereload
import pathlib


from build import build


def preview(post_path: pathlib.Path):

    build(post_path)

    server = livereload.Server()

    server.watch(post_path, lambda: build(post_path))

    url = "http://localhost:8000/{}".format(
        post_path.parent / "{}.html".format(post_path.name)
    )
    print(url)
    # threading.Timer(1, lambda: webbrowser.open(url)).start()

    server.serve(port=8000)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python build.py <metadata>")

    preview(pathlib.Path(sys.argv[1]))
