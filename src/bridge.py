"""
    Websockect bridge to the backend (see Connection)
"""
import os
import json
import asyncio
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

        self._run_task = None

        Connection.LOGIN_ENDPOINT = f"{os.getenv('API_HTTP_ADDRESS')}/auth/login"
        Connection.REGISTER_ENDPOINT = f"{os.getenv('API_HTTP_ADDRESS')}/auth/register"
        Connection.WS_ENDPOINT = f"{os.getenv('API_WS_ADDRESS')}"

        Connection.USERNAME_ENDPOINT = f"{os.getenv('API_HTTP_ADDRESS')}/username"

    def send_message(self, message):
        """ Send a message to the server """
        if self.socket:
            task = asyncio.create_task(self._send(message))
            logging.debug(task) # to prevent a "Task exception was never retrieved"
        else:
            logging.error("socket is not connected")

    async def _send(self, message):
        try:
            await self.socket.send(message)
        except ConnectionClosed as err:
            logging.error(err)

    async def run(self):
        """ Main entry of the program """
        logging.debug("Connecting to WS : %s", self.url)
        async for self.socket in connect(self.url, extra_headers=self.extra_headers):
            try:
                self.status = "Online"
                await self.receive_messages()
            except ConnectionClosed:
                self.status = "Offline"
                break
            except asyncio.exceptions.CancelledError:
                break

    def connect(self, url, token):
        """ connect to a endpoint """
        logging.debug("Connecting at %s ...", url)
        self.url = url
        self.extra_headers = {"Authorization": f"Bearer {token}"}
        logging.debug("TOKEN : %s", token)
        if self._run_task is None:
            self._run_task = asyncio.ensure_future(self.run())
        logging.debug("Running bridge")
        return self

    async def receive_messages(self):
        """ Recieve messages """
        async for received_data in self.socket:
            logging.debug(received_data)
            data = json.loads(received_data)

            # ON JOIN
            if "messages" in data: # last posted messages
                for msg in data["messages"]:
                    self._handle_new_message(msg, on_join_message=True)
                self.app.get_menu("chat").messages.reverse()

            if "online" in data:
                for member in data["online"]:
                    self.app.get_menu("chat").add_online(member["username"])

            if "messages" in data or "online" in data:
                continue

            # when message is just posted and we are connected
            self._handle_new_message(data)

    def _handle_new_message(self, message, on_join_message=False):
        msg_type = message["type"]
        data = message if on_join_message else message.get("data", message)
        match msg_type:
            case "message" if data["message"]:
                self.app.get_menu("chat").print_message(msg_type,
                    data["username"], data["message"], data["at"], _preload = on_join_message)
            case "event":
                self.app.get_menu("chat").print_message(data["event"],
                    data["username"], "", data["at"], _preload = on_join_message)
            case "latency":
                self.app.get_menu("chat").set_latency(data["latency_ms"])

    def close(self):
        """ Close the connection """
        logging.debug("Closing bridge")
        if self.socket:
            try:
                _ = asyncio.create_task(self.socket.close())
            except RuntimeError as err:
                logging.error(err)
        if self._run_task:
            self._run_task.cancel()
            self._run_task = None
