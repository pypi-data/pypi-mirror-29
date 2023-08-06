from os.path import isfile, isdir, basename, join, dirname
from os import listdir, getcwd
import re
import logging
import xlsxwriter
from sys import stdout

def search_dir(dir):
    name = basename(dirname(dir))
    for item in listdir(dir):
        item = join(dir, item)
        if isdir(item):
            search_dir(item)
        elif isfile(item):
            if basename(item).rsplit('.', 1)[-1] == 'html':
                stdout.write("Searching", basename(item))
                translations.setdefault(name, {})
                process_file(item, name)
jh_regex = re.compile('jhiTranslate[\s]?=[\s]?["](.+?)["][\s]*')
translations = {}
def get_text(m, start, l, dir):
    for j, c in enumerate(l[start:]):
        if c == '<':
            translations[dir][m.group(1)] = l[start:j + start]
            break
def process_file(file, dir):
    lines = open(file).readlines()
    #lines = ['<span jhiTranslate= "Hello.title" >Texter {{id}} &qer;</span>',
    #         '<span jhiTranslate="Hello.titel"></span>']
    for l in lines:
        for m in jh_regex.finditer(l):
            if l[m.end()] == '>':
               get_text(m, m.end()+1, l, dir)
            else:
                for j, c in enumerate(l[m.end()+1]):
                    if c == '>':
                        get_text(m, j, l, dir)
                        break
    else:
        if translations[dir] == {}:
            translations.pop(dir)
def save():
    wb = xlsxwriter.Workbook(join(getcwd(), 'Translations.xlsx'))
    row = 2
    top_row_format = wb.add_format()
    top_row_format.set_bg_color('#c5efcd')
    top_row_format.set_bold()
    key_col_format = wb.add_format()
    key_col_format.set_bold()
    for k in translations.keys():
        sheet = wb.add_worksheet(k)
        for jsonKey, value in translations[k].items():
            sheet.write(row, 0, jsonKey)
            sheet.write(row, 1, value)
            row += 1
        sheet.write(0, 1, 'en')
        sheet.write(0, 0, k)
        sheet.set_column(firstcol=1, lastcol=1, width=80)
        sheet.set_column(firstcol=0, lastcol=0, width=60, cell_format=key_col_format)
        sheet.set_row(0, cell_format=top_row_format)
    try:
        wb.close()
    except PermissionError:
        raise PermissionError("ERROR: Close the excel file so that the program can change it!")

from sys import argv
def Extract(arguments=None):
    dir = False
    if arguments == None:
        try:
            dir = argv[1]
            if dir == 'input':
                dir = argv[2]
        except IndexError:
            print("ERROR: no start directory specified\n")
            print("You didn't specify the directory from which to begin looking for .html files!")
            print("Please run: ")
            print("jhlang extract -i <directory_path>")
        if dir == '-h':
            print("'jhlang extract -i <directory_path>' will look for .html files, and in those files it will look for 'jhiTranslate' attributes and store them in an excel file.")
    else:
        try:
            dir = arguments['input']
        except KeyError:
           print("ERROR: no start directory specified\n")
           print("You didn't specify the directory from which to begin looking for .html files!")
           print("To extract jhiTranslate tags run: ")
           print("jhlang extract -i <directory_path>")
    if dir:
        dir = dirname(dir)
        search_dir(dir)
        save()
if __name__ == '__main__':
    Extract()