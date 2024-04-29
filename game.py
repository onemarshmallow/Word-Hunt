import pygame
from tile import Tile
from font import Font, Text
from process_words import WordProcessor
from star import Star


class Game:
    # An object in this class represents a complete game.
    def __init__(self, screen):
        # - screen is the display window surface object

        self.screen = screen
        self.bg = pygame.image.load("resources/background.png").convert()
        self.bg_color = (75, 94, 72)  # (75, 94, 72) is darkGreen
        self.white = (255, 255, 255)
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.timer = 80  # The timer is 80 seconds.
        self.font = Font()
        self.close_clicked = False  # When this is true, the game closes.
        self.continue_game = True  # When this is false, the gameplay has ended but the screen remains present.
        self.words = WordProcessor.readWordsFile("words.txt")  # dictionary of accepted words (in all caps) : score
        self.guessed_words = []  # The self.words that have been guessed.
        self.word_num = 0  # The number of words guessed correctly. Used in the label on screen.
        self.score_num = 0  # The player's score. Used in the label on screen.
        self.grid = []
        self.star = Star(self.screen)  # Initializes the star.
        self.prom_guessed = False



        self.board = [
            ["P", "R", "S", "U"],
            ["E", "S", "O", "I"],
            ["R", "M", "T", "R"],
            ["D", "A", "P", "A"]
        ]

        Tile.set_screen(self.screen)

        self.create_grid()

    def create_grid(self):
        # Creates a grid of tiles.

        for rowNum, row in enumerate(self.board):
            # - rowNum: the numbered row we are on
            # -  row  : the list of letters within the self.board

            # Loads the images into surfaces, for this particular row.
            imgNames = ["resources/" + letter + ".png" for letter in row]
            # must be .convert_alpha() if using transparent image
            imageSurfaces = [pygame.image.load(imgName).convert_alpha() for imgName in imgNames]

            # Creates each row in the grid.
            new_row = self.create_row(rowNum, imageSurfaces, row)
            self.grid.append(new_row)

    def create_row(self, row_num, images, letters, size=4):
        # Create one row in a grid. Each row contains size Tiles.
        # required for calculating the tile's x,y coordinates on screen
        #  -  row_num: the nth row of the grid being created
        #  -   size  : the number of tiles in the row
        #  -  images : a list of surfaces. should be same length or greater than size.
        #  - letters : a list of one char strings to be stored in Tile. should be same length as images.
        # returns the newly created row

        # Padding for the overall board.
        top_pad, bottom_pad, left_pad, right_pad = 30, 30, 30, 30

        # Assuming that the screen's width & height is 640.
        # previously, self.screen.get_height()
        tile_width = (640 - left_pad - right_pad) // size
        tile_height = (640 - top_pad - bottom_pad) // size

        new_row = []
        for i in range(4):
            # Padding between each tile .
            x_pad = 30
            y_pad = 30
            pos = (i * tile_height + x_pad, row_num * tile_width + y_pad)
            content = images[i]
            letter = letters[i]
            # Multiplying by 0.95 to make the tile slightly smaller without changing grid size,
            # so that it's visually more appealing and easier to drag between tiles.
            one_tile = Tile(content, letter, pos, 0.95 * tile_width, 0.95 * tile_height, row_num, i)

            new_row.append(one_tile)
        return new_row

    def play(self):
        # There doesn't seem to be a function for mouseDrag,
        # so the mousedown variable is used to keep track of when the mouse is dragged.
        mousedown = False
        current_tile_coords = ()  # The index (row, col) in self.grid for the tile currently being pressed/dragged.
        pressed_tiles_coords = []  # Indices (row, col) in self.grid of all tiles that are pressed at the moment.
        guess = ""  # The letters being dragged on the screen.
        guess_text = ""  # The text to display as the current guess. Sometimes includes the points of the guess.

        # Draws the board once to set it up.
        self.draw()
        # Sets a timer by creating an event every second (1000 milliseconds).
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        # Main game loop.
        while not self.close_clicked:
            # This for loop handles events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_clicked = True

                if event.type == pygame.USEREVENT:
                    self.timer -= 1 if self.timer > 0 else 0

                if self.continue_game:
                    # Does things depending on if the tile is clicked or not.
                    for rowNum, row in enumerate(self.grid):
                        for colNum, tile in enumerate(row):
                            # These if statements make the tile change to tile.secondary_color if the mouse is
                            # pressed or dragged over the tile.
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mousedown = True
                                # Always updates color if mouse is pressed on that tile.
                                if tile.rect.collidepoint(event.pos):
                                    current_tile_coords = tile.row, tile.col
                                    pressed_tiles_coords.append(current_tile_coords)
                                    guess = tile.letter
                                    guess_text = f"{guess} (+{self.score(guess)})" if self.is_word(guess) else guess

                            elif event.type == pygame.MOUSEBUTTONUP:
                                if "PROM" in self.guessed_words:
                                    self.prom_guessed = True

                                # Handles the score.
                                self.update_score(guess)
                                # Resets color of all tiles to tile.main_color, as it loops thru.
                                tile.draw()
                                # Resets variables.
                                mousedown = False
                                current_tile_coords = ()
                                pressed_tiles_coords = []
                                guess = ""
                                guess_text = ""
                                tile.reset_covers()
                                # Resets screen but keeps word and score labels.
                                self.clear_screen()

                            if event.type == pygame.MOUSEMOTION and mousedown:
                                if tile.rect.collidepoint(event.pos) and tile.isTileNearby(current_tile_coords):
                                    # Updates color if mouse is pressed and the previous tile clicked/dragged was nearby,
                                    # and if the tile has not already been clicked.
                                    if (tile.row, tile.col) not in pressed_tiles_coords:
                                        current_tile_coords = tile.row, tile.col
                                        pressed_tiles_coords.append(current_tile_coords)
                                        guess += tile.letter
                                        guess_text = f"{guess} (+{self.score(guess)})" if self.is_word(guess) else guess

                    # This for loop updates the colors of the tiles accordingly.
                    for row, col in pressed_tiles_coords:
                        tile = self.grid[row][col]
                        # Change the color, depending on what the guess is.
                        if self.is_guessed_word(guess):
                            tile.change_color(tile.yellow)
                        elif self.is_word(guess):
                            tile.change_color(tile.green)
                        else:
                            tile.change_color(tile.white)


                    self.update_text(guess_text)

            if self.prom_guessed:
                self.star.fill_star()

            if self.timer <= 0:
                self.continue_game = False

            pygame.display.update()
            self.game_Clock.tick(self.FPS)

            if not self.continue_game and self.prom_guessed:
                self.end()

    def end(self):
        # Changes the colors of the tiles in PROM.
        # self.board = [
        #     ["P", "R", "S", "U"],
        #     ["E", "S", "O", "I"],
        #     ["R", "M", "T", "R"],
        #     ["D", "A", "P", "A"]
        # ]
        prom_coordinates = [(0, 0), (0, 1), (1, 2), (2, 1)]
        for rowNum, row in enumerate(self.grid):
            for colNum, tile in enumerate(row):
                position = (rowNum, colNum)
                if position in prom_coordinates:
                    tile.change_color(tile.white)
                    tile.change_color(tile.green)


    def draw(self):
        # Draw all game objects, including background and tiles.
        # Only run once at the beginning.

        self.screen.fill(self.bg_color)  # clear the display surface
        # Places the background image on the screen. Note that it covers the background color.
        self.screen.blit(self.bg, (0, 0))

        for row in self.grid:
            for tile in row:
                tile.draw()

        self.draw_text()
        if not self.prom_guessed:
            self.star.draw()


        # updates screen
        pygame.display.update()

    def clear_screen(self):
        # Resets all surfaces on the screen, but keeps the words and score text labels the same.
        # Yes, I know it does the same thing as self.draw(). It used to do different things.
        self.draw()

    def draw_text(self, guess_text=""):
        # Draws the text onto the screen.
        # Extra info:
        # The right half of the screen is 560x640, without the grid. Minus 30 px padding on all sides, 500 x 580.
        # The positioning of each line of text is done relative to the previous line.

        middleX = 890  # the X value for the middle of the right half
        topY = 60
        title = Text("Word Hunt", middleX, topY, self.font.title_font)
        title.draw_centered(self.screen)

        topY += title.size[1]

        words = Text(f"WORDS: {self.word_num}", middleX - 150, topY, self.font.score_font)  # topY = 145
        words.draw_left_aligned(self.screen)

        topY += 60  # These numbers are added arbitrarily to add more space between the lines of text.
        score = Text(f"SCORE:  {self.score_num}", middleX - 150, topY, self.font.score_font)  # topY = 205
        score.draw_left_aligned(self.screen)

        topY += 100
        # Processes the guess_text into just the guess, without the score part of the guess in the string.
        temp = guess_text.split()[0] if len(guess_text.split()) > 0 else ""
        bg_color = self.get_guess_bg_color(temp)
        guess = Text(guess_text, middleX, topY, self.font.guess_font, background=bg_color)
        guess.draw_centered(self.screen)

        rightX, bottomY = self.screen.get_size()
        countdown = f"{self.timer // 60}:{str(self.timer % 60).rjust(2, '0')}".rjust(3)
        countdown_text = Text(countdown, rightX - 170, bottomY - 100, self.font.title_font, background=pygame.Color("white"))
        countdown_text.draw_left_aligned(self.screen)

    def get_guess_bg_color(self, guess):
        color = Tile.white
        if self.is_guessed_word(guess):
            color = Tile.yellow
        elif self.is_word(guess):
            color = Tile.green
        return color

    def update_text(self, guess=""):
        # -  guess  : the word that the player is creating by dragging the mouse.
        # Yes, this function is an alias for self.draw_text(), but update_text makes more sense.
        # It is fine to redraw all the text, because the screen is cleared periodically when the game runs.
        self.draw_text(guess)

    def score(self, guess):
        # Returns an integer, score, for that particular word.
        # Returns 0 if the guess is not a proper guess.
        # - guess : the word for which to find the corresponding score

        score = 0
        if self.is_word(guess):
            score = self.words[guess]
        return score

    def update_score(self, guess):
        # Handles the score and updates the text on the screen with the score.
        # - guess : the word to use to find the corresponding score

        score = self.score(guess)  # a local variable
        if score > 0 and not self.is_guessed_word(guess):
            self.guessed_words.append(guess)
            self.score_num += score
            self.word_num += 1
            self.update_text()



    def is_word(self, guess):
        if guess in self.words:
            return True
        else:
            return False

    def is_guessed_word(self, guess):
        if guess in self.guessed_words:
            return True
        else:
            return False
