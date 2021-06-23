

import os
import cv2



need_cat = ['0','15','16']   #需要的类             #coco 中人猫狗分别是0，15，16
showimg = True


root_path ='./320/coco_chair_labels'                # 源txt路径
img_path = '/home/zhenjia/work/lzj/data/chair_1766/'       # 图片路径，读取wh
save_path = './320/coco_chair_result.txt'              #存放路径

save_txt = open(save_path,'w')

count =0
for file_name in os.listdir(img_path):
    print(file_name)

    img_name = os.path.join(img_path,file_name)
    img = cv2.imread(img_name)
    img_w,img_h = img.shape[1],img.shape[0]

    txt_name = os.path.join(root_path,file_name[:-4]+'.txt')
    try:
        result_txt = open(txt_name,'r').readlines()
    except:
        continue
    flag = 0

    for line in result_txt:
        # print(line)
        line = line.strip().split(' ')
        if line[0] in need_cat:
            flag = 1
            
            new_class = need_cat.index(line[0])
            x,y,w,h = float(line[1]),float(line[2]),float(line[3]),float(line[4])
            xmin = int((x-w/2)*img_w)
            xmax = int((x+w/2)*img_w)
            ymin = int((y-h/2)*img_h)
            ymax = int((y+h/2)*img_h)
            new_line = file_name+' '+str(new_class)+' '+line[5]+' '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+'\n'
            save_txt.write(new_line)
            if showimg:
                img = cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(0,0,255),5)
    if showimg and flag:
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image',1000,800)
        cv2.imshow('image',img)
        cv2.waitKey(1000)
print(count)
            

    