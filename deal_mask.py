import cv2
import os
import numpy as np
import copy
import random


src_path = '/home/rd/lizhenjia/workspace/project/train_data/3060张验收合格文件'

person= np.array([[255,0,0],[180,0,0],[120,0,0],[80,0,0],[255,50,0],[180,50,0],[255,0,50],[180,0,50]])
cat = np.array([[0,255,0],[0,180,0],[0,120,0],[0,80,0],[0,255,50],[0,180,50],[50,255,0],[50,180,0]])
dog = np.array([[0,0,255],[0,0,180],[0,0,120],[0,0,80],[0,50,255],[0,50,180],[50,0,255],[50,0,180]])

black = np.array([0,0,0])

def get_box(image,color):
    b,g,r = cv2.split(image) # 分解Opencv里的标准格式B、G、R
    image = cv2.merge([r,g,b])
    w,h = image.shape[1],image.shape[0]
    k = np.zeros((h,w,3))
    k[(image==color)]=1
    b,g,r = cv2.split(k)
    im = b+g+r
    k = np.zeros((h,w))
    k[(im==3)]= 255
    k = k.astype(np.uint8)
    kdddd = random.randint(0,10000)
    
    

    contours, hierarchy = cv2.findContours(k, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # if np.sum(k)>0:
    #     cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
    #     cv2.imwrite('/home/zhenjia/lzj/wddw/1da/111/'+str(kdddd)+'.jpg',image)
    
    if len(contours)==1:
        x,y,w,h = cv2.boundingRect(contours[0])
        return x,y,x+w,x+h
    elif len(contours)>1:
        bboxes=[cv2.boundingRect(cnt)for cnt in contours]
        x1 = w
        y1 = h
        x2 = 0
        y2 = 0
        for bbox in bboxes:
            x1 = min(bbox[0],x1)
            y1 = min(bbox[1],y1)
            x2 = max(bbox[0]+bbox[2],x2)
            y2 = max(bbox[1]+bbox[3],y2)
        return x1,y1,x2,y2
    return -1,-1,-1,-1





                

count = 0
for root,_,files in os.walk(src_path):
    for file in files:
        if file.endswith('_mask.png'):
            count+=1
            print(count)
            # if count<1220:
            #     continue
            print(file)
            txt = os.path.join(root,file.split('_mask.png')[0]+'.txt')
            lrtb_txt = os.path.join(root,file.split('_mask.png')[0]+'lrtb.txt')
            lrtb_txt_file = open(lrtb_txt,'w')
            txt_file = open(txt,'w')
            try:
                image_name = os.path.join(root,file)
                image = cv2.imread(image_name)
                w,h = image.shape[1],image.shape[0]
                i = 1
                for i in range(8):
                    # print(i)
                    ### lrtb格式
                    # x1,y1,x2,y2=get_box(image,person[i])
                    # if x1!=-1:
                    #     lrtb_txt_file.write('0 lrtb ='+str(x1)+' '+str(x2)+' '+str(y1)+' '+str(y2)+'\n')
                    # x1,y1,x2,y2=get_box(image,cat[i])
                    # if x1!=-1:
                    #     lrtb_txt_file.write('1 lrtb ='+str(x1)+' '+str(x2)+' '+str(y1)+' '+str(y2)+'\n')
                    # x1,y1,x2,y2=get_box(image,dog[i])
                    # if x1!=-1:
                    #     lrtb_txt_file.write('2 lrtb ='+str(x1)+' '+str(x2)+' '+str(y1)+' '+str(y2)+'\n')



                    #############yolo格式
                    x1,y1,x2,y2=get_box(image,person[i])
                    if x1!=-1:
                        x = (x1+x2)/(2.*w)
                        y = (y1+y2)/(2.*h)
                        w_ =(x2-x1)/float(w)
                        h_ =(y2-y1)/float(h)
                        txt_file.write('0 '+str(x)+' '+str(y)+' '+str(w_)+' '+str(h_)+'\n')
                        lrtb_txt_file.write('0 lrtb = '+str(x1)+' '+str(x2)+' '+str(y1)+' '+str(y2)+'\n')
                        # cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,255),5) 
                    x1,y1,x2,y2=get_box(image,cat[i])
                    if x1!=-1:
                        x = (x1+x2)/(2.*w)
                        y = (y1+y2)/(2.*h)
                        w_ =(x2-x1)/float(w)
                        h_ =(y2-y1)/float(h)
                        txt_file.write('1 '+str(x)+' '+str(y)+' '+str(w_)+' '+str(h_)+'\n')
                        lrtb_txt_file.write('1 lrtb = '+str(x1)+' '+str(x2)+' '+str(y1)+' '+str(y2)+'\n')
                        # cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),5) 
                    x1,y1,x2,y2=get_box(image,dog[i])
                    if x1!=-1:
                        x = (x1+x2)/(2.*w)
                        y = (y1+y2)/(2.*h)
                        w_ =(x2-x1)/float(w)
                        h_ =(y2-y1)/float(h)
                        txt_file.write('2 '+str(x)+' '+str(y)+' '+str(w_)+' '+str(h_)+'\n')
                        lrtb_txt_file.write('2 lrtb = '+str(x1)+' '+str(x2)+' '+str(y1)+' '+str(y2)+'\n')
            except:
                continue
                        # cv2.rectangle(image,(x1,y1),(x2,y2),(255,255,0),5) `