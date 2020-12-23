import re
import json
import jsonpath
import requests
fo

url = 'http://api1.gopopon.com/wordoor_uaas_api/v1/busins/login2b'
data_dict = {"acc": "a1@qq.com", "pwd": "123456.."}
response = requests.post(url=url, data=data_dict)
dict1 = {'测试用例编号': 'api_case_02', '测试用例名称': '机构列表接口测试', '用例执行': '否', '用例步骤': 'step_01', '接口名称': 'login2b',
         '请求方式': 'post', '请求头部信息': '', '请求地址': '/wordoor_uaas_api/v1/busins/login2b', '请求参数(get)': '',
         '请求参数(post)': '{"acc": a1@qq.com, "pwd": 123456..}', '取值方式': '无', '多变量取值方式': '响应头取值', '取值次数': '多变量',
         '取值代码': 'A-Token-Header,', '取值变量': 'token',
         '断言类型': 'json_key_value', '期望结果': '{"expires_in":7200}'}
a = dict1['取值变量'].split(',')
# print(a)
b = dict1['取值次数']
dict2 = {}

for c in range(len(dict2['取值变量'].split(','))):
    if dict1['多变量取值方式'].split(',')[c] == 'jsonpath取值':
        value = jsonpath.jsonpath(response.json(), dict1['取值代码'].split(',')[c])[0]
        dict2[a[c]] = value
    elif dict1['多变量取值方式'].split(',')[c] == '正则取值':
        value = re.findall(dict1['取值代码'].split(',')[c], response.text)[0]
        dict2[a[c]] = value
    elif dict1['多变量取值方式'].split(',')[c] == '响应头取值':
        value = response.headers[dict1['取值代码'].split(',')[c]]
        dict2[a[c]] = value
print(dict2)
