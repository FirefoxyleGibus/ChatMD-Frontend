# ---------------------------
# This scripts deals with joining the backend to the UX
# It uses the "websocket" and "asyncio" libs
# ---------------------------
# The script will include I/O type functions that talk to the API
# Example :
#       send_message() : sends a message to the server
#       connect() : connects to a server
# ---------------------------
# First time doing those stuff
# ---------------------------

import asyncio
from websockets.sync.client import connect

def test():
    with connect("https://chatmd.tanukii.dev") as websocket:
        websocket.send("HEARTBEAT")
        message = websocket.recv()
        print(f"\"{message}\" received")

# Created by Foxy - Created at 15/06/2023