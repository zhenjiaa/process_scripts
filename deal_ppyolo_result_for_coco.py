# -*- coding:utf-8 -*-
# Author: Li

import os
import nms
import numpy as np
import cv2

showimg = False

root_path ='output'
image_path ='output'        
save_path = 'test.txt'              #存放路径 

coco_label = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush' ]
coco_cat = [1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,27,28,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,67,70,72,73,74,75,76,77,78,79,80,81,82,84,85,86,87,88,89,90]
print(len(coco_cat))
print(coco_label[22])
save_txt = open(save_path,'w')
for file_ in os.listdir(image_path):
    image_file = os.path.join(image_path,file_)
    txt_file = os.path.join(root_path,file_[0:-4]+'.txt')
    
    try:
        txt_reader = open(txt_file,'r').readlines()
    except:
        continue
    coco_detect = [[] for j in range(80)]
    for line in txt_reader:
        line = line.strip().split(' ')
        len_ = len(line)
        # print(len_)
        if len_==6:
            class_ = line[0]
            score = float(line[1])
            x1 = float(line[2])
            y1 = float(line[3])
            x2 = float(line[2])+float(line[4])
            y2 = float(line[3])+float(line[5])
        if len_==7:
            class_ = line[0]+' '+line[1]
            score = float(line[2])
            x1 = float(line[3])
            y1 = float(line[4])
            x2 = float(line[3])+float(line[5])
            y2 = float(line[4])+float(line[6])
        box = [x1,y1,x2,y2,score]
        cls_id = coco_label.index(class_)
        coco_detect[cls_id].append(box)
    # for i in range(80):
    #     if len(coco_detect[i])!=0:
    #         coco_detect[i] = np.array(coco_detect[i])
    #         coco_detect[i] = coco_detect[i][nms.py_cpu_nms(coco_detect[i],0.5)]
    #         coco_detect[i] = coco_detect[i].tolist()
    for i in range(80):
        if len(coco_detect[i])!=0:
            for box in coco_detect[i]:
                line = file_+' '+str(coco_cat[i])+' '+str(box[4])+' '+str(int(box[0]))+' '+str(int(box[1]))+' '+str(int(box[2]))+ ' ' +str(int(box[3]))+'\n'
                save_txt.write(line)


    if showimg:
        img = cv2.imread(image_file)
        for xx in person:
            img = cv2.rectangle(img,(int(xx[0]),int(xx[1])),(int(xx[2]),int(xx[3])),(0,0,255),5)
        for xx in cat:
            img = cv2.rectangle(img,(int(xx[0]),int(xx[1])),(int(xx[2]),int(xx[3])),(0,0,255),5)
        for xx in dog:
            img = cv2.rectangle(img,(int(xx[0]),int(xx[1])),(int(xx[2]),int(xx[3])),(0,0,255),5)
        
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image',1000,800)
        cv2.imshow('image',img)
        cv2.waitKey(1000)
    # exit()
            