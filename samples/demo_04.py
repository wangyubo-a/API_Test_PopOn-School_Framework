import time
import datetime
import xlrd3

work_book = xlrd3.open_workbook('test_data.xlsx')
sheet = work_book.sheet_by_name('Sheet1')

print(sheet.cell_value(1, 3))
a = time.time()
b = int(round((int(a) + int(sheet.cell_value(1, 3))) * 1000))
print(a)
print(b)
