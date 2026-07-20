#!/usr/bin/env python3
"""Download a Google Scholar profile with Apify and render the website/CV.

Setup:
    # Python 3.11 or newer
    python -m pip install -r requirements.txt
    # Then paste your token into APIFY_TOKEN below.

Download metadata and render all outputs:
    python apify_scholar.py

Render again from the local JSON cache without calling Apify:
    python apify_scholar.py --render-only
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


ACTOR_ID = "johnvc/google-scholar-api"
APIFY_TOKEN = "apify_api_cGsOmyggmdqyjXczUxARF9esIUQwQe4hKVB7"
DEFAULT_AUTHOR_ID = "qHFA5z4AAAAJ"
ROOT = Path(__file__).resolve().parent
PUBLISHER_NETLOC = {
    "proceedings.iclr.cc",
    "proceedings.neurips.cc",
    "proceedings.mlr.press",
    "link.springer.com",
    "ems.press",
    "www.sciencedirect.com",
    "www.tandfonline.com",
    "crm-en.ics.org.ru",
}


def article_id(article: dict[str, Any]) -> str:
    """Return the citation ID without the optional author-ID prefix."""
    raw_value = article.get("citation_id")
    if raw_value is None:
        return ""
    value = str(raw_value)
    return value.rsplit(":", 1)[-1]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
        file.write("\n")


def run_actor(client: Any, run_input: dict[str, Any]) -> list[dict[str, Any]]:
    """Run the Actor once and return every item in its default dataset."""
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise RuntimeError(f"Apify Actor failed for input: {run_input}")

    dataset_id = getattr(run, "default_dataset_id", None)
    if dataset_id is None and isinstance(run, dict):
        dataset_id = run.get("defaultDatasetId")
    if not dataset_id:
        raise RuntimeError("Apify Actor run did not return a default dataset ID")

    items = list(client.dataset(dataset_id).iterate_items(clean=True))
    errors = [item for item in items if item.get("error")]
    if errors:
        message = errors[0].get("error_message", "Unknown Actor error")
        raise RuntimeError(f"Apify Actor error: {message}")
    return items


def unpack_articles(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Accept both the Actor's flat dataset and a nested articles response."""
    if len(items) == 1 and isinstance(items[0].get("articles"), list):
        return [dict(article) for article in items[0]["articles"]]
    return [dict(item) for item in items]


def download_profile(
    client: Any,
    author_id: str,
    cache_path: Path,
    *,
    max_pages: int,
    skip_details: bool,
    refresh_details: bool,
) -> dict[str, Any]:
    """Download the article list, enrich it, and checkpoint it as JSON."""
    cached_articles: list[dict[str, Any]] = []
    if cache_path.exists():
        cached_articles = load_json(cache_path).get("articles", [])
    cached_by_id = {
        article_id(article): article
        for article in cached_articles
        if article_id(article)
    }

    print("Downloading article list...")
    articles = unpack_articles(
        run_actor(
            client,
            {
                "mode": "author_articles",
                "author_id": author_id,
                "hl": "en",
                "sort": "pubdate",
                "num": 100,
                "max_pages": max_pages,
            },
        )
    )
    if not articles:
        raise RuntimeError(f"No articles returned for Google Scholar author {author_id}")

    # Detail calls are one Actor run per paper. Reuse cached details by default so
    # reruns only pay for newly added papers.
    for article in articles:
        cached = cached_by_id.get(article_id(article), {})
        if not refresh_details and isinstance(cached.get("citation"), dict):
            article["citation"] = cached["citation"]
        if not refresh_details and isinstance(cached.get("link_list"), list):
            article["link_list"] = cached["link_list"]

    profile: dict[str, Any] = {
        "actor": ACTOR_ID,
        "author_id": author_id,
        "downloaded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "articles": articles,
    }
    write_json(cache_path, profile)

    if skip_details:
        return profile

    missing = [article for article in articles if "citation" not in article]
    for index, article in enumerate(missing, start=1):
        title = article.get("paper_title") or article.get("title") or "Untitled paper"
        citation_id = article_id(article)
        if not citation_id:
            print(f"Skipping details without citation_id: {title}", file=sys.stderr)
            continue

        print(f"Downloading details {index}/{len(missing)}: {title}")
        details = run_actor(
            client,
            {
                "mode": "author_citation",
                "author_id": author_id,
                "citation_id": citation_id,
                "hl": "en",
            },
        )
        if not details:
            print(f"No details returned for: {title}", file=sys.stderr)
            continue
        article["citation"] = details[0]
        write_json(cache_path, profile)

    return profile


def first_string(mapping: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = mapping.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def clean_venue(publication: str, year: int) -> str:
    if not publication:
        return ""
    if year:
        publication = re.sub(rf",?\s*{year}\s*$", "", publication).strip(" ,")
    return publication


def candidate_urls(article: dict[str, Any], citation: dict[str, Any]) -> Iterable[tuple[str, bool]]:
    """Yield candidate URLs paired with whether Scholar labels them as a PDF."""
    for value in (citation.get("link"), article.get("link")):
        if isinstance(value, str) and value:
            yield value, value.lower().split("?", 1)[0].endswith(".pdf")

    for resource in citation.get("resources", []) or []:
        if not isinstance(resource, dict):
            continue
        url = resource.get("link")
        if isinstance(url, str) and url:
            is_pdf = str(resource.get("file_format", "")).upper() == "PDF"
            yield url, is_pdf

    for url in article.get("link_list", []) or []:
        if isinstance(url, str) and url:
            yield url, url.lower().split("?", 1)[0].endswith(".pdf")


def arxiv_links(url: str) -> tuple[str, str] | None:
    parsed = urlparse(url)
    if parsed.netloc.lower().removeprefix("www.") != "arxiv.org":
        return None
    match = re.match(r"/(?:abs|pdf)/([^/?#]+)", parsed.path)
    if not match:
        return None
    identifier = match.group(1).removesuffix(".pdf")
    return (
        f"https://arxiv.org/abs/{identifier}",
        f"https://arxiv.org/pdf/{identifier}",
    )


def latex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def latin_to_ascii(value: str) -> str:
    """Transliterate Latin accents while leaving other writing systems intact."""
    special = {
        "Æ": "AE",
        "Ð": "D",
        "Ø": "O",
        "Þ": "Th",
        "ß": "ss",
        "æ": "ae",
        "ð": "d",
        "ø": "o",
        "þ": "th",
        "Ł": "L",
        "ł": "l",
        "Œ": "OE",
        "œ": "oe",
    }
    result: list[str] = []
    for character in value:
        if character in special:
            result.append(special[character])
            continue
        normalized = unicodedata.normalize("NFKD", character)
        ascii_character = normalized.encode("ascii", "ignore").decode("ascii")
        result.append(ascii_character or character)
    return "".join(result)


@dataclass(frozen=True)
class Paper:
    title: str
    authors: str
    venue: str
    year: int
    kind: str
    link: str | None
    arxiv: str | None
    pdf: str | None

    @classmethod
    def from_article(cls, article: dict[str, Any]) -> "Paper":
        citation = article.get("citation")
        if not isinstance(citation, dict):
            citation = {}

        title = first_string(citation, "paper_title", "title") or first_string(
            article, "paper_title", "title"
        )
        authors = first_string(citation, "authors") or first_string(article, "authors")

        year_text = first_string(article, "year")
        if not year_text:
            year_text = first_string(citation, "publication_date", "year")
        year_match = re.search(r"(?:19|20)\d{2}", year_text)
        year = int(year_match.group()) if year_match else 0

        venue = ""
        kind = "publication"
        for field in ("journal", "conference", "book"):
            venue = first_string(citation, field)
            if venue:
                break
        if not venue:
            venue = first_string(citation, "institution")
            if venue:
                kind = "thesis"
        if not venue:
            venue = clean_venue(first_string(article, "publication"), year)

        if venue.lower().startswith("arxiv"):
            kind = "preprint"

        link: str | None = None
        arxiv: str | None = None
        pdf: str | None = None
        for url, labeled_pdf in candidate_urls(article, citation):
            arxiv_pair = arxiv_links(url)
            if arxiv_pair:
                arxiv, arxiv_pdf = arxiv_pair
                pdf = pdf or arxiv_pdf
                continue
            if labeled_pdf or url.lower().split("?", 1)[0].endswith(".pdf"):
                pdf = pdf or url
            if link is None and urlparse(url).netloc.lower() in PUBLISHER_NETLOC:
                link = url

        return cls(title, authors, venue, year, kind, link, arxiv, pdf)

    def to_html(self) -> str:
        title = html.escape(self.title)
        if self.link:
            title = f'<a href="{html.escape(self.link, quote=True)}">{title}</a>'
        result = f'<span class="span-paper-title">{title}</span>'
        result += (
            f"<span> ({html.escape(self.authors)}). "
            f"{html.escape(self.venue)}, {self.year or 'n.d.'}."
        )

        links: list[str] = []
        if self.kind != "preprint" and self.link:
            links.append(self._html_link("Link", self.link, "fa fa-solid fa-link"))
        if self.arxiv:
            links.append(self._html_link("arXiv", self.arxiv, "ai ai-arxiv"))
        if self.pdf:
            links.append(self._html_link("PDF", self.pdf, "fa fa-regular fa-file-pdf"))
        if links:
            result += "<br>" + " ".join(links)
        return result + "</span>"

    @staticmethod
    def _html_link(label: str, url: str, icon_class: str) -> str:
        return (
            '<div style="display:inline-block">'
            f'<a class="paper-link" href="{html.escape(url, quote=True)}">'
            f'{label}<i class="{icon_class}"></i></a></div>'
        )

    def to_latex(self) -> str:
        title = latex_escape(self.title)
        latex_link = self.link or self.arxiv
        if latex_link:
            title = rf"\href{{\detokenize{{{latex_link}}}}}{{{title}}}"
        return (
            rf"\textbf{{{title}}} ({latex_escape(latin_to_ascii(self.authors))}). "
            rf"\textit{{{latex_escape(self.venue)}}}, {self.year or 'n.d.'}."
        )


def split_by_year(papers: Iterable[Paper]) -> list[tuple[int | str, list[Paper]]]:
    ordered = sorted(
        papers,
        key=lambda paper: (-paper.year, paper.venue.casefold(), paper.title.casefold()),
    )
    return [
        (year if year else "n.d.", list(group))
        for year, group in groupby(ordered, key=lambda paper: paper.year)
    ]


def render_profile(
    profile: dict[str, Any],
    *,
    template_path: Path,
    html_path: Path,
    tex_path: Path,
    date_path: Path,
) -> tuple[int, int]:
    try:
        import jinja2
    except ImportError as error:
        raise RuntimeError("Jinja2 is missing; run: pip install -r requirements.txt") from error

    papers = [Paper.from_article(article) for article in profile.get("articles", [])]
    publications = [paper for paper in papers if paper.kind == "publication"]
    preprints = [paper for paper in papers if paper.kind == "preprint"]

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_path.parent)),
        keep_trailing_newline=True,
    )
    template = environment.get_template(template_path.name)
    rendered_html = template.render(
        publications=split_by_year(publications),
        preprints=split_by_year(preprints),
    )
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(rendered_html, encoding="utf-8")

    tex_path.parent.mkdir(parents=True, exist_ok=True)
    with tex_path.open("w", encoding="utf-8") as file:
        for heading, section in (("Publications", publications), ("Preprints", preprints)):
            file.write(rf"\section{{{heading}}}" + "\n")
            file.write("\\begin{enumerate}\n")
            for paper in sorted(
                section,
                key=lambda item: (-item.year, item.venue.casefold(), item.title.casefold()),
            ):
                file.write("\\item\n")
                file.write(paper.to_latex() + "\n")
            file.write("\\end{enumerate}\n")

    date_path.parent.mkdir(parents=True, exist_ok=True)
    date_path.write_text(
        "\\begin{center}\n"
        f"Last Updated on {dt.datetime.now().strftime('%B %d, %Y')}\n"
        "\\end{center}\n",
        encoding="utf-8",
    )
    return len(publications), len(preprints)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--author-id",
        default=os.environ.get("SCHOLAR_AUTHOR_ID", DEFAULT_AUTHOR_ID),
        help="Google Scholar author ID (default: %(default)s)",
    )
    parser.add_argument("--profile", type=Path, default=ROOT / "scholar_profile.json")
    parser.add_argument("--template", type=Path, default=ROOT / "template_index.html")
    parser.add_argument("--html", type=Path, default=ROOT / "index.html")
    parser.add_argument("--tex", type=Path, default=ROOT / "CV2" / "papers.tex")
    parser.add_argument("--date", type=Path, default=ROOT / "CV2" / "date.tex")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="maximum author-article pages; 0 means all pages (default: %(default)s)",
    )
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="render the existing JSON profile without calling Apify",
    )
    parser.add_argument(
        "--skip-details",
        action="store_true",
        help="skip per-paper detail calls (faster/cheaper, but produces fewer links)",
    )
    parser.add_argument(
        "--refresh-details",
        action="store_true",
        help="redownload details already present in the JSON cache",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.render_only:
            profile = load_json(args.profile)
        else:
            if not APIFY_TOKEN or APIFY_TOKEN == "YOUR_APIFY_TOKEN":
                raise RuntimeError("Paste your Apify API token into APIFY_TOKEN")
            try:
                from apify_client import ApifyClient
            except ImportError as error:
                raise RuntimeError(
                    "apify-client is missing; run: pip install -r requirements.txt"
                ) from error
            profile = download_profile(
                ApifyClient(APIFY_TOKEN),
                args.author_id,
                args.profile,
                max_pages=args.max_pages,
                skip_details=args.skip_details,
                refresh_details=args.refresh_details,
            )

        publications, preprints = render_profile(
            profile,
            template_path=args.template,
            html_path=args.html,
            tex_path=args.tex,
            date_path=args.date,
        )
        print(f"Rendered {publications} publications and {preprints} preprints")
        print(f"HTML: {args.html}")
        print(f"LaTeX: {args.tex}")
        return 0
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
