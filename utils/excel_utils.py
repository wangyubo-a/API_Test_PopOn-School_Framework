import xlrd3
import os


class ExcelUtils:
    def __init__(self, excel_file_path, sheet_name):
        self.excel_file_path = excel_file_path
        self.sheet_name = sheet_name
        self.sheet = self.get_sheet()

    def get_sheet(self):
        """根据文件路径及文件名称获取表格对象"""
        work_book = xlrd3.open_workbook(self.excel_file_path)
        sheet = work_book.sheet_by_name(self.sheet_name)
        return sheet

    def get_row_count(self):
        """获取表格的行数"""
        row_count = self.sheet.nrows
        return row_count

    def get_column_count(self):
        """获取表格的列数"""
        column_count = self.sheet.ncols
        return column_count

    def get_merge_cell_value(self, row_index, col_index):
        """ 获取excel单元格的数据（包含合并单元格的数据）"""
        cell_value = None  # 防止空值报错
        if self.sheet.merged_cells:
            for (min_row, max_row, min_col, max_col) in self.sheet.merged_cells:
                if min_row <= row_index < max_row:
                    if min_col <= col_index < max_col:
                        cell_value = self.sheet.cell_value(min_row, min_col)
                        break
                    else:
                        cell_value = self.sheet.cell_value(row_index, col_index)  # 合并单元格的值等于合并第一个单元格的值
                else:
                    cell_value = self.sheet.cell_value(row_index, col_index)
        else:
            cell_value = self.sheet.cell_value(row_index, col_index)
        return cell_value

    def get_all_data(self):
        excel_lit = []
        row_head = self.sheet.row_values(0)
        for row_num in range(1, self.get_row_count()):
            row_dict = {}
            for col_num in range(self.get_column_count()):
                row_dict[row_head[col_num]] = self.get_merge_cell_value(row_num, col_num)
            excel_lit.append(row_dict)
        return excel_lit 


if __name__ == "__main__":
    excel_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'testcase_infos.xlsx')
    excelUtils = ExcelUtils(excel_file_path, 'Sheet1')
    # date = excelUtils.get_merge_cell_value(5,0)
    # print(date)
    for row_num in excelUtils.get_all_data():
        print(row_num)
