import requests,re,os,json
from threading import Thread
import threading

class Collect:
    def __init__(self):
        self.list = []
        with open('name.json', mode='r', encoding='UTF-8') as f:
            self.path = json.load(f).get('dirs').get('收藏图片')
        proxies = json.load(open('name.json', mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.os_requests()

    def headers(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "cookie": json.load(open('name.json',mode='r')).get('cookie'),
        }
        return headers

    def header(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "referer": "https://www.pixiv.net/",
        }
        return headers

    def os_requests(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            print('已创建文件夹,路径为:\033[2;32m{}\033[0m'.format(self.path))
            # os.system('start {}'.format(self.path))
            self.Mythread()
        else:
            print('当前路径存在哦~\n路径为:\033[2;32m{}\033[0m'.format(self.path))
            # os.system('start {}'.format(self.path))
            self.Mythread()

    def request_all_id(self):
        for i in range(0,2000,100):
            url = 'https://www.pixiv.net/ajax/user/71068383/illusts/bookmarks?tag=&offset={}&limit=100&rest=show&lang=zh'.format(i)
            if requests.get(url,headers=self.headers(),proxies=self.proxies).json()['body']['works'] != []:
                resp = requests.get(url,headers=self.headers())
                works = resp.json()['body']['works']
                for i in works:
                    a = i.get('id')
                    self.list.append(a)
        print('共\033[2;32m{}\033[0m张图片'.format(len(self.list)))

    def Mythread(self):
        try:
            global n
            self.request_all_id()
            print('开始下载')
            with threading.Semaphore(10):
                for n in (1,len(self.list)):
                    ts = [Thread(target=self.request_aworks_url,args=(i,)) for i in self.list]
                    for it in ts:
                        it.setDaemon(True)
                    for it in ts:
                        it.start()
                    for it in ts:
                        it.join()
                print('下载完成')
        except requests.exceptions.ProxyError:
            print('\033[2;31网络响应超时或请求链接次数过多,并不代表程序已中断\033[0m')

    def request_aworks_url(self,url):
        resp = requests.get('https://www.pixiv.net/artworks/%s' % str(url),headers=self.header(),proxies=self.proxies)
        name = re.search('"illustTitle":"(.*?)"', resp.text,re.S).group(1)
        picurl = re.search('"original":"(.*?)"},', resp.text, re.S).group(1)
        self.download_pic(name,picurl)

    def download_pic(self, name, picurl):
        global n
        resp = requests.get(picurl, headers=self.header(),proxies=self.proxies)
        name = name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_')
        name = name.replace('.', '').replace('|', '_')
        name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        if not os.path.exists(self.path + name + '.' + picurl[-3:]):
            with open(self.path + name.replace(r'/', '_').strip(r'*') + '.' + picurl[-3:],mode='wb') as f:
                f.write(resp.content)
                resp.close()
        else:
            with open(self.path + name.replace(r'/', '_').strip(r'*') + '(' + str(n) + ')' + '.' + picurl[-3:], mode='wb') as f:
                f.write(resp.content)
                resp.close()
                n += 1


if __name__ == '__main__':
    run = Collect()