from csv_parser import csv_convert
import pages
import os

filename = input('Enter filename with extention: ')
csv_convert(filename)
name = os.path.splitext(filename)[0]
pages.make_pages(name)
