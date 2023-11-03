### [===== PROTOGEN IMAGE PROCESSING =====] ###
"""
Written by Andrew maney, 2023
"""

## IMPORTS ##
from statistics import mean
import numpy as np
import threading
import keyboard
import logging
import socket
import time
import cv2
import sys
import os

## VARIABLES ##
# Constants
MIN_CONFIDENCE = 0.75
SERVER_ACK = b"SERV_CON_ACK"
BUFF_SIZE = 1024
PROTOTXT = "SSD_MobileNet_prototxt.txt"
CLASSES = ["aeroplane", "background", "bicycle", "bird", "boat",
   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
   "sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
MODEL = "SSD_MobileNet.caffemodel"
HOST = "127.0.0.1"
PORT = 6006
LOG = "LOG.txt"

# Things that can change
PreviouslyFoundObject = None
UserInputThread = None
ObjectPositions = []
BootVerboseOnly = False
ProcessedFrame = False
IsRunningWithCUDA = False
IsRunningOnJetson = False
DNNMagicNumber = 1 / 127.5
ObjectPosition = (0, 0)
CaptureFrames = True
CamResolution = (640, 480)
SendCountdown = 5
VerboseLog = True
DisplayFPS = True
FrameSize = (320, 240)
Framerate = 30
ScriptFPS = 0.0
ShowFrame = False
Verbose = True
Handler = None
Logger = None
Cam = None

## FUNCTIONS ##
def InputHandler():
    global CaptureFrames, Verbose, ShowFrame, ProcessedFrame
    
    while CaptureFrames:
        # Check if we've pressed a key
        event = keyboard.read_event()

        # Handle any pressed keys
        if event.event_type == keyboard.KEY_DOWN:
            # Toggle verbosity using the '~' key
            if event.name == '~':                
                Verbose = not Verbose
                print(f"[INFO] >> Verbosity enabled: {Verbose}...")

            # Press the 'escape' key to break the loop
            elif event.name == "esc":
                CaptureFrames = False

            # Turn on the frame preview using the Tab key
            elif event.name == "tab":
                ShowFrame = True

def PrintMSG(msg, logToFile = True):
    if logToFile:
        Logger.info(msg)

    if Verbose:
        print(msg)

def SendDataToServer(data):
    PrintMSG(f"[INFO] >> Sending server acknowledgement... (\"{SERVER_ACK}\")", VerboseLog)

    try:
        if type(s) is socket.socket:
            s.sendall(SERVER_ACK)    
            reponse = s.recv(BUFF_SIZE)

            if reponse != SERVER_ACK:
                PrintMSG(f"[ERROR] >> The server sent an invalid acknowledgement! Received data: {reponse}")

            else:        
                PrintMSG(f"[INFO] >> Received acknowledgement: {reponse!r}", VerboseLog)
                PrintMSG(f"[INFO] >> Sending data ({data})...\n", VerboseLog)
                s.sendall(bytes(data, "UTF-8"))

        else:
            PrintMSG(f"[ERROR] >> The type of 's' is not socket.socket! The type is: ({type(s)})")

    except Exception as ex:
        PrintMSG(f"[ERROR:SERV_SEND] >> {ex}")

def CloseProgram():
    global CaptureFrames, InputThread
    CaptureFrames = False

    # Close any CV2 windows and stop the webcam
    PrintMSG("[INFO] >> Closing all CV2 window(s)...")
    cv2.destroyAllWindows()

    PrintMSG("[INFO] >> Stopping the camera...")
    if Cam != None:
        Cam.release()

    PrintMSG("[INFO] >> All tasks completed. The application will now close.")
    sys.exit(0)

## MAIN CODE ##
print("[===== PROTOGEN IMAGE PROCESSING =====]\nPress Escape to stop the program, '~' to toggle verbosity, or Tab to show the frame.\n\n[INFO] >> Initializing...")
if BootVerboseOnly:
    Verbose = True

if os.path.exists(LOG):
    os.remove(LOG)

# Set up logging
# The basicConfig method breaks on python 3.6 (The version the jetson has), so we have to take a slightly different approach
Logger = logging.getLogger()
Logger.setLevel(logging.INFO)
Handler = logging.FileHandler(LOG, 'w', 'utf-8') # or whatever
Handler.setFormatter(logging.Formatter('<%(name)s> %(message)s')) # or whatever
Logger.addHandler(Handler)

try:
    # Create an input thread
    PrintMSG("[INFO] >> Creating and starting thread for keyboard handler...")
    UserInputThread = threading.Thread(target=InputHandler)
    UserInputThread.start()

    # Create a socket
    PrintMSG("[INFO] >> Creating a socket...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the central server
        PrintMSG(f"[INFO] >> Connecting to the central server ({HOST}:{PORT})...")
        s.connect((HOST, PORT))
        
        # Make sure we can send data to the server
        PrintMSG(f"[INFO] >> Verifying data transmission ability...")
        s.sendall(SERVER_ACK)    
        reponse = s.recv(BUFF_SIZE)

        if reponse != SERVER_ACK:
            PrintMSG(f"[ERROR] >> The server sent an invalid acknowledgement! Received data: {reponse}")
            CloseProgram()

        else:        
            PrintMSG(f"[INFO] >> Received acknowledgement: {reponse!r}")
            PrintMSG(f"[INFO] >> Connected to the central server ({HOST}:{PORT})!")

        # Load the serialized model
        PrintMSG(f"[INFO] >> Loading model ({MODEL})...")
        net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)

        # Create chached variable(s)
        frame = None

        # Calculate the number of miliseconds we need to sleep for to achieve the desired Framerate
        # The sleep time is calculated by dividing FPS by 1000, and dividing that by 1000 again
        FPSSleepTime = (1000 / Framerate) / 1000
        PrintMSG(f"[INFO] >> Sleeping for {FPSSleepTime * 1000} ms to achieve an fps of {Framerate}.\n[INFO] >> INIT COMPLETE.")

        # Check if we can use OpenCL (GPU), and enable it accordingly
        PrintMSG(f"[INFO] >> Checking if OpenCL is supported...")

        if cv2.ocl.haveOpenCL():
            PrintMSG("[INFO] >> OpenCL is supported! Enabling...")
            cv2.ocl.setUseOpenCL(True)

        else:
            PrintMSG("[INFO] >> OpenCL is NOT supported and will NOT be enabled.")
        
        # Initialize the video stream
        PrintMSG("[INFO] >> Starting video stream...")

        # Set up the camera
        PrintMSG("[INFO] >> Getting a camera reference...")
        if IsRunningOnJetson:
            Cam = cv2.VideoCapture(0)

        else:
            Cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        PrintMSG("[INFO] >> Configuring camera...")
        PrintMSG(f"[INFO] >> Setting camera resolution ({CamResolution})...")
        Cam.set(cv2.CAP_PROP_FRAME_WIDTH, CamResolution[0])
        Cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CamResolution[1])

        PrintMSG("[INFO] >> Setting FourCC mode to 'MJPG'...")
        Cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        PrintMSG("[INFO] >> Setting autoexposure...")
        Cam.set(cv2.CAP_PROP_EXPOSURE, -5)

        PrintMSG(f"[INFO] >> Setting Framerate ({Framerate})...")
        Cam.set(cv2.CAP_PROP_FPS, Framerate)

        PrintMSG("[INFO] >> Disabling automatic RGB conversion...")
        Cam.set(cv2.CAP_PROP_CONVERT_RGB, 0)

        # Log the current video backend
        PrintMSG(f"[INFO] >> Using video backend \"{Cam.getBackendName()}\".")
    
        # Check if we're running with CUDA support enabled and change the backend as necessary
        if IsRunningWithCUDA:
            PrintMSG("[INFO] >> Running WITH CUDA support.")
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        else:
            PrintMSG("[INFO] >> Running WITHOUT CUDA support.")

        # Send display configuration settings to the server
        SendDataToServer(f"DISP_CFG>>{FrameSize[0]}x{FrameSize[1]}")
        
        # Change the verbosity level if required
        if BootVerboseOnly:
            Verbose = False

        # Grab the frame from the threaded video stream
        while CaptureFrames:     
            # Get the start time of the loop. This will be used for calculating FPS
            tStart = time.time()  

            # Reset the frame and position data
            ProcessedFrame = False
            ObjectPositions.clear()
            
            # Capture a frame from the camera
            status, frame = Cam.read()

            # Convert the frame to UMat so OpenCV functions can run on the GPU (This isn't required anymore because OpenCV automatically does this for us)
            #frame = cv2.UMat(frame)
            #frameUMat = cv2.UMat(frame)
            
            # Resize the frame
            ResizedImage = cv2.resize(frame, FrameSize)

            # Grab the frame dimensions and convert it to a blob
            # The first 2 values are the height and width of the frame
            (h, w) = ResizedImage.shape[:2]
            
            # Create the blob
            blob = cv2.dnn.blobFromImage(ResizedImage, DNNMagicNumber, FrameSize, 127.5, swapRB=True)
            
            # Pass the blob through the network and obtain the predictions                
            net.setInput(blob)
            predictions = net.forward()

            # Loop over any predictions
            for i in np.arange(0, predictions.shape[2]):
                # Extract the confidence (i.e., probability) associated with the prediction
                confidence = predictions[0, 0, i, 2]
                
                # Filter out predictions that aren't confident enough
                if confidence < MIN_CONFIDENCE:
                    continue

                # Extract the index of the class label from the predictions
                idx = int(predictions[0, 0, i, 1])
                
                # Find the X and Y coordinates of the bounding box for the object and convert to integers
                box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Find the object's position
                ObjectPosition = (int((startX + endX) / 2), int((startY + endY) / 2))

                # Create a label with the object type, confidence score, and position
                label = "{}|{:.2f}%|{}".format(CLASSES[idx], confidence * 100, ObjectPosition)

                # Add the object's position to the list
                ObjectPositions.append(ObjectPosition)
                
                # Only draw a rectangle and add text if we should be showing the frame preview.
                # If we do this when the preview isn't visible, we're just doing extra/useless work
                if ShowFrame:
                    # Draw a rectangle across the boundary of the object
                    cv2.rectangle(ResizedImage, (startX, startY), (endX, endY), COLORS[idx], 1)
                    y = startY - 15 if startY - 15 > 15 else startY + 15

                    # Put a dot at the center of the object
                    cv2.circle(ResizedImage, ObjectPosition, 3, COLORS[idx], 2)
                    
                    # Put a label outside the detecion rectangle
                    cv2.putText(ResizedImage, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 1)

                # Print a message saying that an object was detected
                PrintMSG(f"[INFO] >> Object detected: {label}", VerboseLog)

            # Calculate the script FPS            
            loopTime = time.time() - tStart
            ScriptFPS = np.around(0.9 * ScriptFPS + 0.1 * (1 / loopTime), 2)


            # This code isn't under the block above because we don't need to be running this for each object that is detected.
            # It also causes extreme slowdown and freezing when run for every detected object.
            if ShowFrame:                
                # Put a circle at the center of the frame
                cv2.circle(ResizedImage, (int(FrameSize[0] / 2), int(FrameSize[1] / 2)), 3, COLORS[0], 2)

                # Display the FPS, if required
                if DisplayFPS:                    
                    cv2.putText(ResizedImage, f"FPS={ScriptFPS},{np.around(loopTime, 2)}", (0, 10), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 1)                    

                # Show the frame
                cv2.imshow("Object Detection", ResizedImage)
                
                # Wait for a key to be pressed (This is required to make the previous imshow call work properly for some reason)
                key = cv2.waitKey(1) & 0xFF

            else:
                PrintMSG(f"[INFO] >> FPS: {ScriptFPS}")

            # Send data to the server if there is any to send
            if len(ObjectPositions) > 0:
                #threading.Thread(target=SendDataToServer, args=(f"OBJ>>{mean(ObjectPositionsX)},{mean(ObjectPositionsY)}",)).start()
                threading.Thread(target=SendDataToServer, args=(f"OBJ>>{ObjectPosition[0]},{ObjectPosition[1]}",)).start()

            # Signal that we've finished processing the current frame
            ProcessedFrame = True
            
            # Sleep for x milliseconds so we run at the desired Framerate
            # This also helps prevent garbage CPU usage
            time.sleep(FPSSleepTime)

except Exception as ex:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    Verbose = True
    CaptureFrames = False
    PrintMSG(f"[ERROR] >> {ex}: Line #{exc_tb.tb_lineno}\n")

CloseProgram()
