import os
import json
import asyncio
import time
import logging
from websockets import connect, ConnectionClosed

# setup logging
logging.basicConfig(level=logging.DEBUG, filename="debug_log.txt", filemode="w")

class Connection():
    """ Connection abstraction layer class """

    def __init__(self, app):
        self.app = app  
        self.status = "Offline"
        self.socket = None

        self.extra_headers = {}
        self.url = ""

        Connection.LOGIN_ENDPOINT = f"{os.getenv('API_HTTP_ADDRESS')}/auth/login"
        Connection.REGISTER_ENDPOINT = f"{os.getenv('API_HTTP_ADDRESS')}/auth/register"
        Connection.WS_ENDPOINT = f"{os.getenv('API_WS_ADDRESS')}"

    def send_message(self, message):
        """ Send a message to the server """
        if self.socket:
            task = asyncio.create_task(self.socket.send(message))
            logging.debug(task) # to prevent a "Task exception was never retrieved"
        else:
            logging.error("socket is not connected")
    
    async def run(self):
        """ Main entry of the program """
        logging.debug("Connecting to WS : %s", self.url)
        async for self.socket in connect(self.url, extra_headers=self.extra_headers):
            try:
                self.status = "Online"
                await self.receive_messages()
            except ConnectionClosed:
                self.status = "Offline"

    def connect(self, url, token):
        """ connect to a endpoint """
        logging.debug("Connecting at %s ...", url)
        self.url = url 
        self.extra_headers = {"Authorization": f"Bearer {token}"}
        logging.debug("TOKEN : %s", token)
        asyncio.ensure_future(self.run())
        logging.debug("Running bridge")
        return self

    async def receive_messages(self):
        """ Recieve messages """
        logging.debug(".")
        async for received_message in self.socket:
            logging.debug(received_message)
            message = json.loads(received_message)
            if isinstance(message, list): # last posted messages
                logging.info("Recieved Last messages: %s", message)
                for msg in message:
                    self._post_chat_message("", msg["username"], msg["message"], msg["at"], _preload = True)
                self.app.get_menu("chat").messages.reverse()
                continue
            logging.info("Received message: %s", message)
            # when message is just posted and we are connected
            match message["type"]:
                case "message":
                    self._post_chat_message("", message["data"]["username"], message["data"]["message"], int(time.time_ns()/1000))
                case "event":
                    self._post_chat_message(message["data"]["event"], message["data"]["username"], "")

    def _post_chat_message(self, msg_type, username, content, at = 0, _preload = False):
        self.app.get_menu("chat").print_message(msg_type, username, content, at, _preload = _preload)

    def close(self):
        """ Close the connection """
        self.socket.close()
        self.socket = None
    
    
