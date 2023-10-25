# Status
## Current hardware
* 2 Raspberry pi 4's (can be upgraded):
  * One 8G RAM model for the chatbot
  * One 4G RAM model for the central & display servers

* NVidia Jetson Nano Devkit (for computer vision, requires a 64gb or larger MicroSD card)
  
* Raspberry pi camera v2
* Wired networking via ethernet
* An ESP32
* Active cooling for the pis, jetson, and ESP32

## Current software
* Raspberry Pi OS (Must be the 64 bit bookworm release, SSH is currently enabled)
* Ubuntu 20.04 (For the jetson, https://github.com/Qengineering/Jetson-Nano-Ubuntu-20-image)
* Python 3.10.x - 3.11.2
  <details>
   <summary>
    Image processing
   </summary>

   <ul>
    <li>mean (from statistics)</li>
    <li>numpy</li>
    <li>threading</li>
    <li>keyboard</li>
    <li>logging</li>
    <li>socket</li>
    <li>time</li>
    <li>cv2 (OpenCV)</li>
    <li>sys</li>
    <li>os</li>
   </ul>
  </details>

  <details>
   <summary>
    Central server
   </summary>

   <ul>
    <li>partial (from functools)</li>
    <li>multiprocessing</li>
    <li>keyboard</li>
    <li>logging</li>
    <li>signal</li>
    <li>socket</li>
    <li>time</li>
    <li>sys</li>
    <li>os</li>
   </ul>
  </details>

* llama.cpp (https://github.com/ggerganov/llama.cpp)
* llama 7B model (12+ GB, very large)
