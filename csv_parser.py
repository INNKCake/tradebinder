import csv
import os
import images
import pages

def csv_convert(filename):
    with open(filename, 'r') as file:
        data = csv.reader(file, delimiter=';')
        name = set = ''
        filename = os.path.splitext(filename)[0]
        if (os.path.isdir(filename + '_img') == 0):
            os.mkdir(filename + '_img') 
        for row in data:
            name = row[0]
            set = row[1]
            images.get_image(name, set, filename)
