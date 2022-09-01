import numpy as np
from numpy.linalg import inv
import cv2 as cv
import glob
import time
from PIL import Image
import requests
from io import BytesIO
from math import sqrt

_count = 0

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001 )

# prepare object points, like (0,0,0), (1,0,0), (2,0,0), ... (6, 5, 0)
objp = np.zeros((6*9, 3), np.float32)
# objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
objp[:,:2] = np.mgrid[0:87272:9j,0:54545:6j].T.reshape(-1,2) # 87272 = totalength / 2.2um, etc.

# arrays to store object points and iamge points from all images
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane

def _calibrate(gray, corners, ret):
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print(len(objpoints))
    print("Calculate distance: {}".format(tvecs))
    print("Calculate rotation: {}".format(rvecs))
    print("Calculate calbiration matrix: {}".format(mtx))

    return ret, mtx, dist, rvecs, tvecs

def undistort(gray, mtx, dist):
    global _count
    h, w = gray.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    dst = cv.undistort(gray, mtx, dist, None, newcameramtx)
    # cv.imwrite('calibresult.png', dst)

    cv.imshow("undistort", dst)
    cv.waitKey(1000)
    cv.destroyWindow('undistort')

    _proceed = input('Do you wish to add it to the image pile? (y/n)')
    if _proceed == 'n':
        objpoints.pop()
        imgpoints.pop()
    else:
        _count = _count + 1

url_server_port = input("Input server port number: ")
url_resolution = input("Input desired resolution (e.g. '1600x1200'): ")
url = 'http://10.0.0.' + url_server_port + '/' + url_resolution + '.jpg' # TC
#url ='http://10.0.0.61/1600x1200.jpg'

_capture = True
while _capture:
    response = requests.get(url) # remove delay in photo-taking ... but inefficient...
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    frame = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    ret = True

    cv.imshow('img', frame)
    cv.waitKey(1000)

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (9,6), None)
    #--------------------------------------------------------------------------#
    if ret == True:
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria) # WHAT DOES THOSE DIMENSIONS SIGNIFY
        # Draw and display the corners
        cv.drawChessboardCorners(frame, (9,6), corners2, ret) # USE REFERENCE VARIABLE
        time.sleep(0.5)
        cv.imshow('img', frame)
        cv.waitKey(2000)
        cv.destroyWindow('img')
        _proceed = input('Do you wish to calibrate and undistort the img? (y/n)')
        if _proceed == 'y':
            objpoints.append(objp)
            imgpoints.append(corners)
            ret, mtx, dist, rvecs, tvecs = _calibrate(gray, corners, ret)
            undistort(gray, mtx, dist)

    #--------------------------------------------------------------------------#
    else:
        print('.')
