from csv_parser import csv_convert
import pages
import os

filename = input('Enter filename with extention: ')
csv_convert(filename)
name = os.path.splitext(filename)[0]
z = input('Make pages(y/n)?\n')
if z.lower() == 'y':
    pages.make_pages(name)
