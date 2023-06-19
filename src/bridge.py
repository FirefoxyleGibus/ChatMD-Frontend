# SHIT IS GOING DOWN

import json
import asyncio
from websockets.client import connect

import logging
logging.basicConfig(level=logging.DEBUG, filename="debug_sockets.txt")

class Connection():
    """ Connection abstraction layer class """

    def __init__(self, app):
        self.app = app  
        self.status = "Offline"
        self.socket = None

    def send_message(self, message):
        """ Send a message to the server """
        if self.socket:
            self.socket.send(message)
        else:
            print("Nope")
    
    async def run(self):
        """ Main entry of the program """
        while True:
            if self.socket:
                await self.receive_messages()

    def connect(self, url, token):
        """ connect to a endpoint """
        print(f"Connecting at {url} ...")
        self.socket = connect(url, extra_headers={"Authorization": f"Bearer {token}"})
        return self

    async def receive_messages(self):
        """ Recieve messages """
        async for received_message in self.socket:
            message = json.loads(received_message)
            print(message)
            if isinstance(message, list): # last posted messages
                for msg in message:
                    await self.post_chat_message("", msg["username"], msg["message"])
                continue
            # when message is just posted and we are connected
            match message["type"]:
                case "message":
                    await self.post_chat_message("", message["data"]["username"], message["data"]["content"])
                case "event":
                    await self.post_chat_message(message["data"]["content"], message["data"]["username"], message["data"]["content"])

    async def post_chat_message(self, msg_type, username, content):
        self.app.get_menu("chat").print_message(msg_type, username, content)

    def close(self):
        """ Close the connection """
        self.socket.close()
        self.socket = None
    
    
