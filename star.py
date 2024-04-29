import pygame

class Star:
    def __init__(self, screen):
        self.screen = screen
        self.size = (100, 100)
        star = pygame.image.load("resources/star.png").convert_alpha()
        self.star = pygame.transform.smoothscale(star, self.size)
        empty_star = pygame.image.load("resources/star_outline.png").convert_alpha()
        self.empty_star = pygame.transform.smoothscale(empty_star, self.size)



    def draw(self):
        # Draws the empty star.

        rightX, bottomY = self.screen.get_size()
        x_pos, y_pos = rightX - 350, bottomY - 110

        self.screen.blit(self.empty_star, (x_pos, y_pos))


    def fill_star(self):
        # Draws the complete star.
        rightX, bottomY = self.screen.get_size()
        x_pos, y_pos = rightX - 350, bottomY - 110

        self.screen.blit(self.star, (x_pos, y_pos))
