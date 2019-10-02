import requests 
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import os
import re
import shutil

sryfallurl = "https://api.scryfall.com/cards/search?q=!"

def get_image(name, set, filename, sort, num, row_number):
    try:
        zero = ''
        num2 = num
        if(sort): 
            while row_number:
                row_number = row_number // 10
                if num2:
                    num2 = num2 // 10 
                    continue
                zero += '0'       
        if (os.path.isfile('images/{}_{}.jpg'.format(set, name)) == 0):           
            if set == 'Promo':
                set = ''
            api_url = ('{}"{}"set:"{}"'.format(sryfallurl, name, set)) 
            r = requests.get(url = api_url) 
            data = r.json()
            dta = data['data']
            for i in dta:
                    set = i['set_name'].replace(':', '')
                    print('Downloading {} from {}'.format(name, set))
                    img_data = requests.get(i['image_uris']['border_crop']).content
                    with open('images/{}_{}.jpg'.format(set, name), 'wb') as imghandler:
                        imghandler.write(img_data)
        else:
            print('Found {} from {}'.format(name, set))        
        sort_set = '{}{}{}'.format(zero, num, set)
        shutil.copy2('images/{}_{}.jpg'.format(set, name), '{}_img/{}_{}.jpg'.format(filename, sort_set, name))
        return sort_set

    except Exception as e:
        if data['object'] == 'error':
            print('{} from {} : {}'.format(name, set, data['details']))

        if e.args[0] == 'image_uris':
            img_data = requests.get(i['card_faces'][0]['image_uris']['border_crop']).content
            with open('images/{}_1_{}.jpg'.format(set, name), 'wb') as imghandler:
                    imghandler.write(img_data)
            shutil.copy2('images/{}_1_{}.jpg'.format(set, name), '{}_img/{}_1_{}.jpg'.format(filename, set, name))
            img_data = requests.get(i['card_faces'][1]['image_uris']['border_crop']).content
            with open('images/{}_2_{}.jpg'.format(set, name), 'wb') as imghandler:
                    imghandler.write(img_data)
            shutil.copy2('images/{}_2_{}.jpg'.format(set, name), '{}_img/{}_2_{}.jpg'.format(filename, set, name))
        return set

def edit_image(filename, set, name, lang, foil, quantity, promo, foilsheet):
    try:
        if (os.path.isfile('{}_img/{}_{}.jpg'.format(filename, set, name)) == 1):
            if foil == 'foil':
                foil_image('{}_img/{}_{}.jpg'.format(filename, set, name))
            write_text('{}_img/{}_{}.jpg'.format(filename, set, name), 'Количество: {}'.format(quantity), 40, 80)
            write_text('{}_img/{}_{}.jpg'.format(filename, set, name), lang, 40, 120)
            if promo:
                write_text('{}_img/{}_{}.jpg'.format(filename, set, name), 'Промо', 40, 160)
            os.rename('{}_img/{}_{}.jpg'.format(filename, set, name), '{}_img/{}{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil))
            if foilsheet and (foil == 'foil'):
                shutil.copy2('{}_img/{}{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil), '{}_foil_img/{}{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil))
                if os.path.isfile('{}_img/{}{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil)):
                    os.unlink('{}_img/{}{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil))
        elif (os.path.isfile('{}_img/{}_1_{}.jpg'.format(filename, set, name)) == 1):
            if foil == 'foil':
                foil_image('{}_img/{}_1_{}.jpg'.format(filename, set, name))
                foil_image('{}_img/{}_2_{}.jpg'.format(filename, set, name))
            write_text('{}_img/{}_1_{}.jpg'.format(filename, set, name), 'Количество: {}'.format(quantity), 40, 80)
            write_text('{}_img/{}_1_{}.jpg'.format(filename, set, name), lang, 40, 120)
            if promo:
                write_text('{}_img/{}_1_{}.jpg'.format(filename, set, name), 'Промо', 40, 160)
            os.rename('{}_img/{}_1_{}.jpg'.format(filename, set, name), '{}_img/{}1{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil)) 
            os.rename('{}_img/{}_2_{}.jpg'.format(filename, set, name), '{}_img/{}2{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil))
            if foilsheet and foil == 'foil':
                shutil.copy2('{}_img/{}1{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil), '{}_foil_img/{}1{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil))
                shutil.copy2('{}_img/{}2{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil), '{}_foil_img/{}2{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil))
                if os.path.isfile('{}_img/{}1{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil)):
                    os.unlink('{}_img/{}1{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil))
                if os.path.isfile('{}_img/{}2{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil)):
                    os.unlink('{}_img/{}2{}{}{}{}.jpg'.format(filename, set, name, lang, promo, foil))  
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
        img.save('{}_{}.jpg'.format(name, page))
    except Exception as e:
        print(e)
