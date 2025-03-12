import pygame, socketio, json

hintergrundfarbe = (219, 229, 234)

pygame.init()
from gui import GUI

class Client:
    def __init__(self):

        self.screen = pygame.display.set_mode((600, 400))

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
        self.screen.fill(hintergrundfarbe)
        
        self.winner = ""

    def create_gui(self):
        self.start_gui = GUI()
        self.game_gui = GUI()
        self.raueme_gui = GUI()
        self.verbinden_gui = GUI()
        self.raueme_aussuchen_gui = GUI()
        self.winner_gui = GUI()



        self.winner_gui.create_text((300, 200), "", self.get_winnertext)

        self.raueme_aussuchen_gui.create_text((300, 100), "Wähle einen Raum aus")
        #self.raueme_aussuchen_gui.create_liste((300, 200), )

        self.verbinden_gui.create_button((300, 150), "Raum aussuchen", self.start_raum_aussuchen)
        self.verbinden_gui.create_button((300, 250), "Code eingeben", self.start_code_eingeben)
        self.verbinden_gui.create_button((300, 350), "Matchmaking", self.start_matchmaking)

        self.raueme_gui.create_button((300, 150), "normal", self.start_normal)
        self.raueme_gui.create_button((300, 250), "ultimate", self.start_ultimate)
        self.raueme_gui.create_button((300, 350), "limited", self.start_limited)

        self.game_gui.create_text((300, 20), "")
        self.game_gui.create_text((300, 20), "spieler", getter=self.get_spieler)
        self.game_gui.create_text((300, 90), "Status", getter=self.get_status)

        self.tic_tac_x = 100
        self.tic_tac_y = 140
        self.tic_tac_lenght = 200

        self.game_gui.create_tictactoe_field((self.tic_tac_x, self.tic_tac_y), self.tic_tac_lenght, self, 3)


        self.start_gui.create_text((300, 50), "Tic Tac Toe")
        self.start_gui.create_text((300, 100), "Melde dich an um spielen zu können")
        self.start_gui.create_button((300, 150), "Online Spielen", self.start_online_game)
        #self.start_gui.create_button((300, 250), "Offline Spielen", self.start_offline_game)
        self.start_gui.create_button((300, 250), "Anmelden", send_anmelden)
        self.start_gui.create_button((300, 300), "Registrieren", send_register)

        self.start_gui.draw()

        self.current_gui = self.start_gui
        #gui.draw_tic_tac_toe_field()

    def get_winnertext(self):
        if self.player == self.winner:
            return f"{self.username}, du hast Gewonnen"
        return f"{self.username}, du hast Leider verloren"

    def get_raume(self):
        return []
    
    def sende_raum(self, index):
        print(index)

    def init_ultimate_tictactoe(self):
        for y in range(3):
            for x in range(3):
                self.game_gui.create_tictactoe_field((self.tic_tac_x + x/3*200, self.tic_tac_y + y/3*200), self.tic_tac_lenght / 3, self, id=[x, y])


    def enter_room_code(self):
        code = input("Was ist der Raum Code")
        send_room_code(str(code))

    def get_status(self):
        return self.status
    
    def get_spieler(self):
        return f"Spieler {self.player}"
    
    def start_raum_aussuchen(self):
        pass

    def start_code_eingeben(self):
        pass

    def start_matchmaking(self):
        pass
    
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
                self.current_game[y][x] = [["o", "", ""], ["", "x", ""], ["", "", "o"]]

        send_room_code(code, "ultimate")
        print("ultimate")

        self.init_ultimate_tictactoe()

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
        self.screen.fill(hintergrundfarbe)
        self.draw()
        #self.current_gui.draw()
        if self.game_mode == "ultimate":
            self.draw_ultimate()

    def offline_verarbeitung(self, pos):
        if not self.check_if_empty(pos[0], pos[1]):
            return
        
        self.current_game[pos[1]][pos[0]] = self.current_player



    def switch_currentplayer(self):
        if self.current_player == 'o':
            self.current_player = 'x'
        else:
            self.current_player = 'o'

    def tic_tac_toe_input(self, pos, id):

        if self.game_mode == "ultimate":
            pos = [id[0], id[1], pos[0], pos[1]]
            print("ultimate")
            print(pos)
            sio.emit('move', pos)

        print(self.game_mode)

        if self.online == True:
            sio.emit('move', pos)
            print(pos)
        else:
            self.offline_verarbeitung(pos)


    def draw(self):
        self.screen.fill(hintergrundfarbe)
        self.current_gui.draw()

        if self.game_mode == "ultimate":
            self.draw_ultimate()

    def draw_ultimate(self):
        client.game_gui.buttons[len(client.game_gui.buttons) - 1 -9].drawgg(self.screen)

        for y in range(3):
            for x in range(3):
                client.game_gui.buttons[len(client.game_gui.buttons) -9 + self.pos_to_zug([x, y])].draw_single(self.screen, self.current_game[y][x])

        

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

    if not connect_to_server():
        return

    username = input("Gebe ein Username ein: ")
    passwort = input("Gebe ein Passwort ein: ")
    sio.emit("login", [username, passwort])
    client.online = True

    getRooms()


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
    if client.game_mode != "ultimate":
        client.game_gui.buttons[-1].draw(client.screen)

    #client.draw_ultimate()
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


    if data['users'] == 2:
        client.start_game()

    if data['currentTurn'] == 0:
        client.status = "Warte bis Spieler 2 beitritt"
    else:
        client.status = "Warte auf den Zug von Spieler 1"

    client.draw()

        

def get_winner(winner):
    print("Der Gewinner ist: " + winner)
    client.winner = winner
    client.current_gui = client.winner_gui
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
    client.username = data["username"]
    # data["username"]  ["id"]

def sendRooms(räume):
    print(räume)

def getRooms(type="normal"):
    sio.emit("getRooms", type)


sio = socketio.Client()
@sio.event
def connect():
    print("Connected")

def connect_to_server():
    print('Connect')
    if client.online == False:
        with open('data.json') as data:
           adresse = json.load(data)
        try:

            sio.connect(adresse, transports=['websocket'])
        except:
            
            print("Server ist nicht online")
            return False

    client.online = True
    return True



sio.on("codeReceived", code_recieved)
sio.on("userJoined", spieler2_joint)
sio.on("getBoard", get_board)
sio.on("winner", get_winner)
sio.on("registerError", registerError)
sio.on("registerSuccess", registerSuccess)
sio.on("session", get_session)
sio.on("loginError", loginError)
sio.on("sendRooms", sendRooms)



client.create_gui()
client.run()