import os
import json
import asyncio
import time
import logging
from websockets import connect, ConnectionClosed

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
        async for received_data in self.socket:
            logging.debug(received_data)
            data = json.loads(received_data)

            # ON JOIN
            if "messages" in data: # last posted messages
                logging.info("Recieved Last messages: %s", data["messages"])
                for msg in data["messages"]:
                    self._handle_new_message(msg, on_join_message=True)
                self.app.get_menu("chat").messages.reverse()
                continue

            if "online" in data:
                logging.info("Online members: %s", data["online"])
                for member in data["online"]:
                    self.app.get_menu("chat").add_online(member["username"])
            
            logging.info("Received message: %s", data)
            # when message is just posted and we are connected
            self._handle_new_message(data)

    def _handle_new_message(self, message, on_join_message=False):
        msg_type = message["type"]
        data = message if on_join_message else message.get("data", message)
        match msg_type:
            case "message" if data["message"]:
                self.app.get_menu("chat").print_message(msg_type, data["username"], data["message"], data["at"], _preload = on_join_message)
            case "event":
                self.app.get_menu("chat").print_message(data["event"], data["username"], "", data["at"], _preload = on_join_message)
            case "latency":
                self.app.get_menu("chat").set_latency(data["latency_ms"])

    def close(self):
        """ Close the connection """
        self.socket.close()
        self.socket = None

