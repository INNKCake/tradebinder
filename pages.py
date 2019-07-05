#inspired by Vitaliy Krutov
import os
from PIL import Image
import images

def make_pages(name):
    pages = round(len(os.listdir(name + '_img'))/12 + 0.5)
    for page in range(0, pages):
        base_x = 223
        base_y = 310
        binder_y = 3 * 500
        binder_x = round(4 * base_x * 500 / base_y)
        new_im = Image.new('RGB', (binder_x, binder_y))
        counter = 0
        try:
            for x_pos in range(0, binder_x, round(base_x * 500 / base_y)):
                f = os.listdir(name + '_img')
                index = 0
                for y_pos in range(0, binder_y, 500):
                    f_path = os.path.join(name + '_img', f[index])
                    im = Image.open(f_path)
                    width, height = im.size
                    new_im.paste(im.resize((round(width * 500 / height), 500), Image.ANTIALIAS), (x_pos, y_pos))
                    index += 1
                    counter += 1
                    if os.path.isfile(f_path):
                            os.unlink(f_path)
                    if counter == 12:
                        images.write_page(new_im, page, name)
                        break
                if counter == 12:
                    counter = 0
                    break
        except IndexError:
            images.write_page(new_im, page, name)
            break
    for page in range(0, pages):
        os.renames((name + '_' + str(page) + '.png'), (os.path.join(name + '_img', name + '_' + str(page) + '.png')))