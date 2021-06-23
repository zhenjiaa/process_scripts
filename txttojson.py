import cv2
from math import *
import numpy as np
import os, random, shutil
import glob as gb
from time import sleep
import copy
import json


def copyFile2Folder(srcfile,dstfolder):
    '''
    复制文件到指定文件夹，名字和以前相同
    Args:
        srcfile: '/home/wsd/***/yolov5/data/PCB_DATASET/labels/Spur/04_spur_06.txt'  文件的绝对路径
        dstfile: '/home/wsd/***/yolov5/data/PCB_DATASET/train/labels'  文件夹

    Returns:

    '''

    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))

    else:
        src_fpath, src_fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstfolder):
            os.makedirs(dstfolder)  # 创建路径dst_file

        dst_file =os.path.join(dstfolder, src_fname)
        shutil.copyfile(srcfile, dst_file)  # 复制文件
        print ("copy %s -> %s" % (srcfile, dst_file))
        return dst_file



class cocoJsaon(object):
    '''
    coco 的json 的文件格式类
    '''
    def __init__(self,categories):
        self.info = {'description': 'PCB DATASET',
                'url': 'DLH',
                'version': '1.0',
                'year': 2021,
                'contributor': 'DLHgroup',
                 'date_created': '2021-01-12 16:11:52.357475'
                 }
        self.license = {
        "url": "none",
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License"}

        self.images = None
        self.annotations = None
        self.category = categories
        self.cocoJasonDict = {"info": self.info, "images": self.images, "annotations" : self.annotations, "licenses" : self.license,'categories':self.category}
	
    def getDict(self):
        self.cocoJasonDict = {"info": self.info, "images": self.images, "annotations": self.annotations,
                              "licenses": self.license,'categories':self.category}
        return self.cocoJasonDict








if __name__ == '__main__':


    # 文件原本：
    '''
    root: /home/dlh/opt/***/PCB_DATASET
                    ------------------->labels/  # 原本的所有目标检测框的   *.txt
                    ------------------->images/   #  *.jpg  所有的图片
                    ------------------->ImageSets/  # train.txt  和  val.txt
                    ------------------->annotations  /  存放 labels 下所有对应的train.json
                    
    最终：
    root: /home/dlh/opt/***/PCB_DATASET/PCB   
                        ------------------->images/   #  *.jpg  所有的图片
                        ------------------->annotations  /  instances_train_set_name.json   # 存放 labels 下所有对应的train.json
                                                         /  instances_val_set_name.json     # 存放 labels val.json
    
    
    '''

    # 写入的train 还是Val    （修改）
    wrtie_str = 'train'
    # 存放 train.txt  和  val.txt  的绝对地址    （修改）
    # Imageset = '/home/dlh/opt/dinglinhe/PCB_DATASET/ImageSets/' + wrtie_str+'.txt'
    # # 存放 即将所有的原本图片  保存到 该地址  临时       （修改）
    # tarset = '/home/dlh/opt/dinglinhe/PCB_DATASET/' + wrtie_str + '_set_name'
    
    # # 下面是更改 json 文件 的  
    # tempDir = Imageset.replace('txt','json')
    # tempDir = tempDir.replace('ImageSets', 'annotations')
    # jsonFile = tempDir.replace(wrtie_str, 'instances_' + wrtie_str + '_set_name')
    jsonFile = '11.json'
    jasonDir,_ = os.path.split(jsonFile)
    # 告诉你 最新的Jason 文件保存到了那里
    print(f'jsonFile saved {jsonFile}')


    # 检查目标文件夹是否存在
    #if not os.path.exists(tarset):
       # os.makedirs(tarset)
    #if not os.path.exists(jasonDir):
        #os.makedirs(jasonDir)


    # images 段 的字典模板
    images = {	"license":3,
	"file_name":"COCO_val2014_000000391895.jpg",
	"coco_url":"",
	"height":360,"width":640,"date_captured":"2013-11-14 11:18:45",
	"id":0 }

    # annotation 段 的字典模板
    an = {"segmentation": [],
          "iscrowd": 0,
          "keypoints": 0,
          "image_id": 0, "bbox": [], "category_id": 0,
          "id": 0}

    # categories 段 的字典模板
    cate_ = {
        'id':0,
        'name':'a',
    }

    # 用来保存目标类的  字典
    cate_list = []
    # 你的目标类有几个  （修改）
    className = ['missing_hole', 'mouse_bite', 'open_circuit', 'short', 'spur']
    temId = 0
    for idName in className:
        tempCate = cate_.copy()
        tempCate['id'] = temId
        temId += 1
        tempCate['name'] = idName

        cate_list.append(tempCate)

    # print(cate_list)
    # 船舰coco json 的类 实例
    js = cocoJsaon(cate_list)

    image_lsit = []
    annoation_list =[]



    # 打开 train。txt
    #with open(Imageset, 'r') as f:
    #    lines = f.readlines()

    img_id = 0
    bbox_id = 0
    # 按值去打开图片
    dirpath = '/home/rd/lizhenjia/data/test2017'
    txt_dir = '/home/rd/lizhenjia/workspace/yolov5/runs/detect/exp5/labels'
    for file_ in os.listdir(dirpath):
        # 我的train.txt 是按照绝对路径保存的，各位需要的根据自己的实际情况来修改这里的代码
        # 去出  \n 之类的空格
        path = os.path.join(dirpath,file_)
        # 打开图片
        image = cv2.imread(path)
        # 将这个图片副知道新的文件夹  （以实际情况  修改）
        # copyFile2Folder(path,tarset)
        # 得到宽高
        (height, width) = image.shape[:2]
        # 得到文件名子
        _,fname = os.path.split(path)
        # 图像对应的txt 文件路径
        txtPath = path.replace('jpg','txt')
        txtPath = os.path.join(txt_dir,txtPath.split('/')[-1])
        # 复制images 的字典的复制        
        image_temp = images.copy()
        image_temp['file_name'] = fname
        image_temp['height'] = height
        image_temp['width'] = width
        image_temp['id'] = img_id
        # 将其放入到集合中
        image_lsit.append(image_temp)
        # 打开图片的对应的txt 目标文件的txt
        if not os.path.exists(txtPath):
            continue
        with open(txtPath,'r') as re:
            txtlines = re.readlines()
            for txtline in txtlines:
                # 去出  \n 之类的空格
                temp = txtline.rstrip().lstrip().split(' ')
                # 分别的到 目标的类 中心值 xy  和  该检测框的宽高
                classid = int(temp[0])
                x = float(temp[1]) * width
                y = float(temp[2]) * height
                w = float(temp[3]) * width
                h = float(temp[4]) * height
                # 复制annotation 的字典 
                temp_an = an.copy()
                temp_an['image_id'] = img_id
                temp_an['bbox'] = [x,y,w,h]
                temp_an['category_id'] = classid
                temp_an['id'] = bbox_id
                bbox_id += 1 # 这个是 这个annotations 的id 因为一个图像可能对应多个 目标的id
                annoation_list.append(temp_an)
        # 图像的id
        img_id += 1

    # print(js.getDict())
    # print('***********************************************************************\n\n')
    # 将json 的实例 中images  赋值
    js.images = image_lsit
    # 将json 的实例 annotations  赋值
    js.annotations = annoation_list
    # 写入文件
    json_str = json.dumps(js.getDict())
    with open(jsonFile,'w+') as ww:
        ww.write(json_str)
        
    print('finished')
