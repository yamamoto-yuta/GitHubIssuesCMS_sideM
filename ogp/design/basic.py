from PIL import Image

from ogp.utils import paste_icon_image, add_centered_text


class BasicDesign():
    def __init__(self, params):
        """ font """
        self.font_black_path = "fonts/NotoSansJP-Black.otf"
        self.font_medium_path = "fonts/NotoSansJP-Medium.otf"

        """ icon settings """
        self.icon_w = 150
        self.icon_h = 150
        self.icon_pos_h = 220

        """ title settings """
        self.side_padding = 550
        self.text_pos_h = 400
        self.title_font_size = 72

        """ author settings """
        self.author_pos_h = 620
        self.author_font_size = 42

        self.ogp_base_img_path = 'ogp/templates/basic.png'
        self.ogp_icon_img_path = params['ogp_icon_img_path']
        self.title_text = params['title_text']
        self.author_text = params['author_text']

    def create(self):
        base_img = Image.open(self.ogp_base_img_path).copy()
        icon_img = Image.open(self.ogp_icon_img_path).copy()

        img = paste_icon_image(base_img, icon_img, self.icon_w, self.icon_h, self.icon_pos_h)
        base_img = add_centered_text(base_img, self.title_text, self.font_black_path, self.title_font_size, (64, 64, 64), self.text_pos_h, self.side_padding)
        base_img = add_centered_text(base_img, self.author_text, self.font_medium_path, self.author_font_size, (120, 120, 120), self.author_pos_h, self.side_padding)
        return img

