import requests 
from PIL import Image
from io import BytesIO
import os

def get_image(name, set, filename):
    api_url = "https://api.scryfall.com/cards/search?q="
    api_url+=("'" + name + "'+set:" + set) 
    r = requests.get(url = api_url) 
    data = r.json()
    dta = data['data']
    for i in dta:
        img_data = requests.get(i['image_uris']['border_crop']).content
        with open(filename + '_img/' + name + '_' + set + '.jpg', 'wb') as imghandler:
            imghandler.write(img_data)

def write_page(img, page, name):
        page_name = '{}_{}.png'.format(name, page)
        img.save(page_name)