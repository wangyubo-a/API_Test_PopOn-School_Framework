import json
import jsonpath
import ast
import re
from utils.requests_utils import RequestsUtils

#
# str1 = '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}'
# step_list = [{'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '是', '用例步骤': 'step_01', '接口名称': '获取access_token接口',
#               '请求方式': 'get', '请求头部信息': '', '请求地址': '/cgi-bin/token',
#               '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}',
#               '请求参数(post)': '', '取值方式': 'jsonpath取值', '取值代码': '$.access_token', '取值变量': 'token'},
#              {'测试用例编号': 'api_case_02', '测试用例名称': '创建标签接口测试', '用例执行': '是', '用例步骤': 'step_02', '接口名称': '创建标签接口',
#               '请求方式': 'post', '请求头部信息': '', '请求地址': '/cgi-bin/tags/create',
#               '请求参数(get)': '{"access_token":"40_CeejgCpZfvXfhAL1u01zvH8wDNeQSPliNhdpwbrmK91jyU5rZzWJ4IPOMFB2y6yBqQNmkkpFHuMenEf5WN-dnQUdsUlR3LcnrJA9q7K7pfzEhsZVAf3WRPl5thLSGKgiY-X-vBASzm76MmwtDWDcABAYRY"}',
#               '请求参数(post)': '{   "tag" : {     "name" : "p3p4hehehe123" } } ', '取值方式': '无', '取值代码': '', '取值变量': ''}]
#
# str2 = json.loads(str1)
# dict1 = ast.literal_eval(str1)
# print(type(dict1))
# print(str2)
# rquestsUtils = RequestsUtils()
# rquestsUtils.request_by_step(step_list)

# str1 = '{"access_token":${token}}'
# variables_list = re.findall('\${\w+}', str1)
# print(variables_list)
#
#
# str1 = '123'
# str1.replace()

# list7 = [
#     {'测试用例编号': 'api_case_11', '测试用例名称': '创建课堂接口测试', '用例执行': '是', '用例步骤': 'step_01', '接口名称': 'login2b', '请求方式': 'post',
#      '请求头部信息': '', '请求地址': '/wordoor_uaas_api/v1/busins/login2b', '请求参数(get)': '',
#      '请求参数(post)': '{"acc": "a1@qq.com", "pwd": "123456.."}', '取值方式': 'jsonpath取值,响应头取值',
#      '取值代码': '$.result.userExchange.config.id,A-Token-Header', '取值变量': 'userid,token', '断言类型': 'header_key',
#      '期望结果': 'A-Token-Header'},
#     {'测试用例编号': 'api_case_11', '测试用例名称': '创建课堂接口测试', '用例执行': '是', '用例步骤': 'step_02', '接口名称': '机构列表接口', '请求方式': 'post',
#      '请求头部信息': '{"A-Token-Header": ${token}}', '请求地址': '/wordoor_uaas_api/v1/busins/userOrgList', '请求参数(get)': '',
#      '请求参数(post)': '{"identity": "Tutor", "targetUserId": ${userid}}', '取值方式': 'jsonpath取值', '取值代码': '$.result[0].id',
#      '取值变量': 'departmentId', '断言类型': 'code_check', '期望结果': 200.0},
#     {'测试用例编号': 'api_case_11', '测试用例名称': '创建课堂接口测试', '用例执行': '是', '用例步骤': 'step_03', '接口名称': '机构班级列表接口', '请求方式': 'post',
#      '请求头部信息': '{"A-Token-Header": ${token}}', '请求地址': '/wordoor_uaas_api/v1/businsOrg/orgCLass', '请求参数(get)': '',
#      '请求参数(post)': '{"departmentId":${departmentId},"userId":${userid}}', '取值方式': 'jsonpath取值,sta_time',
#      '取值代码': '$.result[0].id,100', '取值变量': 'classid,data_time', '断言类型': 'code_check', '期望结果': 200.0},
#     {'测试用例编号': 'api_case_11', '测试用例名称': '创建课堂接口测试', '用例执行': '是', '用例步骤': 'step_04', '接口名称': '创建课堂接口', '请求方式': 'post',
#      '请求头部信息': '{"A-Token-Header": ${token}}', '请求地址': '/wordoor_uaas_api/v1/busins/cloudClass/create', '请求参数(get)': '',
#      '请求参数(post)': '{"broadPeriod": 2,"classType": 2,"cover": "https://image1.gopopon.com/20201126161620cef6f25be85b98f8a3f1f31a7033bfe048991517","creatorOrgId": ${departmentId},"description": "日常接口测试","name": "API_TEST_日常接口测试_${data_time}","participateMajor": ${classid},"userId": ${userid}}',
#      '取值方式': '', '取值代码': '', '取值变量': '', '断言类型': 'code_check', '期望结果': 200.0}]
list8 = [{'测试用例编号': 'api_case_21', '测试用例名称': '部落帖子列表', '用例执行': '是', '用例步骤': 'step_01', '接口名称': 'create', '请求方式': 'post', '请求头部信息': '', '请求地址': '/wordoor_uaas_api/v1/sessions/create', '请求参数(get)': '', '请求参数(post)': '{"acc": "fl88@sina.com", "pwd": "123456q-"}', '取值方式': 'jsonpath取值,响应头取值', '取值代码': '$.result.config.id,A-Token-Header', '取值变量': 'userid,token', '断言类型': 'json_key', '期望结果': 'result'}, {'测试用例编号': 'api_case_21', '测试用例名称': '部落帖子列表', '用例执行': '是', '用例步骤': 'step_02', '接口名称': 'user/detail', '请求方式': 'post', '请求头部信息': '{"A-Token-Header": "${token}"}', '请求地址': '/wordoor_clan2c_api/v1/user/detail', '请求参数(get)': '', '请求参数(post)': '{"targetUserId": " ${userid}", "userId": " ${userid}"}', '取值方式': 'jsonpath取值,响应头取值', '取值代码': '$.result.tribes.[0].id', '取值变量': 'tribeid', '断言类型': 'code_check', '期望结果': 200.0}, {'测试用例编号': 'api_case_21', '测试用例名称': '部落帖子列表', '用例执行': '是', '用例步骤': 'step_03', '接口名称': 'post/page', '请求方式': 'post', '请求头部信息': '{"A-Token-Header": "${token}"}', '请求地址': '/wordoor_clan2c_api/v1/tribe/post/page', '请求参数(get)': '', '请求参数(post)': '{"userId": " ${userid}","pn":"1","ps":"50","tribeId":"${tribeid}"}', '取值方式': '', '取值代码': '', '取值变量': '', '断言类型': 'code_check', '期望结果': 200.0}]

rquestsUtils = RequestsUtils()
rquestsUtils.request_by_step(list8)
