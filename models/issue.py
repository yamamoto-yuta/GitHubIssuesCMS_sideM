""" The model of GitHub Actions' event data.

Todo:
    * implement setter
    * implement getter
"""
import json
from datetime import datetime, timedelta

import yaml

from const import ISSUE_PATH

def format_time(t):
    if t=="":
        return ""
    return (datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=9)).strftime('%Y年%m月%d日 %H時%M分')

def parse_markdown(text):
    lines = text.split('\n')
    frontmatter = []
    yaml_start_flag = False
    for i in range(0, len(lines)):
        line = lines[i].rstrip('\r\n')
        if line == "```yaml" or line=="```yml":
            yaml_start_flag = True
            continue
        if line == "```" and yaml_start_flag:
            frontmatter = "\n".join(frontmatter)
            markdown = "\n".join(lines[i+1:])
            return frontmatter, markdown
        if line != "" and not yaml_start_flag:
            break
        if yaml_start_flag:
            frontmatter += [line]
    return None, "\n".join(lines)

def load_frontmatter(frontmatter):
    return yaml.safe_load(frontmatter)

class Issue():
    """ The model of GitHub Actions' event data.

    Attributes:
        title (string): Title of the issue
        id (string): Issue id
        fm (Dict): Frontmatter of Issue
            "posted_at": string
        body (string): Issue content
        labels (list<dict>): Labels of the issue
            List:
                Dict:
                    "color": string,
                    "default": bool,
                    "description": string,
                    "id": int,
                    "name": string,
                    "node_id": string,
                    "url": string
        status (string): Status of the issue => open | closed
        closed_at (string): Datetime of the issue closed => "%Y年%m月%d日 %H時%M分"
        posted_at (None / string): Datetime of the article wanted to be posted => "%Y年%m月%d日 %H時%M分"
                                   If None: article will be posted at `closed_at`
                                   If string: article will be posted at `posted_at`
        ogp_img_theme (string): 'basic' | 'kill_la_kill'
    """
    def __init__(self):
        self.title = self._read_title()
        self.id = self._read_issue_id()
        self.fm, self.body = parse_markdown(self._read_body())
        if self.fm is not None:
            self.fm = load_frontmatter(self.fm)
        self.labels = self._read_labels()
        self.status = self._read_status()
        self.closed_at = self._read_closed_at()
        self.posted_at = self._frontmatter_posted_at()
        self.ogp_img_theme = self._frontmatter_ogp_img_theme()
        self.ogp_description = self._frontmatter_ogp_description()

    def _frontmatter_posted_at(self):
        def format_dt(posted_at):
            posted_at = ''.join(posted_at.split(' '))
            posted_at = ''.join(posted_at.split('　'))
            posted_at = datetime.strptime(posted_at, "%Y年%m月%d日%H時%M分") # posted_at format 'YYYY年MM月DD日 hh時mm分'
            posted_at = posted_at.strftime("%Y年%m月%d日 %H時%M分")
            return posted_at

    def _frontmatter_ogp_img_theme(self):
        if self.fm is not None:
            if "ogp_img_theme" in self.fm.keys() and not self.fm['ogp_img_theme'] is None:
                return self.fm["ogp_img_theme"]
        return None

    def _frontmatter_ogp_description(self):
        if self.fm is not None:
            if "ogp_description" in self.fm.keys() and not self.fm['ogp_description'] is None:
                return self.fm["ogp_description"]
        return None

    def get_posted_at(self):
        """ return post datetime

        Return:
            string: 'YYYY年MM月DD日 hh時mm分'
                    posted_at if posted_at is not None
                    closed_at if posted_at is None
        """
        if self.posted_at is None:
            return self.closed_at
        return self.posted_at

    def get_updated_at(self):
        """ return update datetime

        Return:
            string: 'YYYY年MM月DD日 hh時mm分'
                    closed_at if closed_at > posted_at or posted_at is None
                    None if closed_at <= posted_at and posted_at is not None
        """
        posted_at = self.posted_at
        closed_at = self.closed_at
        if posted_at is None:
            # 予約投稿ではない
            return closed_at
        posted_at_dt = datetime.strptime(posted_at, "%Y年%m月%d日 %H時%M分") 
        closed_at_dt = datetime.strptime(closed_at, "%Y年%m月%d日 %H時%M分") 
        if closed_at_dt > posted_at_dt:
            # 現在時刻が予約投稿時刻よりも遅い
            return closed_at
        else:
            # 予約投稿されるまえなのでupdateではない
            return None

    def _read_title(self):
        with open(f'{ISSUE_PATH}/title.txt', 'r') as f:
            data = f.read().split('\n')[0]
        return data

    def _read_issue_id(self):
        with open(f'{ISSUE_PATH}/issue_id.txt', 'r') as f:
            data = f.read().split('\n')[0]
        return data

    def _read_body(self):
        with open(f'{ISSUE_PATH}/body.txt', 'r') as f:
            data = f.read()
        return data

    def _read_labels(self):
        with open(f'{ISSUE_PATH}/labels.txt', 'r') as f:
            data = json.load(f)
        return data

    def _read_status(self):
        with open(f'{ISSUE_PATH}/status.txt', 'r') as f:
            data = f.read().split('\n')[0]
        return data

    def _read_closed_at(self):
        with open(f'{ISSUE_PATH}/closed_at.txt', 'r') as f:
            data = f.read().split('\n')[0]
        return format_time(data)

    def get_tag_labels(self):
        return [label for label in self.labels if label['name'].split('/')[0]=="tag"]

    def is_include(self, labels):
        for label in labels:
            if label in [l['name'] for l in self.labels]:
                return True
        return False

