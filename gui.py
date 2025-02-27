import pygame
import math

font = pygame.font.SysFont(None, 48)

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

    def create_tictactoe_field(self, pos, lenght, client):
        self.buttons.append(Tic_Tac_Toe_field(pos, lenght, client))


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
        
        rendered_text = font.render(self.get_text(), True, "white", None)
        self.rect = rendered_text.get_rect(topleft=self.pos)
        self.rect.x = self.pos[0] - rendered_text.get_width() / 2
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
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.sender(index)

            
class Tic_Tac_Toe_field:
    def __init__(self, pos, length, client):
        self.pos = pygame.Vector2(pos)
        self.length = length
        self.client = client

    def update(self):
        pos = (pygame.Vector2(pygame.mouse.get_pos()) - self.pos) / self.length * 3

        x = math.floor(pos.x)
        y = math.floor(pos.y)

        if not (0 <= x <= 2 and 0 <= y <= 2):
            return

        self.client.tic_tac_toe_input([x, y])

    def drawgg(self, screen):
        # Horizontale Linien
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(0, self.length / 3), self.pos + pygame.Vector2(self.length, self.length / 3))
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(0, 2 * self.length / 3), self.pos + pygame.Vector2(self.length, 2 * self.length / 3))

        # Vertikale Linien
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(self.length / 3, 0), self.pos + pygame.Vector2(self.length / 3, self.length))
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(2 * self.length / 3, 0), self.pos + pygame.Vector2(2 * self.length / 3, self.length))

    def draw(self, screen):
        self.drawgg(screen)
        for y, y_val in enumerate(self.client.current_game):
            for x, val in enumerate(y_val):
                if val == '':
                    continue
                elif val == 'x':
                    self.draw_x(screen, (x, y))
                else:
                    self.draw_o(screen, (x, y))


    def draw_o(self, screen, pos):
        pygame.draw.circle(screen, "blue", self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(1, 1) * self.length / 3 / 2, self.length / 3 / 2 * 0.8, 1)

    def draw_x(self, screen, pos):
        pygame.draw.line(screen, "red", self.pos + pygame.Vector2(pos) * self.length / 3, self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(1, 1) * self.length / 3)
        pygame.draw.line(screen, "red", self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(0, 1) * self.length / 3, self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(1, 0) * self.length / 3)

