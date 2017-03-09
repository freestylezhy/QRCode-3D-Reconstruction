# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 03:53:28 2017

@author: yz
"""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2


image_filenames = []
pattern_points = []

with open('images/pattern_points.txt', 'r') as f:
    for line in f:
        items = line.split()
        image_filenames.append(items[0])
        points = np.array(items[1:]).astype(np.float).reshape(-1, 2)
        pattern_points.append(points)

#position of the pattern in the world coordinate
# the original QR code has 330 pixels and 8.8 cm in width

qr_world_positions = np.array([
    [255.0, 75.0],
    [75.0, 75.0],
    [75.0, 255.0],
    [225.0, 225.0]]) / 330 * 8.8

qr_world_positions = np.hstack((qr_world_positions, np.zeros((qr_world_positions.shape[0], 1))))
qr_world_positions = qr_world_positions.astype(np.float32)

QR_pattern = './images/pattern.jpg'
img = cv2.imread(QR_pattern)
#x, y = np.mgrid[0:img.shape[0], 0:img.shape[1]] /330.0 * 8.8
x, y = np.mgrid[0:img.shape[0], 0:img.shape[1]] / 330.0 * 40
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(x, y, 0, facecolors=img/255.0)
#plt.show()



folder = 'images/'
filename = image_filenames[0]
img = cv2.imread(folder + filename)
img_size = img.shape[:2]


for filename, img_points in zip(image_filenames, pattern_points):
    img_points = img_points.astype(np.float32)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([qr_world_positions], [img_points], img_size, None, None)
    
    tvec = tvecs[0]
    rmat, jac = cv2.Rodrigues(rvecs[0])

    fc = np.array([mtx[0,0], mtx[1,1]])
    cc = mtx[0:2, 2]
    alpha_c = 0
    dX = 10
    nx, ny = img_size
    
    # IP is the shape of camera, borrowed from http://www.vision.caltech.edu/bouguetj/calib_doc/
    IP = 2*dX* np.array([[1/fc[0], 0, 0], [0, 1/fc[1], 0], [0, 0, 1]]).dot(
        np.array([[1, 0, -cc[0]], [0, 1, -cc[1]], [0, 0, 1]])).dot(
        np.array([[0, nx-1, nx-1, 0, 0], [0, 0, ny-1, ny-1, 0], [1, 1, 1, 1, 1]]))
    
    BASE = 2*(.9)*dX*np.array([[0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1]])
    
    IP = np.vstack((IP, np.zeros((3,5)), IP)).T.reshape((15,3)).T

    # BASEk, and IPk are the coordinate of the cammer and its base in the world coordinate
    # relative to the QR code  
    BASEk = rmat.T.dot(BASE - tvec.dot(np.ones((1,6))))
    IPk = rmat.T.dot(IP - tvec.dot(np.ones((1,15)))) 
    
    ax.plot(IPk[0, :], IPk[1, :], IPk[2, :])
    ax.plot(BASEk[0, :], BASEk[1, :], BASEk[2, :])
    zdir = rmat.T.dot(np.array([1, 0, 0]).T)
    x, y, z = BASEk[:, 1]
    u, v, w = BASEk[:, 1] - BASEk[:, 0]
    length = (u**2 + v**2 + w**2)**0.5
    ax.quiver(x, y, z, u, v, w, length=length)   #an arrow denotes the x-direction
    ax.text(x, y, z, filename, zdir)

plt.show()
    
    
    