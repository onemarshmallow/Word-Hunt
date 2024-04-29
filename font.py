import pygame

class Font:
    """Contains fonts for use in the game."""
    def __init__(self):
        pygame.font.init()
        self.title_font = pygame.font.SysFont("arialblack", 60)
        self.score_font = pygame.font.SysFont("arialblack", 30)
        # self.words_font = pygame.font.SysFont("arialblack", 25)
        self.guess_font = pygame.font.SysFont("verdana", 50, bold=True)

class Text:
    def __init__(self, text, x, y, font, color=(0, 0, 0), background=None):
        self.x = x  # Horizontal center or top left of box, depends on which draw method you use.
        self.y = y  # Vertical center or top left of box
        # Start PyGame Font
        pygame.font.init()

        self.txt = font.render(text, True, color, background)
        self.size = font.size(text)  # (width, height)

    def draw_centered(self, screen):
        drawX = self.x - (self.size[0] // 2)
        drawY = self.y - (self.size[1] // 2)
        coords = (drawX, drawY)
        screen.blit(self.txt, coords)

    def draw_left_aligned(self, screen):
        coords = (self.x, self.y)
        screen.blit(self.txt, coords)
