import os
import json
from urllib.parse import urlparse
import urllib.request
import hashlib

from py_ogp_parser.parser import request
from PIL import Image

from const import CONSTS_DIR, IMAGES_DIR, IMAGES_DIR_PRD, MAX_IMAGE_WIDTH

EXTERNAL_METADATA = f"{CONSTS_DIR}/external_metadata.json"

class Resource():
    def __init__(self, external_links, image_links, base_path=''):
        self.external_links = external_links
        self.image_links = image_links
        self.base_path = base_path

    @classmethod
    def load_resources(self):
        if not os.path.exists(EXTERNAL_METADATA):
            return Resource({}, {})
        with open(EXTERNAL_METADATA, "r") as f:
            resources = json.load(f)
        external_links = resources
        image_links = {}
        return Resource(external_links, image_links)

    def set_resources(self, external_links={}, image_links={}, base_path=''):
        for key in external_links.keys():
            self.external_links[key] = external_links[key]
        for key in image_links.keys():
            self.image_links[key] = image_links[key]
        if base_path != '':
            self.base_path = base_path

    def dl_resources(self):
        self._dl_external_links()
        self._dl_images()

    def _dl_images(self):
        for url in self.image_links.keys():
            self._dl_image(url)
            self._optimize_image(url)

    def _dl_image(self, url):
        extension = '.' + url.split('.')[-1]
        file_name = hashlib.md5(url.encode()).hexdigest() + extension
        dst_path = f'{IMAGES_DIR}/article/' + file_name
        dst_prd_path = f'{self.base_path}{IMAGES_DIR_PRD}/article/'+file_name
        try:
            dst_dir = '/'.join(dst_path.split('/')[:-1])
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
                local_file.write(web_file.read())
            self.image_links[url]['path'] = dst_path
            self.image_links[url]['prd_path'] = dst_prd_path
        except urllib.error.URLError as e:
            self.image_links[url]['path'] = None
            self.image_links[url]['prd_path'] = None

    def _optimize_image(self, url):
        if 'path' in self.image_links[url].keys():
            image_path = self.image_links[url]['path']
            image_prd_path = self.image_links[url]['prd_path']
            if image_path is not None:
                img = Image.open(image_path)
                w, h = img.width, img.height
                if w > MAX_IMAGE_WIDTH:
                    resize_ratio = w / MAX_IMAGE_WIDTH
                    resized_w = int(w / resize_ratio)
                    resized_h = int(h / resize_ratio)
                    img = img.resize((resized_w, resized_h))
                img.save(image_path+'.webp', 'webp')
                self.image_links[url]['path'] = image_path+'.webp'
                self.image_links[url]['prd_path'] = image_prd_path+'.webp'
                os.remove(image_path)

    def _dl_site_metadata(self, url):
        status_code, result = request(url)
        try:
            url_parsed = urlparse(url)
            metadata = {
                'url_domain': url_parsed.netloc,
                'url_domain_link': f"{url_parsed.scheme}://{url_parsed.netloc}"
                }
            if 'title' in result.keys():
                metadata['title'] = result['title']
            if 'ogp' in result.keys():
                ogp = result['ogp']
                if 'og:description' in ogp.keys():
                    metadata['description'] = ogp['og:description'][0]
                if 'og:image' in ogp.keys():
                    metadata['image_url'] = ogp['og:image'][0]
                    self.image_links[ogp['og:image'][0]] = {}
                #if 'og:site_name' in ogp.keys():
                #    metadata['site_name'] = ogp['og:site_name'][0]
            return metadata
        except:
            return None

    def _is_external_dl(self, url):
        if self.external_links[url] is None:
            return True
        if 'title' not in self.external_links[url].keys():
            return True
        if 'description' not in self.external_links[url].keys():
            return True
        if 'image_url' not in self.external_links[url].keys():
            return True
        if 'url_domain_link' not in self.external_links[url].keys():
            return True
        return False

    def _dl_external_links(self):
        for url in self.external_links.keys():
            if self._is_external_dl(url):
                self.external_links[url] = self._dl_site_metadata(url)

    def save(self):
        self._save_external_metadata()

    def _save_external_metadata(self):
        for url in self.external_links.keys():
            if 'image_url' in self.external_links[url].keys():
                image_url = self.external_links[url]['image_url']
                if image_url in self.image_links.keys():
                    if self.image_links[image_url]['prd_path'] is not None:
                        self.external_links[url]['image_url'] = self.image_links[image_url]['prd_path']
        if not os.path.exists(CONSTS_DIR):
            os.makedirs(CONSTS_DIR)
        with open(EXTERNAL_METADATA, 'w', encoding="utf-8") as f:
            json.dump(self.external_links, f, indent=4, ensure_ascii=False)


