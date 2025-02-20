import pygame, socketio



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

    def create_gui(self):
        self.start_gui = GUI()
        self.game_gui = GUI()

        self.game_gui.create_text((200, 20), "Spiel 1")
        self.game_gui.create_text((200, 90), "Status", getter=self.get_status)

        self.game_gui.create_tictactoe_field((100, 140), 200, self)


        self.start_gui.create_text((200, 50), "Tic Tac Toe")
        self.start_gui.create_button((200, 150), "Starte Tic Tac Toe", self.start_game_gui)
        self.start_gui.create_button((200, 250), "Anmelden", self.enter_room_code)

        self.start_gui.draw()

        self.current_gui = self.start_gui
        #gui.draw_tic_tac_toe_field()

    def enter_room_code(self):
        code = input("Was ist der Raum Code")
        send_room_code(str(code))

    def get_status(self):
        return self.player



    def start_game_gui(self):
        connect_to_server()
        self.current_gui = self.game_gui
        self.screen.fill("black")
        self.current_gui.draw()




    def zug_to_pos(self, zug):
        return [zug % 3, zug // 3]
    
    def pos_to_zug(self, pos):
        return pos[0] + pos[1] * 3 
    
    def check_if_empty(self, x, y):
        if self.current_game[x][y] == "":
            return True
        return False
    
    def check_if_game_over(self):
        pass


    def switch_currentplayer(self):
        if self.current_player == 'o':
            self.current_player = 'x'
        else:
            self.current_player = 'o'

    def tic_tac_toe_input(self, input):

        if self.player != self.current_player:
            return
        
        self.switch_currentplayer()


        #if not self.check_if_empty(input[0], input[1]):
        #    return
        


        send_zug(input)


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

def send_room_code(code, spielart):
    print(f"{code} wurde gesendet")
    sio.emit("sendCode", [code, spielart])

def send_anmelden(username, passwort):
    sio.emit("login", [username, passwort])

def send_register(username, passwort):
    sio.emit("register", [username, passwort])

def send_zug(pos):
    sio.emit('move', pos)
    print(pos)

def spiel_startet():
    pass

def get_board(data):
    print(data)
    client.current_game = data['gameboard']
    client.draw()
    client.game_gui.buttons[-1].draw(client.screen)
    client.switch_currentplayer()
    print(client.current_player)

def spieler2_joint(data):
    client.current_player = client.player
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

def get_winner(winner):
    print(winner)

def get_all_rooms(rooms):
    print(rooms)


sio = socketio.Client()

@sio.event
def connect():
    print("Connected")

def connect_to_server():
    print('Connect')
    sio.connect('http://45.9.60.185:8903', transports=['websocket'])

    code = input("Code: ")

    send_room_code(code)


sio.on("codeReceived", code_recieved)
sio.on("userJoined", spieler2_joint)
sio.on("getBoard", get_board)
sio.on("winner", get_winner)



client.create_gui()
client.run()