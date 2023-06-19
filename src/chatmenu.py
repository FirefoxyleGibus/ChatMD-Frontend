from src.basemenu import *
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
    currentlytyped = ""
    name = "#Guigui"
    color = 0x17ff67
    channel = "general"
    messages = [
#         ('join', "[null]"),
#         ('message', "[null]", "sup you motherfuckers it's me null the one and only now cry about it hahahahaha, now check this out im gonna make this text multiline and you can't do shit about it"),
#         ('leave', "[null]")
    ]
    cursor = 0
    def draw_messages(self):
        locale = UserSettings.get_current().get_locale()
        curmsg = len(self.messages)-1
        msgdrawpos = term.height-4
        while msgdrawpos > 2 and curmsg >= 0:
            nowmsg = self.messages[curmsg]
            match nowmsg[0]:
                case 'message':
                    usrw = len(f"{nowmsg[1]}: ")
                    maxw = term.width - usrw
                    lineAmount = round((len(nowmsg[2]) / maxw)+0.5)
                    print_at(0,msgdrawpos-(lineAmount-1),f"{nowmsg[1]}: ")
                    for i in range(lineAmount):
                        print_at(usrw,msgdrawpos-(lineAmount-1)+i,nowmsg[2][i*maxw:(i+1)*maxw])
                    msgdrawpos-=lineAmount
                case 'join':
                    print_at(0, msgdrawpos, term.green("[+]") + f" {locale.get('welcome')}, {term.bold(nowmsg[1])}!")
                    msgdrawpos-=1
                case 'leave':
                    print_at(0, msgdrawpos, term.red("[-]") + f" {locale.get('goodbye')}, {term.bold(nowmsg[1])}!")
                    msgdrawpos-=1
            curmsg -= 1

    def draw(self) -> None:
        print_at(0, term.height-2, ">>> " + self.currentlytyped + term.clear_eol)
        print_at(1,0,f"#{self.channel}")
        print_at(0,1, "─"*term.width)
        print_at(0,term.height-3, "─"*term.width)
        self.draw_messages()

    def handle_input(self):
        val = super().handle_input()
        if val.name == "KEY_ENTER" and self.currentlytyped != "":
            self.messages.append(('message', self.name, self.currentlytyped))
            print(term.clear)
            self.currentlytyped = ""
        else:
            self.currentlytyped, self.cursor = textbox_logic(self.currentlytyped, self.cursor, val)

    def connect(self, token):
        # Let's pretend that we connecting
    
    def print_message(self, mesType, username, content, color=0x0):
        """
        Appends a message to the screen
        
        mesType:
            0 : join
            1 : leave
            2 : message
        """
        match mesType:
            case 0:
                self.messages.append(('join', username))
            case 1:
                self.messages.append(('leave', username))
            case 2:
                self.messages.append(('message', username, content))


    def __init__(self) -> None:
        super().__init__()
