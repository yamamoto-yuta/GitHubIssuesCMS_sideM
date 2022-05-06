import os
import json

from const import CONSTS_DIR 


class Tags():
    """ Tags dict of used in articles.

    Attributes:
        tags (Dict): Tags dictionary
            Dict:
                "tag_id": string
                    "name": string
                    "color": string
                    "description": string,
    """
    def __init__(self, tags={}):
        self.tags = tags

    @classmethod
    def load_tags(cls):
        if not os.path.exists(f"{CONSTS_DIR}/tags.json"):
            return None
        with open(f"{CONSTS_DIR}/tags.json", "r") as f:
            tags = json.load(f)
        return Tags(tags)

    def __getitem__(self, key):
        return self.tags[key]

    def keys(self):
        return self.tags.keys()
    
    def set_tag(self, tag_id, name, color, description):
        self.tags[tag_id] = {"name": name, "color": color, "description": description}

    def save(self):
        if not os.path.exists(CONSTS_DIR):
            os.makedirs(CONSTS_DIR)
        with open(f'{CONSTS_DIR}/tags.json', 'w', encoding="utf-8") as f:
            json.dump(self.tags, f, indent=4, ensure_ascii=False)
