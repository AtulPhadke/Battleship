import pygame
import socket

from launch_screen import welcome_screen
from create_party import create_party
from join_party import join_party
import pygame_textinput

pygame.init()
pygame.mixer.quit()
screen = pygame.display.set_mode([1280, 720])

welcome_screen = welcome_screen(screen=screen, pygame=pygame)
create_party = create_party(screen=screen, pygame=pygame, socket=socket)
join_party = join_party(screen=screen, pygame=pygame, socket=socket)

textinput = pygame_textinput.TextInput()
ipinput = pygame_textinput.TextInput()

welcome_screen.run()

classes = [welcome_screen, create_party, join_party]
Class = welcome_screen

clock = pygame.time.Clock()

changeClass_create_party = False
runclass_create_party = False
runclass_join_party = False

loading = False
got_username = False
got_ip = False

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

print(loading_images)

file_number = 0
first_time = True

while True:
   clock.tick(60)
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
               if x>= 448 and x <= 850 and y >= 569 and y <= 703:
                   print("Start Battle")

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
       else:
           screen.blit(loading_images[file_number - 1], (240, 60))
           pygame.display.update(img.get_rect())
           pygame.time.delay(10)
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
           Class.run(username=username, first_time=first_time)
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
               Class.run(username=username, IP=ip)
