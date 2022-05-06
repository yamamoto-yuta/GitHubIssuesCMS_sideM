import os
import json

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

    def _load_yaml(self, yaml_string):
        parsed = ""
        for text in yaml_string.split('\n'):
            if text == "```" or text == "```yaml" or text == "```yml":
                continue
            parsed += f"{text}\n"
        return yaml.safe_load(parsed)

    def set_profile(self, yaml_string):
        self.profile = self._load_yaml(yaml_string)

    def save(self):
        if not os.path.exists(CONSTS_DIR):
            os.makedirs(CONSTS_DIR)
        with open(f'{CONSTS_DIR}/profile.json', 'w', encoding="utf-8") as f:
            json.dump(self.profile, f, indent=4, ensure_ascii=False)

