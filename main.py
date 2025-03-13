import pygame, socketio, json, random

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
        self.anmelden = True
        self.game_mode = 'normal'
        self.currentTurn = 0
        self.status = ""
        self.screen.fill(hintergrundfarbe)
        
        self.winner = ""

        self.raume = []
        self.unfiltered_räume = []

    def create_gui(self):
        self.start_gui = GUI()
        self.game_gui = GUI()
        self.raueme_gui = GUI()
        self.verbinden_gui = GUI()
        self.raueme_aussuchen_gui = GUI()
        self.winner_gui = GUI()
        self.anmelden_gui = GUI()


        self.anmelden_gui.create_text((300, 50), "", self.get_anmelden_registrieren)
        self.anmelden_gui.create_textinput((300, 100), "username", False, self)
        self.anmelden_gui.create_textinput((300, 150), "Passwort", False, self)
        self.anmelden_gui.create_button((300, 200), "Senden", self.sende_anmelden)



        self.winner_gui.create_text((300, 150), "", self.get_winnertext)
        self.winner_gui.create_button((300, 200), "Hauptmenu", self.start_start_gui)

        self.raueme_aussuchen_gui.create_button((100, 40), "zurück", self.start_online_game)
        self.raueme_aussuchen_gui.create_button((400, 40), "refreshen", self.frage_räume)
        self.raueme_aussuchen_gui.create_button((240, 40), "manuell", self.code_manuel_senden)
        self.raueme_aussuchen_gui.create_button((300, 100), "Raum erstellen", self.raum_erstellen)
        self.raueme_aussuchen_gui.create_text((300, 150), "Wähle einen Raum aus")
        self.raueme_aussuchen_gui.create_liste((300, 200), self.get_raeume, self.sende_räume)

        self.verbinden_gui.create_button((300, 150), "Raum aussuchen", self.start_raum_aussuchen)
        self.verbinden_gui.create_button((300, 250), "Code eingeben", self.start_code_eingeben)
        self.verbinden_gui.create_button((300, 350), "Matchmaking", self.start_matchmaking)

        self.raueme_gui.create_button((200, 40), "zurück", self.start_start_gui)
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
        self.start_gui.create_button((300, 250), "Anmelden", self.start_anmelden_gui)
        self.start_gui.create_button((300, 300), "Registrieren", self.start_registrieren_gui)

        self.start_gui.draw()

        self.current_gui = self.start_gui
        #gui.draw_tic_tac_toe_field()

    def code_manuel_senden(self):
        code = input("Gebe einencode ein: ")
        send_room_code(code, self.game_mode)

    def raum_erstellen(self):
        code = self.generiere_neuen_wert(self.raume)
        send_room_code(code, self.game_mode)
        self.start_game_gui()
        #self.draw()

    def generiere_neuen_wert(self, arr):
        while True:
            neu = ''.join(random.choices("0123456789", k=4))
            if neu not in arr:
                return neu

    def frage_räume(self):
        getRooms()
        self.draw()

    def get_raeume(self):
        l = []
        print(self.unfiltered_räume)
        for r in self.unfiltered_räume:
            if r["type"] == self.game_mode:
                l.append(r["code"])

        return l
    
    def sende_räume(self, index):
        send_room_code(self.get_raeume()[index], self.game_mode)
        self.start_game_gui()
        print(index)

    def start_raueme_aussuchen_gui(self):
        self.current_gui = self.raueme_aussuchen_gui
        self.draw()

    def start_anmelden_gui(self):
        self.anmelden = True
        self.current_gui = self.anmelden_gui
        self.draw()

    def start_registrieren_gui(self):
        self.anmelden = False
        self.current_gui = self.anmelden_gui
        self.draw()

    def sende_anmelden(self):
        print("anmelden")
        if self.anmelden:
            send_anmelden(self.anmelden_gui.text_inputs[0].text, self.anmelden_gui.text_inputs[1].text)
        else:
            send_register(self.anmelden_gui.text_inputs[0].text, self.anmelden_gui.text_inputs[1].text)
        self.start_start_gui()

    def get_anmelden_registrieren(self):
        if self.anmelden: 
            return "Anmelden"
        return "Registrieren"

    def get_anmelden_text(text):
        print(text)

    def get_winnertext(self):
        if self.player == self.winner:
            return f"{self.username}, du hast Gewonnen"
        return f"{self.username}, du hast Leider verloren"
    
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
        #code = input("Code: ")
        self.game_mode = 'normal'

        #send_room_code(code, "normal")
        

        self.start_raueme_aussuchen_gui()

    def start_ultimate(self):
        #code = input("Code: ")
        self.game_mode = "ultimate"

        for y in range(3):
            for x in range(3):
                self.current_game[y][x] = [["", "", ""], ["", "", ""], ["", "", ""]]

        #send_room_code(code, "ultimate")
        print("ultimate")

        self.init_ultimate_tictactoe()

        self.start_raueme_aussuchen_gui()

    def start_limited(self):
        #code = input("Code: ")
        
        self.game_mode = "limited"

        #send_room_code(code, "limited")

        self.start_raueme_aussuchen_gui()

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

    def start_start_gui(self):
        self.current_gui = self.start_gui
        self.draw()

    def offline_verarbeitung(self, pos):
        if not self.check_if_empty(pos[0], pos[1]):
            return
        
        self.current_game[pos[1]][pos[0]] = self.current_player

    def pos_to_zug(self, pos):
        return pos[0] + pos[1] * 3

    def switch_currentplayer(self):
        if self.current_player == 'o':
            self.current_player = 'x'
        else:
            self.current_player = 'o'

    def tic_tac_toe_input(self, pos, id):

        if self.game_mode == "ultimate":
            if id[0] == 99:
                return
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

        keys_pressed = set()



        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                try:
                    if event.key not in keys_pressed:
                        keys_pressed.add(event.key)

                        self.current_gui.update_textinputs(event)

                    elif event.key in keys_pressed:
                        keys_pressed.remove(event.key)
                except:
                    pass



            self.current_gui.update()
            pygame.display.flip()

client = Client()

def send_room_code(code, spielart=""):
    print(f"{code} wurde gesendet")
    sio.emit("sendCode", [code, spielart])

def send_anmelden(username, passwort):
    print((username, passwort))

    if client.online == True:
        return

    if not connect_to_server():
        return

    #username = input("Gebe ein Username ein: ")
    #passwort = input("Gebe ein Passwort ein: ")
    sio.emit("login", [username, passwort])
    client.online = True

    getRooms()


def send_register(username, passwort):
    print((username, passwort))

    if client.online == True:
        return

    if not connect_to_server():
        return
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
    if winner == "":
        print("draw")
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
    client.unfiltered_räume = räume
    l = []
    print(räume)
    for raum in räume:
        l.append(raum['code'])
    print(l)
    client.raume = l

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