# ---------------------------
# This scripts deals with joining the backend to the UX
# It uses the "websocket" and "asyncio" libs
# ---------------------------
# The script will include I/O type functions that talk to the API
# Example :
#       send_message() : sends a message to the server
#       connect() : connects to a server
# ---------------------------
# TO DO : Handle HTTPS creds (and that's all)
# ---------------------------

import json
import asyncio
from src.termutil import *

def ping(websocket): # Sends a PING message and prints the answer !! DEBUG FUNCTION !!
    websocket.send("PING")
    print(websocket.recv())

def send_message(message, websocket): # Sends a message to the server !! DOESN'T LOG ANYTHING !!
    websocket.send(message)

def close_connection(websocket): # Closes the connection
    websocket.close()

async def receive(websocket): # Not tested yet but might work
    while True:
        message = await websocket.recv()
        menus["chat"].print_message(2, "server", message)
        
        

# Created by Foxy - Created at 15/06/2023