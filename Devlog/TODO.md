# TODO
## NEEDS TO HAPPEN IMMEDIATELY
* Implement proper safety and failure checks & routines
* Ensure stability

---

## High priority
* Get some sort of fast & realistic chatbot running (llama is currently taking 11+ hours to generate simple responses 💀)
* Use an ESP32 to monitor temperatures, control fan speed via PWM, and do temperature safety checks and actions
* Configure static IP addresses for the ESP32 and the pis
* Improve OpenCV object detection performance

---

## Medium priority
* Get speech recognition working
* Find a way to easily and securely mount the raspberry pi's camera
* Find a way to easily power the pis & ESP32 with enough amperage (We need plenty of current because the reccommended amperage for one pi 4 is 3 amps. There are 3, so 9 amps will be required, not including the ESP32 and external devices)

---

## Low priority
* Get a 12v lead-acid battery, the proper charging, and the voltage regulators
* Get a 5 port ethernet switch to enable communication with all devices. I'll most likely only be using 3-4 of those ports, but having one open port allows me to connect it to a router and gain direct access

---

## Maybe at some point lol
* Order parts and build a full size chassis for all the components (may not be happening due to cost)
