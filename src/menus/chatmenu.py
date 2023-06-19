from src.menus.basemenu import *
from src.user_prefs.user_settings import *

class ChatMenu(BaseMenu):
    """ Chat menu """
    currentlytyped = ""
    name = "#Guigui"
    color = 0x17ff67
    channel = "general"
    messages = [
        ('join', "[null]"),
        ('message', "[null]", "sup you motherfuckers it's me null the one and only now cry about it hahahahaha, now check this out im gonna make this text multiline and you can't do shit about it"),
        ('leave', "[null]")
    ]
    cursor = 0

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
                    for i in range(line_amount):
                        print_at(terminal, usrw,msgdrawpos-(line_amount-1)+i,nowmsg[2][i*maxw:(i+1)*maxw])
                    msgdrawpos-=line_amount
                case 'join':
                    print_at(terminal, 0, msgdrawpos, terminal.green("[+]") + f" {locale.get('welcome')}, {terminal.bold(nowmsg[1])}!")
                    msgdrawpos-=1
                case 'leave':
                    print_at(terminal, 0, msgdrawpos, terminal.red("[-]") + f" {locale.get('goodbye')}, {terminal.bold(nowmsg[1])}!")
                    msgdrawpos-=1
            curmsg -= 1

    def draw(self, terminal) -> None:
        print_at(terminal, 0, terminal.height-2, ">>> " + self.currentlytyped + terminal.clear_eol)
        print_at(terminal, 1,0,f"#{self.channel}")
        print_at(terminal, 0,1, "─"*terminal.width)
        print_at(terminal, 0,terminal.height-3, "─"*terminal.width)
        self._draw_messages(terminal)

    def handle_input(self, terminal):
        val = super().handle_input(terminal)
        if val.name == "KEY_ENTER" and self.currentlytyped != "":
            self.messages.append(('message', self.name, self.currentlytyped))
            print(terminal.clear)
            self.currentlytyped = ""
        else:
            self.currentlytyped, self.cursor = textbox_logic(self.currentlytyped, self.cursor, val)

    def connect(self, token):
        # ---------------------------
        # okay foxy moved your thing here
        # TO DO : Handle connection with ws
        # TO DO : Handle reception
        #       Either a "show message" func or smth else, i'll try to work with it dw
        # ---------------------------

        self.messages.append(("join", self.name))
