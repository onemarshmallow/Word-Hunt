import pygame
from game import Game


def main():

    pygame.init()
    pygame.font.init()
    # The screen size should be roughly (1200, 640).
    # The current dimensions (1150, 627) match the size of the background.png image.
    screen = pygame.display.set_mode((1150, 627))

    # Set the title of the display window.
    pygame.display.set_caption('Word Hunt')

    # Creates a game object.
    game = Game(screen)

    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


if __name__ == "__main__":
    main()
