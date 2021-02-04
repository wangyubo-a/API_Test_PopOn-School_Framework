# _*_coding : UTF-8 _*_
# 开发团队  : 测试
# 开发人员  : 王裕波
# 开发时间  : 2020/12/8 22:37
# 文件名称  : testcase_data_utils.py
# 开发工具  : PyCharm

import xlrd3
import os
from utils.excel_utils import ExcelUtils

excel_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'testcase_infos.xlsx')
excel_file_name = 'Sheet1'


class TestCaseDataUtils:
    def __init__(self):
        self.test_data_obj = ExcelUtils(excel_file_path=excel_file_path, sheet_name=excel_file_name)

    def convert_testcase_data_to_dict(self):
        """ 把excel的所有原始数据转换成符合框架需要的测试用例业务数据 """
        testcase_dict = {}
        for row_data in self.test_data_obj.get_all_data():
            if row_data['用例执行'] == '是':
                testcase_dict.setdefault(row_data['测试用例编号'], []).append(row_data)
        return testcase_dict

    def convert_testcase_data_to_list(self):
        """ 把convert_testcase_data_to_dict产生的数据转换成列表并在每个元素中增加key """
        all_casedata_list = []
        for key, value in self.convert_testcase_data_to_dict().items():
            case_info_dict = {}
            case_info_dict['case_id'] = key
            case_info_dict['case_step'] = value
            all_casedata_list.append(case_info_dict)
        return all_casedata_list


if __name__ == "__main__":
    testCaseDataUtils = TestCaseDataUtils()
    data_dict = testCaseDataUtils.convert_testcase_data_to_dict()
    data_list = testCaseDataUtils.convert_testcase_data_to_list()
    for list1 in data_list:
        print(list1)
