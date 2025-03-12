import pygame
import math
import time

font = pygame.font.SysFont(None, 48)
buttonfarbe =  (14, 24, 62)
textfarbe = "white"

class GUI:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.maus_gedrückt = False

        self.texts = []
        self.text_inputs = []
        self.buttons = []

    def create_button(self, pos, text, func):
        self.buttons.append(Button(pos, text, func))

    def create_text(self, pos, text, getter=False):
        self.texts.append(Text(pos, text, getter))

    def create_textinput(self, pos, text, sender, client):
        self.text_inputs.append(TextInput(pos, text, sender, client))

    def create_liste(self, pos, getter, sender):
        self.buttons.append(Liste(pos, getter, sender))

    def create_tictactoe_field(self, pos, lenght, client, dicke=1, id=[99, 99]):
        self.buttons.append(Tic_Tac_Toe_field(pos, lenght, client, dicke, id))


    def draw(self):
        for element in self.texts + self.buttons + self.text_inputs:
            element.draw(self.screen)

    def update(self):

        if self.maus_gedrückt == pygame.mouse.get_pressed()[0]:
            return

        self.maus_gedrückt = pygame.mouse.get_pressed()[0]
            
        for element in self.buttons:
            element.update()

        for element in self.text_inputs:
            element.check_active()

    def update_textinputs(self, event):
        for element in self.text_inputs:
            element.update(event)


class Text:
    def __init__(self, pos, text, getter):
        self.pos =  pygame.Vector2(pos)
        self.text = text

        if getter:
            self.get_text = getter

    def get_text(self):
        return self.text
        
    def draw(self, screen):
        rendered_text = font.render(self.get_text(), True, textfarbe, None)
        self.rect = rendered_text.get_rect(topleft=self.pos)
        self.rect.x = self.pos[0] - rendered_text.get_width() / 2

        pygame.draw.rect(screen, buttonfarbe,  self.rect.inflate(10, 10))
        screen.blit(rendered_text, (self.pos.x - rendered_text.get_width() / 2, self.pos.y))


class Button(Text):
    def __init__(self, pos, text, func):
        super().__init__(pos, text, False)

        self.func = func

    def update(self):
        
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            
            self.func()

class Liste():
    def __init__(self, pos, getter, sender):
        self.pos = pygame.Vector2(pos)
        self.getter = getter
        self.sender = sender

        self.elements = []

    def draw(self, screen):
        self.elements = []
        for index, text in enumerate(self.getter()):
            self.elements.append(Text(self.pos + pygame.Vector2(0, index * 50), text, None))
            self.elements[index].draw(screen)


    def update(self):
        for index, element in enumerate(self.elements):
            if element.rect.collidepoint(pygame.mouse.get_pos()):
                self.sender(index)

class TextInput(Text):
    def __init__(self, pos, text, sender, client):
        super().__init__(pos, text, getter=False)
        self.active = False
        self.sender = sender
        self.client = client

    def check_active(self):
        self.active = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.active:
            self.text = ''
            #self.client.draw()

    def update(self, event):
        if self.active:
            try:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.client.draw()
                elif event.key == 13:
                    print(13)
                    #self.text = ""
                    #self.client.draw()
                    #self.sender(self.text)  
                    #print(self.sender)
                    self.active = False
                else:
                    self.text += event.unicode 
                    self.client.draw()
                    time.sleep(0.2)
            except:
                pass


            
class Tic_Tac_Toe_field:
    def __init__(self, pos, length, client, dicke=1, id=[99, 99]):
        self.pos = pygame.Vector2(pos)
        self.length = length
        self.client = client
        self.dicke = dicke
        self.id = id

    def update(self):
        pos = (pygame.Vector2(pygame.mouse.get_pos()) - self.pos) / self.length * 3

        x = math.floor(pos.x)
        y = math.floor(pos.y)

        if not (0 <= x <= 2 and 0 <= y <= 2):
            return

        self.client.tic_tac_toe_input([x, y], self.id)

    def draw_single(self, screen, game):
        self.drawgg(screen)
        for y, y_val in enumerate(game):
            for x, val in enumerate(y_val):
                if val == '':
                    continue
                elif val == 'x':
                    self.draw_x(screen, (x, y))
                elif val == 'o':
                    self.draw_o(screen, (x, y))

    def drawgg(self, screen):
        # Horizontale Linien
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(0, self.length / 3), self.pos + pygame.Vector2(self.length, self.length / 3), self.dicke)
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(0, 2 * self.length / 3), self.pos + pygame.Vector2(self.length, 2 * self.length / 3), self.dicke)

        # Vertikale Linien
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(self.length / 3, 0), self.pos + pygame.Vector2(self.length / 3, self.length), self.dicke)
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(2 * self.length / 3, 0), self.pos + pygame.Vector2(2 * self.length / 3, self.length), self.dicke)

    def draw(self, screen):
        self.draw_single(screen, self.client.current_game)


    def draw_o(self, screen, pos):
        pygame.draw.circle(screen, "blue", self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(1, 1) * self.length / 3 / 2, self.length / 3 / 2 * 0.8, 1)

    def draw_x(self, screen, pos):
        pygame.draw.line(screen, "red", self.pos + pygame.Vector2(pos) * self.length / 3, self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(1, 1) * self.length / 3)
        pygame.draw.line(screen, "red", self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(0, 1) * self.length / 3, self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(1, 0) * self.length / 3)

