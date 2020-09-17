import pygame
import socket
import numpy as np
import math

from launch_screen import welcome_screen
from create_party import create_party
from join_party import join_party
from battleship import battleship_game
from missile import launch_missiles
import pygame_textinput

pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode([1280, 720])

CELLS = 10
BOARD = np.zeros(shape=(CELLS,CELLS), dtype=int)

welcome_screen = welcome_screen(screen=screen, pygame=pygame)
create_party = create_party(screen=screen, pygame=pygame, socket=socket, server=None)
join_party = join_party(screen=screen, pygame=pygame, socket=socket)
Game = battleship_game(screen=screen, pygame=pygame, socket=socket, board=BOARD)

textinput = pygame_textinput.TextInput()
ipinput = pygame_textinput.TextInput()

welcome_screen.run()

classes = [welcome_screen, create_party, join_party, Game]
Class = welcome_screen

clock = pygame.time.Clock()

changeClass_create_party = False
changeClass_join_party = False
changeClass_boat_locations = False

runclass_create_party = False
runclass_join_party = False
runclass_choose_boat_locations = False
runclass_fire_missiles = False

loading = False
got_username = False
got_ip = False
missile_first_time = True

file_number = 0
loading_images = []

def get_username():
    font = pygame.font.Font("coolvetica rg.ttf", 72)
    Title = font.render("Type in your Username!", True, (0, 0, 0))
    screen.blit(Title, (550, 600))

def get_ip():
    font = pygame.font.Font("coolvetica rg.ttf", 72)
    Title = font.render("Type in the Party Code!", True, (0, 0, 0))
    screen.blit(Title, (500, 600))

while file_number < 214:

    if file_number < 10:
        img = pygame.image.load("frames/" + "frame_" + "00" + str(file_number) + "_delay-0.02s.png")
    elif file_number < 100 and file_number > 9:
        img = pygame.image.load("frames/" + "frame_" + "0" + str(file_number) + "_delay-0.02s.png")
    elif file_number < 215 and file_number > 99:
        img = pygame.image.load("frames/" + "frame_" + str(file_number) + "_delay-0.02s.png")

    loading_images.append(img)
    file_number = file_number + 1



file_number = 0
first_time = True
second_time = True
first_connect = True
choose_locations_first_time = True
place_boats = False
joined_party = False

image = ""
ship = ""

opp_username = None
server = None
start_battle = False

client_board = None
server_board = None
change_board = False

server_player = None
client_player = None

while True:
   clock.tick(120)
   events = pygame.event.get()

   for event in events:
       if event.type == pygame.QUIT:
           break
       if event.type == pygame.MOUSEBUTTONDOWN:
           x, y = pygame.mouse.get_pos()
           if Class == classes[0]:
               if x >= 1020 and x <= 1220 and y >= 58 and y <= 126:
                   changeClass_join_party = True
                   loading = True
               elif x >= 1020 and x <= 1220 and y >= 610 and y <= 675:
                   changeClass_create_party = True
                   loading = True
           elif Class == classes[1]:
               if Class.start_game:
                   if x>= 448 and x <= 850 and y >= 569 and y <= 703:
                       print("Start Battle")
                       changeClass_boat_locations = True
                       changeClass_create_party = False
                       changeClass_join_party = False
                       runclass_create_party = False
                       runclass_join_party = False
                       loading = True
           elif Class == classes[3]:
               dir = "images/"

               print(x, y)
               if x >= 36 and x <= 334 and y >= 446 and y <= 483:
                   if Class.Submarine_counter != 0:
                       image = pygame.image.load(dir + "image1.png")
                       ship = "Submarine"

               elif x >= 28 and x <= 311 and y >= 343 and y <= 389:
                   if Class.Reg_Ship_counter != 0:
                       image = pygame.image.load(dir + "image2.png")
                       ship = "Regular_Ship"

               elif x >= 33 and x <= 494 and y >= 658 and y <= 696:
                   if Class.Carrier_counter != 0:
                       image = pygame.image.load(dir + "image3.png")
                       ship = "Carrier"

               elif x >= 36 and x <= 382 and y >= 554 and y <= 583:
                   if Class.Battle_Ship_counter != 0:
                       image = pygame.image.load(dir + "image4.png")
                       ship = "Battle_Ship"

               elif x >= 28 and x <= 216 and y >= 253 and y <= 286:
                   if Class.Small_Ship_counter != 0:
                       image = pygame.image.load(dir + "image5.png")
                       ship = "Small_Ship"

               elif x >= 30 and x <= 230 and y >= 130 and y <= 200:
                   print("started battle")
                   start_battle = True

           elif Class == launch_missiles:
               x, y = pygame.mouse.get_pos()
               x = math.floor((x - 650) / 60)
               y = math.floor((y - 90) / 60)
               change_board = True

   if loading:
       if file_number == 0:
           screen.fill((13, 17, 31))
       if file_number > 214:
           if changeClass_create_party:
               runclass_create_party = True
               loading = False
           elif changeClass_join_party:
               runclass_join_party = True
               loading = False
           elif changeClass_boat_locations:
               print("heeer")
               runclass_choose_boat_locations = True
               runclass_create_party = False
               loading = False
       else:
           screen.blit(loading_images[file_number - 1], (240, 60))
           pygame.display.update(img.get_rect())
           file_number = file_number + 1

   if runclass_create_party:
       if not got_username:
           screen.fill((214, 229, 255))
           returned = textinput.update(events)
           screen.blit(textinput.get_surface(), (10,10))
           get_username()
           pygame.display.update()

           if returned:
               username = textinput.get_text()
               got_username = True

       else:
           Class = classes[1]
           change_second_time = Class.run(username=username, first_time=first_time, second_time=second_time, changeClass_boat_locations=changeClass_boat_locations, sendBoat=False)
           if not change_second_time:
               second_time = change_second_time
           first_time = False

   elif runclass_join_party:
       if not got_username:
           screen.fill((214, 229, 255))
           returned = textinput.update(events)
           screen.blit(textinput.get_surface(), (10,10))
           get_username()
           pygame.display.update()

           if returned:
               username = textinput.get_text()
               got_username = True

       else:
           if not got_ip:
               screen.fill((214, 229, 255))
               returned = ipinput.update(events)
               screen.blit(ipinput.get_surface(), (10, 10))
               get_ip()
               pygame.display.update()

               if returned:
                   ip = ipinput.get_text()
                   got_ip = True
           else:
               Class = classes[2]
               place_boats = Class.run(username=username, IP=ip, first_connect=first_connect)
               print("ran")
               if place_boats:
                   changeClass_boat_locations = True
                   changeClass_create_party = False
                   changeClass_join_party = False
                   runclass_create_party = False
                   runclass_join_party = False
                   joined_party = True
                   loading = True
               first_connect = False

   elif runclass_choose_boat_locations:
       if choose_locations_first_time:
           if not joined_party:
               create_party.run(username=username, first_time=first_time, second_time=second_time, changeClass_boat_locations=changeClass_boat_locations, sendBoat=True)
               sendBoat = False
           Class = classes[3]
           Class.run_first()
           pygame.display.update()
           BOARD_CELL_POS = Class.generate_board_positions()
           choose_locations_first_time = False
       else:
           if image != "":
               Class.load_image_to_mouse(image, event)

           if ship != "" and event.type == pygame.MOUSEBUTTONDOWN:
               x, y = pygame.mouse.get_pos()
               change_image = Class.calc_position(ship=ship)
               if change_image:
                   image = ""
                   ship = ""
                   Class.run_first()
                   pygame.display.update()

           if start_battle and joined_party:
               client_board = Class.board
               is_client = True
               is_server = False
               runclass_choose_boat_locations = False
               client_player = launch_missiles(screen=screen, pygame=pygame, socket=socket, board=client_board, is_client=is_client,
                                   is_server=is_server)
               runclass_fire_missiles = True
           elif start_battle:
               server_board = Class.board
               is_client = False
               is_server = True
               runclass_choose_boat_locations = False
               server_player = launch_missiles(screen=screen, pygame=pygame, socket=socket, board=server_board, is_client=is_client,
                                   is_server=is_server)
               runclass_fire_missiles = True

   elif runclass_fire_missiles:
       if missile_first_time:
           Class = launch_missiles
           missile_first_time = not missile_first_time
       if server_player:
           server_player.run(IP=None)
           if change_board:
               change_board = False
               server_player.change_board(x, y)
       else:
           client_player.run(IP=str(join_party.decrypted))
           if change_board:
               change_board = False
               client_player.change_board(x, y)



