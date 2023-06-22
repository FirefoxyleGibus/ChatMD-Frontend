from websockets import connect

from src.menus.basemenu import BaseMenu
from src.menus.ui_elements import TextBox
from src.menus.ui_elements.base_selectable import BaseSelectable
from src.app import App
from src.user_prefs.user_settings import UserSettings
from src.bridge import Connection
from src.termutil import *

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
        self._textbox = TextBox(1, "", ">>> ", anchor='center', align="left", reverse_background=False)
        self._esc_focus = BaseSelectable()
        self.focus_selectable(self._textbox)

    def _draw_messages(self, terminal, max_message_draw_pos=1, start_pos=4):
        locale = UserSettings.get_current().get_locale()
        curmsg = len(self.messages)-1
        msgdrawpos = terminal.height-start_pos
        while msgdrawpos > max_message_draw_pos and curmsg >= 0:
            nowmsg = self.messages[curmsg]
            match nowmsg[0]:
                case 'message':
                    usrw = len(f"{nowmsg[1]}: ")
                    maxw = terminal.width - usrw
                    line_amount = round((len(nowmsg[2]) / maxw)+0.5)
                    print_at(terminal, 0,msgdrawpos-(line_amount-1),f"{terminal.bold(nowmsg[1])}: ")
                    col = terminal.normal if nowmsg[3] != -1 else terminal.grey50
                    for i in range(line_amount):
                        print_at(terminal, usrw, msgdrawpos-(line_amount-1)+i, col + nowmsg[2][i*maxw:(i+1)*maxw] + terminal.clear_eol() + terminal.normal)
                    msgdrawpos-=line_amount
                case 'join':
                    print_at(terminal, 0, msgdrawpos, terminal.green("[+] ") + locale.get('welcome').format(user = terminal.bold(nowmsg[1])) + terminal.clear_eol())
                    msgdrawpos-=1
                case 'leave':
                    print_at(terminal, 0, msgdrawpos, terminal.red("[-] ") + locale.get('goodbye').format(user = terminal.bold(nowmsg[1])) + terminal.clear_eol())
                    msgdrawpos-=1
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
        lang = App.get_instance().user_settings.get_locale()
        for option,button in enumerate(self.esc_buttons):
            prefix = terminal.blink(">") + " " + terminal.reverse if self.esc_pos == option \
                else "  "
            print_at(terminal, 1, option, prefix+lang.get(button) + " " * (terminal.width - len(lang.get(button)) - 5) + terminal.normal)
        print_at(terminal, 0,len(self.esc_buttons), "─"*terminal.width)

    def draw(self, terminal) -> None:
        self._textbox.resize(terminal.width-1)

        print_at(terminal, 0, terminal.height-3, "─"*terminal.width)
        self._textbox.draw(terminal, terminal.width//2, terminal.height - 2)
        if self.esc_menu:
            self._esc_focus.draw(terminal, 0, 0) # this will be used when i make a proper options dropdown
            self._draw_esc_menu(terminal)
            self._draw_messages(terminal, max_message_draw_pos=len(self.esc_buttons), start_pos=4)
        else:
            self._draw_messages(terminal, start_pos=4)
            print_at(terminal, terminal.width-10,0, self.connection.status)
            print_at(terminal, 1,0,f"#{self.channel}")
            print_at(terminal, 0,1, "─"*terminal.width)



    def handle_input(self, terminal):
        val = super().handle_input(terminal)
        if self.esc_menu:
            if val.name == "KEY_ESCAPE":
                self.esc_menu = False
                self.focus_selectable(self._textbox)
                print(terminal.clear)
            elif val.name in ("KEY_DOWN", "KEY_UP"):
                self.esc_pos += {"KEY_DOWN":1, "KEY_UP": -1}[val.name]
                self.esc_pos %= len(self.esc_buttons)
            elif val.name == "KEY_ENTER":
                # pass # TODO: THE BUTTONS
                self._execute_esc_button(self.esc_buttons[self.esc_pos], terminal)
        else:
            if val.name == "KEY_ENTER":
                if self._textbox.text != "":
                    self.messages.append(('message', self.name, self._textbox.text, -1))
                    print(terminal.clear)
                    self.connection.send_message(self._textbox.text)
                    self._textbox.text = ""
            elif val.name == "KEY_ESCAPE":
                self.focus_selectable(self._esc_focus)
                print(terminal.clear)
                self.esc_menu = True
                self.esc_pos = 0
            else:
                pass

    def connect(self, token):
        """ Connect to the backend """
        self.connection = App.get_instance().websocket.connect(Connection.WS_ENDPOINT,token)

    def print_message(self, message_type, username, content, at, _color=0x0):
        """
        Appends a message to the screen
        
        message_type:
            "Join" : join
            "Leave" : leave
            others : message
        """
        match message_type:
            case "Join":
                self.messages.append(('join', username, at))
            case "Leave":
                self.messages.append(('leave', username, at))
            case _:
                if ('message', username, content, -1) in self.messages:
                    self.messages.remove(('message', username, content, -1))
                self.messages.append(('message', username, content, at))
