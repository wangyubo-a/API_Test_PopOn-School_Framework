import time
import datetime
import xlrd3
import re

# work_book = xlrd3.open_workbook('test_data.xlsx')
# sheet = work_book.sheet_by_name('Sheet1')
#
# print(sheet.cell_value(1, 3))
# a = time.time()
# b = int(round((int(a) + int(sheet.cell_value(1, 3))) * 1000))
# print(a)
# print(b)
# str2 = 'ToB_CloudClass_V2_${id}'
# dict2 = {'n': 'xiaoming', 'id': 18}
# variables_list1 = re.findall('\\${\w+}', str2)
# print(variables_list1)
# for v in variables_list1:
#     str2 = str2.replace(v, '"%s"' % dict2[v[2:-1]])
# print(str2)
# print('ToB_CloudClass_V2_%s'% dict2['id'])

str2 = 'ToB_CloudClass_V2_${id}'
dict2 = {'n': 'xiaoming', 'id': 18}
variables_list1 = re.findall('\\${\w+}', str2)
print(variables_list1)
for v in variables_list1:
    str2 = str2.replace(v, '%s' % dict2[v[2:-1]])
print(str2)
