import csv
import os
import images
import pages

def csv_convert(filename):
    if (os.path.isdir('{}_img'.format(os.path.splitext(filename)[0])) == 0):
        os.mkdir('{}_img'.format(os.path.splitext(filename)[0])) 
    with open(filename, 'r') as file:
        data = csv.reader(file, delimiter=',')
        next(data)
        filename = os.path.splitext(filename)[0]
        for row in data:
            if row:
                try:
                    name = set = lang = quantity = foil = promo = ''
                    quantity = row[1]
                    name = row[2]
                    set = row[3]
                    lang = row[6]
                    foil = row[7]
                except Exception as e:
                    print('Row parsing error: {}'.format(e))
                    pass
                if (set == "Friday Night Magic") or (set == "Launch Parties") or (set == "Standard Showdown Promos"):
                    set = 'Promo'
                    promo = 1
                if set.startswith('Prerelease Events'):
                    set = set.replace('Prerelease Events: ', '')
                    set = '{} Promos'.format(set)
                name = name.replace('//', '-') 
                set = images.get_image(name, set, filename)
                images.edit_image(filename, name, set, lang, foil, quantity, promo)
