from PIL import Image
from kanjize import int2kanji

from ogp.utils import paste_icon_image, add_centered_text


class KillLaKillDesign():
    def __init__(self, params):
        """ font """
        self.font_path = "fonts/GN-KillGothic-U-KanaNA.ttf"
        self.font_color = (233, 3, 5)

        """ image """
        self.ogp_base_img_path = 'ogp/templates/white.png'
        self.base_img = Image.open(self.ogp_base_img_path).copy()
        self.base_img_size = self.base_img.size

        """ common settings """
        self.side_padding = 0

        """ slug settings """
        slug = int2kanji(int(params['slug']))
        self.slug_text = f'第{slug}稿'
        self.slug_font_size = 200

        """ title settings """
        title = params['title_text']
        self.title_text = [t for t in (title[0:7], title[7:14], title[14:]) if t!='']
        self.title_row_number = len(self.title_text)
        if self.title_row_number == 1:
            self.slug_pos_h = 50
            self.margin = 150
        if self.title_row_number == 2:
            self.slug_pos_h = 50
            self.margin = 50
        if self.title_row_number == 3:
            self.slug_pos_h = 10
            self.margin = -5

        self.text_pos_h = self.slug_pos_h + self.slug_font_size + self.margin
        self.title_font_size = self._decide_font_size(self.title_text[0])

    def create(self):
        base_img = self.base_img
        img = self.base_img
        """ slug """
        base_img = add_centered_text(base_img, self.slug_text, self.font_path, self.slug_font_size, self.font_color, self.slug_pos_h, self.side_padding)

        """ title """
        for title in self.title_text:
            if title == '':
                break
            base_img = add_centered_text(base_img, title, self.font_path, self.title_font_size, self.font_color, self.text_pos_h, self.side_padding)
            self.text_pos_h += self.title_font_size + self.margin
        return img

    def _decide_font_size(self, text):
        image_width = self.base_img_size[0]
        font_width = image_width // len(text)
        if font_width>405:
            font_width = 405
        return font_width

