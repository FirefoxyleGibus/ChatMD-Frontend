"""
    ChatMenu class file
"""
import asyncio
import logging
from notifypy import Notify

from .basemenu import BaseMenu
from .ui_elements import TextBox, ElementStyle, DropDown
from .ui_elements.base_selectable import BaseSelectable
from src.app import App
from src.bridge import Connection
from src.termutil import print_at, color_text

# ---------------------------
# TO DO : Handle reception
#       Either a "show message" func or smth else, i'll try to work with it dw
# Tell me how it works
# ---------------------------
# Also now you can type send_message(message, self.websocket) when you want to send a message
# and close_connection(self.websocket) to close the connection
# /!\ DON'T FORGET TO CLOSE THE CONNECTION /!\


class ChatMenu(BaseMenu):
    """ Chat menu """
    name = "#Guigui"
    color = 0x17ff67
    channel = "general"
    messages = []
    _online_members = set()
    connection = None

    def __init__(self):
        super().__init__("chat")
        self._textbox = TextBox(1, "", ">>> ", style={
            'anchor':'center', 'align':"left", 'background':False
        })
        
        lang = App.get_locale();
        self._esc_menu = DropDown(40, button_text=lang.get('menu'), options=[
            (lang.get("return_to_chat"), "return_to_chat"),
            (lang.get("profile"),        "profile"),
            (lang.get("view_connected"), "view_connected"),
            (lang.get("disconnect"),     "disconnect"),
            (lang.get("quit"),           "quit"),
        ], style={'anchor': 'left'}).set_on_change(self._execute_esc_button)

        self._users_list_menu = DropDown(40, button_text=lang.get("online_users"), 
            options=[('', '')], style={'anchor': 'left'}
        ).set_on_change(self._close_users_list)

        self._latency = 0
    
    def start(self):
        self.focus_selectable(self._textbox)
        self.messages = []

    def set_latency(self, latency):
        """ Set the latency """
        self._latency = latency

    def add_online(self, username):
        """ Add online member to list """
        self._online_members.add(username)

    def remove_online(self, username):
        """ Remove online member """
        self._online_members.discard(username)

    def _draw_messages(self, terminal, max_message_draw_pos=1, start_pos=4):
        locale = App.get_locale()
        curmsg = len(self.messages)-1
        msgdrawpos = terminal.height-start_pos
        while msgdrawpos > max_message_draw_pos and curmsg >= 0:
            nowmsg = self.messages[curmsg]
            match nowmsg[0]:
                case 'message':
                    usrw = len(f"{nowmsg[1]}: ")
                    maxw = terminal.width - usrw
                    coltxt = color_text(terminal, nowmsg[2])
                    line_amount = round(
                        (len(terminal.strip_seqs(coltxt)) / maxw)+0.5)
                    col = terminal.normal if nowmsg[3] != - \
                        1 else terminal.grey50
                    if msgdrawpos-line_amount+1 > max_message_draw_pos:
                        print_at(terminal, 0, msgdrawpos-line_amount+1,
                                 col + terminal.bold(nowmsg[1]) + col + ": ")
                        print_at(terminal, usrw, msgdrawpos-line_amount+1,
                                 terminal.ljust(col + coltxt, int(terminal.width-usrw))
                                 + terminal.normal + terminal.clear_eol())
                    else:
                        text_to_crop = terminal.ljust(
                            col + coltxt, int(terminal.width-usrw)).split("\n")
                        print_at(terminal, usrw, max_message_draw_pos, "\n".join(
                            text_to_crop[-((msgdrawpos-line_amount+1)-max_message_draw_pos):]))
                    msgdrawpos -= max(1, line_amount)
                case 'join':
                    print_at(terminal, 0, msgdrawpos, terminal.green("[+] ")
                        + locale.get('welcome').format(user=terminal.bold(nowmsg[1]))
                        + terminal.clear_eol())
                    msgdrawpos -= 1
                case 'leave':
                    print_at(terminal, 0, msgdrawpos, terminal.red("[-] ")
                        + locale.get('goodbye').format(user=terminal.bold(nowmsg[1]))
                        + terminal.clear_eol())
                    msgdrawpos -= 1
            curmsg -= 1

    def _execute_esc_button(self, button):
        app = App.get_instance()
        match button:
            case "quit":
                # adios
                app.quit()
            case "profile":
                # Yeee baby
                logging.debug("profile username")
                app.get_menu("profile").set_username(self.name)
                logging.debug("profile lang")
                app.get_menu("profile").set_lang(app.user_settings.get("locale"))
                logging.debug("Showing profile?")
                app.show_menu("profile")
                return self._textbox
            case "view_connected":
                # update user list
                self._users_list_menu.set_options([(username, username) for username in self._online_members])
                self._users_list_menu.set_choosing(True)
                # force it to show menu bcoz its pretty
                self._esc_menu.set_choosing(True)
                return self._users_list_menu
            case "disconnect":
                # smaller adios (with abandonment issues ig plz fix it)
                # FIX: fix killing connection
                if self.connection:
                    _ = asyncio.create_task(self.connection.close())
                # remove auto connect
                app.user_settings.set("auto_connect", False)
                app.user_settings.set("session_token", '')
                app.show_menu("login")
                # close menu
                return self._textbox
            case _:
                # get back to real stuff bby
                return self._textbox
        
    def _close_users_list(self, _value):
        self._esc_menu.set_choosing(True)
        return self._esc_menu

    def draw(self, terminal) -> None:
        self._textbox.resize(terminal.width-1)

        print_at(terminal, 0, terminal.height-3, "─"*terminal.width)
        self._textbox.draw(terminal, terminal.width//2, terminal.height - 2)
        
        # connection status
        latency = terminal.center(f"{self._latency}ms", 6)
        topright = f"   {self.connection.status} | {latency} | {len(self._online_members)} online"
        print_at(terminal, terminal.width-len(topright), 0, topright)
        
        # Esc menu
        if self._esc_menu.is_selected:
            self._esc_menu.draw(terminal, 0, 0)
            self._draw_messages(terminal, max_message_draw_pos=self._esc_menu.render_height, start_pos=4)
        elif self._users_list_menu.is_selected:
            self._esc_menu.draw(terminal, 0, 0)
            self._users_list_menu.draw(terminal, self._esc_menu.width + 2, 0)
            self._draw_messages(terminal,
                max_message_draw_pos=max(self._esc_menu.render_height, self._users_list_menu.render_height), start_pos=4)
        else:
            self._draw_messages(terminal, start_pos=4)

            print_at(terminal, 1, 0, f"#{self.channel}")
            print_at(terminal, 0, 1, "─"*terminal.width)

    def handle_input(self, terminal):
        val = super().handle_input(terminal)
        if val.name == "KEY_ENTER":
            if self._textbox.text.strip() != "":
                self.messages.append(
                    ('message', self.name, self._textbox.text, -1))
                print(terminal.clear)
                self.connection.send_message(self._textbox.text)
                self._textbox.set_text("")
        elif val.name == "KEY_ESCAPE" and self._textbox.is_selected:
            self.focus_selectable(self._esc_menu)
            self._esc_menu.set_choosing(True)
            print(terminal.clear)
        else:
            pass

    def connect(self, token):
        """ Connect to the backend """
        self.connection = App.get_instance().websocket.connect(
            Connection.WS_ENDPOINT, token)

    def print_message(self, message_type, username, content, date, _preload=False, _color=0x0):
        """
        Appends a message to the screen

        message_type:
            "Join" : join
            "Leave" : leave
            others : message
        """
        match message_type:
            case "Join":
                self.messages.append(('join', username, date))
                if not _preload:
                    Notify(default_notification_application_name="ChatMD",
                           default_notification_icon=r"chatmd.ico",
                           default_notification_title=username,
                           default_notification_message="just joined !").send(block=False)
                    self.add_online(username)
            case "Leave":
                self.messages.append(('leave', username, date))
                if not _preload:
                    Notify(default_notification_application_name="ChatMD",
                           default_notification_icon=r"chatmd.ico",
                           default_notification_title=username,
                           default_notification_message="just left !").send(block=False)
                    self.remove_online(username)
            case _:
                if ('message', username, content, -1) in self.messages:
                    self.messages.remove(('message', username, content, -1))
                elif not _preload:
                    Notify(default_notification_application_name="ChatMD",
                            default_notification_icon=r"chatmd.ico",
                            default_notification_title=username,
                            default_notification_message=content).send(block=False)
                self.messages.append(('message', username, content, date))
