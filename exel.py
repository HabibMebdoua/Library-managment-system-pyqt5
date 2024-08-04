from xlsxwriter import *

file = Workbook('test.xlsx')

print(help(file.formats[0]))