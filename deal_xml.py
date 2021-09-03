import os
import xml.etree.ElementTree as ET


save_dir = '/home/zhenjia/lzj/wddw/dog_cat_dataset/牛津大学开源数据集/annotations/yolo'
lrtb_save_dir = '/home/zhenjia/lzj/wddw/dog_cat_dataset/牛津大学开源数据集/annotations/lrtb'
def load_xml(labels_dir):
    files = os.listdir(labels_dir)
    for file in files:
        xml_path = os.path.join(labels_dir,file)
        txt_path = os.path.join(save_dir,file[0:-4]+'.txt')
        lrtb_txt_path = os.path.join(lrtb_save_dir,file[0:-4]+'.txt')
        txt_file = open(txt_path,'w')
        lrtb_txt_file = open(lrtb_txt_path,'w')
        tree = ET.parse(xml_path)
        for size in tree.findall('size'):
            img_w = int(size.find('width').text)
            img_h = int(size.find('height').text)
        for obj in tree.findall('object'):
            cls = obj.find('name').text
            if cls=='cat':
                cls=1
            elif cls=='dog':
                cls=2
        
            bbox = obj.find('bndbox')
            x1 = int(bbox.find('xmin').text)
            y1 = int(bbox.find('ymin').text)
            x2 = int(bbox.find('xmax').text)
            y2 = int(bbox.find('ymax').text)
            x = (x1+x2)/(2.*img_w)
            y = (y1+y2)/(2.*img_h)
            w_ =(x2-x1)/float(img_w)
            h_ =(y2-y1)/float(img_h)
            txt_file.write(str(cls)+' '+str(x)+' '+str(y)+' '+str(w_)+' '+str(h_)+'\n')
            lrtb_txt_file.write(str(cls)+' lrtb = '+str(x1)+' '+str(x2)+' '+str(y1)+' '+str(y2)+'\n')


    # return labels
load_xml('/home/zhenjia/lzj/wddw/dog_cat_dataset/牛津大学开源数据集/annotations/annotations/xmls')