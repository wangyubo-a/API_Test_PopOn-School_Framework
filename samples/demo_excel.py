import xlrd3
import xlwt

work_book = xlrd3.open_workbook('test_data.xlsx')
sheet = work_book.sheet_by_name('Sheet1')


# print(sheet.cell_value(0, 1))
# print(sheet.merged_cells)


# row_index = 1
# col_index = 3
# for min_row, max_row, min_col, max_col in sheet.merged_cells:
#     if min_row <= row_index < max_row:
#         if min_col <= col_index < max_col:
#             cell_value = sheet.cell_value(min_row, min_col)
#         else:
#             cell_value = sheet.cell_value(row_index, col_index)
#     else:
#         cell_value = sheet.cell_value(row_index, col_index)


def get_cell_merged_value(row_index, col_index):
    cell_value = None
    for min_row, max_row, min_col, max_col in sheet.merged_cells:
        if min_row <= row_index < max_row:
            if min_col <= col_index < max_col:
                cell_value = sheet.cell_value(min_row, min_col)
                break
            else:
                cell_value = sheet.cell_value(row_index, col_index)
        else:
            cell_value = sheet.cell_value(row_index, col_index)
    return cell_value


# for i in range(1, 9):
#     for j in range(0, 4):
#         cell_value = get_cell_merged_value(i, j)
#         print(cell_value, end=' ')
#     print( )
# 
# excel_list_data = []
# row_head = sheet.row_values(0)
# row_dict = {}
# row_dict[row_head[0]] = get_cell_merged_value(1,0)
# row_dict[row_head[1]] = get_cell_merged_value(1,1)
# row_dict[row_head[2]] = get_cell_merged_value(1,2)
# row_dict[row_head[3]] = get_cell_merged_value(1,3)
# print(row_dict)

excel_list_data = []
row_head = sheet.row_values(0)
# print(row_head)

for row_num in range(1, sheet.nrows):
    row_dict = {}
    for col_num in range(sheet.ncols):
        row_dict[row_head[col_num]] = get_cell_merged_value(row_num, col_num)
        # print(row_dict)
    excel_list_data.append(row_dict)
print(excel_list_data)
# for data in excel_list_data:
#     print(data)

data_dict = {}
for row_data in excel_list_data:
    data_dict.setdefault(row_data["事件"], []).append(row_data)
# print(data_dict)


a_dict = {'小红': [{'book1': '朝花夕拾'}, {'book2': '红楼梦'}],
          '小黑': [{'book1': '呐喊'}, {'book2': '红楼梦'}]}
data_list = []
for key,value in a_dict.items():
    b_dict = {}
    b_dict['name'] = key
    b_dict['books'] = value
    data_list.append(b_dict)
print(data_list)