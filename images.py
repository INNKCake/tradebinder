import requests 
from PIL import Image
from io import BytesIO
import os
import re

def get_image(name, set, filename):
    try:       
        if (os.path.isfile(filename + '_img/' + name + '_' + set + '.jpg') == 0):
            api_url = "https://api.scryfall.com/cards/search?q=!"
            api_url+=('"' + name + '"' + 'set:' + set) 
            r = requests.get(url = api_url) 
            data = r.json()
            dta = data['data']
            for i in dta:
                    print('Downloading {} from set {}'.format(name, set))
                    img_data = requests.get(i['image_uris']['border_crop']).content
                    with open(filename + '_img/' + name + '_' + set + '.jpg', 'wb') as imghandler:
                        imghandler.write(img_data)
    except Exception as e:
        if data['object'] == 'error':
            print(name + ';'+ set + ' : ' + data['details'])
        if e.args[0] == 'image_uris':
            img_data = requests.get(i['card_faces'][0]['image_uris']['border_crop']).content
            with open(filename + '_img/' + name + '_' + set + '.jpg', 'wb') as imghandler:
                    imghandler.write(img_data)
            img_data = requests.get(i['card_faces'][1]['image_uris']['border_crop']).content
            with open(filename + '_img/' + name + '_back_' + set + '.jpg', 'wb') as imghandler:
                    imghandler.write(img_data)       
def write_page(img, page, name):
        page_name = '{}_{}.jpg'.format(name, page)
        img.save(page_name)
