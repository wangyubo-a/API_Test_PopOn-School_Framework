# -*- coding:UTF-8 -*-
import os
import unittest
import paramunittest
import warnings
from utils.testcase_data_utils import TestCaseDataUtils
from utils.requests_utils import RequestsUtils
from utils.config_utils import local_config
from nb_log import LogManager

logger = LogManager('PopOn-School_API_TEST').get_logger_and_add_handlers(is_add_stream_handler=True,
                                                                         log_filename=local_config.LOG_NAME)

test_case_lists = TestCaseDataUtils().convert_testcase_data_to_list()


@paramunittest.parametrized(
    *test_case_lists
)
class TestApiCase(paramunittest.ParametrizedTestCase):
    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)

    def setParameters(self, case_id, case_step):
        self.case_ids = case_id
        self.case_steps = case_step

    def test_api_case(self):
        logger.info('测试用例编号：%s 开始执行' % self.case_steps[0].get('测试用例编号'))
        self._testMethodName = self.case_steps[0].get('测试用例编号')
        self._testMethodDoc = str(self.case_steps[0].get('测试用例名称'))
        test_result = RequestsUtils().request_by_step(self.case_steps)
        logger.info('测试用例编号：%s 执行结束' % self.case_steps[0].get('测试用例编号'))
        self.assertTrue(test_result['check_result'], test_result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
