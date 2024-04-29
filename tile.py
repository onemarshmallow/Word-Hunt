import pygame


class Tile:
    # A Tile represents one letter on the grid.
    # A Tile holds the surface (image) and letter of that spot on the grid.
    main_color = pygame.Color("green")
    secondary_color = pygame.Color("red")
    # The format of the colors is pygame.Color(r, g, b, a) where a is the transparency. 255 = opague; 0 = transparent.
    white = pygame.Color(255, 255, 255, 150)
    green = pygame.Color(135, 247, 135, 75)
    yellow = pygame.Color(254, 252, 130, 125)
    border_width = 3

    @classmethod
    def set_screen(cls, screen):
        # sets the class attribute, screen
        # -  screen : the entire game display surface
        cls.screen = screen

    def __init__(self, surface, letter, screen_position, width, height, row, column):
        # initialize one instance of our Tile class. Tiles represent
        # one 'position' in our board.
        #  - screen_position: the [x, y] coordinates to draw the tile at
        #  -     width      : width of the tile
        #  -     height     : height of the tile
        #  -     row        : nth row in the board grid, starting at 0
        #  -     column     : nth column in the board grid, starting at 0

        self.screen_position = screen_position
        # Smoothscale resizes the image and makes it appear smooth on the screen.
        self.image = pygame.transform.smoothscale(surface, (width, height)) # This is the letter, with a transparent background.

        self.letter = letter
        self.row = row
        self.col = column
        rounded_square = pygame.image.load("resources/square_rounded_corners.png").convert_alpha() # This is image used as the background of the tile.
        self.background = pygame.transform.smoothscale(rounded_square, (width, height))

        # Creates a rectangle defining our boundaries.
        x, y = screen_position
        padding = 10  # between rectangle outline and the tile
        self.rect = pygame.Rect(x + padding, y + padding, width - 2 * padding, height - 2 * padding)

        # Creates the surfaces for the three different covers: white, green, yellow.
        self.white_cover = pygame.Surface((width, height), pygame.SRCALPHA)
        self.green_cover = pygame.Surface((width, height), pygame.SRCALPHA)
        self.yellow_cover = pygame.Surface((width, height), pygame.SRCALPHA)
        # Makes semi-transparent covers that appear when pressed.
        # border_radius makes the rectangle have rounded corners.
        pygame.draw.rect(self.white_cover, Tile.white, self.white_cover.get_rect(), border_radius=10)
        self.white_cover.set_alpha(0)  # Set them invisible for now, at the beginning.

        pygame.draw.rect(self.green_cover, Tile.green, self.green_cover.get_rect(), border_radius=10)
        self.green_cover.set_alpha(0)

        pygame.draw.rect(self.yellow_cover, self.yellow, self.yellow_cover.get_rect(), border_radius=10)
        self.yellow_cover.set_alpha(0)

    def draw_content(self):
        # Draws the tile, with the bakcground and letter, onto the screen.

        # Makes the drawn tile the same size as self.image.
        image_rect = self.image.get_rect(center=self.rect.center)
        # Blits to the screen the wooden square background and the tile.
        Tile.screen.blit(self.background, image_rect)
        Tile.screen.blit(self.image, image_rect)

    def draw(self, color=main_color):
        # Draw the tile, then draws the rectangle border on top in color.
        self.draw_content()
        # pygame.draw.rect(Tile.screen, color, self.rect, Tile.border_width)

    def set_cover(self, cover):
        # Helper function for self.change_color that makes the cover visible.

        # Makes the drawn tile the same size as self.image.
        image_rect = self.image.get_rect(center=self.rect.center)

        cover.set_alpha(255)
        Tile.screen.blit(cover, image_rect)
        # This is unneeded.
        # self.reset_other_covers(cover)

    def reset_covers(self):
        # Makes all covers invisible. Necessary so that when you do make the covers visible, you can check
        # the alpha value to blit it once, rather than continually blitting it onto the screen (which makes it opaque).

        self.white_cover.set_alpha(0)
        self.green_cover.set_alpha(0)
        self.yellow_cover.set_alpha(0)

    def reset_other_covers(self, cover):
        # Makes the covers beside the color cover invisible.
        # This is done specifically to fix the bug where multiple covers are visible at the same time.

        if cover is self.white_cover:
            self.green_cover.set_alpha(0)
            self.yellow_cover.set_alpha(0)
        elif cover is self.green_cover:
            self.white_cover.set_alpha(0)
            self.yellow_cover.set_alpha(0)
        elif cover is self.yellow_cover:
            self.white_cover.set_alpha(0)
            self.green_cover.set_alpha(0)

    def change_color(self, color):
        # Makes the semi-transparent rectangle over the tile visible.

        if color == Tile.white:
            transparency = self.white_cover.get_alpha()
            if transparency == 0:
                self.set_cover(self.white_cover)
        elif color == Tile.green:
            transparency = self.green_cover.get_alpha()
            if transparency == 0:
                self.set_cover(self.green_cover)
        elif color == Tile.yellow:
            transparency = self.yellow_cover.get_alpha()
            if transparency == 0:
                self.set_cover(self.yellow_cover)



    def isTileNearby(self, other_coords: tuple):
        # Checks if the other tile is next to this tile (horizontally, vertically, diagonally).
        # Assumes the board is 4x4.
        #  - other_coords : (row, column) of the other tile in the game board.
        if other_coords != ():
            other_row, other_col = other_coords
            col_difference = self.col - other_col
            row_difference = self.row - other_row

            # Case 1: the other tile is the same as this tile.
            if self.row == other_row and self.col == other_col:
                return False
            # Case 2: in same row (horizontal)
            elif self.row == other_row:
                if col_difference == 1 or col_difference == -1:
                    return True
            # Case 3: in same column (vertical)
            elif self.col == other_col:
                if row_difference == 1 or row_difference == -1:
                    return True
            # Case 4: diagonal
            elif (row_difference == 1 or row_difference == -1) and (col_difference == 1 or col_difference == -1):
                return True
            # Otherwise, they are not nearby.
            else:
                return False
