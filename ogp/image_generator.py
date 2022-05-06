import os
import re

from ogp.design.basic import BasicDesign
from ogp.design.kill_la_kill import KillLaKillDesign
from ogp.design.image import ImageDesign

def create_ogp_image(theme, params, thumbnail_save_path):
    if theme=='kill_la_kill':
        design = KillLaKillDesign(params)
    if re.match(r"https?://[a-zA-Z\d!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", theme):
        params['url'] = theme
        design = ImageDesign(params)
    else:
        design = BasicDesign(params)
    
    img = design.create()

    """ OGP image """
    img = format_thumbnail(img)
    save_dir = "/".join(thumbnail_save_path.split('/')[:-1])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    img.save(thumbnail_save_path)


def format_thumbnail(img):
    img = _crop_img(img)
    img = _resize_img(img)
    return img

def _crop_img(img):
    """ 1.91:1になるようにクロップする """
    w, h = img.width, img.height
    crop_w = w
    crop_h = w / 1.92
    if h < crop_h:
        crop_w = h * 1.92
        crop_h = h
    return img.crop(((w - crop_w) // 2,
                     (h - crop_h) // 2,
                     (w + crop_w) // 2,
                     (h + crop_h) // 2))

def _resize_img(img):
    resize_w = 1200
    resize_h = 630
    w, h = img.width, img.height
    if resize_w > w or resize_h > h:
        resize_w = w
        resize_h = h
    img = img.resize((resize_w, resize_h))
    return img

