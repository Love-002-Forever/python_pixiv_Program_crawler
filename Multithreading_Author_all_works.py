import re
import requests
import os, json
from threading import Thread


"""多线程(下载速度极快,没限制最大线程)"""
class Author_All_Works:
    def __init__(self):
        proxies = json.load(open('name.json',mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.count = 1
        self.count_manga = 1
        self.request()

    """带 referer 的请求头"""

    def user_agin_referer(self):
        header = {
            'referer': 'https://www.pixiv.net/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        return header

    """带 cookie 的请求头"""

    def user_agin_cookie(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "cookie":json.load(open('name.json',mode='r')).get('cookie'),
        }
        return headers

    def request(self):
        b = 5
        while b < 10:
            if b == 0:
                print('你不能再输入了')
                break
            try:
                self.a = int(input('请输入画师 id 号:'))
                # self.path = 'F:/two_dimension/ID/ID_%d/' % self.a
                with open('name.json',mode='r',encoding='UTF-8') as f:
                    path = json.load(f).get('dirs').get('ID')
                    self.path = (path + 'ID_%d/' % self.a)
                if os.path.exists(self.path) is False:# and requests.get('https://www.pixiv.net/ajax/user/%d/profile/all' % self.a).json()['error'] is False:
                    os.mkdir(self.path)
                    print('已创建文件夹,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/', '\\'))
                    os.system('start {}'.format(self.path))
                    self.get()
                elif os.path.exists(self.path) is True:
                    print('当前路径已存在,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/', '\\'))
                    os.system('start {}'.format(self.path))
                    self.get()
                else:
                    print('啊咧咧,请问您输入的是真实的画师ID嘛 (*^-^)\n你还能输入 %d 次哦~' % (b - 1))
            # except requests.exceptions.ConnectionError:
            #     print('响应超时,请检查网络设置')
            #     exit()
            except ValueError:
                print('您输入的不是数字，请重新输入\n你还能输入 %d 次哦~' % (b - 1))
            b -= 1

    def request_1_pic(self, id):
        url = 'https://www.pixiv.net/ajax/user/%d/profile/all' % int(id)
        resp = requests.get(url=url, headers=self.user_agin_cookie(),proxies=self.proxies)
        self.body = resp.json()['body']
        self.keys = self.body.get('illusts').keys()
        imgs = len(self.keys)
        print('该画师有 %d 张插画'.center(50 // 2, '-') % imgs)

    def get(self):
        try:
            global q
            self.request_1_pic(self.a)
            for q in (1,len(self.keys)):
                ts = [Thread(target=self.request_2_pic,args=(i,)) for i in self.keys]
                print('\033[2;32m开始下载')
                for it in ts:
                    it.setDaemon(True)
                for it in ts:
                    it.start()
                print('等待子进程运行完成...')
                for n in ts:
                    n.join()
                print('下载完成\033[0m')
                self.thread_manga()
        except requests.exceptions.ConnectionError:
            print('\033[2;31m网络响应超时,并不代表程序已中断\033[0m')

    def request_2_pic(self, url):
        resp = requests.get('https://www.pixiv.net/artworks/' +url, headers=self.user_agin_cookie(),proxies=self.proxies)
        name = re.search('"illustTitle":"(.+?)"', resp.text).group(1)
        picurl = re.search('"original":"(.*?)"},', resp.text, re.S).group(1)
        self.download_pic(name, picurl)

    def download_pic(self, name, picurl):
        global q
        resp = requests.get(picurl, headers=self.user_agin_referer(),proxies=self.proxies)
        name = name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_')
        name = name.replace('.', '').replace('|', '_')
        name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        if not os.path.exists(self.path + name + '.' + picurl[-3:]):
            with open(self.path + name.replace(r'/', '_').strip(r'*') + '.' + picurl[-3:],mode='wb') as f:
                f.write(resp.content)
        else:
            with open(self.path + name.replace(r'/', '_').strip(r'*') +'(' + str(q) + ')' + '.' + picurl[-3:], mode='wb') as f:
                f.write(resp.content)
                q += 1

    def request_1_manga(self):
        try:
            self.manga = self.body.get('manga')
            if len(self.manga) != 0:
                self.a = 5
                print('\033[2;32m\r(1 为"是" , 2 为"否")\033[0m\033[2;33m\n该画师有 %d 张漫画作品,是否下载\033[0m' % len(self.manga))
                while 0 < self.a:
                    try:
                        b = int(input('请输入你的选项:'))
                        if b == 1:
                            self.imgs_manga = len(self.manga)
                            # print('该画师有 %d 张漫画作品'.center(50 // 2, '-') % self.imgs_manga)
                            self.list_manga = []
                            for it in self.manga.keys():
                                if it in self.manga.keys():
                                    pic = 'https://www.pixiv.net/artworks/%d' % int(it)
                                    self.list_manga.append(pic)
                            break
                        elif b == 2 and self.a != 0:
                            print('当前程序已关闭')
                            self.a -= 1
                            exit()
                        elif b < 2 or b > 2 and self.a != 0:
                            if self.a == 5:
                                print('(输入次数为 0 时自动退出)\n您输入的不是有效数字,请重新输入\n你还能输入 %d 次' % (self.a - 1))
                            else:
                                print('请输入有效数字\n你还能输入 %d 次' % (self.a - 1))
                            self.a -= 1
                            continue
                        else:
                            exit()
                        # self.a -= 1
                    except ValueError:
                        if self.a == 5:
                            print('(输入次数为 0 时自动退出)\n您输入的不是数字，请重新输入\n你还能输入 %d 次' % (self.a - 1))
                        elif self.a < 5:
                            print('你还能输入 %d 次' % (self.a - 1))
                        elif self.a == 0:
                            exit()
                        else:
                            return None
                    self.a -= 1
            else:
                print('该画师并没有漫画作品')
                exit()

        except requests.exceptions.ConnectionError:
            print('响应超时,请检查网络设置')
            exit()

        except AttributeError:
            print('画师作品未获取到,也可能是画师ID输入有误,请检查!')
            exit()

    def thread_manga(self):
        try:
            global w
            self.request_1_manga()
            for w in (1,len(self.list_manga)):
                ts = [Thread(target=self.requests_2_maga,args=(i,)) for i in self.list_manga]
                print('\033[2;32m下载开始')
                for it in ts:
                    it.setDaemon(True)
                for it in ts:
                    it.start()
                for it in ts:
                    it.join()
                print('下载完成\033[0m')
                exit()
        except requests.exceptions.ProxyError:
            print('\033[2;31网络响应超时,并不代表程序已中断\033[0m')

    def requests_2_maga(self, url):
        resp = requests.get(url, headers=self.user_agin_referer(),proxies=self.proxies)
        name = re.search('"illustTitle":"(.+?)"', resp.text).group(1)
        picurl = re.search('"original":"(.*?)"},', resp.text, re.S).group(1)
        self.download_manga(name, picurl)

    def download_manga(self, name, picurl):
        global w
        resp = requests.get(picurl, headers=self.user_agin_referer(),proxies=self.proxies)
        name = name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_')
        name = name.replace('.', '').replace('|', '_')
        name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        if not os.path.exists(self.path + name + '.' + picurl[-3:]):
            with open(self.path + '漫画_' + name.replace(r'/', '_').strip(r'*') + '.' + picurl[-3:], mode='wb') as f:
                f.write(resp.content)
        else:
            with open(self.path + '漫画_' + name + '(' + str(w) + ')'.replace(r'/', '_').strip(r'*') + '.' + picurl[-3:], mode='wb') as f:
                f.write(resp.content)
                w += 1

if __name__ == '__main__':
    # 实例化后将执行类方法的 request 函数
    Author_all_works = Author_All_Works()

# \033[显示方式;字体色;背景色m打印内容\033[0m


# """多线程(下载速度极快,没限制最大线程)"""
# class Author_All_Works:
#     def __init__(self):
#         self.proxies = {'https': 'http://127.0.0.1:10809'}
#         self.count = 1
#         self.count_manga = 1
#         self.request()
#
#     """带 referer 的请求头"""
#
#     def user_agin_referer(self):
#         header = {
#             'referer': 'https://www.pixiv.net/',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
#         }
#         return header
#
#     """带 cookie 的请求头"""
#
#     def user_agin_cookie(self):
#         headers = {
#             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
#             "cookie":json.load(open('name.json',mode='r')).get('cookie'),
#         }
#         return headers
#
#     def request(self):
#         b = 5
#         while b < 10:
#             if b == 0:
#                 print('你不能再输入了')
#                 break
#             try:
#                 self.a = int(input('请输入画师 id 号:'))
#                 # self.path = 'F:/two_dimension/ID/ID_%d/' % self.a
#                 with open('name.json',mode='r',encoding='UTF-8') as f:
#                     path = json.load(f).get('dirs').get('ID')
#                     self.path = (path + 'ID_%d/' % self.a)
#                 if os.path.exists(self.path) is False and requests.get('https://www.pixiv.net/ajax/user/%d/profile/all' % self.a).json()['error'] is False:
#                     os.mkdir(self.path)
#                     print('已创建文件夹,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/', '\\'))
#                     # os.system('start {}'.format(self.path))
#                     self.get()
#                 elif os.path.exists(self.path) is True:
#                     print('当前路径已存在,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/', '\\'))
#                     # os.system('start {}'.format(self.path))
#                     self.get()
#                 else:
#                     print('啊咧咧,请问您输入的是真实的画师ID嘛 (*^-^)\n你还能输入 %d 次哦~' % (b - 1))
#             except requests.exceptions.ConnectionError:
#                 print('响应超时,请检查网络设置')
#                 exit()
#             except ValueError:
#                 print('您输入的不是数字，请重新输入\n你还能输入 %d 次哦~' % (b - 1))
#             b -= 1
#
#     def request_1_pic(self, id):
#         url = 'https://www.pixiv.net/ajax/user/%d/profile/all' % int(id)
#         resp = requests.get(url=url, headers=self.user_agin_cookie())
#         self.body = resp.json()['body']
#         self.keys = self.body.get('illusts').keys()
#         imgs = len(self.keys)
#         print('该画师有 %d 张插画'.center(50 // 2, '-') % imgs)
#
#     def get(self):
#         try:
#             global q
#             self.request_1_pic(self.a)
#             for q in (1,len(self.keys)):
#                 ts = [Thread(target=self.request_2_pic,args=(i,)) for i in self.keys]
#                 print('\033[2;32m开始下载')
#                 for it in ts:
#                     it.setDaemon(True)
#                 for it in ts:
#                     it.start()
#                 print('等待子进程运行完成...')
#                 for n in ts:
#                     n.join()
#                 print('下载完成\033[0m')
#                 self.thread_manga()
#         except requests.exceptions.ConnectionError:
#             print('\033[2;31网络响应超时,并不代表程序已中断\033[0m')
#
#     def request_2_pic(self, url):
#         resp = requests.get('https://www.pixiv.net/artworks/' +url, headers=self.user_agin_cookie())
#         name = re.search('"illustTitle":"(.+?)"', resp.text).group(1)
#         picurl = re.search('"original":"(.*?)"},', resp.text, re.S).group(1)
#         self.download_pic(name, picurl)
#
#     def download_pic(self, name, picurl):
#         global q
#         resp = requests.get(picurl, headers=self.user_agin_referer())
#         name = name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_')
#         name = name.replace('.', '').replace('|', '_')
#         name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
#         if not os.path.exists(self.path + name + '.' + picurl[-3:]):
#             with open(self.path + name.replace(r'/', '_').strip(r'*') + '.' + picurl[-3:],mode='wb') as f:
#                 f.write(resp.content)
#         else:
#             with open(self.path + name.replace(r'/', '_').strip(r'*') +'(' + str(q) + ')' + '.' + picurl[-3:], mode='wb') as f:
#                 f.write(resp.content)
#                 q += 1
#
#     def request_1_manga(self):
#         try:
#             self.manga = self.body.get('manga')
#             if len(self.manga) != 0:
#                 self.a = 5
#                 print('\033[2;32m\r(1 为"是" , 2 为"否")\033[0m\033[2;33m\n该画师有 %d 张漫画作品,是否下载\033[0m' % len(self.manga))
#                 while 0 < self.a:
#                     try:
#                         b = int(input('请输入你的选项:'))
#                         if b == 1:
#                             self.imgs_manga = len(self.manga)
#                             # print('该画师有 %d 张漫画作品'.center(50 // 2, '-') % self.imgs_manga)
#                             self.list_manga = []
#                             for it in self.manga.keys():
#                                 if it in self.manga.keys():
#                                     pic = 'https://www.pixiv.net/artworks/%d' % int(it)
#                                     self.list_manga.append(pic)
#                             break
#                         elif b == 2 and self.a != 0:
#                             print('当前程序已关闭')
#                             self.a -= 1
#                             exit()
#                         elif b < 2 or b > 2 and self.a != 0:
#                             if self.a == 5:
#                                 print('(输入次数为 0 时自动退出)\n您输入的不是有效数字,请重新输入\n你还能输入 %d 次' % (self.a - 1))
#                             else:
#                                 print('请输入有效数字\n你还能输入 %d 次' % (self.a - 1))
#                             self.a -= 1
#                             continue
#                         else:
#                             exit()
#                         # self.a -= 1
#                     except ValueError:
#                         if self.a == 5:
#                             print('(输入次数为 0 时自动退出)\n您输入的不是数字，请重新输入\n你还能输入 %d 次' % (self.a - 1))
#                         elif self.a < 5:
#                             print('你还能输入 %d 次' % (self.a - 1))
#                         elif self.a == 0:
#                             exit()
#                         else:
#                             return None
#                     self.a -= 1
#             else:
#                 print('该画师并没有漫画作品')
#                 exit()
#
#         except requests.exceptions.ConnectionError:
#             print('响应超时,请检查网络设置')
#             exit()
#
#         except AttributeError:
#             print('画师作品未获取到,也可能是画师ID输入有误,请检查!')
#             exit()
#
#     def thread_manga(self):
#         try:
#             global w
#             self.request_1_manga()
#             for w in (1,len(self.list_manga)):
#                 ts = [Thread(target=self.requests_2_maga,args=(i,)) for i in self.list_manga]
#                 print('\033[2;32m下载开始')
#                 for it in ts:
#                     it.setDaemon(True)
#                 for it in ts:
#                     it.start()
#                 for it in ts:
#                     it.join()
#                 print('下载完成\033[0m')
#                 exit()
#         except requests.exceptions.ProxyError:
#             print('\033[2;31网络响应超时,并不代表程序已中断\033[0m')
#
#     def requests_2_maga(self, url):
#         resp = requests.get(url, headers=self.user_agin_referer())
#         name = re.search('"illustTitle":"(.+?)"', resp.text).group(1)
#         picurl = re.search('"original":"(.*?)"},', resp.text, re.S).group(1)
#         self.download_manga(name, picurl)
#
#     def download_manga(self, name, picurl):
#         global w
#         resp = requests.get(picurl, headers=self.user_agin_referer())
#         name = name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_')
#         name = name.replace('.', '').replace('|', '_')
#         name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
#         if not os.path.exists(self.path + name + '.' + picurl[-3:]):
#             with open(self.path + '漫画_' + name.replace(r'/', '_').strip(r'*') + '.' + picurl[-3:], mode='wb') as f:
#                 f.write(resp.content)
#         else:
#             with open(self.path + '漫画_' + name + '(' + str(w) + ')'.replace(r'/', '_').strip(r'*') + '.' + picurl[-3:], mode='wb') as f:
#                 f.write(resp.content)
#                 w += 1
#
# if __name__ == '__main__':
#     Author_all_works = Author_All_Works()