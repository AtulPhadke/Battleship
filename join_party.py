import base64

class join_party:

    def __init__(self, screen, pygame, socket):
        self.screen = screen
        self.pygame = pygame
        self.socket = socket
        self.client = None
        self.place_boats = None
        self.waiting_for_game = False
        self.waiting_for_game2 = False
        self.decrypted = None

    def Title(self):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render("Waiting for Game to start...", True, (0, 0, 0))
        self.screen.blit(Title, (30, 30))

    def background(self):
        self.screen.fill((214, 229, 255))

    def connect_to_client(self, HOST, username):
        self.client = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        print(HOST)
        self.client.connect((HOST, 8080))
        self.client.send(bytes(username, 'utf-8'))

    def decrypt(self, IP):
        self.decrypted = ""
        for character in IP:
            if character == "#":
                next_char = "."
            else:
                next_char = str(ord(character) - 98)
            self.decrypted = self.decrypted + next_char

    def run(self, username, IP, first_connect):
        self.background()
        self.Title()
        self.decrypt(IP=IP)
        if self.decrypted and first_connect:
            self.connect_to_client(self.decrypted, username=username)
            self.waiting_for_game = True
        self.pygame.display.update()
        if self.waiting_for_game2:
            message = self.client.recv(1024)
            if message.decode("utf-8") == "Place Boats":
                print(message)
                self.place_boats = True
                return self.place_boats
        if self.waiting_for_game:
            self.waiting_for_game2 = True
        print(self.waiting_for_game2)
        return False

