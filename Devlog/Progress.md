# Progress
<details>
  <summary>10-19-23</summary>
  [*] Object detection works, but is slow when run on a Raspberry Pi 4 (5 fps 💀) (NEEDS OPTIMIZATION BADLY!!!)
  <br/>
  [*] Communication between the central server (4GB RAM RPI) and the ImageProcessingClient (8GB RAM RPI) works decently well
  <br/>
  [*] The frame size in "ImageProcessingClient.py" should be set to a low resolution for best results (Currently using 320x200)
</details>

<details>
  <summary>10-21-23</summary>
  [*] Improved object detection speed from 5 to ~8 FPS by changing the camera's resolution
  <br/>
  [*] Object detection works better, 3 FPS increase, 5 to ~8 FPS (STILL NEEDS OPTIMIZATION!!!)
  <br/>
  [*] Drastically improved object detection speed when running on a desktop by changing the camera resolution, setting auto exposure to -5, setting camera framerate, and disbaling automatic RGB conversion (15 fps to ~50)
  <br/>
  [*] The camera's resolution should be set to 640x480 becasue that's the lowest resolution the rpi camera V2 currently supports. It's also decently fast
  <br/>
  [*] The frame size in "ImageProcessingClient.py" should be set to a low resolution for best results (Currently using 320x200)
</details>

<details>
  <summary>10-24-23</summary>
  [*] I'm working on switching the computer vision processor to a jetson nano (from an rpi 4) because it has CUDA (GPU) accelaration. I'm hvaing trouble updating the OS (Ubuntu 18.04) and the packages. Python 3.6 is too old, and I need the best security I can get. The current issue with "sudo apt-get update" and "sudo apt-get upgrade" is that it doesn't want to connect to some package servers, and then dies. 
  <br/><br/>
  I've found some instructions on my robotics team's (RoboLions) github that explains how to install Discombobulated88's Xubuntu image (https://github.com/Discombobulated88/Xubuntu-20.04-L4T-32.3.1/releases/download/v1.0/Xubuntu-20.04-l4t-r32.3.1.tar.tbz2), and how to uprade to 22.04. Hopefully everything works fine. I'm also thinking about armbian 23.8 (https://www.armbian.com/jetson-nano/).
  <br/><br/>
  [*] Removed the imutils requirement, as OpenCV already has a built-in function to resize frames
</details>

<details>
  <summary>10-25-23</summary>
  [*] I'm still working on switching the computer vision processor to a jetson nano (from an rpi 4) because it has CUDA (GPU) accelaration. I found an Ubuntu 20.04 image (https://github.com/Qengineering/Jetson-Nano-Ubuntu-20-image), and I'm having far fewer issues now. I'll still need to upgrade packages, as Python 3.8 is a bit too old.
  <br/><br/>
  The instructions on my robotics team's (RoboLions) github didn't work, but only because Discombobulated88's Xubuntu image (https://github.com/Discombobulated88/Xubuntu-20.04-L4T-32.3.1/releases/download/v1.0/Xubuntu-20.04-l4t-r32.3.1.tar.tbz2) booted but froze on the NVidia splash screen. Armbian disabled HDMI output completely, but SSH worked. I chose to go to Ubuntu 20.04 because I need a desktop env for OpenCV's imshow function.
</details>
