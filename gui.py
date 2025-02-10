import pygame
import math

font = pygame.font.SysFont(None, 48)

class GUI:
    def __init__(self):
        self.screen = pygame.display.get_surface()

        self.texts = []
        self.buttons = []

    def create_button(self, pos, text, func):
        self.buttons.append(Button(pos, text, func))

    def create_text(self, pos, text):
        self.texts.append(Text(pos, text))

    def create_tictactoe_field(self, pos, lenght, client):
        self.buttons.append(Tic_Tac_Toe_field(pos, lenght, client))


    def draw(self):
        for element in self.texts + self.buttons:
            element.draw(self.screen)

    def update(self):
        if not pygame.mouse.get_pressed()[0]:
            return
            
        for element in self.buttons:
            element.update()


class Text:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text
        
    def draw(self, screen):
        rendered_text = font.render(self.text, True, "white", None)
        self.rect = rendered_text.get_rect(topleft=self.pos)
        self.rect.x = self.pos[0] - rendered_text.get_width() / 2
        screen.blit(rendered_text, (self.pos[0] - rendered_text.get_width() / 2, self.pos[1]))


class Button(Text):
    def __init__(self, pos, text, func):
        super().__init__(pos, text)

        self.func = func

    def update(self):
        
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            
            self.func()
            
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

        self.client.tic_tac_toe_input(self.client.pos_to_zug((x, y)))

    def draw(self, screen):
        # Horizontale Linien
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(0, self.length / 3), self.pos + pygame.Vector2(self.length, self.length / 3))
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(0, 2 * self.length / 3), self.pos + pygame.Vector2(self.length, 2 * self.length / 3))

        # Vertikale Linien
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(self.length / 3, 0), self.pos + pygame.Vector2(self.length / 3, self.length))
        pygame.draw.line(screen, "white", self.pos + pygame.Vector2(2 * self.length / 3, 0), self.pos + pygame.Vector2(2 * self.length / 3, self.length))


    def draw_o(self, screen, pos):
        pygame.draw.circle(screen, "blue", self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(1, 1) * self.length / 3 / 2, self.length / 3 / 2 * 0.8, 1)

    def draw_x(self, screen, pos):
        pygame.draw.line(screen, "red", self.pos + pygame.Vector2(pos) * self.length / 3, self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(1, 1) * self.length / 3)
        pygame.draw.line(screen, "red", self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(0, 1) * self.length / 3, self.pos + pygame.Vector2(pos) * self.length / 3 + pygame.Vector2(1, 0) * self.length / 3)

