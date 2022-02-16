import requests
import os, json, re
from fake_useragent import UserAgent


class download_img:
    def __init__(self):
        self.proxies = eval(json.load(open('name.json', mode='r')).get('proxies'))
        self.artworks_url = 'https://www.pixiv.net/artworks/'
        self.artworks_url_list = []
        self.url_or_int = input('请输入图片链接 或 图片ID: ')

    def path(self):
        with open('name.json', mode='r', encoding='UTF-8') as f:
            path = json.load(f).get('dirs').get('Single_picture')
            return path

    def headers(self):
        headers = {
            "User-Agent": str(UserAgent().random),
            "Referer": "https://www.pixiv.net/"
        }
        return headers

    def headers_cookie(selfs):
        headers = {
            "cookie": json.load(open('name.json',mode='r')).get('cookie'),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        }
        return headers

    def request_url(self,text,num):
        name = re.search(r'<meta property="twitter:title" content="(.*?)"', text).group(1)
        name = self.filter_name(name)
        user_name = re.search(r'"userName":"(.*?)"', text).group(1)
        user_id = re.search(r'"userId":"(.*?)"', text).group(1)
        if self.url_or_int.isdigit() is True:
            img_url = requests.get('https://www.pixiv.net/ajax/illust/%s/pages?lang=zh' % str(self.url_or_int),headers=self.headers_cookie(), proxies=self.proxies)
        else:
            img_url = requests.get('https://www.pixiv.net/ajax/illust/%s/pages?lang=zh' % str(num),headers=self.headers_cookie(), proxies=self.proxies)
        print('画师昵称: {}   ID: {}\n正在下载'.format(user_name, user_id))
        return name,user_name,user_id,img_url

    def filter_name(self,name):
        name = name.replace('*', '').replace('?', '？').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_').replace('\\', '').replace('\\\\', '')
        name = name.replace('.', '').replace('|', '_').replace(r'/', '_').replace('"','_').replace(' ','').strip(r'*')
        name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        return name

    def judgment_parameter(self):
        global num
        for num in range(1,50):
            if self.url_or_int.isdigit() is False:
                a = re.search(r'https://www.pixiv.net/artworks/(\d+)',self.url_or_int)
                v = re.search(r'(http.*?/.*?.jpg|.png)',self.url_or_int)
                if a is not None:
                    if self.url_or_int == self.artworks_url + a.group(1):
                        resp = requests.get(self.url_or_int)
                        name, user_name, user_id, img_url = self.request_url(resp.text,num=a.group(1))
                        for i in img_url.json()['body']:
                            picurl = i.get('urls').get('original')
                            self.artworks_url_list.append(picurl)
                        if len(self.artworks_url_list) > 3:
                            for ii in self.artworks_url_list:
                                self.more_artworks_url_download(folder_name=a.group(1),img_name=self.filter_name(name),img_url=ii)
                        else:
                            for vv in self.artworks_url_list:
                                self.artworks_url_download(name, vv)
                elif v is not None:
                    self.url_download(self.url_or_int)
                else:
                    print('?')
                    break
            else:
                if self.url_or_int.isdigit() is not False:
                    if self.url_or_int == re.search(r'(\d+)',self.url_or_int).group(1):
                        url = self.artworks_url + self.url_or_int
                        resp = requests.get(url)
                        name,user_name,user_id,img_url = self.request_url(resp.text,num=None)
                        for i in img_url.json()['body']:
                            picurl = i.get('urls').get('original')
                            self.artworks_url_list.append(picurl)
                        if len(self.artworks_url_list) > 3:
                            for ii in self.artworks_url_list:
                                # 传入三个参数 作品ID , 图片昵称 , 图片url
                                self.more_artworks_url_download(folder_name=self.url_or_int, img_name=self.filter_name(name), img_url=ii)
                        else:
                            for vv in self.artworks_url_list:
                                self.artworks_url_download(name, vv)
            print('下载完成\n共下载 {} 张插画'.format(len(self.artworks_url_list)))
            break

    def more_artworks_url_download(self,folder_name,img_name,img_url):
        global num
        resp = requests.get(img_url, headers=self.headers(), proxies=self.proxies)
        folder = self.path() + '作品ID_' + folder_name + '/'
        if not os.path.exists(folder):
            os.mkdir(folder)
        if not os.path.exists(folder + img_name + '.' + img_url[-3:]):
            with open(folder + img_name + '.' + img_url[-3:], mode='wb') as f:
                f.write(resp.content)
            os.system('start {}'.format(folder))
        else:
            with open(folder + img_name + '({})'.format(str(num)) + '.' + img_url[-3:], mode='wb') as f:
                f.write(resp.content)
                num += 1

    def artworks_url_download(self,name,img_url):
        global num
        resp = requests.get(img_url, headers=self.headers(), proxies=self.proxies)
        if not os.path.exists(self.path() + name + '.' + img_url[-3:]):
            img_name = name + '.' + img_url[-3:]
            with open(self.path() + img_name, mode='wb') as f:
                f.write(resp.content)
            os.system('start {}&start {}'.format(self.path(),self.path() + img_name))
        else:
            with open(self.path() + name + '({})'.format(str(num)) + '.' + img_url[-3:], mode='wb') as f:
                f.write(resp.content)
                num += 1
            os.system('start {}'.format(self.path()))

    def url_download(self,url):
        resp = requests.get(url, headers=self.headers(),proxies=self.proxies)
        a = input('定义即将保存的图片名称：')
        with open(self.path() + '%s.%s' % (a,url[-3:]),mode='wb') as f:
            f.write(resp.content)
        self.artworks_url_list.append(url)
        os.system('start {}&start {}'.format(self.path(),self.path() + '%s.%s' % (a,url[-3:])))


if __name__ == '__main__':
    download = download_img()
    download.judgment_parameter()