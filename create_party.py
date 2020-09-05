import base64
import os
import time
import numpy as np
import threading

class create_party:

    def __init__(self, screen, pygame, socket, server, conn=None, addr=None):
        self.screen = screen
        self.pygame = pygame
        self.socket = socket
        self.server = server
        self.conn = conn
        self.addr = addr
        self.start_game = False
        self.data = None

    def create_socket(self):
        PORT = 8080
        self.server = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        self.server.bind(('', PORT))
        self.server.listen()

    def get_ip(self):
        s = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        font_sized = self.pygame.font.Font("coolvetica rg.ttf", 60)
        IP = s.getsockname()[0].replace(".", "")
        s.close()
        encrypted = ""
        for character in IP:
            encrypted = encrypted + chr(98 + int(character))
        IP_enter = font_sized.render(str(encrypted), True, (0,0,0))
        party_IP = font.render("Party Code", True, (0,0,0))
        self.screen.blit(party_IP, (900, 30))
        self.screen.blit(IP_enter, (960, 120))

    def display_username(self, username):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render(username, True, (0, 0, 0))
        self.screen.blit(Title, (100, 300))

    def versus(self):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render("versus", True, (0, 0, 0))
        self.screen.blit(Title, (550, 300))

    def pending_oppenent_username(self, data):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        if not data:
            Title = font.render("Pending....", True, (0, 0, 0))
        else:
            Title = font.render(str(data), True, (0, 0, 0))
        self.screen.blit(Title, (950, 300))

    def title(self):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render("Battle Ship", True, (0,0,0))
        self.screen.blit(Title, (30, 30))

    def beginBattle(self):
        button = self.pygame.image.load("images/Battle.Begin.png")
        self.screen.blit(button, (210, 450))

    def run(self, username, first_time, second_time, changeClass_boat_locations, sendBoat):
        if first_time == True:
            self.screen.fill((214, 229, 255))
            self.get_ip()
            self.display_username(username=username)
            self.create_socket()
            self.title()
            self.beginBattle()
            self.versus()
            self.pending_oppenent_username(None)
            self.pygame.display.update()

        elif not first_time and second_time:
            self.conn, self.addr = self.server.accept()
            data = self.conn.recv(1024)
            if data:
                self.screen.fill((214, 229, 255))
                self.get_ip()
                self.display_username(username=username)
                self.title()
                self.beginBattle()
                self.versus()
                self.pending_oppenent_username(data=data.decode("utf-8"))
                self.pygame.display.update()
                self.start_game = True
                self.data = data
                return False
        if sendBoat:
            print("sent")
            self.conn.send(bytes("Place Boats", "utf-8"))

        return True
