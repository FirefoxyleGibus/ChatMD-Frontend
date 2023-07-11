"""
    Websockect bridge to the backend (see Connection)
"""
import os
import json
import asyncio
import logging
import requests
from websockets import connect, ConnectionClosed

class Connection():
    """ Connection abstraction layer class """

    def __init__(self, app):
        self.app = app
        self.status = "Offline"
        self._is_logged_in = False
        self.socket = None

        self.extra_headers = {}
        self.url = ""

        self._run_task = None

        Connection.LOGIN_ENDPOINT = f"{os.getenv('API_HTTP_ADDRESS')}/auth/login"
        Connection.LOGOUT_ENDPOINT = f"{os.getenv('API_HTTP_ADDRESS')}/auth/logout"
        Connection.REGISTER_ENDPOINT = f"{os.getenv('API_HTTP_ADDRESS')}/auth/register"
        Connection.WS_ENDPOINT = f"{os.getenv('API_WS_ADDRESS')}"

        Connection.USERNAME_ENDPOINT = f"{os.getenv('API_HTTP_ADDRESS')}/account/update/username"

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
                logging.info("Connection Closed")
                break
            except asyncio.exceptions.CancelledError:
                logging.info("Trying to close this thread")
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
        """ Receive messages """
        async for received_data in self.socket:
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

    def logout(self):
        """ Log out from server """
        logging.info("Logging out")
        if self._is_logged_in:
            res = self._http_request("delete", Connection.LOGOUT_ENDPOINT)
            if res.status_code == 200:
                self._is_logged_in = False
            return res
        return None

    async def close(self):
        """ Close the connection """
        self.logout()
        logging.debug("Closing bridge")
        if self._run_task:
            self._run_task.cancel()
            self._run_task = None

        if self.socket:
            await self.socket.close()

    def _http_request(self, method, url, data=None, needs_auth=True):
        token = self.app.token
        headers = {}
        request_data = data if data else {}
        if needs_auth:
            headers = {"Authorization": f"Bearer {token}"}
        logging.debug("REQUEST:[%s] AT %s WITH %s [Headers:%s]", method, url, request_data, headers)
        match method:
            case "post"|"POST":
                return requests.post(url, data=request_data, headers=headers, timeout=5.0)
            case "get"|"GET":
                return requests.get(url, data=request_data, headers=headers, timeout=5.0)
            case "put"|"PUT":
                return requests.put(url, data=request_data, headers=headers, timeout=5.0)
            case "delete"|"DELETE":
                return requests.delete(url, data=request_data, headers=headers, timeout=5.0)
            case _:
                return None
        return None

    def request_login(self, username, password):
        """ Request login HTTP Request
            :username: string
            :password: string
        """
        data = {'username': username, 'password': password}
        return self._http_request("post", Connection.LOGIN_ENDPOINT, data, needs_auth=False)

    def request_register(self, username, password):
        """ Request register HTTP Request
            :username: string
            :password: string
        """
        data = {'username': username, 'password': password}
        return self._http_request("post", Connection.REGISTER_ENDPOINT, data, needs_auth=False)

    def request_update_username(self, new_username):
        """ Request update username HTTP Request
            :new_username: string
        """
        return self._http_request("put", Connection.USERNAME_ENDPOINT,
                data = {"username": new_username})
