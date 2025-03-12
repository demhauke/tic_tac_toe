import pygame
import math

font = pygame.font.SysFont(None, 48)
buttonfarbe =  (14, 24, 62)
textfarbe = "white"

class GUI:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.maus_gedrückt = False

        self.texts = []
        self.buttons = []

    def create_button(self, pos, text, func):
        self.buttons.append(Button(pos, text, func))

    def create_text(self, pos, text, getter=False):
        self.texts.append(Text(pos, text, getter))

    def create_liste(self, pos, getter, sender):
        self.buttons.append(Liste(pos, getter, sender))

    def create_tictactoe_field(self, pos, lenght, client, dicke=1, id=[99, 99]):
        self.buttons.append(Tic_Tac_Toe_field(pos, lenght, client, dicke, id))


    def draw(self):
        for element in self.texts + self.buttons:
            element.draw(self.screen)

    def update(self):

        if self.maus_gedrückt == pygame.mouse.get_pressed()[0]:
            return

        self.maus_gedrückt = pygame.mouse.get_pressed()[0]
            
        for element in self.buttons:
            element.update()


class Text:
    def __init__(self, pos, text, getter):
        self.pos = pos
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
        screen.blit(rendered_text, (self.pos[0] - rendered_text.get_width() / 2, self.pos[1]))


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
            self.elements.append(Text(self.pos + pygame.Vector2(0, index * 50), text))
            self.elements[index].draw(screen)


    def update(self):
        for index, element in enumerate(self.elements):
            if element.rect.collidepoint(pygame.mouse.get_pos()):
                self.sender(index)

class TextInput(Text):
    def __init__(self, pos, width, getter=None, sender=None):
        super().__init__(pos, "", getter)
        self.pos = pygame.Vector2(pos)
        self.width = width
        self.getter = getter  
        self.sender = sender  

        self.text = "" if not getter else getter()
        self.active = False

    def draw(self, screen):
        input_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, 40)
        pygame.draw.rect(screen, "white" if self.active else "gray", input_rect, 2)
        
        text_surface = font.render(self.text, True, textfarbe)
        screen.blit(text_surface, (self.pos.x + 5, self.pos.y + 5))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Prüfen, ob auf das Eingabefeld geklickt wurde
            input_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, 40)
            self.active = input_rect.collidepoint(event.pos)

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                if self.sender:
                    self.sender(self.text)  # Senden des Textes, wenn Sender gesetzt
                self.active = False
            else:
                self.text += event.unicode  # Zeichen hinzufügen

            
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

