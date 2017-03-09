# Camera calibration and 3D reconstruction using photos of a QR code

The QR code pattern and the photos are in the images folder. The original pattern that was photographed is 8.8cm x 8.8cm. A number of images taken from different positions and orientations with an iPhone 6. Each image is the view of a pattern on a flat surface. 

A Java code (images/QRPatternPositions.java) using the zxing package is used to extract the patter positions from QR code photos. The result is stored in the file pattern_positions.txt

Python codes use the pattern_positions to calibrate the camera and reconstruct the 3D view of the QR code and the camera. 

## show_QRCode_pattern_points.py
Show the QR code pattern points in the QR photos

## show_QRCode_in_3D.py
Plot the QR code in 3D space

## camera_calibration.py
Calibrate the camera using the cooresponding points in the world and image coordinate

## reconstruct_world_view.py
Reconstruct 3D view of the QR code and the cameras. 

## cameras_in_world_view.png
This image is a snapshot of the 3D reconstruction result. The arrow in the camer's base denotes the x-axis.
