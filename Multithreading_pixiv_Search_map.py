import requests
import re,random,time
import os,json
from threading import Thread


class Search_map:
    def __init__(self):
        proxies = json.load(open('name.json', mode='r')).get('proxies')
        self.proxies = eval(proxies)
        self.main()

    def headers(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "referer": "https://www.pixiv.net",
            "cookie": json.load(open('name.json', mode='r')).get('cookie'),
        }
        return headers

    def request(self,id):
        global d
        pic = requests.get('https://www.pixiv.net/artworks/' + id)
        name_1 = re.search('"illustTitle":"(.+?)"', pic.text).group(1)
        name = name_1.strip('?').replace('*', '').replace('|', '_').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_')
        name = name.replace('.', '').replace('\\', '').replace('/', '_')
        name = name.replace('\u0027', '_').replace('\u3000', '_')
        # 提取图片源地址
        picture = re.search('"original":"(.*?)"},', pic.text, re.S)
        piic = requests.get(picture.group(1), headers=self.headers())
        if not os.path.exists(path + name + '.' + picture.group(1)[-3:]):
            with open(path + name.replace(r'/', '_').strip(r'*') + '.' + picture.group(1)[-3:], mode='wb') as f:
                f.write(piic.content)
        else:
            with open(path + name.replace(r'/', '_').strip(r'*') + '(' + str(d) + ')' + '.' + picture.group(1)[-3:],
                      mode='wb') as f:
                f.write(piic.content)
                d += 1

    def s(self):
        try:
            global i, d
            url = f'https://www.pixiv.net/ajax/search/artworks/{i}%201000users?word={i}%201000users&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh'
            resp = requests.get(url, headers=self.headers())
            body = resp.json().get('body')
            illustManga = body.get('illustManga')
            data = illustManga.get('data')

            if data != []:
                print('\033[2;32m获取图片地址成功\033[0m')
                print('任务写入列表中...', end='')
                # 创建任务列表
                list = []
                for t in data:
                    id = t.get('id')
                    list.append(id)
                for d in (1, len(list)):
                    ts = [Thread(target=self.request, args=(i,)) for i in list]
                    print('共 %d 张插画\n正在下载...' % len(list))
                    for it in ts:
                        it.start()
                        time.sleep(random.uniform(0.1, 0.3))
                    print('正在等待子进程结束...')
                    for n in ts:
                        n.join()
                    print('\033[2;32m已将该页面内所有的图片下载完成~\033[0m')
                    break
                    # exit()
            else:
                print('输入的专栏未被找到 qaq\n已删除当前路径')
                os.rmdir(path)
                print('请重新输入 (*´-`)')
                self.main()
        except requests.exceptions.ProxyError:
            print('网络错误,请检查网络配置')
        except requests.exceptions.ChunkedEncodingError:
            print('\033[2;32m网络请求失败,并不代表程序已中断\033[0m')

    def main(self):
        global path, i
        # 下载地址
        i = str(input('请输入你想下载的专栏:'))
        with open('name.json', mode='r', encoding='UTF-8') as f:
            path = json.load(f).get('dirs').get('专栏')
            path = (path + '%s/' % i)
        if os.path.exists(path) is False and requests.get(f'https://www.pixiv.net/ajax/search/artworks/{i}%201000users?word={i}%201000users&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh').json()['body']['illustManga']['data'] != []:
            os.mkdir(path)
            print('已创建文件夹,准备下载...\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
            os.system('start {}'.format(path.replace('/', '\\')))
            self.s()
        elif os.path.exists(path) is True:
            print('当前路径已存在,准备下载...\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
            os.system('start {}'.format(path.replace('/', '\\')))
            self.s()
        else:
            print('啊咧咧,请问您输入的是鬼嘛 (*^-^)')
            # exit()

if __name__ == '__main__':
    # 实例化后运行类方法中的 main 函数
    pixiv = Search_map()



"""======================================================="""
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
#     "referer": "https://www.pixiv.net",
#     "cookie": json.load(open('name.json',mode='r')).get('cookie'),
# }
#
#
# def request(id):
#     global d
#     pic = requests.get('https://www.pixiv.net/artworks/' + id)
#     name_1 = re.search('"illustTitle":"(.+?)"', pic.text).group(1)
#     name = name_1.strip('?').replace('*', '').replace('|','_').replace('<','_').replace('>','_').replace('"','_').replace(':','_')
#     name = name.replace('.', '').replace('\\', '').replace('/','_')
#     name = name.replace('\u0027', '_').replace('\u3000', '_')
#     # 提取图片源地址
#     picture = re.search('"original":"(.*?)"},', pic.text, re.S)
#     piic = requests.get(picture.group(1),headers=headers)
#     if not os.path.exists(path + name + '.' + picture.group(1)[-3:]):
#         with open(path + name.replace(r'/', '_').strip(r'*') + '.' + picture.group(1)[-3:], mode='wb') as f:
#             f.write(piic.content)
#     else:
#         with open(path + name.replace(r'/', '_').strip(r'*') + '(' + str(d) + ')' + '.' + picture.group(1)[-3:], mode='wb') as f:
#             f.write(piic.content)
#             d += 1
#
# def s():
#     try:
#         global i,d
#         url = f'https://www.pixiv.net/ajax/search/artworks/{i}%201000users?word={i}%201000users&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh'
#         resp = requests.get(url, headers=headers)
#         body = resp.json().get('body')
#         illustManga = body.get('illustManga')
#         data = illustManga.get('data')
#
#         # if body and illustManga and 'id' is not None:
#         if data != []:
#             print('\033[2;32m获取图片地址成功\033[0m')
#             print('任务写入列表中...',end='')
#             list = []
#             for t in data:
#                 id = t.get('id')
#                 list.append(id)
#             for d in (1,len(list)):
#                 ts = [Thread(target=request, args=(i,)) for i in list]
#                 print('共 %d 张插画\n正在下载...' % len(list))
#                 for it in ts:
#                     it.start()
#                     time.sleep(random.uniform(0.1, 0.3))
#                 print('正在等待子进程结束...')
#                 for n in ts:
#                     n.join()
#                 print('\033[2;32m已将该页面内所有的图片下载完成~\033[0m')
#                 exit()
#         else:
#             print('输入的专栏未被找到 qaq\n已删除当前路径')
#             os.rmdir(path)
#             print('请重新输入 (*´-`)')
#             main()
#     except requests.exceptions.ProxyError:
#         print('网络错误,请检查网络配置')
#     except requests.exceptions.ChunkedEncodingError:
#         print('\033[2;32m网络请求失败,并不代表程序已中断\033[0m')
#
# def main():
#     global path,i
#     # 下载地址
#     i = str(input('请输入你想下载的专栏：'))
#     # path = 'F:/two_dimension/专栏/%s/' % i
#     with open('name.json', mode='r', encoding='UTF-8') as f:
#         path = json.load(f).get('dirs').get('专栏')
#         path = (path + '%s/' % i)
#     if os.path.exists(path) is False and requests.get(f'https://www.pixiv.net/ajax/search/artworks/{i}%201000users?word={i}%201000users&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh').json()['body']['illustManga']['data'] != []:
#         os.mkdir(path)
#         print('已创建文件夹,准备下载...\n地址为:\033[2;32m%s\033[0m' % path.replace('/', '\\'))
#         # os.system('start {}'.format(path.replace('/', '\\')))
#         s()
#     elif os.path.exists(path) is True:
#         print('当前路径已存在,准备下载...\n地址为:\033[2;32m%s\033[0m' % path.replace('/','\\'))
#         # os.system('start {}'.format(path.replace('/', '\\')))
#         s()
#     else:
#         print('啊咧咧,请问您输入的是鬼嘛 (*^-^)')
#         exit()
#
#
# if __name__ == '__main__':
#    main()