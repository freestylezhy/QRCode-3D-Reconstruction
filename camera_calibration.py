# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 17:37:32 2017

@author: yz
"""

# find the camera parameters, including the camera matrix, rotation vectors, 
# and translation vectors.

import numpy as np
from matplotlib import pyplot as plt
import cv2
from pprint import pprint

image_filenames = []
pattern_points = []

with open('images/pattern_points.txt', 'r') as f:
    for line in f:
        items = line.split()
        image_filenames.append(items[0])
        points = np.array(items[1:]).astype(np.float).reshape(-1, 2)
        pattern_points.append(points)

#qr_world_positions = np.array([
#    [75.0, 255.0],
#    [75.0, 75.0],
#    [255.0, 75.0],
#    [225.0, 225.0]]) / 330 * 8.8

qr_world_positions = np.array([
    [255.0, 75.0],
    [75.0, 75.0],
    [75.0, 255.0],
    [225.0, 225.0]]) / 330 * 8.8

qr_world_positions = np.hstack((qr_world_positions, np.zeros((qr_world_positions.shape[0], 1))))
qr_world_positions = qr_world_positions.astype(np.float32)

img_num = 6
img_points = pattern_points[img_num]
img_points = img_points.astype(np.float32)

folder = 'images/'
filename = image_filenames[img_num]
img = cv2.imread(folder + filename)
img_size = img.shape[:2]


ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([qr_world_positions], [img_points], img_size, None, None)

# show the pattern points on the image
# project 3D points to image plane
imgpts, jac = cv2.projectPoints(qr_world_positions, rvecs[0], tvecs[0], mtx, dist)

for point in imgpts:
    point_tuple = tuple(point.ravel().round().astype(int))
    cv2.circle(img, point_tuple, 30, (0,0,255), -1)
    print(point_tuple)
    
plt.figure()
plt.imshow(img)

# simulate the photo of the QR code to compare with the supplied photo

QR_pattern = './images/pattern.jpg'
QR_pattern_img = cv2.imread(QR_pattern, 0)
x_grid, y_grid = np.mgrid[0:QR_pattern_img.shape[0], 0:QR_pattern_img.shape[1]] / 330.0 * 8.8

# 
img = 255 - np.zeros(img_size, np.uint8)
black_pixels = np.array([0, 0, 0], np.float32)

for x, y, color in zip(x_grid.ravel(), y_grid.ravel(), QR_pattern_img.ravel()):
    if color == 0:
        black_pixels = np.vstack((black_pixels, np.array([x, y, 0], np.float32)))

black_pixels = black_pixels[1:]

imgpts, jac = cv2.projectPoints(black_pixels, rvecs[0], tvecs[0], mtx, dist)        

for point in imgpts:
    point_tuple = tuple(point.ravel().round().astype(int))
    cv2.circle(img, point_tuple, 1, 0, -1)

plt.figure()
plt.imshow(img, cmap='gray')
