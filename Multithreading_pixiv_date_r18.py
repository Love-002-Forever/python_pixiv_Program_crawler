import requests
import re, os ,json
from threading import Thread
from fake_useragent import UserAgent


class pixiv_date_r18:
    def __init__(self):
        proxies = json.load(open('name.json', mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.list_img_url = []
        self.thread_requests()

    def user_agin(self):
        headers = {
            "User-Agent": str(UserAgent().random),
            'cookie': json.load(open('name.json',mode='r')).get('cookie'),
            'Referer': 'https://www.pixiv.net/ranking.php?mode=daily_r18',
        }
        return headers

    def create_request(self):
        try:
            self.a = input('请输入您想爬取的图片日期：')
            b = self.a[:4]
            c = self.a[4:-2]
            d = self.a[-2:]
            with open('name.json', mode='r', encoding='UTF-8') as f:
                path = json.load(f).get('dirs').get('r18_assign_date')
                self.path = (path + 'R18_%d-%d-%d/' % (int(b), int(c), int(d)))
            if os.path.exists(self.path) is False:
                os.mkdir(self.path)
                print('已创建文件夹,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/', '\\'))
                os.system('start {}'.format(self.path))
                self.request_1()
            elif os.path.exists(self.path) is True:
                print('当前路径已存在,准备下载...\n地址为:\033[2;32m%s\033[0m' % self.path.replace('/','\\'))
                os.system('start {}'.format(self.path))
                self.request_1()
        except ValueError:
            print('啊咧咧,请问您输入的是真实的日期嘛 (*^-^)')

    def request_1(self):
        for n in range(1,2 + 1):
            url = 'https://www.pixiv.net/ranking.php?mode=daily_r18&date=%d&p=%d' % (int(self.a),n)
            resp = requests.get(url,headers=self.user_agin(),proxies=self.proxies)
            title_url = re.findall(r'<h2>.*?<a href="(.*?)"', resp.text)
            print('写入任务:第\033[2;32m{}\033[0m页内容'.format(n))
            print('\033[2;32m任务写入执行列表中...\033[0m\n',end='')
            for i in title_url:
                url = 'https://www.pixiv.net' + i
                self.list_img_url.append(url)
        print('写入完成')

        # 第二次请求
    def request_2(self, url):
        response = requests.get(url,proxies=self.proxies)
        img_name = re.search(r'"illustTitle":"(.+?)"', response.text).group(1)
        name = img_name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"', '_').replace(':', '_')
        name = name.replace('.', '').replace('|', '_')
        name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        img_url = re.search(r'original":"(.*?)"}', response.text).group(1)
        self.request_3(img_url,name)


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
            new_list_img_url = []
            for i in self.list_img_url:
                if i not in new_list_img_url:
                    new_list_img_url.append(i)
            print('共 \033[2;32m{}\033[0m 张插画'.format(len(new_list_img_url)))
            for d in (1,len(new_list_img_url)):
                ts = [Thread(target=self.request_2, args=(i,)) for i in new_list_img_url]
                print('开始下载')
                for it in ts:
                    it.setDaemon(True)
                for it in ts:
                    it.start()
                for it in ts:
                    it.join()
                print('下载完成')
                break
        except requests.exceptions.ChunkedEncodingError:
            print('\033[2;32m网络请求失败,并不代表程序已中断\033[0m')

if __name__ == '__main__':
    # 实例化后将执行类方法的 thread_requests 函数
    pixiv = pixiv_date_r18()