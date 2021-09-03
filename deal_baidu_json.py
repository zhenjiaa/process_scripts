import json
import os
import shutil
import cv2

#/home/nas01/chunsheng/datasets/pos/Objects365/Annotations/
json_file =json.load(open('/home/zhenjia/lzj/wddw/dog_cat_dataset/baidu-6972张猫狗实例分割数据/annotations/baidu_v1_wapdg_train_cocofied.json','r'))
save_path = '/home/zhenjia/lzj/wddw/dog_cat_dataset/baidu-6972张猫狗实例分割数据/annotations/train/lrtb'
if os.path.exists(save_path):
    shutil.rmtree(save_path)
os.makedirs(save_path)
yolo_save_dir = '/home/zhenjia/lzj/wddw/dog_cat_dataset/baidu-6972张猫狗实例分割数据/annotations/train/yolo'
if os.path.exists(yolo_save_dir):
    shutil.rmtree(yolo_save_dir)
os.makedirs(yolo_save_dir)



# for i in json_file:
    # print(i)
print(json_file['categories'])

im_ids = dict()
for images in json_file['images']:
    im_id = int(images['id'])
    im_name = images['file_name']
    im_h = int(images['height'])
    im_w = (images['width'])
    im_ids[im_id]=[im_name,im_w,im_h]
print(len(im_ids))
cat_ids = dict()
# 

for obj in json_file['annotations']:
    im_name,im_w,im_h = im_ids[int(obj['image_id'])]
    x1 = max(round(obj['bbox'][0]),0)
    y1 = max(round(obj['bbox'][1]),0)
    x2 = min(round(obj['bbox'][0])+round(obj['bbox'][2]),im_w)
    y2 = min(round(obj['bbox'][1])+round(obj['bbox'][3]),im_h)
    cat_id = obj['category_id']
    if cat_id==1:
        cat_id =0
    elif cat_id==18:
        cat_id =2
    elif cat_id==17:
        cat_id =1
    else:
        continue
    with open(os.path.join(save_path,im_name[:-4]+'.txt'),'a+') as f:
        f.write(str(cat_id)+' lrtb = '+str(x1)+' '+str(x2)+' '+str(y1)+' '+str(y2)+'\n')

    # yolo
    dw = 1. / im_w
    dh = 1. / im_h
    x = (x1 + x2)/ 2.0 - 1
    y = (y1 + y2) / 2.0 - 1
    w = x2-x1
    h = y2-y1
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    with open(os.path.join(yolo_save_dir,im_name[:-4]+'.txt'),'a+') as f:
        f.write(str(cat_id)+' '+str(x)+' '+str(y)+' '+str(w)+' '+str(h)+'\n')
    
    # if im_name=='obj365_val_000000000492.jpg':
    #     print(im_w,im_h)
    #     show_im = cv2.rectangle(show_im,(int(x1),int(y1)),(int(x2),int(y2)),(100,100,200))
    #     cv2.imshow('show_im',show_im)
    #     cv2.waitKey(1000)
        

    # exit()






for i in json_file:
    print(i)
print(json_file['categories'])