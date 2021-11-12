import requests
import re, os ,json
from threading import Thread


class pixiv_date_r18:
    def __init__(self):
        proxies = json.load(open('name.json', mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.thread_requests()

    def user_agin(self):
        headers = {
            'cookie': json.load(open('name.json',mode='r')).get('cookie'),
            'Referer': 'https://www.pixiv.net/ranking.php?mode=daily_r18',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
        }
        return headers

    def create_request(self):
        try:
            self.a = input('请输入您想爬取的图片日期：')
            b = self.a[:4]
            c = self.a[4:-2]
            d = self.a[-2:]
            # self.path = 'F:/two_dimension/r18_assign_date/R18_%d-%d-%d/' % (int(b), int(c), int(d))
            with open('name.json', mode='r', encoding='UTF-8') as f:
                path = json.load(f).get('dirs').get('r18_assign_date')
                self.path = (path + 'R18_%d-%d-%d/' % (int(b), int(c), int(d)))
            if os.path.exists(self.path) is False:
                os.mkdir(self.path)
                print('已创建文件夹,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/', '\\'))
                # os.system('start {}'.format(self.path))
                self.request_1()
            elif os.path.exists(self.path) is True:
                print('当前路径已存在,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/','\\'))
                # os.system('start {}'.format(self.path))
                self.request_1()
        except ValueError:
            print('啊咧咧,请问您输入的是真实的日期嘛 (*^-^)')

    def request_1(self):
        url = 'https://www.pixiv.net/ranking.php?mode=daily_r18&date=%d' % int(self.a)
        resp = requests.get(url,headers=self.user_agin(),proxies=self.proxies)
        title_url = re.findall(r'<h2>.*?<a href="(.*?)"', resp.text)
        self.list_img_url = []
        print('\033[2;32m任务写入执行列表中...',end='')
        for i in title_url:
            url = 'https://www.pixiv.net' + i
            self.list_img_url.append(url)
        print('共 %d 张插画\033[0m' % len(self.list_img_url))

        # 第二次请求
    def request_2(self, url):
        response = requests.get(url,proxies=self.proxies)
        # print(response.text)
        img_name = re.search(r'"illustTitle":"(.+?)"', response.text).group(1)
        name = img_name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"', '_').replace(':', '_')
        name = name.replace('.', '').replace('|', '_')
        name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        img_url = re.findall(r'original":"(.*?)"}', response.text)
        for i in img_url:
            self.request_3(i,name)


    # 第三次请求 + 下载
    def request_3(self, img_url,name):
        global d
        resp = requests.get(img_url, headers=self.user_agin(),proxies=self.proxies)
        if not os.path.exists(self.path + name + '.' + img_url[-3:]):
            with open(self.path + name.replace(r'/', '_').strip(r'*') + '.' + img_url[-3:], mode='wb') as f:
                f.write(resp.content)
        else:
            with open(self.path + name.replace(r'/', '_').strip(r'*') + '(' + str(d) + ')' + '.' + img_url[-3:], mode='wb') as f:
                f.write(resp.content)
                d += 1

    def thread_requests(self):
        try:
            global d
            self.create_request()
            for d in (1,len(self.list_img_url)):
                ts = [Thread(target=self.request_2, args=(i,)) for i in self.list_img_url]
                print('开始下载')
                for it in ts:
                    it.start()
                for it in ts:
                    it.join()
                print('over！')
                exit()
        except requests.exceptions.ChunkedEncodingError:
            print('\033[2;32m网络请求失败,并不代表程序已中断\033[0m')

if __name__ == '__main__':
    # 实例化后将执行类方法的 thread_requests 函数
    pixiv = pixiv_date_r18()