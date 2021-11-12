import os,json
import requests

# a = input('输入:')

proxies = json.load(open('name.json',mode='r')).get('proxies')
print(proxies,end='')
print(type(proxies))
proxies = (proxies)
print(eval(proxies),end='')
print(type(eval(proxies)))
# proxies = {'http':'http://127.0.0.1:10809'}
# print(proxies,end='')
# print(type(proxies))
resp = requests.get('https://www.google.com',proxies=eval(proxies))
print(resp)

# path = 'f:/123/123'
#
# if os.path.exists(path) is False and requests.get('https://www.pixiv.net/ajax/user/%d/profile/all' % a, proxies=proxies).json()['error'] is False:
#     print(123)
#     print('已创建文件夹,准备下载...\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))