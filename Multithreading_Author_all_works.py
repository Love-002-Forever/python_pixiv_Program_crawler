import re
import requests
import os, json,time,random
from threading import Thread
from tqdm import tqdm
import os
from download_Zip import ABC
from fake_useragent import UserAgent


class Author_All_Works:
    def __init__(self):
        proxies = json.load(open('name.json',mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.count = 1
        self.count_manga = 1
        self.list = []
        self.manga_list = []
        self.zip_list = []
        self.request()

    """带 referer 的请求头"""

    def user_agin_referer(self):
        header = {
            'referer': 'https://www.pixiv.net/',
            'user-agent': str(UserAgent().random)
        }
        return header

    """带 cookie 的请求头"""

    def user_agin_cookie(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "cookie":json.load(open('name.json',mode='r')).get('cookie'),
        }
        return headers

    def name(self,name):
        name = name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_').replace('\\', '').replace('\\\\', '').replace('.', '').replace('|', '_').replace(r'/', '_')
        name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        return name

    def request(self):
        b = 5
        while b <= 5:
            if b == 0:
                print('你不能再输入了')
                break
            try:
                # 只能输入数字
                self.a = int(input('请输入画师 id 号:'))
                # 读取 name.json 文件中的 ID 参数
                with open('name.json',mode='r',encoding='UTF-8') as f:
                    path = json.load(f).get('dirs').get('ID')
                    self.path = (path + 'ID_%d/' % self.a)
                # 如果 画师ID文件夹不存在  和   请求 URL 没有碰到错误
                if os.path.exists(self.path) is False and requests.get('https://www.pixiv.net/ajax/user/%d/profile/all' % self.a).json()['error'] is False:
                    os.mkdir(self.path)
                    print('已创建文件夹,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/', '\\'))
                    os.system('start {}'.format(self.path))
                    self.get()
                # 如果 画师ID文件夹存在  和   请求 URL 没有碰到错误
                elif os.path.exists(self.path) is True and requests.get('https://www.pixiv.net/ajax/user/%d/profile/all' % self.a).json()['error'] is False:
                    print('当前画师的作品存在哦~')
                    # print('当前路径已存在,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/', '\\'))
                    os.system('start {}'.format(self.path))
                    # self.get()
                else:
                    print('啊咧咧,请问您输入的是真实的画师ID嘛 (*^-^)\n你还能输入 %d 次哦~' % (b - 1))
            except requests.exceptions.ConnectionError:
                print('响应超时,请检查网络设置')
                break
            # 碰到不是数字的情况触发该事件
            except ValueError:
                print('您输入的不是数字，请重新输入\n你还能输入 %d 次哦~' % (b - 1))
            b -= 1

    # 2
    def request_user(self,ID):
        # 画师URL主页
        url = 'https://www.pixiv.net/users/%d' % ID
        resp = requests.get(url).text
        user_name = re.search(r'<title>(.*?) - pixiv</title>',resp).group(1)
        print('画师昵称为: \033[2;32m{}\033[0m'.format(user_name))
        self.request_1_pic(self.a)

    # 3
    def request_1_pic(self, id):
        # 画师URL 所有作品
        url = 'https://www.pixiv.net/ajax/user/%d/profile/all' % int(id)
        resp = requests.get(url=url, headers=self.user_agin_cookie(),proxies=self.proxies)
        self.body = resp.json()['body']
        if len(self.body.get('illusts')) != 0:
            self.keys = self.body.get('illusts').keys()
            imgs = len(self.keys)
            print('该画师有 %d 张插画/插画集/动图'.center(50 // 2, '-') % imgs)
        else:
            print('该ID为普通用户ID哦')
            os.rmdir(self.path)
            exit()

    # 1
    def get(self):
        try:
            global q
            self.request_user(self.a)
            for q in (1,len(self.keys)):
                ts = [Thread(target=self.request_2_pic,args=(i,)) for i in self.keys]
                print('\033[2;32m开始下载\033[0m')
                for it in ts:
                    it.setDaemon(True)
                for it in tqdm(ts, desc='下载进度', unit='img', ncols=100):
                    it.start()
                    time.sleep(random.uniform(0.1, 0.3))
                print('\033[2;32m等待子进程运行完成...\033[0m')
                for n in ts:
                    n.join()
                print('下载完成\033[0m\n共下载\033[2;32m {} \033[0m张插画'.format(len(self.list)))
                # 下载漫画
                if json.load(open('name.json',mode='r')).get('manga_set') == True:
                    self.thread_manga()
                time.sleep(3)
                # 下载动态图片
                if json.load(open('name.json',mode='r')).get('gif_set') == True:
                    if len(self.zip_list) >= 1:
                        gif = self.path + '动图/'
                        if os.path.exists(self.path + gif) is False:
                            os.mkdir(gif)
                        print('获取到\033[2;32m {} \033[0m张动态图片\n正在下载...'.format(len(self.zip_list)))
                        download_num_list = []
                        for i in self.zip_list:
                            RUN = ABC(i,gif)
                            RUN.request_zip_url()
                            download_num_list.append(i)
                        print('下载完成\n共下载\033[2;32m {} \033[0m张动态图片'.format(len(download_num_list)))
        except requests.exceptions.ConnectionError:
            print('\033[2;31m网络响应超时,并不代表程序已中断\033[0m')

    def request_2_pic(self, url):
        gif_url = 'https://www.pixiv.net/ajax/illust/{}/ugoira_meta?lang=zh'.format(url)
        if requests.get(gif_url,headers=self.user_agin_cookie()).json()['error'] is False:
            self.zip_list.append(url)
        if str(self.zip_list[-1:]).strip(']').replace('[','').replace("'",'') != url:
            # print(str(self.zip_list[-1:]).strip(']').replace('[',''))
            resp = requests.get('https://www.pixiv.net/artworks/' + url, headers=self.user_agin_cookie(),proxies=self.proxies)
            name = re.search('"illustTitle":"(.+?)"', resp.text).group(1)
            resp_img = requests.get('https://www.pixiv.net/ajax/illust/%s/pages?lang=zh' % str(url),headers=self.user_agin_cookie(),proxies=self.proxies)
            for i in resp_img.json()['body']:
                if len(i) > 2:
                    time.sleep(random.uniform(0.5,1))
                picurl = i.get('urls').get('original')
                self.download_pic(self.name(name), picurl)
                self.list.append(picurl)
                time.sleep(random.uniform(0.1, 0.3))

    def download_pic(self, name, picurl):
        global q
        resp = requests.get(picurl, headers=self.user_agin_referer(),proxies=self.proxies)
        if not os.path.exists(self.path + name + '.' + picurl[-3:]):
            with open(self.path + name + '.' + picurl[-3:],mode='wb') as f:
                f.write(resp.content)
        else:
            with open(self.path + name +'(' + str(q) + ')' + '.' + picurl[-3:], mode='wb') as f:
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
                            self.list_manga = []
                            for it in self.manga.keys():
                                self.list_manga.append(it)
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
            print('画师作品未获取到...')
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
                    time.sleep(random.uniform(0.1, 0.3))
                for it in ts:
                    it.join()
                print('下载完成\033[0m\n共下载\033[2;32m {} \033[0m张漫画作品'.format(len(self.manga_list)))
                exit()
        except requests.exceptions.ProxyError:
            print('\033[2;31网络响应超时,并不代表程序已中断\033[0m')

    def requests_2_maga(self, url):
        resp = requests.get('https://www.pixiv.net/artworks/' + url, headers=self.user_agin_cookie(),proxies=self.proxies)
        name = re.search('"illustTitle":"(.+?)"', resp.text).group(1)
        resp_img = requests.get('https://www.pixiv.net/ajax/illust/%s/pages?lang=zh' % str(url),headers=self.user_agin_cookie(), proxies=self.proxies)
        for i in resp_img.json()['body']:
            if len(i) > 200:
                time.sleep(random.randint(0.5,1))
            picurl_manga = i.get('urls').get('original')
            self.download_manga(self.name(name), picurl_manga)
            time.sleep(random.uniform(0.1, 0.3))

    def download_manga(self, name, picurl):
        global w
        self.manga_list.append(picurl)
        resp = requests.get(picurl, headers=self.user_agin_referer(),proxies=self.proxies)
        if not os.path.exists(self.path + name + '(1)' + '.' + picurl[-3:]):
            with open(self.path + name + '(1)' + '.' + picurl[-3:], mode='wb') as f:
                f.write(resp.content)
        else:
            with open(self.path + name + '(' + str(int(1) + int(w)) + ')'.replace(r'/', '_').strip(r'*') + '.' + picurl[-3:], mode='wb') as f:
                f.write(resp.content)
                w += 1

if __name__ == '__main__':
    # 实例化后将执行类方法的 request 函数
    Author_all_works = Author_All_Works()
