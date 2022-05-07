import os
import re

import yaml

from const import MD_DIR

def parse_markdown(lines):
    frontmatter = []
    for i in range(1, len(lines)):
        line = lines[i].rstrip('\r\n')
        if line == "---":
            frontmatter = "\n".join(frontmatter)
            markdown = "\n".join(lines[i+1:])
            return frontmatter, markdown
        frontmatter += [line]
    return None, "\n".join(lines)

def load_frontmatter(frontmatter):
    return yaml.safe_load(frontmatter)


class Article():
    """ The model of GitHub Actions' event data.

    Attributes:
        slug (string): slug
        title (string): Title of the article
        markdown (string): The body content of the article
        tag_ids (list<string>): Tag ids of the article
        posted_at (string): Datetime of the article posted => %Y年%m月%d日 %H時%M分
        updated_at (string): Datetime of the article updated => %Y年%m月%d日 %H時%M分
        description (string): OGP description
    """
    def __init__(self, slug="", title="", markdown="", tag_ids=[], posted_at="", updated_at="", description=""):
        self.slug = slug
        self.title = title
        self.markdown = markdown
        self.tag_ids = tag_ids
        self.posted_at = posted_at
        self.updated_at = updated_at
        self.description = description
        assert self.slug != "" and type(self.slug) == str, f"slug is not valid, {self.slug}"
        assert self.title != "" and type(self.title) == str, f"title is not valid, {self.title}"
        assert self.markdown != "" and type(self.markdown) == str, f"markdown is not valid, {self.markdown}"
        assert self.posted_at != "" and type(self.posted_at) == str, f"posted_at is not valid, {self.posted_at}"

    @classmethod
    def from_article(cls, slug):
        if not os.path.exists(f"{MD_DIR}/{slug}"):
            return None
        with open(f"{MD_DIR}/{slug}/index.md", "r") as f:
            lines = f.readlines()
        fm, markdown = parse_markdown(lines)
        fm = load_frontmatter(fm)

        def fm_getter(key):
            if key in fm.keys():
                return fm[key]
            else:
                return None

        title = fm_getter("title")
        tag_ids = fm_getter("tag_ids")
        posted_at = fm_getter("posted_at")
        updated_at = fm_getter("updated_at")
        updated_at = fm_getter("description")
        return Article(slug=slug, title=title, markdown=markdown, tag_ids=tag_ids, posted_at=posted_at, updated_at=updated_at)

    def __str__(self):
        text =  ""
        text += f"{self.slug}\n"
        text += f"{self.title}\n"
        text += f"{self.markdown[:10]}\n"
        text += f"{self.tag_ids}\n"
        text += f"posted_at: {self.posted_at}\n"
        text += f"updated_at: {self.updated_at}\n"
        text += f"description: {self.description}\n"
        return text

    def set_values(self, slug=None, title=None, markdown=None, tag_ids=None, posted_at=None, updated_at=None, description=None):
        if slug is not None:
            self.slug = slug
        if title is not None:
            self.title = title
        if markdown is not None:
            self.markdown = markdown
        if tag_ids is not None:
            self.tag_ids = tag_ids
        if posted_at is not None:
            self.posted_at = posted_at
        if updated_at is not None:
            self.updated_at = updated_at
        if description is not None:
            self.description = description

    def _format_frontmatter(self):
        fm = {"slug": self.slug, "title": self.title, "tag_ids": self.tag_ids, "posted_at": self.posted_at, "updated_at": self.updated_at, "description": self.description}
        fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
        return fm

    def _format_markdown(self):
        return self.markdown

    def _format_output(self):
        fm = self._format_frontmatter()
        md = self._format_markdown()
        output = f"---\n{fm}\n---\n{md}"
        return output

    def _replace_issue_link(self, base_path):
        pattern1 = r'^\s*#(\d+)[^\S\n\r]*$'
        pattern2 = r'\[(.+)\]\(#(\d+)[^\S\n\r]*\)'
        ARTICLE_URL = 'https://shotarokataoka.github.io/article/'
        texts = []
        for text in self.markdown.split('\n'):
            text = re.sub(pattern1, r'<p slug=\1 basePath='+f'"{base_path}"></p>', text)
            texts += [re.sub(pattern2, r'[\1]('+f'{base_path}/article/'+r'\2)' ,text)]
        self.markdown = "\n".join(texts)

    def _parse_raw_url(self):
        pattern = r'^\s*https?:\/\/\S+[^\S\n\r]*$'
        urls = []
        for text in self.markdown.split('\n'):
            is_match = re.match(pattern, text) and 'https://shotarokataoka.github.io' not in text
            if is_match:
                urls += [text]
        self.urls = urls

    def _parse_image_url(self):
        pattern = r'^\s*!\[.+\]\((https?:\/\/\S+)\)$'
        images = []
        for text in self.markdown.split('\n'):
            if re.match(pattern, text):
                images += [re.sub(pattern, r'\1', text)]
        self.images = images

    def format_url(self, base_path):
        self._replace_issue_link(base_path)
        self._parse_raw_url()
        self._parse_image_url()

    def replace_images(self, image_links):
        pattern = r'^\s*!\[.+\]\((https?:\/\/\S+)\)$'
        texts = []
        for text in self.markdown.split('\n'):
            if re.match(pattern, text):
                url = re.sub(pattern, r'\1', text)
                image_path = image_links[url]['prd_path']
                if image_path is not None:
                    text = text.replace(url, f"{image_path}{url}")
            texts += [text]
        self.markdown = "\n".join(texts)

    def save(self):
        article_path = f"{MD_DIR}/{self.slug}"
        if not os.path.exists(article_path):
            os.makedirs(article_path)
        output = self._format_output()
        with open(f'{article_path}/index.md', 'w') as f:
            f.write(output)

