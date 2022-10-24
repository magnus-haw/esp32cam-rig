import asyncio
import os
from utils import get_calib_image_from_url, save_camera_calib, load_camera_calib

### Get images
id = 22
folder = "nasa%02d_calib/"%id
# if not os.path.isdir(folder):
#     os.makedirs(folder)
# url = "http://nasa%02d.local:8081"%(id)
# for i in range(0,5):
#     response = get_calib_image_from_url(url,id,index=i,write=True,show=True, folder=folder)
#     if i<4:
#         input("continue?")

### calibrate camera
mdict = save_camera_calib(folder)
mtx,dist,err = load_camera_calib(folder+'calib.yaml')

print(mtx)