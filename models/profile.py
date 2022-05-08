import os
import io
import json
from urllib.parse import urlparse
import urllib.request

import yaml
from PIL import Image

from const import CONSTS_DIR, PUBLIC_DIR, IMAGES_DIR

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
        self._sanitize_url()
        self._split_root_url()

    def _sanitize_url(self):
        self.profile['root_url'] = self._strip_last_slash(self.profile['root_url'])
        self.profile['issues_edit_page'] = self._strip_last_slash(self.profile['issues_edit_page'])

    def _strip_last_slash(self, url):
        if url[-1]=='/':
            url = url[:-1]
        return url

    def _split_root_url(self):
        root_url = self.profile['root_url']
        parsed = urlparse(root_url)
        self.profile['url_scheme'] = parsed.scheme
        self.profile['url_domain'] = parsed.netloc
        self.profile['url_subpath'] = parsed.path

    def _dl_img(self, url):
        try:
            with urllib.request.urlopen(url) as web_file:
                img = io.BytesIO(web_file.read())
                img = Image.open(img)
            return img
        except urllib.error.URLError as e:
            print(e)

    def _format_img(self, img):
        img = self._crop_img(img)
        img = self._resize_img(img)
        return img

    def _crop_img(self, img):
        """ 1:1になるようにクロップする """
        w, h = img.width, img.height
        crop_w = w
        crop_h = w
        if h < crop_h:
            crop_w = h
            crop_h = h
        return img.crop(((w - crop_w) // 2,
                         (h - crop_h) // 2,
                         (w + crop_w) // 2,
                         (h + crop_h) // 2))

    def _resize_img(self, img):
        resize_w = 64
        resize_h = 64
        w, h = img.width, img.height
        if resize_w > w or resize_h > h:
            resize_w = w
            resize_h = h
        img = img.resize((resize_w, resize_h))
        return img

    def save_img(self, img, save_dir, file_name, img_format, sizes=None):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if sizes is not None:
            img.save(f'{save_dir}/{file_name}.{img_format}', sizes=sizes)
        else:
            img.save(f'{save_dir}/{file_name}.{img_format}')

    def dl_img(self, url):
        img = self._dl_img(url)
        img = self._format_img(img)
        return img

    def save(self):
        if not os.path.exists(CONSTS_DIR):
            os.makedirs(CONSTS_DIR)
        with open(f'{CONSTS_DIR}/profile.json', 'w', encoding="utf-8") as f:
            json.dump(self.profile, f, indent=4, ensure_ascii=False)

        favicon_img = self.dl_img(self.profile['favicon_url'])
        self.save_img(favicon_img, PUBLIC_DIR+'/static', 'favicon', 'ico', sizes=[(16,16), (32, 32), (48, 48), (64,64)])
        avatar_img = self.dl_img(self.profile['avatar_url'])
        self.save_img(avatar_img, IMAGES_DIR+'/avatar', 'avatar', 'webp')

