"""
The pattern points of the QR code on the picture were found by the Java zxing 
package. The pattern points were saved to a text file named 'images/pattern_points.txt'.
This script display the QR code photos, and the pattern points found by zxing. 
"""

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

pprint(image_filenames)
pprint(pattern_points)

folder = 'images/'

for filename, points in zip(image_filenames, pattern_points):
    img = cv2.imread(folder+filename)
    for point in points:
        point_tuple = tuple(point.round().astype(int))
        cv2.circle(img, point_tuple, 30, (0,0,255), -1)
    plt.figure()
    plt.imshow(img)
