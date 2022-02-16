from PIL import Image, ImageChops


def get_diff_position(before, after):
    before_img = Image.open(before)
    after_img = Image.open(after)
    before_img = before_img.convert('RGB')
    after_img = after_img.convert('RGB')
    diff = ImageChops.difference(before_img, after_img)
    diff_position = diff.getbbox()
    position_x = diff_position[0]
    return position_x