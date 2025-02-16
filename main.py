import pygame, socketio



pygame.init()
from gui import GUI

class Client:
    def __init__(self):

        self.screen = pygame.display.set_mode((400, 400))

        #self.create_gui()


        self.player_blue = True
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
        self.game_gui.create_text((200, 90), "Status")

        self.game_gui.create_tictactoe_field((100, 140), 200, self)


        self.start_gui.create_text((200, 50), "Tic Tac Toe")
        self.start_gui.create_button((200, 150), "Starte Tic Tac Toe", self.start_game_gui)
        self.start_gui.create_button((200, 250), "Anmelden", self.enter_room_code)

        self.game_gui.draw()

        self.current_gui = self.game_gui
        self.current_mode = self.tic_tac_toe_mode
        #gui.draw_tic_tac_toe_field()

    def enter_room_code(self):
        code = input("Was ist der Raum Code")
        send_room_code(str(code))



    def start_game_gui(self):
        self.current_gui = self.game_gui
        self.screen.fill("black")
        self.current_gui.draw()

        self.current_mode = self.tic_tac_toe_mode


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

    def draw_tic_tac_toe(self):
        pass

    
    def tic_tac_toe_mode(self):

        wert = input("feld: ")
        print(self.zug_to_pos(int(wert)))

        pos = self.zug_to_pos(int(wert))

        
        while not self.check_if_empty(pos[0], pos[1]):

            wert = input("feld: ")
            print(self.zug_to_pos(int(wert)))

            pos = self.zug_to_pos(int(wert))



        if self.player_blue:
            self.game_gui.buttons[-1].draw_o(self.screen, pos)
            self.current_game[pos[0]][pos[1]] = "o"
            self.player_blue = False

        else:
            self.game_gui.buttons[-1].draw_x(self.screen, pos)
            self.current_game[pos[0]][pos[1]] = "x"
            self.player_blue = True

    def switch_currentplayer(self):
        if self.player == 'o':
            self.current_player = 'x'
        else:
            self.current_player = 'o'

    def tic_tac_toe_input(self, input):

        if self.player != self.current_player:
            return

        pos = self.zug_to_pos(input)

        if not self.check_if_empty(pos[0], pos[1]):
            return
        

        
        if self.player_blue:
            self.game_gui.buttons[-1].draw_o(self.screen, pos)
            self.current_game[pos[0]][pos[1]] = "o"
            self.player_blue = False

        else:
            self.game_gui.buttons[-1].draw_x(self.screen, pos)
            self.current_game[pos[0]][pos[1]] = "x"
            self.player_blue = True


        send_zug(pos)

    def draw(self):
        self.current_gui.draw()




    def start_mode(self):
        pass

    def start_game(self):
        print("spiel startet")
        

    def run(self):
        running = True



        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



            self.current_gui.update()
            pygame.display.flip()
            #self.current_mode()

client = Client()

sio = socketio.Client()

@sio.event
def connect():
    print("Connected")


sio.connect('http://45.9.60.185:8903', transports=['websocket'])

def send_room_code(code):
    print(f"{code} wurde gesendet")
    sio.emit("sendCode", code)

def send_zug(pos):
    sio.emit('move', pos)

def spiel_startet():
    pass

def get_board(data):
    print(data)
    client.current_game = data['gameboard']
    client.current_gui.draw()
    client.switch_currentplayer()

def spieler2_joint(data):
    client.current_player = client.player
    client.start_game()

def code_recieved(data):
    print(data) # {'roomName': 'a', 'gameboard': [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']], 'users': 1, 'currentTurn': 0, 'char': 'x'}
    client.current_game = data['gameboard']


    client.player = data['char']

    if client.player == 'o':
        client.current_player = 'x'
    else:
        client.current_player = 'o'


    #client.player = client.player_blue

    if data['users'] == 2:
        client.start_game()





sio.on("codeReceived", code_recieved)
sio.on("userJoined", spieler2_joint)
sio.on("getBoard", get_board)

code = input("Code: ")

send_room_code(code)



client.create_gui()
client.run()