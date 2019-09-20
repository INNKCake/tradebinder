from csv_parser import csv_convert
import pages
import os
import sys, getopt

filename = sort = foilsheet = ''
help = 'Tradebinder - a small python programm to create a 4x3 sheets of card images to simplify trading.\nIt uses scryfall.com as an image source and deckbox.org as .csv source.\nWritten by Ivan Scherbakov\n\nUsage:\n\n-n, --name : name of .csv file with extention\n-s, --sort : order cards as they listed in .csv\n-f, --foil : use this if separated sheet for foil&promo is needed\n-h, --help : print this help\n'
#command-line arguments handler
argumentList = sys.argv[1:]
unixOptions = 'hsfn:'
gnuOptions = ['help', 'sort', 'foil', 'name=']
try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    sys.exit(2)
for currentArgument, currentValue in arguments:
    if currentArgument in ("-n", "--name"):
        filename = currentValue
    elif currentArgument in ("-h", "--help"):
        print (help)
        sys.exit(0)
    elif currentArgument in ("-f", "--foil"):
        foilsheet = 1
    elif currentArgument in ("-s", "--sort"):
        sort = 1

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