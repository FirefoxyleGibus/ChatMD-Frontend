"""
    ChatMenu class file
"""
from notifypy import Notify

from src.menus.basemenu import BaseMenu
from src.menus.ui_elements import TextBox, ElementStyle
from src.menus.ui_elements.base_selectable import BaseSelectable
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
    esc_menu = False
    esc_pos = 0
    esc_buttons = [
        "return_to_chat",
        "profile",
        "view_connected",
        "quit",
    ]

    def __init__(self):
        super().__init__("chat")
        self._textbox = TextBox(1, "", ">>> ", style=ElementStyle({
                'anchor':'center', 'align':"left", 'background':False
            }))
        self._esc_focus = BaseSelectable()

        self._latency = 0
    
    def start(self):
        self.focus_selectable(self._textbox)

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

    def _execute_esc_button(self, button, terminal):
        match button:
            case "quit":
                App.get_instance().quit()
            case "profile":
                pass
            case "view_connected":
                pass
            case _:
                self.esc_menu = False
                self.focus_selectable(self._textbox)
                print(terminal.clear)

    def _draw_esc_menu(self, terminal):
        lang = App.get_locale()
        for option, button in enumerate(self.esc_buttons):
            prefix = terminal.blink(">") + " " + terminal.reverse if self.esc_pos == option \
                else "  "
            print_at(terminal, 1, option, prefix+lang.get(button) + " " *
                     (terminal.width - len(lang.get(button)) - 5) + terminal.normal)
        print_at(terminal, 0, len(self.esc_buttons), "─"*terminal.width)

    def draw(self, terminal) -> None:
        self._textbox.resize(terminal.width-1)

        print_at(terminal, 0, terminal.height-3, "─"*terminal.width)
        self._textbox.draw(terminal, terminal.width//2, terminal.height - 2)
        if self.esc_menu:
            # this will be used when i make a proper options dropdown
            self._esc_focus.draw(terminal, 0, 0)
            self._draw_esc_menu(terminal)
            self._draw_messages(terminal, max_message_draw_pos=len(
                self.esc_buttons), start_pos=4)
        else:
            self._draw_messages(terminal, start_pos=4)
            # connection status
            latency = terminal.center(f"{self._latency}ms", 6)
            topright = f"   {self.connection.status} | {latency} | {len(self._online_members)} online"
            print_at(terminal, terminal.width-len(topright), 0, topright)

            print_at(terminal, 1, 0, f"#{self.channel}")
            print_at(terminal, 0, 1, "─"*terminal.width)

    def handle_input(self, terminal):
        val = super().handle_input(terminal)
        if self.esc_menu:
            if val.name == "KEY_ESCAPE":
                self.esc_menu = False
                self.focus_selectable(self._textbox)
                print(terminal.clear)
            elif val.name in ("KEY_DOWN", "KEY_UP"):
                self.esc_pos += {"KEY_DOWN": 1, "KEY_UP": -1}[val.name]
                self.esc_pos %= len(self.esc_buttons)
            elif val.name == "KEY_ENTER":
                # TODO: THE BUTTONS
                self._execute_esc_button(
                    self.esc_buttons[self.esc_pos], terminal)
        else:
            if val.name == "KEY_ENTER":
                if self._textbox.text.strip() != "":
                    self.messages.append(
                        ('message', self.name, self._textbox.text, -1))
                    print(terminal.clear)
                    self.connection.send_message(self._textbox.text)
                    self._textbox.set_text("")
            elif val.name == "KEY_ESCAPE":
                self.focus_selectable(self._esc_focus)
                print(terminal.clear)
                self.esc_menu = True
                self.esc_pos = 0
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
