import numpy as np
from numpy.linalg import inv
import cv2 as cv
import glob
import time
from PIL import Image
import requests
from io import BytesIO
from math import sqrt

# import calibration as calb
# from triangulation import triangulate

import matplotlib.pyplot as plt
import mpldatacursor

_count = 0

#------------------------------------------------------------------------------#

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001 )

# prepare object points, like (0,0,0), (1,0,0), (2,0,0), ... (6, 5, 0)
# np.mgrid[0:TOTAL_LENGTH_X:9j, 0:TOTAL_LENGTH_Y:6j].T.reshape(-1, 2) where TOTAL_LENGTH = (n - 1) * grid_square_length
gridSquareLength = 24
gridSquareLength = gridSquareLength / 2.2e-6 #converts to units of pixels
objp = np.zeros((6*9, 3), np.float32)
objp[:,:2] = np.mgrid[0:gridSquareLength*8:9j,0:gridSquareLength*5:6j].T.reshape(-1,2)

# arrays to store object points and iamge points from all images
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane

#------------------------------------------------------------------------------#

mtx1 = dist1 = None
mtx2 = dist2 = None
rvecs1 = rvecs2 = None
tvecs1 = tvecs2 = None

mtx_arr = np.empty(2).astype(np.object)
dist_arr = np.empty(2).astype(np.object)
rvecs_arr = np.empty(2).astype(np.object)
tvecs_arr = np.empty(2).astype(np.object)

def _calibrate(gray, corners, ret):
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print("Calculate distance: {}".format(tvecs))
    print("Calculate rotation: {}".format(rvecs))

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

def triangulate(r, s, p, q):
    r_dot_r = np.dot(r, r)
    s_dot_s = np.dot(s, s)
    r_dot_s = np.dot(r, s)
    r_dot_p_q = np.dot(r, (p - q))
    s_dot_p_q = np.dot(s, (p - q))

    mu_nom = s_dot_p_q * r_dot_r - r_dot_s * r_dot_p_q
    mu_den = s_dot_s * r_dot_r - r_dot_s ** 2
    mu = mu_nom / mu_den

    lambda_nom = r_dot_s * s_dot_p_q - s_dot_s * r_dot_p_q
    lambda_den = s_dot_s * r_dot_r - r_dot_s ** 2
    lambda_ = lambda_nom / lambda_den

    f = p + lambda_ * r
    g = q + mu * s
    h = (f + g) / 2

    return h

#------------------------------------------------------------------------------#
# Main Code

# Check if cameras are calibrated, if not initiate calibration
# NEED TO REITERATE CALIBRATION
_calibrated = input("Are cameras calibrated? (y/n)")
if (_calibrated == 'n'):
    # all-in-one calibration function
    for i in [0, 1]:
        url_server_port = input("Input server port number: ") # TC
        url_resolution = input("Input desired resolution (default resolution '1600x1200'): ") or "1600x1200"

        _capture = True
        while _capture:
        #--------------------------------------------------------------------------#
            url = 'http://10.0.0.' + url_server_port + '/' + url_resolution + '.jpg'
            #url ='http://10.0.0.61/1600x1200.jpg'
            response = requests.get(url, timeout = 5) # remove delay in photo-taking ... but inefficient...
            response = requests.get(url, timeout = 5)
            img = Image.open(BytesIO(response.content))

            frame = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
            ret = True

            cv.imshow('img', frame)
            cv.waitKey(500)

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
                    print(type(mtx))

        #--------------------------------------------------------------------------#
            else:
                print('.')
            if _count > 4:
                _capture = False
                objp = np.zeros((6*9, 3), np.float32)
                objp[:,:2] = np.mgrid[0:gridSquareLength*8:9j,0:gridSquareLength*5:6j].T.reshape(-1,2) # definitely better way of doign this, e.g. find shape, construct index array, .delete() all ememnts from index array
                objpoints = []
                imgpoints = []
                _count = 0

                mtx_arr[i] = mtx
                dist_arr[i] = dist
                rvecs_arr[i] = np.average(rvecs, axis=0)
                tvecs_arr[i] = np.average(tvecs, axis=0)

                print("Calculate calbiration matrix: {}".format(mtx))
            cv.destroyAllWindows()
    #--------------------------------------------------------------------------#

#     # Use static calibration board for position and orientation estimation
# else:
#     # User input of corresponding calibration matrices and position vectors
#     R = int(input("Enter the number of rows:"))
#     C = int(input("Enter the number of columns:"))
#
#
#     print("Enter the entries in a single line (separated by space): ")
#
#     # User input of entries in a
#     # single line separated by space
#     entries = list(map(int, input().split()))
#
#     # For printing the matrix
#     matrix = np.array(entries).reshape(R, C)
#     print(matrix)
#
#     mtx1 = matrix
#
#     # DO THE SAME FOR DISTORTION COEFFICIENTS MATRIX dist

#--------------------------------------------------------------------------#
# SOLVE FOR P AND Q
p = np.dot(tvecs_arr[0], -1)
q = np.dot(tvecs_arr[1], -1)

print(p, q)

R_mtx_arr = np.empty(2).astype(np.object)
R_mtx_arr[0],_ = cv.Rodrigues(rvecs_arr[0])
R_mtx_arr[1],_ = cv.Rodrigues(rvecs_arr[1])

print(R_mtx_arr[0], R_mtx_arr[1])

R_mtx_arr[0] = inv(R_mtx_arr[0])
R_mtx_arr[1] = inv(R_mtx_arr[1])

p = np.reshape(np.dot(R_mtx_arr[0], p), (3,))
q = np.reshape(np.dot(R_mtx_arr[1], q), (3,)) # p and q is now in the object coordinate space

print(p)
print(np.shape(p))
print(q)
print(np.shape(q))

# -------------------------------------------------------------------------#
h1 = h2 = None

# Capture real-time images of target of interest to perform triangulation

for i in [0, 1]:
    # Grab captures from stero configuraton
    url_server_port = input("Input server port number: ") # TC
    url_resolution = input("Input desired resolution (default resolution '1600x1200'): ")  or "1600x1200"
    url = 'http://10.0.0.' + url_server_port + '/' + url_resolution + '.jpg'
    response = requests.get(url)
    response = requests.get(url)
    img1 = Image.open(BytesIO(response.content))

    url_server_port = input("Input server port number: ")
    url_resolution = input("Input desired resolution (default resolution '1600x1200'): ") or "1600x1200"
    url = 'http://10.0.0.' + url_server_port + '/' + url_resolution + '.jpg'
    response = requests.get(url)
    response = requests.get(url)
    img2 = Image.open(BytesIO(response.content))

    frame1 = cv.cvtColor(np.array(img1), cv.COLOR_RGB2BGR)
    plt.imshow(frame1[:,:,1], cmap='gray', vmin = 0, vmax = 255,interpolation='none')
    mpldatacursor.datacursor(hover=True, bbox=dict(alpha=1, fc='w'),
                             formatter='i, j = {i}, {j}\nz = {z:.02g}'.format)
    plt.show()
    plt.close()

    frame2 = cv.cvtColor(np.array(img2), cv.COLOR_RGB2BGR)
    plt.imshow(frame2[:,:,1], cmap='gray', vmin = 0, vmax = 255,interpolation='none')
    mpldatacursor.datacursor(hover=True, bbox=dict(alpha=1, fc='w'),
                             formatter='i, j = {i}, {j}\nz = {z:.02g}'.format)
    plt.show()
    plt.close()

    # -------------------------------------------------------------------------#

    # -------------------------------------------------------------------------#
    #TO-DO: Automate the r and s vector inputs (clicking image save pixel coordinates)

    # User inputs for pixel selection
    # f1 = float(input('Cam1: Enter focal length (mm): \n')) # f1 = avg(mtx_arr[0][0][0], mtx_arr[0][1][1])

    f1 = (mtx_arr[0][0][0] + mtx_arr[0][1][1]) / 2
    r_x = (float(input('Enter pixel x-coordinate for r-direction vector: \n')) - frame1.shape[0]/2)
    r_y = (frame1.shape[1]/2 - float(input('Enter pixel y-coordinate for r-direction vector: \n')))
    print(f1, r_x, r_y, np.array([r_x, r_y, f1]))
    r = np.array([r_x, r_y, f1]) / np.linalg.norm(np.array([r_x, r_y, f1]))

    # f2 = float(input('Cam2: Enter focal length (mm): \n')) # f2 = avg(mtx_arr[1][0][0], mtx_arr[1][1][1])
    f2 = (mtx_arr[1][0][0] + mtx_arr[1][1][1]) / 2
    s_x = (float(input('Enter pixel x-coordinate for s-direction vector: \n')) - frame2.shape[0]/2)
    s_y = (frame2.shape[1]/2 - float(input('Enter pixel y-coordinate for s-direction vector: \n')))
    s = np.array([s_x, s_y, f2]) / np.linalg.norm(np.array([s_x, s_y, f2]))

    print(r)
    print(np.shape(r))
    print(s)
    print(np.shape(s))

    # Calculate using triangulation algorithm
    h = triangulate(r, p, s, q)
    print(h)
    if i == 1:
        h1 = h
    else:
        h2 = h
# -------------------------------------------------------------------------#

# -------------------------------------------------------------------------#
# Calculate distance from the two-point comparison
h_delta = sqrt((h1[0] - h2[0])**2 + (h1[1] - h2[1])**2 + (h1[2] - h2[2])**2)
print("Distance between h1 and h2 is ... " + str(h_delta))
# -------------------------------------------------------------------------#

cv.destroyAllWindows()
