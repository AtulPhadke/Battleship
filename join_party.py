import base64

class join_party:

    def __init__(self, screen, pygame, socket):
        self.screen = screen
        self.pygame = pygame
        self.socket = socket

    def Title(self):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render("Join Party", True, (0, 0, 0))
        self.screen.blit(Title, (500, 30))

    def background(self):
        self.screen.fill((214, 229, 255))

    def connect_to_client(self, HOST, username):
        client = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        client.connect((HOST, 8888))
        client.send(username)

    def run(self, username, IP):
        self.background()
        self.Title()
        self.connect_to_client(base64.b64decode(str(IP)), username=username)
        self.pygame.display.update()