import re,requests,json,os,time
import zipfile,imageio

class ABC:
    def __init__(self,ID,path):
        self.proxies = eval(json.load(open('name.json', mode='r')).get('proxies'))
        self.ID = ID
        self.url = 'https://www.pixiv.net/ajax/illust/%s/ugoira_meta?lang=zh' % str(ID)
        self.path = path

    def headers(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'cookie': json.load(open('name.json',mode='r')).get('cookie'),
        }
        return headers

    def headers_refer(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'referer' : "https://www.pixiv.net/member_illust.php?"
        }
        return headers

    # 将目录最后的名字提取出来
    def extract_name(self,name):
        fanxu_1 = []
        for i in range(1,len(name) + 1):
            fanxu_1.append(name[len(name) - i])
        fanxu_2 = ''.join(fanxu_1)

        name = re.search(r'\.(.*?)/',fanxu_2).group(1)

        zhenxu_name = []
        for ii in range(1,len(name) + 1):
            zhenxu_name.append(name[len(name) - ii])
        zhenxu_name = ''.join(zhenxu_name)
        # print(zhenxu_name)
        return zhenxu_name


    # 过滤会报错的字符
    def artworks_name(self,id):
        resp = requests.get('https://www.pixiv.net/artworks/' + str(id), headers=self.headers(),proxies=self.proxies)
        name = re.search('"illustTitle":"(.+?)"', resp.text).group(1)
        name = name.strip('?').replace('*', '').replace('?', '!').replace('<', '_').replace('>', '_').replace('"','_').replace(':', '_').replace('\\', '').replace('\\\\', '').replace('.', '').replace('|', '_').replace(r'/', '_')
        name = name.replace('\u3000', '_').replace('\u0027', '_').replace("\\u0027", "'")
        return name


    def decompress(self,zip_name,delay):
        # print('zip_name:',zip_name)
        # print(os.path.join(self.path, str(self.artworks_name(self.ID)) + ".gif"))
        # 解压的文件名
        generate_name = []
        decompress_zip = zipfile.ZipFile(zip_name,mode='r')
        for file in decompress_zip.namelist():
            generate_name.append(file)
            # 全部解压到当前目录
            decompress_zip.extract(file,self.path)
        decompress_zip.close()
        # 读取图片，合成gif
        image_data = []
        for i in generate_name:
            image_data.append(imageio.imread(self.path + i))
        imageio.mimsave(os.path.join(self.path, str(self.artworks_name(self.ID)) + ".gif"),image_data, "GIF",duration=delay/1000)
        # 清除所有中间文件。
        for file in generate_name:
            os.remove(self.path + file)
        os.remove(zip_name)


    # 访问url
    def request_zip_url(self):
        # 访问带有压缩文件的网页
        resp = requests.get(self.url,headers=self.headers())
        # 获取动图所需要的帧数
        delay = [key["delay"] for key in resp.json()["body"]["frames"]]
        delay = sum(delay) / len(delay)
        # 提取压缩文件url并访问
        zip_url = resp.json()['body']['originalSrc']
        resp_zip = requests.get(zip_url, headers=self.headers_refer())
        # 下载压缩文件
        zip_name = '{}.zip'.format(self.extract_name(zip_url))
        with open(self.path + zip_name, mode='wb') as f:
            f.write(resp_zip.content)
        time.sleep(2)
        self.decompress(self.path + zip_name,delay)






if __name__ == '__main__':
    id = int(input('请输入作品ID:'))
    # path = input('请输入存储地址:')
    # print(path.replace('\\','/').strip('/') + '/')
    # A = ABC(id,path.replace('\\','/').strip('/') + '/')
    path = json.load(open('name.json',mode='r')).get('dirs').get('image_gif')
    A = ABC(id,path)
    A.request_zip_url()