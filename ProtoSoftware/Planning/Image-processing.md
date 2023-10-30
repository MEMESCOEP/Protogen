# Image processing plan
This file outlines my plan for what the image processing code should do, and how it will work.

---
## What it does
This script is written in Python and targets version 3.6 (This is the version that comes pre-installed on the Jetson).
<br/>
The image processing script will do the following (in order):
* On bootup, attempt to connect to the central server. (If the connection is unsuccessful, print an error and trigger the error screen)
* Once connected, verify data transmission ability by sending a predefined server acknowledgement (string --> UTF-8 byte array) and waiting for the server to send the exact same data back. (If this fails, print an error and trigger the error screen)
* Once data transmission ability is verified, load the caffe model and build a deep neural network from it
* Set up required variables like sleep time and frame cache
* Initialize and configure the camera. There INIT/CONFIG stage consists of 8 steps:
  * Automatically detect whether or not we're using a raspberry pi camera, and create an object accordingly
  * Call the init method and use the first available camera, which should be at index 0. (If we're using a regular webcam, use cv2.CAP_DSHOW to significantly improve init times)
  * Set the resolution
  * Set the color format to BGR (This is done unintuitively using "RGB888". Picamera specific!)
  * Set the FOURCC mode to MJPG (This only works on regular webcams, and improved processing time)
  * Set the auto exposure to -5 (This is for regular webcams only! It improves performance in low light conditions)
  * Set the camera's framerate
  * Disable automatic RGB conversion for regular webcams (This can potentially increase performance)
* 
