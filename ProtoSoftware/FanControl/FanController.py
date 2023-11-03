### [===== PROTOGEN FAN CONTROL (JETSON) =====] ###
""" 
Written by Andrew maney, 2023
Note: THIS CODE ONLY RUNS ON THE JETSON NANO!
"""


## IMPORTS ##
import numpy as np
import logging
import psutil
import time
import os

## VARIABLES ##
# Constants
MAX_TEMP = 35.0
ROOM_TEMP = 22.0
MAX_PWM = 255.0
LOG = "log.txt"

# Things that can change
CurrentTempCelcius = 0.0
WaitTime = 10.0
PWMSpeed = 0
TempList = np.arange(ROOM_TEMP, MAX_TEMP, 0.1)
PWMList = np.arange(0, MAX_PWM, MAX_PWM / len(TempList))
PrevPWM = 0.0

## FUNCTIONS ##
# Get the index of the nearest value in a numpy array 
def find_nearest(array, value):
    return np.absolute(array - value).argmin()

## MAIN CODE ##
print("[== PROTOGEN FAN CONTROL (Jetson) ==]")

# Set up logging
# The basicConfig method breaks on python 3.6 (The version the jetson has), so we have to take a slightly different approach
print("[INFO] >> Setting up the logger...")
Logger = logging.getLogger()
Logger.setLevel(logging.INFO)
Handler = logging.FileHandler(LOG, 'w', 'utf-8') # or whatever
Handler.setFormatter(logging.Formatter('<%(name)s> %(message)s')) # or whatever
Logger.addHandler(Handler)

# Run the clocks program
print("[INFO] >> Starting \"/usr/bin/jetson_clocks\"...")
os.system("sudo /usr/bin/jetson_clocks")

# Fill the first 3/4 of the PWM array with the calulated speed (should be 75%).
# This ensures that the fan is always running, which (hopefully) reduces current spikes as well as
# keeping the temperature more stable
print("[INFO] >> Filling the first 75% of PWM list...")
FillPoint = int(len(PWMList) * 0.75)
for x in range(FillPoint):
    PWMList[x] = PWMList[FillPoint]

# Set the last PWM value to be it's maximum value (100% speed)
PWMList[len(PWMList) - 1] = MaximumPWM

# Monitor the temperature and speed up/slow down the fan if required
while True:
    # Get the temperature
    print("[INFO] >> Getting the temperature...")
    CurrentTempCelcius = psutil.sensors_temperatures()['thermal-fan-est'][0][1]

    # Get the PWM speed that should be applied
    print("[INFO] >> Setting the fan speed...")
    PWMSpeed = int((PWMList[find_nearest(TempList, CurrentTempCelcius)] + PrevPWM) / 2)
    PrevPWM = PWMSpeed

    # Set the PWM fan's speed
    os.system(f"sudo sh -c 'echo {PWMSpeed} > /sys/devices/pwm-fan/target_pwm'")

    # Print statistics
    Logger.info(f"Temp={CurrentTempCelcius} || PWM Speed={PWMSpeed}")

    # Sleep for x seconds (keeps CPU usage low, and we don't need to be changing the PWM speed every millisecond lol)
    time.sleep(WaitTime)