# -*- coding:utf-8 -*-
# Author: Li

import os
import nms
import numpy as np
import cv2

showimg = True

root_path ='/home/zhenjia/work/paddle_result/ppyolotiny_320/2404'
image_path ='/home/zhenjia/work/lzj/data/2404'        
save_path = 'test.txt'              #存放路径 

# coco_label =

save_txt = open(save_path,'w')
for file_ in os.listdir(image_path):
    image_file = os.path.join(image_path,file_)
    txt_file = os.path.join(root_path,file_[0:-4]+'.txt')
    
    try:
        txt_reader = open(txt_file,'r').readlines()
    except:
        continue
    person = []
    cat = []
    dog = []
    for line in txt_reader:
        line = line.strip().split(' ')
        try:
            score = float(line[1])
            x1 = float(line[2])
            y1 = float(line[3])
            x2 = float(line[2])+float(line[4])
            y2 = float(line[3])+float(line[5])
        except:
            score = float(line[2])
            x1 = float(line[3])
            x2 = float(line[3])+float(line[5])
            y2 = float(line[4])+float(line[6])
        box = [x1,y1,x2,y2,score]
        if line[0]=='person':
            person.append(box)
        if line[0]== 'cat':
            cat.append(box)
        if line[0]=='dog':
            dog.append(box)
    if len(person)!=0:
        person = np.array(person)
        person = person[nms.py_cpu_nms(person,0.5)]
        person = person.tolist()
    if len(cat)!=0:
        cat = np.array(cat)
        cat = cat[nms.py_cpu_nms(cat,0.5)]
        cat = cat.tolist()
    if len(dog)!=0:
        dog = np.array(dog)
        dog = dog[nms.py_cpu_nms(dog,0.5)]
        dog = dog.tolist()


    for box in person:
        line = file_+' 0 '+str(box[4])+' '+str(int(box[0]))+' '+str(int(box[1]))+' '+str(int(box[2]))+ ' ' +str(int(box[3]))+'\n'
        save_txt.write(line)
    for box in cat:
        line = file_+' 1 '+str(box[4])+' '+str(int(box[0]))+' '+str(int(box[1]))+' '+str(int(box[2]))+ ' ' +str(int(box[3]))+'\n'
        save_txt.write(line)
    for box in dog:
        line = file_+' 2 '+str(box[4])+' '+str(int(box[0]))+' '+str(int(box[1]))+' '+str(int(box[2]))+ ' ' +str(int(box[3]))+'\n'
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
            