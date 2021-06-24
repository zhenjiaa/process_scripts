import cv2
import os
import random
import sys
import numpy as np



def get_file(path,dist_path,num):
    dist = []
    if path.endswith('.txt'):
        files = open(path,'r').readlines()
        for i in range(len(files)):
            files[i] = files[i].strip()
            dist.append(os.path.join(dist_path,files[i].split('/')[-1]))
            files[i] = '/home/nas01/chunsheng/datasets/pos/Objects365/images/train/train/'+files[i]


    else:
        files = []
        count =0
        for root,_,files_ in os.walk(path):
            for file_ in files_:
                if file_.endswith('.jpg') or file_.endswith('.png'):
                    files.append(os.path.join(root,file_))
                    dist.append(os.path.join(dist_path,file_))
    print('The number of pic:',len(files))
    assert len(files)>num,'The number of augmented pictures must be less than the number of all pictures '
    index = random.sample(range(len(files)),num)
    files = [files[i] for i in index]
    dist = [dist[i] for i in index]
    return files,dist
        


def motion_blur(image, degree, angle):
    image = np.array(image)
    # 这里生成任意角度的运动模糊kernel的矩阵， degree越大，模糊程度越高
    M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
    
    motion_blur_kernel = np.diag(np.ones(degree))
    motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))
    motion_blur_kernel = motion_blur_kernel / degree

    blurred = cv2.filter2D(image, -1, motion_blur_kernel)
    # convert to uint8
    cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
    blurred = np.array(blurred, dtype=np.uint8)
    return blurred


src_path = '/home/rd/lizhenjia/object365/train_imagelist_nonhuman_dog_cat.txt'
dist_path = '/home/nas01/chunsheng/share/nonhuman_dog_cat_image'
if not os.path.exists(dist_path):
    os.mkdir(dist_path)
num = 5000
files_,dist_ = get_file(src_path,dist_path,num)

print(files_,dist_)
for i in range(len(files_)):
    file = files_[i]
    img = cv2.imread(file)
    rand_degree = random.randint(8,32)
    rand_angle = random.randint(0,360)
    img = motion_blur(img,rand_degree,rand_angle)
    cv2.imwrite(dist_[i],img)


