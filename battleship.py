import pygame
import socket
import numpy as np
import math


class battleship_game:

    def __init__(self, screen, pygame, socket, board, cell_offset=0):
        self.screen = screen
        self.pygame = pygame
        self.socket = socket
        self.board = board
        self.cell_offset = cell_offset
        self.rotated = False
        dir = "images/"
        self.Submarine = self.pygame.image.load(dir + "image1.png")
        self.Reg_Ship = self.pygame.image.load(dir + "image2.png")
        self.Carrier = self.pygame.image.load(dir + "image3.png")
        self.Battle_Ship = self.pygame.image.load(dir + "image4.png")
        self.Small_Ship = self.pygame.image.load(dir + "image5.png")
        self.Small_Ship_counter = 1
        self.Reg_Ship_counter = 1
        self.Carrier_counter = 1
        self.Battle_Ship_counter = 1
        self.Submarine_counter = 1
        self.Ready = self.pygame.image.load(dir + "Battle.Ready.png")
        self.Ready = self.pygame.transform.scale(self.Ready, (480, 360))

    def background(self):
        self.screen.fill((13, 17, 31))
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render("Battle Ship", True, (255, 255, 255))
        self.screen.blit(Title, (30, 30))

    def draw_board(self):
        for idx, i in enumerate(self.board):

            for jdx, j in enumerate(i):

                if j == 0:
                    self.pygame.draw.rect(self.screen, (214, 229, 255), (600 + 65 * jdx, 63 + self.cell_offset, 63, 63), 1)
                    self.pygame.draw.circle(self.screen, (163, 163, 162), ((600 + (65 * jdx)) + 30, (63 + self.cell_offset) + 30), 6)
                else:
                    self.pygame.draw.rect(self.screen, (25, 209, 83), (600 + 65 * jdx, 63 + self.cell_offset, 63, 63),
                                          1)
                    self.pygame.draw.circle(self.screen, (25, 209, 83),
                                            ((600 + (65 * jdx)) + 30, (63 + self.cell_offset) + 30), 6)
            self.cell_offset = self.cell_offset + 65

        self.cell_offset = 0

    def draw_numbers(self):
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        for idx, i in enumerate(self.board):
            font = self.pygame.font.Font("coolvetica rg.ttf", 48)
            counter = font.render(str(idx + 1), True, (255, 255, 255))
            if (idx+1) != 10:
                self.screen.blit(counter, (620 + (idx) * 65, 8))
            else:
                self.screen.blit(counter, (610 + (idx) * 65, 8))

            letter = font.render(alphabet[idx], True, (255,255,255))
            if alphabet[idx] == "f" or alphabet[idx] == "i":
                self.screen.blit(letter, (573, 60 + (idx) * 65))
            else:
                self.screen.blit(letter, (568, 60 + (idx) * 65))

    def draw_boats(self):

        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Small_Ship_counter = font.render(str(self.Small_Ship_counter), True, (255, 255, 255))
        Reg_Ship_counter = font.render(str(self.Reg_Ship_counter), True, (255, 255, 255))
        Submarine_counter = font.render(str(self.Submarine_counter), True, (255, 255, 255))
        Battle_Ship_counter = font.render(str(self.Battle_Ship_counter), True, (255, 255, 255))
        Carrier_counter = font.render(str(self.Carrier_counter), True, (255, 255, 255))

        self.screen.blit(self.Submarine, (30, 425))# (36, 446) (334, 483)
        self.screen.blit(self.Reg_Ship, (30, 300)) # (28, 343) (311, 389)
        self.screen.blit(self.Carrier, (30, 600))# (33, 658) (494, 694)
        self.screen.blit(self.Battle_Ship, (30, 500))# (36, 554) (382, 583)
        self.screen.blit(self.Small_Ship, (30, 200)) # (28, 253) (216, 286)
        self.screen.blit(Submarine_counter, (350, 415))
        self.screen.blit(Reg_Ship_counter, (325, 325))
        self.screen.blit(Carrier_counter, (500, 615))
        self.screen.blit(Battle_Ship_counter, (400, 515))
        self.screen.blit(Small_Ship_counter, (225, 215))

    def load_image_to_mouse(self, image, event):
        x, y = self.pygame.mouse.get_pos()
        keys = self.pygame.key.get_pressed()
        if image != "":
            if keys[self.pygame.K_LEFT] and not self.rotated:
                image = pygame.transform.rotate(image, 90)
                self.rotated = True
            elif self.rotated == True:
                image = pygame.transform.rotate(image, 90)
                if keys[self.pygame.K_LEFT]:
                    image = pygame.transform.rotate(image, -90)
                    self.rotated = False

            width, height = image.get_size()
            self.run_first()
            self.screen.blit(image, (x - width/2, y - height/2))
            self.pygame.display.update()

    def generate_board_positions(self):
        init_pos_x = 600
        init_pos_y = 30

        MATRIX = np.zeros(shape=(10, 10), dtype=tuple)

        cell_map = 0

        for idx, i in enumerate(self.board):

            for jdx, j in enumerate(i):

                pos_x = init_pos_x + (jdx * 65)
                pos_y = init_pos_y + (cell_map * 65)

                position = (pos_x, pos_y)

                MATRIX[idx][jdx] = position

            cell_map = cell_map + 1

        return MATRIX

    def calc_position(self, ship):
        x, y = self.pygame.mouse.get_pos()

        x = math.floor((x - 600)/65)
        y = math.floor((y - 30)/65)

        if x >= 0 and y >= 0:
            if ship == "Small_Ship":
                if self.rotated:
                    self.board[y-1][x] = 1
                    self.board[y][x] = 1
                    self.board[y+1][x] = 1
                else:
                    self.board[y][x-1:x+2] = 1
                self.Small_Ship_counter = 0

            elif ship == "Regular_Ship":
                if self.rotated:
                    self.board[y-2][x] = 1
                    self.board[y-1][x] = 1
                    self.board[y][x] = 1
                    self.board[y+1][x] = 1
                else:
                    self.board[y][x - 2:x + 2] = 1
                self.Reg_Ship_counter = 0

            elif ship == "Carrier":
                if self.rotated:
                    self.board[y - 3][x] = 1
                    self.board[y - 2][x] = 1
                    self.board[y - 1][x] = 1
                    self.board[y][x] = 1
                    self.board[y + 1][x] = 1
                    self.board[y + 2][x] = 1
                    self.board[y + 3][x] = 1

                else:
                    self.board[y][x - 3:x + 4] = 1
                self.Carrier_counter = 0

            elif ship == "Submarine" or ship == "Battle_Ship":
                if self.rotated:
                    self.board[y-2][x] = 1
                    self.board[y - 1][x] = 1
                    self.board[y][x] = 1
                    self.board[y + 1][x] = 1
                    self.board[y + 2][x] = 1
                else:
                    self.board[y][x - 2:x + 3] = 1
                if ship == "Submarine":
                    self.Submarine_counter = 0
                else:
                    self.Battle_Ship_counter = 0

            return True


    def run_first(self):
        self.background()
        self.draw_board()
        self.draw_boats()
        self.draw_numbers()
        if self.Carrier_counter == 0 and self.Battle_Ship_counter == 0  \
                and self.Submarine_counter == 0 and self.Reg_Ship_counter == 0 and self.Small_Ship_counter == 0:
            self.screen.blit(self.Ready, (-90, 70)) # 30, 130 - 230, 200

'''
pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode([1280, 720])

CELLS = 10

BOARD = np.zeros(shape=(CELLS,CELLS), dtype=int)

game = battleship_game(screen=screen, pygame=pygame, socket=socket, board=BOARD)

game.run_first()
pygame.display.update()

BOARD_CELL_POS = game.generate_board_positions()

image = ""
ship = ""

clock = pygame.time.Clock()

while True:
    clock.tick(120)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            dir = "//Users/atulphadke/Documents/Projects/battleship/images/"
            if x >= 36 and x <= 334 and y >= 446 and y <= 483:
                if game.Submarine_counter != 0:
                    image = pygame.image.load(dir + "image1.png")
                    ship = "Submarine"
            elif x >= 28 and x <= 311 and y >= 343 and y <= 389:
                if game.Reg_Ship_counter != 0:
                    image = pygame.image.load(dir + "image2.png")
                    ship = "Regular_Ship"

            elif x >= 33 and x <= 494 and y >= 658 and y <= 696:
                if game.Carrier_counter != 0:
                    image = pygame.image.load(dir + "image3.png")
                    ship = "Carrier"

            elif x >= 36 and x <= 382 and y >= 554 and y <= 583:
                if game.Battle_Ship_counter != 0:
                    image = pygame.image.load(dir + "image4.png")
                    ship = "Battle_Ship"

            elif x >= 28 and x <= 216 and y >= 253 and y <= 286:
                if game.Small_Ship_counter != 0:
                    image = pygame.image.load(dir + "image5.png")
                    ship = "Small_Ship"
            # 30, 130 - 230, 200

        if image != "":
            game.load_image_to_mouse(image, event)
        if ship != "" and event.type == pygame.MOUSEBUTTONDOWN:
            change_image = game.calc_position(ship=ship)
            print(change_image)
            if change_image:
                image = ""
                ship = ""
                game.run_first()
                pygame.display.update()

'''
