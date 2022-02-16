import re,json,requests
from urllib import parse
from fake_useragent import UserAgent

class ID:
    def __init__(self):
        self.url = 'https://www.pixiv.net/artworks/'
        self.user_url = 'https://www.pixiv.net/users/{}'
        self.artworks()

    def headers(self):
        header = {
            'referer': 'https://www.pixiv.net/',
            'user-agent': str(UserAgent().random)
        }
        return header

    def headers_cookie(self):
        headers = {
            'referer': 'https://www.pixiv.net/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'cookie': json.load(open('name.json',mode='r')).get('cookie'),
        }
        return headers

    def artworks(self):
        srtworksid_or_nickname = input('请输入作品ID号 或 画师昵称:')
        try:
            if srtworksid_or_nickname.isdigit() is True:
                url = self.url + srtworksid_or_nickname
                resp = requests.get(url,headers = self.headers())
                user_id = re.search(r'"authorId":"(.*?)"',resp.text).group(1)
                print('Painter Homepage url is: {}'.format(self.user_url.format(user_id)))
                print('user id is: {}'.format(user_id))
            else:
                url = 'https://www.pixiv.net/search_user.php?s_mode=s_usr&nick={}&nick_mf=1'.format(parse.quote(srtworksid_or_nickname))
                resp = requests.get(url,headers=self.headers_cookie())
                user_id = re.search(r'href="/users/(\d+)"class="_user-icon size-128 cover-texture ui-scroll-view"',resp.text)
                if user_id is not None:
                    print('Painter Homepage url is: {}'.format(self.user_url.format(user_id.group(1))))
                    print('user id is: {}'.format(user_id.group(1)))
                else:
                    print('没有获取到画师 id 请确认昵称是对的...')
        except AttributeError:
            print('该ID不是作品ID')

if __name__ == '__main__':
    id = ID()