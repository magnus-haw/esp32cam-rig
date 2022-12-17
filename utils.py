#!/usr/bin/env python3

# API libraries
import aiohttp
import asyncio
import aiofiles
import aioesphomeapi
import requests
from io import BytesIO

# fileio imports
from pathlib import Path
from glob import glob
import yaml

# Image libraries
import cv2 as cv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

CONFIGPATH = Path('/Users/mhaw/esp32cam-rig/config')
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001 )
# prepare object points, like (0,0,0), (1,0,0), (2,0,0), ... (6, 5, 0)
OBJP = np.zeros((6*9, 3), np.float32)

def unknown(loader, suffix, node):
    if isinstance(node, yaml.ScalarNode):
        constructor = loader.__class__.construct_scalar
    elif isinstance(node, yaml.SequenceNode):
        constructor = loader.__class__.construct_sequence
    elif isinstance(node, yaml.MappingNode):
        constructor = loader.__class__.construct_mapping

    data = constructor(loader, node)

    return data
yaml.add_multi_constructor('!secret', unknown)

def get_calib_image_from_url(url,id,index=0,folder='',show=False,write=True):
    ret=False
    while ret==False:
        response = requests.get(url) # remove delay in photo-taking ... but inefficient...
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        # Find the chess board corners
        frame = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
        gray = cv.cvtColor(np.array(img), cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (9,6), None) 
        if ret == True:
            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria) 
            cv.drawChessboardCorners(frame, (9,6), corners2, ret) 

        if show:
            plt.imshow(frame)
            plt.show()
        
        if ret:
            inp = input("save this one (y/n)?")
            if inp=='y':
                ### Modify EXIF here for later use
                exif = update_exif(img.getexif())
                img.save(folder+"nasa%02d_%02d.png"%(id,index),exif=exif)
                ret = True
            else:
                ret=False

def update_exif(exif,FocalLength=None, SerialNumber=None):
    exif[271]='OMNIVISION' # Make
    exif[272]='OV5640' # Model
    exif[256]='2592' #ImageWidth
    exif[257]='1944' #ImageLength
    exif[50829] = '3673.6 um x 2738.4 um'
    if FocalLength is not None:
        exif[37386] = FocalLength+' mm'
    if SerialNumber is not None:
        exif[50735] = str(SerialNumber)

    #exif[] = '2592 x 1944'
    #pixel size: 1.4 μm x 1.4 μm
    #image area: 3673.6 μm x 2738.4 μm
    return exif

def get_camera_calib(folder):
    objpoints, imgpoints = [],[]

    # prepare object points
    objp = np.zeros((6*9,3),np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

    # loop over images
    fpaths = glob(folder+"*.png") 
    for im in fpaths:
        frame = cv.imread(im)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (9,6), None)
        if ret:
            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria) 
            objpoints.append(objp)
            imgpoints.append(corners2)
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    # estimate error
    mean_error =0 
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx,dist)
        error = cv.norm(imgpoints[i],imgpoints2,cv.NORM_L2)/len(imgpoints2)
        #print(imgpoints[i][0],imgpoints2[0])
        mean_error += error
    

    return ret,mtx,dist,mean_error/len(objpoints)

def save_camera_calib(folder,outputfilepath=None):
    ret,mtx,dist,err = get_camera_calib(folder)

    mdict = {'mtx':mtx.tolist(),'dist':dist.tolist(),'err':err}
    if outputfilepath is None:
        outputfilepath = folder + 'calib.yaml'
    with open(outputfilepath, 'w') as f:
        yaml.dump(mdict, f)
    return mdict

def load_camera_calib(fpath):
    with open(fpath, 'r') as fin:
        mdict = yaml.load(fin, Loader=yaml.FullLoader)
        mtx = np.array(mdict['mtx'])
        dist = np.array(mdict['dist'][0])
        err = mdict['err']
    return mtx,dist,err

def parse_config_files(CONFIGPATH= CONFIGPATH):
    outdict = {}
    paths = glob(str(CONFIGPATH / 'nasa*.yaml'))
    
    for path in paths:
        name = path.split('/')[-1].strip('.yaml')
        id = int(name[-2:])
        outdict[id] = {'name': name}
        with open(path, 'r') as fin:
            config = yaml.load(fin, Loader=yaml.FullLoader)
            outdict[id]['api'] = config['api']
            outdict[id]['wifi'] = config['wifi']
        
    return outdict




async def get_esp_connection(id, pswd=None, enc_key=None, ip=None):
    url = "nasa%02d.local"%id
    cli = aioesphomeapi.APIClient("nasa%02d.local"%id, 6053, password=pswd, noise_psk=enc_key)
    try:
        await cli.connect(login=True)
        #entities = await cli.list_entities_services()

        # ip = []
        # def callback(state, ip=ip):
        #     if type(state) is aioesphomeapi.TextSensorState:
        #         ip.append(state.state)
        #         print(state)
                
        # await cli.subscribe_states(callback)
        # await asyncio.sleep(.5)
        # url = "%s"%(ip[0])
    except:
        cli = None; entities=None; url=''

    return cli, entities, url

async def disconnect(cli, entitites):
    if cli is not None:
        await cli.disconnect()

async def esp32_lighton(cli, entities):
    if cli is not None:
        light_on = await cli.light_command(key=entities[0][0].key, state=True)

async def esp32_lightoff(cli, entities):
    if cli is not None:
        light_off = await cli.light_command(key=entities[0][0].key, state=False)

async def fetch_img(id, folder='',index=0, write=True, ip=None):
    async with aiohttp.ClientSession() as session:
        url = "http://nasa%02d.local:8081"%id
        if ip is not None:
            url = "http://%s:8081"%ip
        async with session.get(url) as resp:
            if resp.status == 200 and write:
                f = await aiofiles.open(folder+'nasa%02d_%02d.jpg'%(id,index),mode='wb')
                await f.write(await resp.content.read())

async def esp32_get_images(ids, folder='', index=0):
    await asyncio.gather(*(fetch_img(id,folder,index, write=False) for id in ids))
    await asyncio.gather(*(fetch_img(id,folder,index) for id in ids))

async def download_imgs(ids, folder='', index=0):

    # connections = [asyncio.create_task(get_esp_connection(int(key), pswd= value['api']['password'], 
    #                                                       enc_key= value['api']['encryption']['key'], ip=None)) for key, value in outdict.items()]
    # conns = await asyncio.gather(*connections)
    # lighton = await asyncio.gather(*(esp32_lighton(cli, ents) for cli,ents,ip in conns))
    # await asyncio.sleep(.2)
    print('start')
    await esp32_get_images(ids, folder=folder, index=index)
    print('end')
    # lightoff = await asyncio.gather(*(esp32_lightoff(cli, ents) for cli,ents,ip in conns))
    # disconn = await asyncio.gather(*(disconnect(cli, ents) for cli,ents,ip in conns))
