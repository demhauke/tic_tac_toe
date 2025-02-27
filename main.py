import pygame, socketio, json



pygame.init()
from gui import GUI

class Client:
    def __init__(self):

        self.screen = pygame.display.set_mode((400, 400))

        #self.create_gui()

        self.player = 'x'
        self.current_player = 'x'

        self.current_game = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

        self.online = False
        self.game_mode = "normal"
        self.currentTurn = 0
        self.status = ""

    def create_gui(self):
        self.start_gui = GUI()
        self.game_gui = GUI()
        self.raueme_gui = GUI()


        self.raueme_gui.create_button((200, 150), "normal", self.start_normal)
        self.raueme_gui.create_button((200, 250), "ultimate", self.start_ultimate)
        self.raueme_gui.create_button((200, 350), "limited", self.start_limited)

        self.game_gui.create_text((200, 20), "")
        self.game_gui.create_text((200, 20), "spieler", getter=self.get_spieler)
        self.game_gui.create_text((200, 90), "Status", getter=self.get_status)

        self.game_gui.create_tictactoe_field((100, 140), 200, self)


        self.start_gui.create_text((200, 50), "Tic Tac Toe")
        self.start_gui.create_button((200, 150), "Online Spielen", self.start_online_game)
        #self.start_gui.create_button((200, 250), "Offline Spielen", self.start_offline_game)
        self.start_gui.create_button((200, 250), "Anmelden", send_anmelden)
        self.start_gui.create_button((200, 300), "Registrieren", send_register)

        self.start_gui.draw()

        self.current_gui = self.start_gui
        #gui.draw_tic_tac_toe_field()

    def enter_room_code(self):
        code = input("Was ist der Raum Code")
        send_room_code(str(code))

    def get_status(self):
        return self.status
    
    def get_spieler(self):
        return f"Spieler {self.player}"
    
    def start_normal(self):
        code = input("Code: ")
        self.game_mode = "normal"

        send_room_code(code, "normal")
        

        self.start_game_gui()

    def start_ultimate(self):
        code = input("Code: ")
        self.game_mode = "ultimate"

        for y in range(3):
            for x in range(3):
                self.current_game[y][x] = [["", "", ""], ["", "", ""], ["", "", ""]]

        send_room_code(code, "ultimate")

        self.start_game_gui()

    def start_limited(self):
        code = input("Code: ")
        
        self.game_mode = "limited"

        send_room_code(code, "limited")

        self.start_game_gui()

    def start_raume_gui(self):
        self.current_gui = self.raueme_gui
        self.draw()

    def start_online_game(self):
        # send_anmelden() #ja gerade buggy 
        print("Online")
        self.online = True
        connect_to_server()
        
        self.start_raume_gui()

    def start_offline_game(self):
        print("offline")
        self.online = False
        self.start_game_gui()


    def start_game_gui(self):
        self.current_gui = self.game_gui
        self.screen.fill("black")
        self.current_gui.draw()

    def offline_verarbeitung(self, pos):
        if not self.check_if_empty(pos[0], pos[1]):
            return
        
        self.current_game[pos[1]][pos[0]] = self.current_player


        

    def zug_to_pos(self, zug):
        return [zug % 3, zug // 3]
    
    def pos_to_zug(self, pos):
        return pos[0] + pos[1] * 3 
    
    def check_if_empty(self, x, y):
        if self.current_game[y][x] == "":
            return True
        return False
    
    def check_if_winning(self):
        pass
        #for i in range(3):
        #    if self.current_game[i]



    def switch_currentplayer(self):
        if self.current_player == 'o':
            self.current_player = 'x'
        else:
            self.current_player = 'o'

    def tic_tac_toe_input(self, pos):

        #if self.player != self.current_player:
        #    return
        
        #self.switch_currentplayer()


        #if not self.check_if_empty(pos[0], pos[1]):
        #    return
        

        if self.online == True:
            sio.emit('move', pos)
            print(pos)
        else:
            self.offline_verarbeitung(pos)


    def draw(self):
        self.screen.fill('black')
        self.current_gui.draw()


    def start_mode(self):
        pass

    def start_game(self):
        print("spiel startet")
        self.draw()
        

    def run(self):
        running = True



        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



            self.current_gui.update()
            pygame.display.flip()

client = Client()

def send_room_code(code, spielart=""):
    print(f"{code} wurde gesendet")
    sio.emit("sendCode", [code, spielart])

def send_anmelden():
    if client.online == True:
        return

    connect_to_server()

    username = input("Gebe ein Username ein: ")
    passwort = input("Gebe ein Passwort ein: ")
    sio.emit("login", [username, passwort])
    client.online = True


def send_register():
    if client.online == False:
        connect_to_server()
    username = input("Gebe ein Username ein: ")
    passwort = input("Gebe ein Passwort ein: ")
    sio.emit("register", [username, passwort])

def spiel_startet():
    pass

def get_board(data):
    print(data)
    client.current_game = data['gameboard']
    client.game_gui.buttons[-1].draw(client.screen)
    client.switch_currentplayer()
    if client.current_player == client.player:
        client.status = "Mache einen Zug"
    else:
        client.status = "Warte"
    print(client.current_player)
    client.draw()

def spieler2_joint(data):
    client.current_player = client.player
    client.status = "Mache einen Zug"
    client.start_game()

def code_recieved(data):
    print(data) # {'roomName': 'a', 'gameboard': [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']], 'users': 1, 'currentTurn': 0, 'char': 'x'}
    client.current_game = data['gameboard']


    client.player = data['char']
    print(client.player)

    if client.player == 'o':
        client.current_player = 'x'
    else:
        client.current_player = 'o'


    #client.player = client.player_blue

    if data['users'] == 2:
        client.start_game()

    if data['currentTurn'] == 0:
        client.status = "Warte bis Spieler 2 beitritt"
    else:
        client.status = "Warte auf den Zug von Spieler 1"

    client.draw()

    
        

def get_winner(winner):
    print("Der Gewinner ist: " + winner)
    client.current_gui = client.start_gui
    client.draw()

def get_all_rooms(rooms):
    print(rooms)

def registerError(data):
    if data == 1:
        print("Error")
    elif data == 2:
        print("Benutzer existiert bereits")

def loginError(data):
    if data == 1:
        print("Error")
    elif data == 2:
        print("Benutzer existiert bereits")
    else:
        print("Das Passwort ist falsch")

def registerSuccess(data):
    if data == True:
        print("Du bist jetzt registriert")

def get_session(data):
    print(data)
    # data["username"]  ["id"]


sio = socketio.Client()
#sio.connect('http://45.9.60.185:8903', transports=['websocket'])
@sio.event
def connect():
    print("Connected")

def connect_to_server():
    print('Connect')
    if client.online == False:
        with open('data.json') as data:
           adresse = json.load(data)
        sio.connect(adresse, transports=['websocket'])

    client.online = True



sio.on("codeReceived", code_recieved)
sio.on("userJoined", spieler2_joint)
sio.on("getBoard", get_board)
sio.on("winner", get_winner)
sio.on("registerError", registerError)
sio.on("registerSuccess", registerSuccess)
sio.on("session", get_session)
sio.on("loginError", loginError)



client.create_gui()
client.run()