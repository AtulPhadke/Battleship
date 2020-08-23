class welcome_screen:

    def __init__(self, screen, pygame):
        self.screen = screen
        self.pygame = pygame

    def background(self):
        self.screen.fill((255, 255, 255))
        battleship = self.pygame.image.load("images/battleship.png")
        #battleship = self.pygame.transform.scale(battleship, (1280, 720))
        self.screen.blit(battleship, (-170,0))

    def title(self):
        font = self.pygame.font.Font("coolvetica rg.ttf", 72)
        Title = font.render("Battle Ship", True, (0,0,0))
        self.screen.blit(Title, (30, 30))

    def join_party_button(self):
        #1020, 58 to 1220, 126
        joinParty = self.pygame.image.load("images/Button.Party.Join.png")
        joinParty = self.pygame.transform.scale(joinParty, (480, 360))
        self.screen.blit(joinParty, (900, 0))

    def create_party_button(self):
        #1020, 610 to 1280, 675
        createParty = self.pygame.image.load("images/Button.Party.Create.png")
        createParty = self.pygame.transform.scale(createParty, (480, 360))
        self.screen.blit(createParty, (900, 550))

    def run(self):
        self.background()
        self.title()
        self.join_party_button()
        self.create_party_button()
        self.pygame.display.update()