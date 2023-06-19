# SHIT IS GOING DOWN

import json
import asyncio
from websockets import connect
from src.app import App

class Connection():
    """ Connection abstraction layer class """

    def __init__(self, url, token):
        self.app = App.get_instance()
        self.socket = None

        self.main_task = asyncio.run(self._start(url, token))
        

    def send_message(self, message):
        """ Send a message to the server """
        self.socket.send(message)
    
    async def _start(self, url, token):
        print(f"Connecting at {url} ...")
        self.socket = await connect(url, extra_headers={"Authorization": f"Bearer {token}"})
        print("CONNECTED !")
        await self.receive_messages()

    async def receive_messages(self):
        """ Recieve messages """
        async for received_message in self.socket:
            message = json.loads(received_message)
            print(message)
            if type(message) == list: # last posted messages
                for msg in message:
                    self.post_chat_message("", msg["username"], msg["message"])
                continue
            # when message is just posted and we are connected
            match message["type"]:
                case "message":
                    self.post_chat_message("", message["data"]["username"], message["data"]["content"])
                case "event":
                    self.post_chat_message(message["data"]["content"], message["data"]["username"], message["data"]["content"])

    def post_chat_message(self, msg_type, username, content) -> None:
        self.app.get_menu("chat").print_message(msg_type, username, content)


    def close(self):
        """ Close the connection """
        self.main_task.close(),
        self.socket.close()
    
    
