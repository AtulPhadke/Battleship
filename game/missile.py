import pygame
import socket
import numpy as np
import math
import random
import time
import sys

class launch_missiles:

    def __init__(self, screen, pygame, socket, board, is_client, is_server):
        self.screen = screen
        self.pygame = pygame
        self.socket = socket
        self.board = board
        self.missile_board = np.zeros(shape=(CELLS, CELLS), dtype=int)
        self.is_client = is_client
        self.is_server = is_server
        self.our_turn = is_client
        self.cell_offset = 0
        self.first = True
        self.very_first = True
        self.server = None
        self.client = None

    def generate_rand_board(self):
        for i_idx, i in enumerate(self.board):
            for j_idx, j in enumerate(i):
                self.board[i_idx][j_idx] = random.randint(0, 1)

    def title(self):
        font = self.pygame.font.Font("//Users/atulphadke/Documents/Projects/battleship/coolvetica rg.ttf", 48)
        self.screen.fill((13, 17, 31))
        your_board = font.render("Your Board", True, (255, 255, 255))
        self.screen.blit(your_board, (200, 10))
        missile_board = font.render("Missile Board", True, (255, 255, 255))
        self.screen.blit(missile_board, (820, 10))

    def createSocket(self, IP):
        if self.is_server:
            self.server = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
            self.server.bind(('', 8088))
            self.server.listen()
            self.conn, self.addr = self.server.accept()
        else:
            self.client = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
            time.sleep(3)
            self.client.connect((IP, 8088))

    def draw_your_board(self):
        x_loc = 20
        for idx, i in enumerate(self.board):

            for jdx, j in enumerate(i):

                if j == 0:
                    self.pygame.draw.rect(self.screen, (214, 229, 255),
                                          (x_loc + 60 * jdx, 90 + self.cell_offset, 58, 58), 1)
                    self.pygame.draw.circle(self.screen, (163, 163, 162),
                                            ((x_loc + (60 * jdx)) + 30, (88 + self.cell_offset) + 30), 6)
                elif j == 1:
                    self.pygame.draw.rect(self.screen, (25, 209, 83),
                                          (x_loc + 60 * jdx, 90 + self.cell_offset, 58, 58), 1)
                    self.pygame.draw.circle(self.screen, (25, 209, 83),
                                            ((x_loc + (60 * jdx)) + 30, (88 + self.cell_offset) + 30), 6)
                elif j == 2:
                    self.pygame.draw.rect(self.screen, (242, 19, 19),
                                        (x_loc + 60 * jdx, 90 + self.cell_offset, 58, 58), 1)
                    self.pygame.draw.circle(self.screen, (242, 19, 19),
                                        ((x_loc + (60 * jdx)) + 30, (88 + self.cell_offset) + 30), 6)

            self.cell_offset = self.cell_offset + 60

        self.cell_offset = 0

    def draw_missile_board(self):
        x_loc = 650
        for idx, i in enumerate(self.missile_board):

            for jdx, j in enumerate(i):

                if j == 0:
                    self.pygame.draw.rect(self.screen, (214, 229, 255),
                                          (x_loc + 60 * jdx, 90 + self.cell_offset, 58, 58), 1)
                    self.pygame.draw.circle(self.screen, (163, 163, 162),
                                            ((x_loc + (60 * jdx)) + 30, (88 + self.cell_offset) + 30), 6)
                elif j == 2:
                    self.pygame.draw.rect(self.screen, (242, 19, 19),
                                          (x_loc + 60 * jdx, 90 + self.cell_offset, 58, 58), 1)
                    self.pygame.draw.circle(self.screen, (242, 19, 19),
                                            ((x_loc + (60 * jdx)) + 30, (88 + self.cell_offset) + 30), 6)

            self.cell_offset = self.cell_offset + 60

        self.cell_offset = 0

    def turn(self):
        font = self.pygame.font.Font("//Users/atulphadke/Documents/Projects/battleship/coolvetica rg.ttf", 36)
        if self.our_turn:
            myTurn = font.render("Your Turn!", True, (255, 255, 255))
            self.screen.blit(myTurn, (560, 20))
        else:
            myTurn = font.render("Oppenent's Turn!", True, (255, 255, 255))
            self.screen.blit(myTurn, (510, 20))

    def change_board(self, x, y):
        self.missile_board[y][x] = 2
        self.first = True
        self.our_turn = False
        if self.client:
            self.client.send(bytes(str(x) + "_" + str(y), 'utf-8'))
        else:
            print("sent server")
            self.conn.send(bytes(str(x) + "_" + str(y), 'utf-8'))
        print("overall sent")

    def missed_hit(self, description):
        font = self.pygame.font.Font("//Users/atulphadke/Documents/Projects/battleship/coolvetica rg.ttf", 32)
        description = font.render(str(description) + "!", True, (255, 255, 255))
        self.screen.blit(description, (30, 20))
        self.pygame.display.update()

    def drawui(self, IP):
        if self.very_first:
            self.createSocket(IP=IP)
            self.very_first = False
        if self.first:
            self.title()
            self.draw_your_board()
            self.draw_missile_board()
            self.turn()
            self.pygame.display.update()
            self.first = not self.first
            if not self.our_turn:
                if self.server:
                    array_x_y = self.conn.recv(1024).decode().split("_")
                    if array_x_y[0] == "Target Hit" or array_x_y[0] == "Missed":
                        self.missed_hit(array_x_y[0])
                        self.first = True
                        pass
                    else:
                        print(array_x_y)
                        x = int(array_x_y[0])
                        y = int(array_x_y[1])
                        print(x, y)
                        if x < 0 and y < 0:
                            pass
                        else:
                            if self.board[y][x] == 1:
                                self.conn.send(bytes("Target Hit", 'utf-8'))
                            else:
                                self.conn.send(bytes("Missed", 'utf-8'))
                            self.board[y][x] = 2
                            self.our_turn = True
                            self.first = True
                else:
                    array_x_y = self.client.recv(1024).decode().split("_")
                    print("received " + str(array_x_y[0]))
                    if array_x_y[0] == "Target Hit" or array_x_y[0] == "Missed":
                        self.missed_hit(array_x_y[0])
                        self.first = True
                        pass
                    else:
                        print(array_x_y[0] + "yo")
                        x = int(array_x_y[0])
                        y = int(array_x_y[1])
                        print(x, y)
                        if x < 0 and y < 0:
                            pass
                        else:
                            if self.board[y][x] == 1:
                                self.client.send(bytes("Target Hit", 'utf-8'))
                            else:
                                self.client.send(bytes("Missed", 'utf-8'))
                            self.board[y][x] = 2
                            self.our_turn = True
                            self.first = True

    def run(self, IP):
        self.drawui(IP=IP)

'''
pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode([1280, 720])

CELLS = 10

#SERVER_BOARD = np.zeros(shape=(CELLS, CELLS), dtype=int)
#server_player = launch_missiles(screen=screen, pygame=pygame, socket=socket)
#SERVER_BOARD = server_player.generate_rand_board()

CLIENT_BOARD = np.zeros(shape=(CELLS, CELLS), dtype=int)
client_server = sys.argv[1]

if client_server == "server":
    is_server = True
    is_client = False
else:
    is_server = False
    is_client = True

client_player = launch_missiles(screen=screen, pygame=pygame, socket=socket, board=CLIENT_BOARD, is_client=is_client, is_server=is_server)
client_player.generate_rand_board()
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN and client_player.our_turn:
            x, y = pygame.mouse.get_pos()
            print("debug")
            x = math.floor((x - 650) / 60)
            y = math.floor((y - 90) / 60)
            client_player.change_board(x, y)

    client_player.run()
'''