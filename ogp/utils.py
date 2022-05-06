from PIL import Image, ImageDraw, ImageFilter, ImageFont

def paste_icon_image(base_img, icon_img, icon_w, icon_h, icon_pos_h):
    mask = Image.new("L", icon_img.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0,0, icon_img.size[0], icon_img.size[1]), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    icon_img.putalpha(mask)
    paste_img = Image.new("RGB", icon_img.size, (255,255,255))
    paste_img.paste(icon_img, mask=icon_img.convert("RGBA").split()[-1])
    
    w, h = icon_w, icon_h
    base_img.paste(paste_img.resize((w, h), resample=Image.BICUBIC), (int(base_img.size[0] / 2 - w/2), icon_pos_h))
    return base_img


def add_centered_text(base_img, text, font_path, font_size, font_color, height, side_padding, stroke_width=0):
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(base_img)
    
    # 文字がベース画像からはみ出ないように処理
    if draw.textsize(text, font=font)[0] > base_img.size[0] - side_padding:
        while draw.textsize(text + '…', font=font)[0] > base_img.size[0] - side_padding:
            text = text[:-1]
        text = text + '…'

    draw.text(((base_img.size[0] - draw.textsize(text, font=font)[0]) / 2, height), text, font_color, font=font, stroke_width = stroke_width)

    return base_img
