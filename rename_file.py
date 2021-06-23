
import os
import random
import hashlib
file_path = 'partofbody'

for root,_,files_ in os.walk(file_path):
    for file_ in files_:
        file_name = os.path.join(root,file_)
        with open(file_name,'rb') as f:
            md5 = hashlib.md5()
            md5.update(f.read())
            hash = md5.hexdigest()
        print(len(hash))
        os.rename(file_name,os.path.join(root,hash+'.'+file_name.split('.')[-1]))
        












        # new_name = ''
        # new_name=new_name.join(random.choice("0123456789abcdef") for _ in range(32))
        # print(new_name)
