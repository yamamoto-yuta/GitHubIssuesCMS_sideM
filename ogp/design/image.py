import io
from PIL import Image
import urllib.request

class ImageDesign():
    def __init__(self, params):
        self.url = params['url']

    def create(self):
        return self._dl_image()

    def _dl_image(self):
        try:
            with urllib.request.urlopen(self.url) as web_file:
                img = io.BytesIO(web_file.read())
                img = Image.open(img)
            return img
        except urllib.error.URLError as e:
            print(e)

