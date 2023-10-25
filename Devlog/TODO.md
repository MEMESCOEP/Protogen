# TODO
## NEEDS TO HAPPEN IMMEDIATELY
* Install & configure Jetson Nano devkit software
* Implement proper safety/failure checks & routines
* Ensure stability

---

## High priority
* Get some sort of fast & realistic chatbot running (llama is currently taking 11+ hours to generate simple responses 💀)
* Use an ESP32 to monitor temperatures, control fan speed via PWM (with a custom pcb), and perform safety checks & actions
* Configure static IP addresses for the ESP32, pis, and Jetson
* Improve OpenCV object detection performance
* Build a proper battery voltage detection/protection system. This will shut everything down safely when the battery voltage drops too low

---

## Medium priority
* Get speech recognition working
* Find a way to easily and securely mount the raspberry pi's camera
* Find a way to easily power the pis, ESP32, and Jetson with enough amperage. The recommended amperage for one pi 4 is 3 amps, and there are 2 (as well as a Jetson, which needs 4 amps), so a minimum of 10 amps should be provided. (Note that this figure doesn't include the ESP32, motor, external devices, or other loads.)

---

## Low priority
* Get a 12v lead-acid battery, proper charging equipment, voltage regulators, and electrical protection
* Get a 5 port ethernet switch to enable communication with all devices. I'll probably only use 3-4 of those ports, but having one open port allows me to connect it to the internet, as well as giving me direct access to to the internal network

---

## Maybe at some point lol
* Order parts and build a full size chassis for all the components (may not be happening due to high cost)
