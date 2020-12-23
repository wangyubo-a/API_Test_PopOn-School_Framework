import requests

session = requests.session()
hosts = 'http://api1.gopopon.com'
da = {"identity": "Tutor", "targetUserId": 841}
login_data_dict = {"acc": "a1@qq.com", "pwd": "123456.."}
headers = {"A-Token-Header": "NCpCWVdSVERFFk0OWQNXcB8="}

data_dict = {"title": "11212", "departmentId": 917, "userId": 841}
# books_data_dict = {"departmentId": 917,"userId": 841,}
books_data_dict = {"groupId": 10, "userId": 841, "ps": 1000, "pn": 1}
# response = session.post(url='%s/wordoor_uaas_api/v1/busins/login2b' % hosts, data=login_data_dict)

response = session.post(url='%s/wordoor_uaas_api/v1/busins/book/books' % hosts, headers=headers, data=books_data_dict)
print(response.text)
