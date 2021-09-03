
import cv2
import numpy as np
import os

from numpy.lib.npyio import save
def contrast_img(img1, c, b): 
    rows, cols, channels = img1.shape
    blank = np.zeros([rows, cols, channels], img1.dtype)
    rst = cv2.addWeighted(img1, c, blank, 1-c, b)
    return rst

def turn_in_hsv(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hsv_img[:, :, 2] = hsv_img[:, :, 2]*1.1
    darker_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
    # (b, g, r) = cv2.split(darker_img)
    # bH = cv2.equalizeHist(b)
    # gH = cv2.equalizeHist(g)
    # rH = cv2.equalizeHist(r)
    # # 合并每一个通道
    # result = cv2.merge((bH, gH, rH))
    return darker_img








pre_path = '/home/zhenjia/lzj/space_work/video/test_set/1'
save_path = '/home/zhenjia/lzj/space_work/video/test_set/hsv_1.1'
for file_name in os.listdir(pre_path):
    file = os.path.join(pre_path,file_name)
    img = cv2.imread(file)


    #第二个参数调节亮度，越大越亮，越小越暗
    #变暗：rst = contrast_img(img, 0.5, 3)
    # rst = contrast_img(img, 3, 3)

    rst = turn_in_hsv(img)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    cv2.imwrite(os.path.join(save_path,file_name),rst)

