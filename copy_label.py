import os
import shutil
path = 'nonhuman_dog_cat/nonhuman_dog_cat_image/'
for file in os.listdir(path):
    file = file[0:-4]+'.txt'
    shutil.copy('/home/rd/lizhenjia/object365/Annotations/train_lrtb/'+file,'nonhuman_dog_cat/label_lrtb/'+file)                      