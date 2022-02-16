import os,re,json


class Repair:
    def __init__(self):
        self.download_address = json.load(open('name.json',mode='r')).get('dir').get('Pic_repair')
        print('默认保存地址为：{}'.format(self.download_address))

    def name(self,name):
        fanxu_1 = []
        for i in range(1,len(name) + 1):
            fanxu_1.append(name[len(name) - i])
        fanxu_2 = ''.join(fanxu_1)

        name = re.search(r'(.*?)/',fanxu_2).group(1)

        zhenxu_name = []
        for ii in range(1,len(name) + 1):
            zhenxu_name.append(name[len(name) - ii])
        zhenxu_name = ''.join(zhenxu_name)

        # print(zhenxu_name)
        return zhenxu_name

    def judge(self):
        pic_local_address = input(r'请输入本地图片目录地址：').replace('\\', '/')
        if os.path.isdir(pic_local_address) is True:
            # 可不写后缀
            pic_name = input(r'请输入该目录下的图片文件名：')
            if os.path.exists(pic_local_address + '/' + pic_name) is True:
                self.algorithm(pic_local_address,pic_name)
            if os.path.exists(pic_local_address + '/' + pic_name) is False:
                if os.path.exists(pic_local_address + '/' + pic_name + '.jpg') is True:
                    pic_name = pic_name + '.jpg'
                    self.algorithm(pic_local_address, pic_name)
                if os.path.exists(pic_local_address + '/' + pic_name + '.png') is True:
                    pic_name = pic_name + '.png'
                    self.algorithm(pic_local_address, pic_name)
        elif os.path.isfile(pic_local_address) is True:
            if self.name(pic_local_address)[-3:].replace('J','j').replace('P','p').replace('G','g') == 'jpg':
                present_pic_name = re.sub('jpg','png',self.name(pic_local_address))
            else:
                present_pic_name = self.name(pic_local_address)
            os.system('chcp 65001&E:/图片修复/realesrgan-ncnn-vulkan-20211212-windows/realesrgan-ncnn-vulkan.exe -i {} -o {}'.format(pic_local_address,self.download_address + present_pic_name))
            os.system('start {}&start {}'.format(self.download_address, self.download_address + present_pic_name))


    def algorithm(self,pic_local_address,pic_name):
        try:
            present_pic_name = re.sub('jpg','png',pic_name)
            os.system('chcp 65001&E:/图片修复/realesrgan-ncnn-vulkan-20211212-windows/realesrgan-ncnn-vulkan.exe -i {} -o {}'.format(pic_local_address + '/' + pic_name,self.download_address + present_pic_name))
            os.system('start {}&start {}'.format(self.download_address,self.download_address + present_pic_name))
        except ValueError:
            print('未找到该图片, 请重新输入(* - *)')
            print(ValueError)


if __name__ == '__main__':
    pic = Repair()
    pic.judge()