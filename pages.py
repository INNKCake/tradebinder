#inspired by Vitaliy Krutov
import os
from PIL import Image
import images
import shutil

def make_pages(name):
    if (os.path.isdir(name + '_img_backup') == 0):
            os.mkdir(name + '_img_backup') 
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
                        shutil.copy2(f_path, name + '_img_backup')
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
        os.renames((name + '_' + str(page) + '.jpg'), (os.path.join(name + '_img', name + '_' + str(page) + '.jpg')))
