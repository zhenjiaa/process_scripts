from posix import sched_param
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
        # self.info = {'description': 'PCB DATASET',
        #         'url': 'DLH',
        #         'version': '1.0',
        #         'year': 2021,
        #         'contributor': 'DLHgroup',
        #          'date_created': '2021-01-12 16:11:52.357475'
        #          }
        # self.license = {
        # "url": "none",
        # "id": 1,
        # "name": "Attribution-NonCommercial-ShareAlike License"}

        self.images = None
        self.annotations = None
        self.category = categories
        self.cocoJasonDict = { "annotations" : self.annotations}
	
    def getDict(self):
        self.cocoJasonDict = {"annotations": self.annotations}
        return self.cocoJasonDict








if __name__ == '__main__':
    jsonFile = 'pp_yolo.json'
    jasonDir,_ = os.path.split(jsonFile)
    # 告诉你 最新的Jason 文件保存到了那里
    print(f'jsonFile saved {jsonFile}')



    # images 段 的字典模板
    images = {	"license":3,
	"file_name":"COCO_val2014_000000391895.jpg",
	"coco_url":"",
	"height":360,"width":640,"date_captured":"2013-11-14 11:18:45",
	"id":0 }

    # annotation 段 的字典模板
    an = {"image_id": 0, "bbox": [], "category_id": 0,
          "score":0}

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
    txtPath = 'test.txt'

    with open(txtPath,'r') as re:
        txtlines = re.readlines()
        for txtline in txtlines:
            # 去出  \n 之类的空格
            temp = txtline.rstrip().lstrip().split(' ')
            # 分别的到 目标的类 中心值 xy  和  该检测框的宽高
            image_name = temp[0]
            img_id = int(image_name.split('.')[0])
            classid = int(temp[1])
            x = float(temp[3]) 
            y = float(temp[4]) 
            x1 = float(temp[5]) 
            y1 = float(temp[6])
            score = float(temp[2])
            # 复制annotation 的字典 
            temp_an = an.copy()
            temp_an['score'] = score
            temp_an['image_id'] = img_id
            temp_an['bbox'] = [x,y,x1-x,y1-y]
            temp_an['category_id'] = classid
            annoation_list.append(temp_an)
        # 图像的id

    # print(js.getDict())
    # print('***********************************************************************\n\n')
    # 将json 的实例 中images  赋值
    # js.images = image_lsit
    # 将json 的实例 annotations  赋值
    js.annotations = annoation_list
    # 写入文件
    json_str = json.dumps(js.getDict())
    with open(jsonFile,'w') as ww:
        json.dump(annoation_list,ww)
        
    print('finished')
