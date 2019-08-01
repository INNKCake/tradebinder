import requests 
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import os
import re
import shutil

def get_image(name, set, filename):
    try:       
        if (os.path.isfile('images/{}_{}.jpg'.format(name, set)) == 0):
            api_url = "https://api.scryfall.com/cards/search?q=!"
            if set == 'Promo':
                set = ''
            api_url+=('"{}"set:"{}"'.format(name, set)) 
            r = requests.get(url = api_url) 
            data = r.json()
            dta = data['data']
            for i in dta:
                    set = i['set_name']
                    print('Downloading {} from {}'.format(name, set))
                    img_data = requests.get(i['image_uris']['border_crop']).content
                    with open('images/{}_{}.jpg'.format(name, set), 'wb') as imghandler:
                        imghandler.write(img_data)
        else:
            print('Found {} from {}'.format(name, set))
        shutil.copy2('images/{}_{}.jpg'.format(name, set), '{}_img/{}_{}.jpg'.format(filename, name, set))
        return set

    except Exception as e:
        if data['object'] == 'error':
            print('{} from {} : {}'.format(name, set, data['details']))

        if e.args[0] == 'image_uris':
            img_data = requests.get(i['card_faces'][0]['image_uris']['border_crop']).content
            with open('images/{}_1_{}.jpg'.format(name, set), 'wb') as imghandler:
                    imghandler.write(img_data)
            shutil.copy2('images/{}_1_{}.jpg'.format(name, set), '{}_img/{}_1_{}.jpg'.format(filename, name, set))
            img_data = requests.get(i['card_faces'][1]['image_uris']['border_crop']).content
            with open('images/{}_2_{}.jpg'.format(name, set), 'wb') as imghandler:
                    imghandler.write(img_data)
            shutil.copy2('images/{}_2_{}.jpg'.format(name, set), '{}_img/{}_2_{}.jpg'.format(filename, name, set))
        return set

def edit_image(filename, name, set, lang, foil, quantity, promo):
    try:
        if (os.path.isfile('{}_img/{}_{}.jpg'.format(filename, name, set)) == 1):
            if foil == 'foil':
                foil_image('{}_img/{}_{}.jpg'.format(filename, name, set))
            write_text('{}_img/{}_{}.jpg'.format(filename, name, set), 'Количество: {}'.format(quantity), 40, 80)
            write_text('{}_img/{}_{}.jpg'.format(filename, name, set), lang, 40, 120)
            if promo:
                write_text('{}_img/{}_{}.jpg'.format(filename, name, set), 'Промо', 40, 160)
            os.rename('{}_img/{}_{}.jpg'.format(filename, name, set), '{}_img/{}{}{}{}{}.jpg'.format(filename, name, set, lang, promo, foil))
        elif (os.path.isfile('{}_img/{}_1_{}.jpg'.format(filename, name, set)) == 1):
            if foil == 'foil':
                foil_image('{}_img/{}_1_{}.jpg'.format(filename, name, set))
                foil_image('{}_img/{}_2_{}.jpg'.format(filename, name, set))
            write_text('{}_img/{}_1_{}.jpg'.format(filename, name, set), 'Количество: {}'.format(quantity), 40, 80)
            write_text('{}_img/{}_1_{}.jpg'.format(filename, name, set), lang, 40, 120)
            if promo:
                write_text('{}_img/{}_1_{}.jpg'.format(filename, name, set), 'Промо', 40, 160)
            os.rename('{}_img/{}_1_{}.jpg'.format(filename, name, set), '{}_img/{}1{}{}{}{}.jpg'.format(filename, name, set, lang, promo, foil)) 
            os.rename('{}_img/{}_2_{}.jpg'.format(filename, name, set), '{}_img/{}2{}{}{}{}.jpg'.format(filename, name, set, lang, promo, foil)) 
    except Exception as e:
            print(e)

def write_text(image, text, x, y):
    try:
        font = ImageFont.truetype('TTF/Akrobat-ExtraBold.ttf', 36)
        text_color = "white"
        shadow_color = "black"
        img = Image.open(image)
        draw = ImageDraw.Draw(img)
        # thick border
        draw.text((x-1, y-1), text, font=font, fill=shadow_color)
        draw.text((x+1, y-1), text, font=font, fill=shadow_color)
        draw.text((x-1, y+1), text, font=font, fill=shadow_color)
        draw.text((x+1, y+1), text, font=font, fill=shadow_color)
        # draw the text over it
        draw.text((x, y), text, font=font, fill=text_color)
        img.save(image)
    except Exception as e:
        print(e)

def foil_image(image):
    try:
        background = Image.open(image)
        foreground = Image.open('images/templates/foil.png')
        background.paste(foreground, (0, 0), foreground)
        background.save(image)
    except Exception as e:
        print(e)

def save_page(img, page, name):
    try:
        page_name = '{}_{}.jpg'.format(name, page)
        img.save(page_name)
    except Exception as e:
        print(e)
