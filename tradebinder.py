from csv_parser import csv_convert
import pages
import os
import sys
import argparse
from argparse import RawTextHelpFormatter

filename = sort = foilsheet = ''

#command-line arguments handler
parser = argparse.ArgumentParser(description='Tradebinder - a small python programm to create a 4x3 sheets of card images to simplify trading.\nIt uses scryfall.com as an image source and deckbox.org as .csv source.\nWritten by Ivan Scherbakov\n\n', formatter_class=RawTextHelpFormatter)
parser.add_argument("-n", "--name", nargs=1, help="name of .csv file with extention", action='store', type=argparse.FileType('r'))
parser.add_argument("-s", "--sort", help="order cards as they listed in .csv", action='store_true')
parser.add_argument("-f", "--foil", help="use this if separated sheet for foil&promo is needed", action='store_true')
args = parser.parse_args()

sort = True
if (not filename):
    filename = input('Enter filename with extention: ')
if (os.path.isdir('images') == 0):
    os.mkdir('images')
csv_convert(filename, sort, foilsheet)
name = os.path.splitext(filename)[0]
pages.make_pages(name)
if foilsheet:
    pages.make_pages('{}_foil'.format(name))
print('Done!')