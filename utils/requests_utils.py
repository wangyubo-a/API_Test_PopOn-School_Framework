import requests
import time
from utils.config_utils import local_config
import json
import jsonpath
import re
from utils.check_utils import CheckUtils
from requests.exceptions import RequestException, ProxyError, ChunkedEncodingError
from nb_log import LogManager

logger = LogManager('PopOn-School_API_TEST').get_logger_and_add_handlers(is_add_stream_handler=True,
                                                                         log_filename=local_config.LOG_NAME)


class RequestsUtils:
    def __init__(self):
        self.hosts = local_config.HOSTS
        self.session = requests.session()
        self.tmp_variables = {}

    # 封装get方法
    def __get(self, requests_info):
        try:
            logger.info('%s 接口调用get请求 --开始执行' % requests_info['接口名称'])
            url = self.hosts + requests_info['请求地址']
            # 处理接口间的关联
            post_variable_list = re.findall('\\${\w+}', requests_info['请求参数(post)'])
            for variable in post_variable_list:
                logger.info('%s 接口开始将请求参数(post)里的变量替换成值--开始执行' % requests_info['接口名称'])
                requests_info['请求参数(post)'] = requests_info['请求参数(post)'].replace(variable,
                                                                                  '%s' % self.tmp_variables[
                                                                                      variable[2:-1]])
                logger.info('%s 接口开始将请求参数(post)里的变量替换成值--执行结束' % requests_info['接口名称'])
            headers_variable_list = re.findall('\\${\w+}', requests_info['请求头部信息'])
            for variable in headers_variable_list:
                # 将接口中的变量替换成值  replace为替换
                logger.info('%s 接口开始将头部信息里的变量替换成值--开始执行' % requests_info['接口名称'])
                requests_info['请求头部信息'] = requests_info['请求头部信息'].replace(variable,
                                                                          '%s' % self.tmp_variables[variable[2:-1]])
                logger.info('%s 接口开始将头部信息里的变量替换成值--执行结束' % requests_info['接口名称'])
            get_variable_list = re.findall('\\${\w+}', requests_info['请求参数(get)'])
            for variable in get_variable_list:
                logger.info('%s 接口开始将请求参数(get)里的变量替换成值--开始执行' % requests_info['接口名称'])
                requests_info['请求参数(get)'] = requests_info['请求参数(get)'].replace(variable,
                                                                                '%s' % self.tmp_variables[
                                                                                    variable[2:-1]])
                logger.info('%s 接口开始将请求参数(get)里的变量替换成值--执行结束' % requests_info['接口名称'])
            if requests_info['请求头部信息'] != '':
                if requests_info['请求参数(post)'] != '':
                    logger.info('%s 接口开始调用--带请求头--带post请求参数 ,(--get请求)' % requests_info['接口名称'])
                    response = self.session.get(url=url,
                                                headers=eval(requests_info['请求头部信息']),
                                                params=json.loads(requests_info['请求参数(get)']),
                                                data=json.loads(requests_info['请求参数(post)']))
                else:
                    logger.info('%s 接口开始调用--带请求头,(--get请求)' % requests_info['接口名称'])
                    response = self.session.get(url=url,
                                                headers=eval(requests_info['请求头部信息']),
                                                params=json.loads(requests_info['请求参数(get)']))
            elif requests_info['请求参数(post)'] != '':
                logger.info('%s 接口开始调用--带post请求参数 ,(--get请求)' % requests_info['接口名称'])
                response = self.session.get(url=url,
                                            params=json.loads(requests_info['请求参数(get)']),
                                            data=json.loads(requests_info['请求参数(post)']))
            else:
                logger.info('%s 接口开始调用 ,(--get请求)' % requests_info['接口名称'])
                response = self.session.get(url=url, params=json.loads(requests_info['请求参数(get)']))
            response.encoding = response.apparent_encoding  # 防止乱码
            for data in range(len(requests_info['取值方式'].split(','))):
                if requests_info['取值方式'].split(',')[data] == 'jsonpath取值':
                    logger.info('%s 接口开始使用jsonpath取值' % requests_info['接口名称'])
                    value = jsonpath.jsonpath(response.json(), requests_info['取值代码'].split(',')[data])[0]
                    self.tmp_variables[requests_info['取值变量'].split(',')[data]] = value
                    logger.info('%s 接口使用jsonpath取值完毕，值为：%s' % (requests_info['接口名称'], value))
                elif requests_info['取值方式'].split(',')[data] == '正则取值':
                    logger.info('%s 接口开始使用正则取值' % requests_info['接口名称'])
                    value = re.findall(requests_info['取值代码'].split(',')[data], response.text)[0]
                    self.tmp_variables[requests_info['取值变量'].split(',')[data]] = value
                    logger.info('%s 接口使用正则取值取值完毕，值为：%s' % (requests_info['接口名称'], value))
                elif requests_info['取值方式'].split(',')[data] == '响应头取值':
                    logger.info('%s 接口开始使用响应头取值' % requests_info['接口名称'])
                    value = response.headers[requests_info['取值代码'].split(',')[data]]
                    self.tmp_variables[requests_info['取值变量'].split(',')[data]] = value
                    logger.info('%s 接口使用响应头取值完毕，值为：%s' % (requests_info['接口名称'], value))
            result = CheckUtils(response).run_check(requests_info['断言类型'], requests_info['期望结果'])
        except ProxyError as e:
            result = {'code': 3, 'message': '调用接口 [%s] 时发生代理异常,异常原因：%s' % (requests_info['接口名称'], e.__str__()),
                      'check_result': False}
            logger.error('调用接口 [%s] 时发生代理异常,异常原因：%s' % (requests_info['接口名称'], e.__str__()))
        except ConnectionError as e:
            result = {'code': 3, 'message': '调用接口 [%s] 时发生链接异常，异常原因是：%s' % (requests_info['接口名称'], e.__str__()),
                      'check_result': False}
            logger.error('调用接口 [%s] 时发生链接异常，异常原因是：%s' % (requests_info['接口名称'], e.__str__()))
        except RequestException as e:
            result = {'code': 3, 'message': '调用接口 [%s] 时发生Request异常，异常原因是：%s' % (requests_info['接口名称'], e.__str__()),
                      'check_result': False}
            logger.error('调用接口 [%s] 时发生Request异常，异常原因是：%s' % (requests_info['接口名称'], e.__str__()))
        except Exception as e:
            result = {'code': 3, 'message': '调用接口 [%s] 时发生异常,异常原因：%s' % (requests_info['接口名称'], e.__str__()),
                      'check_result': False}
            logger.error('调用接口 [%s] 时发生异常,异常原因：%s' % (requests_info['接口名称'], e.__str__()))
        logger.info('%s 接口调用get请求 --执行结束' % requests_info['接口名称'])
        return result

    # 封装post方法
    def __post(self, requests_info):
        try:
            logger.info('%s 接口调用post请求 --开始执行' % requests_info['接口名称'])
            url = self.hosts + requests_info['请求地址']
            # 处理接口间的关联
            headers_variable_list = re.findall('\\${\w+}', requests_info['请求头部信息'])
            for variable in headers_variable_list:
                # 将头部信息里的变量替换成值
                logger.info('%s 接口开始将头部信息里的变量替换成值--开始执行' % requests_info['接口名称'])
                requests_info['请求头部信息'] = requests_info['请求头部信息'].replace(variable,
                                                                          '%s' % self.tmp_variables[variable[2:-1]])
                logger.error(requests_info['请求头部信息'])
                logger.info('%s 接口开始将头部信息里的变量替换成值--执行结束' % requests_info['接口名称'])
            get_variable_list = re.findall('\\${\w+}', requests_info['请求参数(get)'])
            for variable in get_variable_list:
                logger.info('%s 接口开始将请求参数(get)里的变量替换成值--开始执行' % requests_info['接口名称'])
                requests_info['请求参数(get)'] = requests_info['请求参数(get)'].replace(variable,
                                                                                '%s' % self.tmp_variables[
                                                                                    variable[2:-1]])
                logger.info('%s 接口开始将请求参数(get)里的变量替换成值--执行结束' % requests_info['接口名称'])
            post_variable_list = re.findall('\\${\w+}', requests_info['请求参数(post)'])
            for variable in post_variable_list:
                logger.info('%s 接口开始将请求参数(post)里的变量替换成值--开始执行' % requests_info['接口名称'])
                requests_info['请求参数(post)'] = requests_info['请求参数(post)'].replace(variable,
                                                                                  '%s' % self.tmp_variables[
                                                                                      variable[2:-1]])
                logger.error(requests_info['请求参数(post)'])
                logger.info('%s 接口开始将请求参数(post)里的变量替换成值--执行结束' % requests_info['接口名称'])
            if requests_info['请求头部信息'] != '':
                if requests_info['请求参数(get)'] != '':
                    if requests_info['请求参数(post)'] != '':
                        logger.info('%s 接口开始调用--带求头--带get请求参数--带post请求参数 ,(--post请求)' % requests_info['接口名称'])
                        response = self.session.post(url=url,
                                                     headers=eval(requests_info['请求头部信息']),
                                                     params=json.loads(requests_info['请求参数(get)']),
                                                     data=json.loads(requests_info['请求参数(post)']))
                    else:
                        logger.info('%s 接口开始调用--带求头--带get请求参数 ,(--post请求)' % requests_info['接口名称'])
                        response = self.session.post(url=url,
                                                     headers=eval(requests_info['请求头部信息']),
                                                     params=json.loads(requests_info['请求参数(get)']))
                else:
                    if requests_info['请求参数(post)'] != '':
                        logger.info('%s 接口开始调用--带请求头--带post请求参数,(--post请求)' % requests_info['接口名称'])
                        response = self.session.post(url=url,
                                                     headers=eval(requests_info['请求头部信息']),
                                                     data=json.loads(requests_info['请求参数(post)']))
                    else:
                        logger.info('%s 接口开始调用--带求头-- ,(--post请求)' % requests_info['接口名称'])
                        response = self.session.post(url=url,
                                                     headers=eval(requests_info['请求头部信息']))

            else:
                if requests_info['请求参数(get)'] != '':
                    if requests_info['请求参数(post)'] != '':
                        logger.info('%s 接口开始调用--带get请求参数--带post请求参数 ,(--post请求)' % requests_info['接口名称'])
                        response = self.session.post(url=url,
                                                     params=json.loads(requests_info['请求参数(get)']),
                                                     data=json.loads(requests_info['请求参数(post)']))
                    else:
                        logger.info('%s 接口开始调用--带get请求参数--,(--post请求)' % requests_info['接口名称'])
                        response = self.session.post(url=url,
                                                     params=json.loads(requests_info['请求参数(get)']))
                else:
                    if requests_info['请求参数(post)'] != '':
                        logger.info('%s 接口开始调用--带post请求参数,(--post请求)' % requests_info['接口名称'])
                        response = self.session.post(url=url,
                                                     data=json.loads(requests_info['请求参数(post)']))
                    else:
                        logger.info('%s 接口开始调用--无post请求参数 ,(--post请求)' % requests_info['接口名称'])
                        response = self.session.post(url=url)
            response.encoding = response.apparent_encoding
            logger.error(response.text)
            for data in range(len(requests_info['取值方式'].split(','))):
                if requests_info['取值方式'].split(',')[data] == 'jsonpath取值':
                    logger.info('%s 接口开始使用jsonpath取值' % requests_info['接口名称'])
                    value = jsonpath.jsonpath(response.json(), requests_info['取值代码'].split(',')[data])[0]
                    self.tmp_variables[requests_info['取值变量'].split(',')[data]] = value
                    logger.info('%s 接口使用jsonpath取值完毕，值为：%s' % (requests_info['接口名称'], value))
                elif requests_info['取值方式'].split(',')[data] == '正则取值':
                    logger.info('%s 接口开始使用正则取值' % requests_info['接口名称'])
                    value = re.findall(requests_info['取值代码'].split(',')[data], response.text)[0]
                    self.tmp_variables[requests_info['取值变量'].split(',')[data]] = value
                    logger.info('%s 接口使用正则取值完毕，值为：%s' % (requests_info['接口名称'], value))
                elif requests_info['取值方式'].split(',')[data] == '响应头取值':
                    logger.info('%s 接口开始使用响应头取值' % requests_info['接口名称'])
                    value = response.headers[requests_info['取值代码'].split(',')[data]]
                    self.tmp_variables[requests_info['取值变量'].split(',')[data]] = value
                    logger.info('%s 接口使用响应头取值完毕，值为：%s' % (requests_info['接口名称'], value))
                elif requests_info['取值方式'].split(',')[data] == 'sta_time':
                    logger.error(int(time.time())+int(requests_info['取值代码'].split(',')[data]))
                    logger.info('%s 接口开始使用sta_time取值' % requests_info['接口名称'])
                    value = (int(time.time()) + int(requests_info['取值代码'].split(',')[data])) * 1000
                    self.tmp_variables[requests_info['取值变量'].split(',')[data]] = value
                    logger.info('%s 接口sta_time取值完毕，值为：%s' % (requests_info['接口名称'], value))
            result = CheckUtils(response).run_check(requests_info['断言类型'], requests_info['期望结果'])
            print(result)
        except ProxyError as e:
            result = {'code': 3, 'message': '调用接口 [%s] 时发生代理异常,异常原因：%s' % (requests_info['接口名称'], e.__str__()),
                      'check_result': False}
            logger.error('调用接口 [%s] 时发生代理异常,异常原因：%s' % (requests_info['接口名称'], e.__str__()))
        except ConnectionError as e:
            result = {'code': 3, 'message': '调用接口 [%s] 时发生链接异常，异常原因是：%s' % (requests_info['接口名称'], e.__str__()),
                      'check_result': False}
            logger.error('调用接口 [%s] 时发生链接异常，异常原因是：%s' % (requests_info['接口名称'], e.__str__()))
        except RequestException as e:
            result = {'code': 3, 'message': '调用接口 [%s] 时发生Request异常，异常原因是：%s' % (requests_info['接口名称'], e.__str__()),
                      'check_result': False}
            logger.error('调用接口 [%s] 时发生Request异常，异常原因是：%s' % (requests_info['接口名称'], e.__str__()))
        except Exception as e:
            result = {'code': 3, 'message': '调用接口 [%s] 时发生异常,异常原因：%s' % (requests_info['接口名称'], e.__str__()),
                      'check_result': False, 'response_url': response.url}
            logger.error(result)
            logger.error('调用接口 [%s] 时发生异常,异常原因：%s' % (requests_info['接口名称'], e.__str__()))
        logger.info('%s 接口调用post请求 --执行结束' % requests_info['接口名称'])
        return result

    # 封装request方法，单接口可执行
    def request(self, step_info):
        request_type = step_info['请求方式']
        logger.info('%s 开始调用' % step_info['接口名称'])
        if request_type == "get":
            result = self.__get(step_info)
        elif request_type == "post":
            result = self.__post(step_info)
        else:
            result = {'code': 2, 'message': '请求方式不支持', 'check_result': False}
            logger.error('%s 调用时，%s' % (step_info['接口名称'], result['message']))
        logger.info('%s 调用结束' % step_info['接口名称'])
        return result

    # 封装多接口执行方法，一个用例多个接口执行
    def request_by_step(self, test_steps):
        for test_step in test_steps:
            result = self.request(test_step)
            if result['code'] != 0:
                break
        return result
