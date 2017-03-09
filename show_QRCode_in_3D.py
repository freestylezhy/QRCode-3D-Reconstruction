# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 01:59:12 2017

@author: yz
"""

#show the QR code in 3D space

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2

QR_pattern = './images/pattern.jpg'

img = cv2.imread(QR_pattern)

x, y = np.mgrid[0:img.shape[0], 0:img.shape[1]] /330.0 * 8.8

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot_surface(x, y, 0, rstride=2, cstride=2,
                facecolors=img/255.0)
plt.show()



