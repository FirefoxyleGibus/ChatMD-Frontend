from websockets import connect

from src.menus.basemenu import *
from src.app import App
from src.user_prefs.user_settings import *
from src.bridge import *

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
    currentlytyped = ""
    name = "#Guigui"
    color = 0x17ff67
    channel = "general"
    messages = []
    cursor = 0
    quit_button_selected = False
    connection = None

    def __init__(self):
        super().__init__("chat")

    def _draw_messages(self, terminal):
        locale = UserSettings.get_current().get_locale()
        curmsg = len(self.messages)-1
        msgdrawpos = terminal.height-4
        while msgdrawpos > 2 and curmsg >= 0:
            nowmsg = self.messages[curmsg]
            match nowmsg[0]:
                case 'message':
                    usrw = len(f"{nowmsg[1]}: ")
                    maxw = terminal.width - usrw
                    line_amount = round((len(nowmsg[2]) / maxw)+0.5)
                    print_at(terminal, 0,msgdrawpos-(line_amount-1),f"{nowmsg[1]}: ")
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

    def draw(self, terminal) -> None:
        lang = App.get_instance().user_settings.get_locale()
        print_at(terminal, 0, terminal.height-2, ">>  " + self.currentlytyped + terminal.clear_eol)
        print_at(terminal, 1,0,f"#{self.channel}")
        print_at(terminal, 0,1, "─"*terminal.width)
        print_at(terminal, 0,terminal.height-3, "─"*terminal.width)
        print_at(terminal, terminal.width - len(lang.get("quit")),0, terminal.reverse + terminal.red(lang.get("quit")))

        print_at(terminal, terminal.width - len(lang.get("quit"))-10,0, self.connection.status)

        if self.quit_button_selected:
            print_at(terminal, terminal.width - len(lang.get("quit")) - 2, 0, terminal.blink(">"))
        else:
            print_at(terminal, 2,terminal.height-2,terminal.blink('>'))

        self._draw_messages(terminal)

    def handle_input(self, terminal):
        val = super().handle_input(terminal)
        if val.name == "KEY_ENTER":
            if self.currentlytyped != "":
                self.messages.append(('message', self.name, self.currentlytyped, -1))
                print(terminal.clear)
                self.connection.send_message(self.currentlytyped)
                self.currentlytyped = ""
            elif self.quit_button_selected:
                App.get_instance().quit()
        elif val.name in ("KEY_DOWN", "KEY_UP"):
            print(terminal.clear)
            self.quit_button_selected = not self.quit_button_selected
        else:
            self.currentlytyped, self.cursor = textbox_logic(self.currentlytyped, self.cursor, val)

    def connect(self, token):
        """ Connect to the backend """
        self.connection = App.get_instance().websocket.connect("ws://localhost:8081",token)

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
