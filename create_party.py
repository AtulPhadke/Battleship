import base64
import os
import time
import numpy as np
import threading

class create_party:

    def __init__(self, screen, pygame, socket):
        self.screen = screen
        self.pygame = pygame
        self.socket = socket

    def create_socket(self):
        HOST = '127.0.0.1'
        PORT = 8888
        server = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server.bind((HOST, PORT))

    def get_ip(self):
        s = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        font_sized = self.pygame.font.Font("coolvetica rg.ttf", 36)
        IP = s.getsockname()[0]
        s.close()
        IP_enter = font_sized.render(base64.b64encode(bytes(IP, 'utf-8')), True, (0,0,0))
        party_IP = font.render("Party Code", True, (0,0,0))
        self.screen.blit(party_IP, (900, 30))
        self.screen.blit(IP_enter, (920, 120))

    def display_username(self, username):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render(username, True, (0, 0, 0))
        self.screen.blit(Title, (100, 300))

    def versus(self):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render("versus", True, (0, 0, 0))
        self.screen.blit(Title, (550, 300))

    def pending_oppenent_username(self):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render("Pending....", True, (0, 0, 0))
        self.screen.blit(Title, (950, 300))

    def title(self):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render("Battle Ship", True, (0,0,0))
        self.screen.blit(Title, (30, 30))

    def beginBattle(self):
        button = self.pygame.image.load("images/Battle.Begin.png")
        self.screen.blit(button, (210, 450))

    def run(self, username, first_time):
        if first_time == True:
            self.screen.fill((214, 229, 255))
            self.get_ip()
            self.display_username(username=username)
            self.create_socket()
            self.title()
            self.beginBattle()
            self.versus()
            self.pending_oppenent_username()
            self.pygame.display.update()
