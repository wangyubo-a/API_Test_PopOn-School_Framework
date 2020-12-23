import unittest
import os
from utils import HTMLTestReportCN
from utils.config_utils import local_config
from nb_log import LogManager

logger = LogManager('PopOn-School_API_TEST').get_logger_and_add_handlers(is_add_stream_handler=True,
                                                                         log_filename=local_config.LOG_NAME)
case_path = os.path.join(os.path.dirname(__file__), '..', 'testcases')
result_path = os.path.join(os.path.dirname(__file__), '..', local_config.REPORT_PATH)


def load_testcase():
    logger.info('加载接口测试用例')
    discover = unittest.defaultTestLoader.discover(start_dir=case_path,
                                                   pattern='test_api_case.py',
                                                   top_level_dir=case_path)
    all_case_suite = unittest.TestSuite()
    all_case_suite.addTest(discover)
    return all_case_suite


result_dir = HTMLTestReportCN.ReportDirectory(result_path)
result_dir.create_dir('PopOn-School接口自动化测试报告_')
report_html_path = HTMLTestReportCN.GlobalMsg.get_value('report_path')
report_html_obj = open(report_html_path, 'wb')
runner = HTMLTestReportCN.HTMLTestRunner(stream=report_html_obj,
                                         title='PopOn-School接口自动化测试报告',
                                         description='数据驱动+关键字驱动测试',
                                         tester='王裕波')
logger.info('接口自动化测试开始执行')
runner.run(load_testcase())
report_html_obj.close()
