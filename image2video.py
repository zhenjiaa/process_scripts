import cv2
import os
import numpy as np


fps = 25
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(filename='/home/zhenjia/lzj/space_work/video/result.mp4', fourcc=fourcc, fps=fps, frameSize=(1080,2400))  # 图片实际尺寸，不然生成的视频会打不开
for i in range(0,4500):
    p = i
    if p<10:
        p = '00'+str(p)
    elif p<100:
        p = '0'+str(p)
    else:
        p = str(p)


    if os.path.exists('/home/zhenjia/lzj/space_work/k9_before_out/vf_'+p+'.jpg'):
        print(p)
        img1 = cv2.imread('/home/zhenjia/lzj/space_work/k9_before_out/vf_'+p+'.jpg')
        # img2 = cv2.imread('/home/zhenjia/lzj/space_work/video/test_set/07_after/exp/vf_'+p+'.jpg')

        # final_matrix = np.zeros((2400, 1080*2, 3), np.uint8)
        # final_matrix[0:2400, 0:1080] = img1
        # final_matrix[0:2400,1080:1080*2] = img2
        # cv2.resize(2400)
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('image',1200,1080)
        # cv2.imshow('image',final_matrix)
        # cv2.waitKey(10)
        video_writer.write(img1)
video_writer.release()