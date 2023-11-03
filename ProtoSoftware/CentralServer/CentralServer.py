### [===== PROTOGEN CENTRAL SERVER =====] ###
"""
Written by Andrew maney, 2023
"""

## IMPORTS ##
from functools import partial
import multiprocessing
import keyboard
import logging
import socket
import signal
import time
import sys
import os

## VARIABLES ##
# Constants
ACCEPTED_CLIENT_IP = "127.0.0.1"
SERVER_ACK = b"SERV_CON_ACK"
BUFF_SIZE = 1024
QUIT_KEY = "escape"
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 6006
LOG = "LOG.txt"

# Things that can change
KeepServerOpen = True
ScreenCenter = (0, 0)
ScreenSize = (0, 0)
Verbose = True

## FUNCTIONS ##
def PrintMSG(MSG, LogToFile = True):
    if LogToFile:
        logging.info(MSG)

    print(MSG)

def KillServer(THD):
    global KeepServerOpen, SOCK
    
    PrintMSG(f"[INFO] >> Stopping the server...")
    KeepServerOpen = False

    PrintMSG(f"[INFO] >> Terminating the server thread...")
    THD.terminate()

    PrintMSG(f"[INFO] >> Closing the socket...")
    SOCK.close()

    PrintMSG(f"[INFO] >> Exitting...")
    sys.exit(0)
    
def HandleCTRLC(THD, sig, frame):
    KillServer(THD)

# Starts the server, checks if there's any keys pressed, and kills the server if required
def Monitor():
    try:
        # Create a thread for the server
        PrintMSG(f"[INFO] >> Creating new server thread...")
        ServerThread = multiprocessing.Process(target=Server)

        # Start the server
        PrintMSG(f"[INFO] >> Starting the server thread...")
        ServerThread.start()
        
        # Handle CTRL-C so we can gracefully shut down the server
        PrintMSG(f"[INFO] >> Creating event handler for \"CTRL-C\"...")
        signal.signal(signal.SIGINT, partial(HandleCTRLC, ServerThread))        

        # Check for keys every 1/10 of a second
        while KeepServerOpen:
            try:
                time.sleep(0.1)

                if keyboard.is_pressed(QUIT_KEY):
                    KillServer(ServerThread)

            except Exception as ex:
                PrintMSG(f"[ERROR] >> {ex}\n")

    except Exception as ex:
        PrintMSG(f"[ERROR] >> {ex}\n")

def Server():
    # Get a global reference to variables
    global ScreenSize, ScreenCenter, KeepServerOpen

    # Set socket options. I'm using SO_REUSEADDR here so that the same TCP connection can be used after the server has closed.
    # This helps if there's a crash where the TCP connection can't be killed (fuk you windows >:3)
    PrintMSG(f"[INFO] >> Setting socket options...")
    SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the host and port
    PrintMSG(f"[INFO] >> Binding socket to \"{HOST}:{PORT}\"...")
    SOCK.bind((HOST, PORT))

    # Start listening for clients
    PrintMSG(f"[INFO] >> Waiting for a connection...")
    SOCK.listen()

    # Keep listening until we should kill the server
    while KeepServerOpen:
        # Accept a connection of a client wants to connect
        conn, addr = SOCK.accept()

        # This method of "security" is like putting a children's toy lock on something. It's something, but it's so easy to break through that it's basically useless.
        # It can be bypassed by simply changing the IP address of the client. It's that easy. Thisi s literally baby level security. I'll need to implement better security eventually
        # Check to see if the client is authorized
        if addr[0] != ACCEPTED_CLIENT_IP:
            PrintMSG(f"[WARN] >> /!\\ UNAUTHORIZED CONNECTION ATTEMPT MADE BY CLIENT! CLIENT IP: {addr} /!\\")
            PrintMSG("[INFO] >> Closing socket...\n")
            conn.close()

        # The client is authorized, so we can accept and continue
        else:
            # Handle data
            with conn:
                PrintMSG(f"[INFO] >> Accepted connection request from \"{addr}\", waiting for data...")

                # Keep listening until we should kill the server
                while KeepServerOpen:
                    try:
                        # Receive data from the client
                        PrintMSG("[INFO] >> Receiving data...", False)
                        data = conn.recv(BUFF_SIZE)
                    
                        # If we received nothing, the client disconnected
                        if not data or len(data) == 0:
                            break

                        # Check what type of data the client sent
                        # Data transmission acknowledgement
                        if data == SERVER_ACK:
                            # Echo the acknowledgement so that the client knows that data transmission is working
                            PrintMSG(f"[INFO] >> Received acknowledgement from {addr}: {data} (Length = {len(data)})", False)
                            conn.sendall(data)

                        # Object
                        elif data.startswith(b"OBJ>>"):
                            decodedData = data.decode('UTF-8')

                            # Check for invalid display config data
                            if ',' not in decodedData:
                                raise Exception("Invalid display configuration data received: no splitting character!")

                            objProperties = decodedData.replace("OBJ>>", '').split(',')

                            # Check for invalid display config data again after the string has been split
                            if len(objProperties) <= 0:
                                raise Exception(f"Invalid display configuration data received: missing size information! Received: {objProperties}")
                            
                            elif not str(objProperties[0]).isnumeric() or not str(objProperties[1]).isnumeric():
                                raise Exception(f"Invalid display configuration data received: missing width or height information! Received: {objProperties}")
                            
                            #PrintMSG(f"[INFO] >> Received detected object data from {addr}:\n\tObject type: {objProperties[0]}\n\tConfidence: {objProperties[1]}\n\tObject position: {objProperties[2]}\n\tData length: {len(data)}\n", False)
                            PrintMSG(f"[INFO] >> Received detected object data from {addr}:\n\tObject position: {objProperties}\n\tData length: {len(data)}\n", False)

                            # Use the object's X coordinate to figure out if it's to the left or right
                            RelativePos = float(objProperties[0]) - float(ScreenSize[0] / 2)

                            """if RelativePos < -10:
                                PrintMSG("Turn to the left!", False)

                            elif RelativePos > 10:
                                PrintMSG("Turn to the right!", False)

                            else:
                                PrintMSG("Don't turn", False)"""

                        # Display configuration
                        elif data.startswith(b"DISP_CFG>>"):                            
                            decodedData = data.decode('UTF-8')

                            if 'x' not in decodedData:
                                raise Exception("Invalid display configuration data received: no x!")

                            dispProperties = decodedData.replace("DISP_CFG>>", '').split('x')

                            if len(dispProperties) != 2:
                                raise Exception("Invalid display configuration data recieved: invalid resolution!")

                            ScreenSize = (int(dispProperties[0]), int(dispProperties[1]))
                            ScreenCenter = (ScreenSize[0] / 2, ScreenSize[1] / 2)
                            PrintMSG(f"[INFO] >> Received display configuration data from {addr}:\n\tScreen size: {ScreenSize}\n\tScreen center: {ScreenCenter}\n\tData length: {len(data)}\n", False)

                        else:
                            PrintMSG(f"[WARN] >> Garbage data received from {addr}: {data} (length of {len(data)})\n")

                    except Exception as ex:
                        PrintMSG(f"[ERROR] >> {ex}\n")
                        break

                PrintMSG(f"[INFO] >> {addr} disconnected.\n")

    # Close the socket and kill the server
    SOCK.close()
    KeepServerOpen = False

## MAIN CODE ##
if __name__ == '__main__':
    print("[===== PROTOGEN CENTRAL SERVER =====]\nPress \"ESCAPE\" or \"CTRL-C\" to quit.")

    # Remove the log if it exists
    if os.path.exists(LOG):
        os.remove(LOG)

    logging.basicConfig(filename=LOG, encoding='utf-8', level=logging.DEBUG)
    Monitor()
