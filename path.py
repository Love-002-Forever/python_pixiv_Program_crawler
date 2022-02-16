import os,json

a = {
    'c':'C',
    'C':'C',
    'd':'D',
    'D':'D',
    'e':'E',
    'E':'E',
    'f':'F',
    'F':'F',
    'g':'G',
    'G':'G',
    'h':'H',
    'H':'H',
}

c = a.get(input('输入你想创建文件夹的磁盘名:').strip(':'))
d = input('输入自己pixiv的cookie:')
p = input('输入自己的代理地址(若没有可不填):')
if p == '':
    p = None


def pan():
    try:
        if os.path.exists('name.json') is False:
            name = '{}:/two_dimension'.format(c)
            if not os.path.exists('{}:/two_dimension'.format(c)):
                os.mkdir('{}:/two_dimension'.format(c))
                print('已创建主文件夹,路径:{}'.format(name))
                for i in range(1,50 + 1):
                    if not os.path.exists('{}/Daily_ranking'.format(name)):
                        os.mkdir('{}/Daily_ranking'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('Daily_ranking'))

                    elif not os.path.exists('{}/ID'.format(name)):
                        os.mkdir('{}/ID'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('ID'))

                    elif not os.path.exists('{}/r18_Today_date'.format(name)):
                        os.mkdir('{}/r18_Today_date'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('r18_Today_date'))

                    elif not os.path.exists('{}/r18_assign_date'.format(name)):
                        os.mkdir('{}/r18_assign_date'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('r18_assign_date'))

                    elif not os.path.exists('{}/Rankings'.format(name)):
                        os.mkdir('{}/Rankings'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('Rankings'))

                    elif not os.path.exists('{}/专栏'.format(name)):
                        os.mkdir('{}/专栏'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('专栏'))

                    elif not os.path.exists('{}/收藏图片'.format(name)):
                        os.mkdir('{}/收藏图片'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('收藏图片'))

                    elif not os.path.exists('{}/Single_picture'.format(name)):
                        os.mkdir('{}/Single_picture'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('Single_picture'))

                    elif not os.path.exists('{}/image_gif'.format(name)):
                        os.mkdir('{}/image_gif'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('image_gif'))

                    elif not os.path.exists('{}/Pic_repair'.format(name)):
                        os.mkdir('{}/Pic_repair'.format(name))
                        print('创建文件夹\033[2;32m{}\033[0m完成'.format('Pic_repair'))

                    elif not os.path.exists('name.json'):
                        path = {
                            "name": c,
                            "manga_set":True,
                            "gif_set":True,
                            "dirs":
                                {
                                    "Daily_ranking": "{}:/two_dimension/Daily_ranking/".format(c),
                                    "ID": "{}:/two_dimension/ID/".format(c),
                                    "r18_Today_date": "{}:/two_dimension/r18_Today_date/".format(c),
                                    "r18_assign_date": "{}:/two_dimension/r18_assign_date/".format(c),
                                    "Rankings": "{}:/two_dimension/Rankings/".format(c),
                                    "Single_picture": "{}:/two_dimension/Single_picture/".format(c),
                                    "专栏": "{}/专栏/".format(name),
                                    "收藏图片": "{}:/two_dimension/收藏图片/".format(c),
                                    "image_gif": "{}:/two_dimension/image_gif/".format(c),
                                    "Pic_repair": "{}:/two_dimension/Pic_repair/".format(c),
                                },
                            "proxies": "{'http':'http://%s'}" % p,
                            "cookie": d,
                        }
                        with open('name.json', mode='w', encoding='UTF-8') as f:
                            f.write(json.dumps(path, indent=4, ensure_ascii=False))
                            print('\033[2;32mjson文件创建完成\033[0m')

                    else:
                        print('你已拥有所有所需文件夹哦~')
                        exit()

            elif not os.path.exists('name.json'):
                path = {
                    "name": c,
                    "manga_set": True,
                    "gif_set": True,
                    "dirs":
                        {
                            "Daily_ranking": "{}:/two_dimension/Daily_ranking/".format(c),
                            "ID": "{}:/two_dimension/ID/".format(c),
                            "r18_Today_date": "{}:/two_dimension/r18_Today_date/".format(c),
                            "r18_assign_date": "{}:/two_dimension/r18_assign_date/".format(c),
                            "Rankings": "{}:/two_dimension/Rankings/".format(c),
                            "Single_picture": "F:/two_dimension/Single_picture/",
                            "专栏": "{}/专栏/".format(name),
                            "收藏图片": "{}:/two_dimension/收藏图片/".format(c),
                            "image_gif":"{}:/two_dimension/image_gif/".format(c),
                            "Pic_repair": "{}:/two_dimension/Pic_repair/".format(c),
                        },
                    "proxies": "{'http':'http://%s'}" % p,
                    "cookie": d,
                }
                with open('name.json', mode='w', encoding='UTF-8') as f:
                    f.write(json.dumps(path, indent=4, ensure_ascii=False))
                    print('\033[2;32mjson文件创建完成\033[0m')

            else:
                print('你已拥有所有所需文件夹哦~')

        else:
            print('\033[2;32m请删除json文件后再进行操作\033[0m')

    except OSError as o:
        print('\033[2;33m名称错误:{}\033[0m'.format(str(o)))

pan()