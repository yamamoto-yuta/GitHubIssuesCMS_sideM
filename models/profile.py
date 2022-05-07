import os
import json
from urllib.parse import urlparse

import yaml

from const import CONSTS_DIR 

class Profile():
    """ Profile dict of used in blog.

    Attributes:
        profile (Dict): Profile dictionary
            Dict:
                "blog_title": string
                "author_name": string
                "author_description": string
                "copylight_name": string
                "copylight_url": string
                "root_url": string
                "sns": List of Dict
                    List:
                        Dict:
                            "name": string (e.g. "GitHub"), 
                            "url": string
    """
    def __init__(self, profile={}):
        self.profile = profile

    @classmethod
    def load_profile(cls):
        if not os.path.exists(f"{CONSTS_DIR}/profile.json"):
            return None
        with open(f"{CONSTS_DIR}/profile.json", "r") as f:
            profile = json.load(f)
        return Profile(profile)

    def __getitem__(self, key):
        return self.profile[key]

    def keys(self):
        return self.profile.keys()

    def set_profile(self, yaml_dict):
        self.profile = yaml_dict
        self._sanitize_root_url()
        self._split_root_url()

    def _sanitize_root_url():
        url = self.profile['root_url']
        if url[-1]!='/':
            url += '/'
        self.profile['root_url'] = url

    def _split_root_url(self):
        root_url = self.profile['root_url']
        parsed = urlparse(root_url)
        self.profile['url_scheme'] = parsed.scheme
        self.profile['url_domain'] = parsed.netloc
        self.profile['url_subpath'] = parsed.path

    def save(self):
        if not os.path.exists(CONSTS_DIR):
            os.makedirs(CONSTS_DIR)
        with open(f'{CONSTS_DIR}/profile.json', 'w', encoding="utf-8") as f:
            json.dump(self.profile, f, indent=4, ensure_ascii=False)

