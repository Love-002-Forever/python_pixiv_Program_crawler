import requests,os,json
import re,random,time,datetime
from threading import Thread





class Leaderboard:
    def __init__(self):
        # 任务列表
        self.list = []
        proxies = json.load(open('name.json', mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.main()


    def headers(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
        }
        return headers

    def getSinglePic(self,url):
        global d
        response = requests.get(url, headers=self.headers(),proxies=self.proxies)
        # 提取图片名称
        name = re.search('"illustTitle":"(.+?)"', response.text).group(1)
        name = name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_')
        name = name.replace('.', '').replace('|', '_').replace('/', '_')
        name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        # 提取图片原图地址
        picture = re.search('"original":"(.*?)"},', response.text, re.S)
        pic = requests.get(picture.group(1), headers=self.headers(),proxies=self.proxies)
        if not os.path.exists(path + '%s.%s' % (name.replace('\\', '_'), picture.group(1)[-3:])):
            with open(path + '%s.%s' % (name.replace('\\', '_'), picture.group(1)[-3:]), mode='wb') as f:
                f.write(pic.content)
        else:
            with open(path + '%s(%d).%s' % (name.replace('\\', '_'), d, picture.group(1)[-3:]), mode='wb') as f:
                f.write(pic.content)
                d += 1

    def getAllPicUrl(self):
        try:
            print('\033[2;32m写入任务列表中...', end='')
            for n in range(1, 10 + 1):
                url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=%d&format=json' % n
                response = requests.get(url, headers=self.headers(),proxies=self.proxies)
                illust_id = re.findall('"illust_id":(\d+?),', response.text)
                picUrl = ['https://www.pixiv.net/artworks/' + i for i in illust_id]
                for url in picUrl:
                    self.list.append(url)
            print('写入完成...共 %d 张图片\033[0m' % len(self.list))
            return None
        except OSError as f:
            print('文件名错误' + str(f))

    def thread_request(self):
        try:
            global d
            self.getAllPicUrl()
            for d in (1, len(self.list)):
                ts = [Thread(target=self.getSinglePic, args=(i,)) for i in self.list]
                print('开始下载')
                for it in ts:
                    it.start()
                    time.sleep(random.uniform(0.1, 0.3))
                print('\033[2;32m等待子进程结束中...\033[0m')
                for it in ts:
                    it.join()
                print('下载完成!')
                exit()
        except requests.exceptions.ChunkedEncodingError:
            print('\033[2;32m网络请求失败,并不代表程序已中断\033[0m')

    def main(self):
        global path
        # path = 'F:/two_dimension/Rankings/%s/' % datetime.date.today()
        with open('name.json', mode='r', encoding='UTF-8') as f:
            path = json.load(f).get('dirs').get('Rankings')
            path = (path + '%s/' % datetime.date.today())
        if os.path.exists(path) is False:
            os.mkdir(path)
            print('已创建文件夹,准备下载\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
            os.system('start {}'.format(path))
            self.thread_request()
        else:
            print('当前路径存在,地址为:\033[2;32m%s\033[0m\n准备下载...' % path)
            os.system('start {}'.format(path))
            self.thread_request()

if __name__ == '__main__':
    # 实例化后将执行类方法的 main 函数
    pixiv = Leaderboard()


"""============================================================================"""
#
# headers = {
#      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
#      'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
#  }
#
#
#
# def getSinglePic(url):
#     global d
#     response = requests.get(url, headers=headers)
#     # 提取图片名称
#     name = re.search('"illustTitle":"(.+?)"', response.text).group(1)
#     name = name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_')
#     name = name.replace('.', '').replace('|', '_').replace('/','_')
#     name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
#     # 提取图片原图地址
#     picture = re.search('"original":"(.*?)"},', response.text,re.S)
#     pic = requests.get(picture.group(1), headers=headers)
#     if not os.path.exists(path + '%s.%s' % (name.replace('\\', '_'), picture.group(1)[-3:])):
#         with open(path + '%s.%s' % (name.replace('\\', '_'), picture.group(1)[-3:]),mode='wb') as f:
#             f.write(pic.content)
#     else:
#         with open(path + '%s(%d).%s' % (name.replace('\\', '_'),d , picture.group(1)[-3:]),mode='wb') as f:
#             f.write(pic.content)
#             d += 1
#
# def getAllPicUrl():
#     try:
#         print('\033[2;32m写入任务列表中...', end='')
#         for n in range(1, 10 + 1):
#             url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=%d&format=json' % n
#             response = requests.get(url, headers=headers)
#             illust_id = re.findall('"illust_id":(\d+?),', response.text)
#             picUrl = ['https://www.pixiv.net/artworks/' + i for i in illust_id]
#             for url in picUrl:
#                 list.append(url)
#         print('写入完成...共 %d 张图片\033[0m' % len(list))
#         return None
#     except OSError as f:
#         print('文件名错误' + str(f))
#
# def thread_request():
#     try:
#         global d
#         getAllPicUrl()
#         for d in (1,len(list)):
#             ts = [Thread(target=getSinglePic,args=(i,)) for i in list]
#             print('开始下载')
#             for it in ts:
#                 it.start()
#                 time.sleep(random.uniform(0.1,0.3))
#             print('\033[2;32m等待子进程结束中...\033[0m')
#             for it in ts:
#                 it.join()
#             print('下载完成!')
#             exit()
#     except requests.exceptions.ChunkedEncodingError:
#         print('\033[2;32m网络请求失败,并不代表程序已中断\033[0m')
#
# def main():
#     global path
#     # path = 'F:/two_dimension/Rankings/%s/' % datetime.date.today()
#     with open('name.json', mode='r', encoding='UTF-8') as f:
#         path = json.load(f).get('dirs').get('Rankings')
#         path = (path + '%s/' % datetime.date.today())
#     if os.path.exists(path) is False:
#         os.mkdir(path)
#         print('已创建文件夹,准备下载\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
#         # os.system('start {}'.format(path))
#         thread_request()
#     else:
#         print('当前路径存在,地址为:\033[2;32m%s\033[0m\n准备下载...' % path)
#         # os.system('start {}'.format(path))
#         thread_request()
#
# if __name__ == '__main__':
#     main()