import re
import requests
import datetime
import os ,json
from threading import Thread




class today_r18:
    def __init__(self):
        proxies = json.load(open('name.json', mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.url = 'https://www.pixiv.net/ranking.php?mode=daily_r18'
        self.run()

    def headers(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "referer": "https://www.pixiv.net/ranking.php?mode=daily_r18",
            "cookie": json.load(open('name.json', mode='r')).get('cookie'),
        }
        return headers


    def request_2(self,url):
        try:
            global d
            response = requests.get('https://www.pixiv.net' + url,proxies=self.proxies)
            name = re.search(r'"title":"(.*?)"', response.text).group(1)
            name = name.strip('?').replace('\*', '').replace('<', '_').replace('>', '_').replace('"', '_').replace(':',
                                                                                                                   '_')
            name = name.replace('.', '').replace('\\', '').replace('|', '_')
            name = name.replace('\u0027', '_').replace('\u3000', '_')
            img_url = re.findall(r'"original":"(.*?)"},', response.text, re.S)
            for it in img_url:
                resp = requests.get(it, headers=self.headers(),proxies=self.proxies)
                if not os.path.exists(path + name + it[-3:]):
                    with open(path + '%s.%s' % (name.replace(r'/', '_'), it[-3:]), mode='wb') as f:
                        f.write(resp.content)
                else:
                    with open(path + '%s(%s).%s' % (name.replace(r'/', '_'), str(d), it[-3:]), mode='wb') as f:
                        f.write(resp.content)
                        d += 1
        except OSError as a:
            print('\033[2;32m{}\033[0m'.format(str(a)))

    def request_1(self):
        try:
            global d
            resp = requests.get(self.url, headers=self.headers(),proxies=self.proxies)
            resp.encoding = 'utf-8'
            # print(resp.text)
            title_url = re.findall(r'<h2>.*?<a href="(.*?)"', resp.text)
            list = []
            print('共 %d 张插画'.center(20, '-') % len(title_url))
            print('正在将所需下载内容写入列表')
            for i in title_url:
                if i is not None:
                    list.append(i)
                else:
                    print('查看url是否有误')
                    exit()
            print('写入完成,开始下载')
            for d in (1, len(list)):
                ts = [Thread(target=self.request_2, args=(i,)) for i in list]
                for it in ts:
                    it.start()
                for it in ts:
                    it.join()
            print('已将所有内容下载完成')
        except requests.exceptions.ChunkedEncodingError:
            print('\033[2;32m网络请求失败,并不代表程序已中断\033[0m')

    def run(self):
        global path
        # path = 'F:/two_dimension/r18_Today_date/%s/' % datetime.date.today()
        with open('name.json', mode='r', encoding='UTF-8') as f:
            path = json.load(f).get('dirs').get('r18_Today_date')
            path = (path + '%s/' % datetime.date.today())
        if os.path.exists(path) is False:
            os.mkdir(path)
            print('已创建文件夹,准备下载\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
            # os.system('start {}'.format(path))
            self.request_1()
        else:
            print('当前路径已存在,准备下载\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
            # os.system('start {}'.format(path))
            self.request_1()

if __name__=='__main__':
    # 实例化后将执行类方法的 run 函数
    pixiv = r_18()


# url = 'https://www.pixiv.net/ranking.php?mode=daily_r18'
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
#     "referer": "https://www.pixiv.net/ranking.php?mode=daily_r18",
#     "cookie": json.load(open('name.json',mode='r')).get('cookie'),
# }
#
#
#
# def request_2(url):
#     try:
#         global d
#         response = requests.get('https://www.pixiv.net' + url)
#         name = re.search(r'"title":"(.*?)"', response.text).group(1)
#         name = name.strip('?').replace('\*', '').replace('<','_').replace('>','_').replace('"','_').replace(':','_')
#         name = name.replace('.', '').replace('\\', '').replace('|','_')
#         name = name.replace('\u0027', '_').replace('\u3000', '_')
#         img_url = re.findall(r'"original":"(.*?)"},', response.text, re.S)
#         for it in img_url:
#             resp = requests.get(it,headers=headers)
#             if not os.path.exists(path + name + it[-3:]):
#                 with open(path + '%s.%s'%(name.replace(r'/','_'),it[-3:]),mode='wb') as f:
#                     f.write(resp.content)
#             else:
#                 with open(path + '%s(%s).%s'%(name.replace(r'/','_'),str(d),it[-3:]),mode='wb') as f:
#                     f.write(resp.content)
#                     d += 1
#     except OSError as a:
#         print('\033[2;32m{}\033[0m'.format(str(a)))

# def request_1():
#     try:
#         global d
#         resp = requests.get(url,headers=headers)
#         resp.encoding = 'utf-8'
#         # print(resp.text)
#         title_url = re.findall(r'<h2>.*?<a href="(.*?)"', resp.text)
#         list = []
#         print('共 %d 张插画'.center(20,'-') % len(title_url))
#         print('正在将所需下载内容写入列表')
#         for i in title_url:
#             if i is not None:
#                 list.append(i)
#             else:
#                 print('查看url是否有误')
#                 exit()
#         print('写入完成,开始下载')
#         for d in (1,len(list)):
#             ts = [Thread(target=request_2,args=(i,)) for i in list]
#             for it in ts:
#                 it.start()
#             for it in ts:
#                 it.join()
#         print('已将所有内容下载完成')
#     except requests.exceptions.ChunkedEncodingError:
#         print('\033[2;32m网络请求失败,并不代表程序已中断\033[0m')

# def main():
#     global path
#     # path = 'F:/two_dimension/r18_Today_date/%s/' % datetime.date.today()
#     with open('name.json', mode='r', encoding='UTF-8') as f:
#         path = json.load(f).get('dirs').get('r18_Today_date')
#         path = (path + '%s/' % datetime.date.today())
#     if os.path.exists(path) is False:
#         os.mkdir(path)
#         print('已创建文件夹,准备下载\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
#         # os.system('start {}'.format(path))
#         request_1()
#     else:
#         print('当前路径已存在,准备下载\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
#         # os.system('start {}'.format(path))
#         request_1()
#
# if __name__ == '__main__':
#     main()