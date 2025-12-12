import pygame
from pygame.locals import *
import random

pygame.init()

#Creating window
width=500
height=500
screen_size=(width,height)
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Racing Game')

#colours
gray=(128, 128, 128)
green=(34, 139, 34)
red=( 255, 0, 0)
white=(255, 255, 255)
yellow=(255, 255, 0)

#images
grass_img=pygame.image.load('car_images/grass.jpg').convert()
grass_img=pygame.transform.scale(grass_img,screen_size)
grass_img_rect=grass_img.get_rect(topleft=(0,0))

bg=pygame.image.load('car_images/start_bg.jpg').convert()
bg=pygame.transform.scale(bg,screen_size)
bg_rect=bg.get_rect(topleft=(0,0))

crash=pygame.image.load('car_images/explosion.png')
crash_rect=crash.get_rect()
#game settings
gameover=False
speed=2
score=0

#marker size
marker_width=10
marker_height=50

#x coordinates of lanes
left_lane=150
center_lane=250
right_lane=350
lanes=[left_lane,center_lane,right_lane]
#for animating movement of lanes
lane_marker_move_y=0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        image_scale=45/image.get_rect().width
        new_width=int(image.get_rect().width*image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image=pygame.transform.scale(image,(new_width,new_height))

        self.rect=self.image.get_rect()
        self.rect.center=[x,y]

class PlayerVehicle(Vehicle):
    def __init__(self,x,y):
        image=pygame.image.load('car_images/pinkcar.png')
        super().__init__(image,x,y)
#player start coordinates
player_x=250
player_y=400

#creating player car
player_group=pygame.sprite.Group()
player=PlayerVehicle(player_x,player_y)
player_group.add(player)

#other vehicles
vehicle_files=['Ambulance1.png','Audi1.png','Black_viper1.png','blue_car.png','Car1.png'
,'Mini_truck1.png','Mini_van1.png','Police1.png','red_car.png','taxi1.png']
vehicle_images=[]
for vehicle_file in vehicle_files:
    image=pygame.image.load('car_images/'+vehicle_file)
    vehicle_images.append(image)

vehicle_group=pygame.sprite.Group()

#road and edge markers
road=(100,0,300,height)
left_edge_marker=(95,0,marker_width,height)
right_edge_marker=(400,0,marker_width,height)
#game loop
clock=pygame.time.Clock()
fps=120
running=True

def show_start_screen():
    title_font = pygame.font.Font(pygame.font.get_default_font(), 45)
    text_font = pygame.font.Font(pygame.font.get_default_font(), 30)

    while True:
        screen.blit(bg,bg_rect)

        title = title_font.render("CAR RACING GAME", True, (255, 255, 255))
        start_text = text_font.render("Press ENTER to Start", True, (255, 255, 0))
        quit_text = text_font.render("Press Q to Quit", True, (255, 255, 0))

        screen.blit(title, (width//2 - title.get_width()//2, 100))
        screen.blit(start_text, (width//2 - start_text.get_width()//2, 200))
        screen.blit(quit_text, (width//2 - quit_text.get_width()//2, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == pygame.K_RETURN:   # ENTER key
                    return            # exit start screen, begin game
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
show_start_screen()

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type==QUIT:
            running=False
        #move player car using left/right arrow key
        if event.type==KEYDOWN:
            if event.key==K_LEFT and player.rect.center[0]>left_lane:
                player.rect.x-=100
            elif event.key==K_RIGHT and player.rect.center[0]<right_lane:
                player.rect.x+=100

            for vehicle in vehicle_group:
               if pygame.sprite.collide_rect(vehicle,player):
                     gameover=True

                     if event.key==K_LEFT:
                         player.rect.left=vehicle.rect.left
                         crash_rect.center=[player.rect.left,(player.rect.center[1]+vehicle.rect.center[1])/2]
                     elif event.key==K_RIGHT:
                         player.rect.right=vehicle.rect.right
                         crash_rect.center=[player.rect.right,(player.rect.center[1]+vehicle.rect.center[1])/2]


    #grass
    screen.blit(grass_img,grass_img_rect)
    #road
    pygame.draw.rect(screen,gray,road)
    #left_edge_marker
    pygame.draw.rect(screen,yellow,left_edge_marker)
    # right_edge_marker
    pygame.draw.rect(screen, yellow, right_edge_marker)
    #lanes
    lane_marker_move_y+=2*speed
    if lane_marker_move_y>=marker_height*2:
        lane_marker_move_y=0
    for y in range(marker_height*-2,height,marker_height*2):
        pygame.draw.rect(screen,white,(left_lane+45,y+lane_marker_move_y,marker_width,marker_height))
        pygame.draw.rect(screen, white, (center_lane+45, y + lane_marker_move_y, marker_width, marker_height))



    player_group.draw(screen)


    if len(vehicle_group)<2:
        add_vehicle=True
        for vehicle in vehicle_group:
            if vehicle.rect.top<vehicle.rect.height*1.5:
                add_vehicle=False

        if add_vehicle:
            lane=random.choice(lanes)
            image=random.choice(vehicle_images)
            vehicle=Vehicle(image,lane,height/-2)
            vehicle_group.add(vehicle)

    for vehicle in vehicle_group:
        vehicle.rect.y+=speed

        if vehicle.rect.top>=height:
           vehicle.kill()
           score+=1

           if score>0 and score%5==0:
                speed+=1

    vehicle_group.draw(screen)
    #display score
    font=pygame.font.Font(pygame.font.get_default_font(),20)
    text=font.render(f"Score: {score}",True,white)
    text_rect=text.get_rect()
    text_rect.center=(50,450)
    pygame.draw.rect(screen,red, text_rect)
    screen.blit(text, text_rect)


    #to check head on collision:
    if pygame.sprite.spritecollide(player,vehicle_group,True):
        gameover=True
        crash_rect.center=[player.rect.center[0],player.rect.top]

    if gameover:
        screen.blit(crash,crash_rect)
        pygame.draw.rect(screen,red,(0,50,width,100))
        text=font.render("Game Over !!! Play Again? (Enter Y or N)",True,white)
        text_rect=text.get_rect()
        text_rect.center=(width/2,100)
        screen.blit(text,text_rect)
    pygame.display.update()

    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==QUIT:
                gameover=False
                running=False

            if event.type==KEYDOWN:
                if event.key==K_y:
                    gameover=False
                    speed=2
                    score=0
                    vehicle_group.empty()
                    player.rect.center=[player_x,player_y]
                elif event.key==K_n:
                    gameover=False
                    running=False

pygame.quit()