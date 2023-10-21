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
  [*] Improved object detection speed from 5 to 8 FPS by changing the camera's resolution
  <br/>
  [*] Object detection works better, 3 FPS increase, 5 to 8 FPS (STILL NEEDS OPTIMIZATION!!!)
  <br/>
  [*] Drastically improved object detection speed when running on a desktop by changing the camera resolution, setting auto exposure to -5, setting camera framerate, and disbaling automatic RGB conversion (15 fps to ~50)
  <br/>
  [*] The camera's resolution should be set to 640x480 becasue that's the lowest resolution the rpi camera V2 currently supports. It's also decently fast
  <br/>
  [*] The frame size in "ImageProcessingClient.py" should be set to a low resolution for best results (Currently using 320x200)
</details>
