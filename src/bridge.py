# SHIT IS GOING DOWN

import json
from threading import Thread
from src.app import App
from websockets.sync.client import connect

class Connection():
    def __init__(self, url, token):
        self.app = App.get_instance()
        self.socket = connect(url, additional_headers={"Authorization": f"Bearer {token}"})
        Thread(target = self.receive_message).start()
    
    def send_message(self, message):
        self.socket.send(message)
    
    async def receive_message(self):
        async for message in self.socket:
            unpack = json.loads(message)
            match unpack["type"]:
                case "message":
                    app.get_menu("chat").print_message(0, unpack["data"]["username"], unpack["data"]["content"])
                case "event":
                    app.get_menu("chat").print_message(unpack["data"]["content"], unpack["data"]["username"], "")
    
    def close(self):
        self.socket.close()
    
    