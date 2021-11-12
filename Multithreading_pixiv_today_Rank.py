import requests,re,datetime,os,random,json
from threading import Thread

class pixiv:
    def __init__(self):
        proxies = json.load(open('name.json', mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.thread_requests()


    def request_start(self):
        while True:
            try:
                with open('name.json',mode='r',encoding='UTF-8') as f:
                    path = json.load(f).get('dirs').get('Daily_ranking')
                    self.path = (path + '%s/' % datetime.date.today())
                if os.path.exists(self.path) is False:
                    os.mkdir(self.path)
                    print('已创建文件夹\n地址为:\033[2;32m%s\033[0m' % self.path)
                    # os.system('start {}'.format(self.path))
                else:
                    print('文件夹已存在\n地址为:\033[2;32m%s\033[0m' % self.path)
                    # os.system('start {}'.format(self.path))
                a = int(input('输入起始页:'))
                b = int(input('输入结束页:'))
                if a > b:
                    print('请认真输入!!!')
                elif a <= 0 and b > 10:
                    print('你故意找茬是不是!!!')
                    exit()
                elif b > 10:
                    print('排行榜内至多 10 页,每页共 50 张插画,\n请重新输入!!!')
                elif a <= 0:
                    print('不正确的输入内容,\n请重新输入!!!')
                else:
                    self.list_img_url = []
                    print('\r\033[2;32m将任务写入列表中...', end='')
                    for i in range(a,b + 1):
                        url = 'https://www.pixiv.net/ranking.php?p=%d' % i
                        self.list_img_url.append(url)
                    print('写入完成.\033[0m')
                    print('共下载 %d 页插画...' % len(self.list_img_url))
                    break
            except ValueError:
                print('请输入数字!')
                exit()
            except requests.exceptions.ProxyError:
                print('网络错误,请检查网络配置!')

    def user_agen(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Referer": "https://www.pixiv.net/ranking.php?mode=daily&content=illust",
            # "cookie": json.load(open('name.json',mode='r')).get('cookie'),
        }
        return headers

    # 第一次请求
    def request_1(self,url):
        resp = requests.get(url,headers = self.user_agen(),proxies=self.proxies)
        # print(resp.text)
        data_url = re.findall(r'<div class="ranking-image-item"><a href="(.*?)"class=".*?"target="_blank"',resp.text,re.S)
        for i in data_url:
            response = requests.get('https://www.pixiv.net' + i)
            self.request_2(response)

    # 第二次请求
    def request_2(self,response):
        # print(response.text)
        img_name = re.search(r'"illustTitle":"(.+?)"',response.text).group(1)
        name = img_name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_')
        name = name.replace('.', '').replace('|', '_')
        self.name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        img_url = re.findall(r'original":"(.*?)"}',response.text)
        for i in img_url:
            self.request_3(i)

    # 第三次请求 + 下载
    def request_3(self,img_url):
        global q
        resp = requests.get(img_url,headers = self.user_agen(),proxies=self.proxies)
        if not os.path.exists(self.path + self.name + '.' + img_url[-3:]):
            with open(self.path + self.name.replace(r'/', '_').strip(r'*') + '.' + img_url[-3:], mode='wb') as f:
                f.write(resp.content)
        else:
            with open(self.path + self.name.replace(r'/', '_').strip(r'*') + '(' + str(q) + ')' + '.' + img_url[-3:], mode='wb') as f:
                f.write(resp.content)
                q += 1


    def thread_requests(self):
        try:
            global q
            self.request_start()
            for q in (1,len(self.list_img_url)):
                ts = [Thread(target=self.request_1, args=(i,)) for i in self.list_img_url]
                print('\033[2;32m开始下载...')
                for it in ts:
                    it.start()
                print('等待子进程运行完成...')
                for it in ts:
                    it.join()
                print('over！\033[0m')
                exit()
        except requests.exceptions.ChunkedEncodingError:
            print('\033[2;32m网络请求失败,并不代表程序已中断\033[0m')


if __name__ == '__main__':
    # 实例化后将执行类方法的 thread_requests 函数
    pixiv = pixiv()