import pygame
import random
import pygame.font
import os
pygame.font.init()
basic_font = pygame.font.SysFont('Impact', 35)

width = 300
height = 500

circle_image = os.path.dirname(__file__)+"/circle.png"
circle_size = 200
circle_pos = (150,150)
rotation_speed = 3
clock_yes = True

shot_speed = 25 # 10 or 20 or 25

knife_image = os.path.dirname(__file__)+"/knife.png"
knife_pos = (150,350)
knife_rect = (15, 75)
long_knife_size = (15, 260)


class Circle(object):
    def __init__(self):
        self.og_image = pygame.transform.scale(pygame.image.load(circle_image), (circle_size, circle_size))
        self.image = self.og_image
        self.angle = 0
        self.pos = circle_pos
        self.center = self.image.get_rect().center

    def changeSpeed(self):
        global rotation_speed,clock_yes
        if clock_yes:
            rotation_speed += random.uniform(0,0.1)
        else:
            rotation_speed -= random.uniform(0,0.1)
        if rotation_speed >= 6: 
            clock_yes = False
        if rotation_speed <= -6:
            clock_yes = True
        if random.random() < 0.002: clock_yes = not clock_yes
    def draw(self,win):
        self.angle += rotation_speed
        self.image = pygame.transform.rotate(self.og_image,self.angle)
        self.center = self.image.get_rect().center
        win.blit(self.image,(self.pos[0]-self.center[0],self.pos[1]-self.center[1]))


class Knife(object):
    def __init__(self):
        self.moving = False
        self.rotating = False
        self.og_image = pygame.transform.scale(pygame.image.load(knife_image),long_knife_size)
        self.image = self.og_image
        self.center = self.image.get_rect().center
        self.x = knife_pos[0]
        self.y = knife_pos[1]
        self.angle = 0
    def move(self):
        self.y -= shot_speed

    def rotate(self):
        self.angle += rotation_speed
        if self.angle >= 360: self.angle = 0
        self.image = pygame.transform.rotate(self.og_image,self.angle)
        self.center = self.image.get_rect().center

    def draw(self,win):
        win.blit(self.image,(self.x-self.center[0],self.y-self.center[1]))



def redrawWin(win):
    global losing
    win.fill((100,20,250)) 
    if started:
        textsurface = basic_font.render(str(score), True, (233, 255, 35))
        win.blit(textsurface,(width/2-textsurface.get_width()/2,5))
    k.draw(win)
    
    for kn in knifes:
        kn.draw(win)
        other_kn = list(knifes)
        other_kn.remove(kn)
        for knn in other_kn:
            if knn.y == circle_pos[0] and kn.y == circle_pos[0] and abs(knn.angle - kn.angle) <= 8  : 
                losing = True
                if losing:
                    win.fill((100,20,250)) 
                    textsurface = basic_font.render("GAMER OVER :  "+str(score-1), True, (233, 255, 200))
                    win.blit(textsurface,(width/2-textsurface.get_width()/2,height/2+50))
                    textsurface = basic_font.render("Press TAB to restart", True, (233, 255, 100))
                    win.blit(textsurface,(width/2-textsurface.get_width()/2,height/2+100))
    circle.draw(win)
    if not started:
        textsurface = basic_font.render("Press Space", True, (233, 255, 100))
        win.blit(textsurface,(width/2-textsurface.get_width()/2,height/2+100))
        textsurface2 = basic_font.render("Knife hit", True, (233, 255, 100))
        win.blit(textsurface2,(width/2-textsurface2.get_width()/2,25))
    

    
    pygame.display.update()


def main():
    global circle,k,knifes,score,losing,started
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Knife Hit  | By Zayd")
    clock = pygame.time.Clock()
    circle = Circle()
    k = Knife()
    knifes = []
    score = 0
    flag = True
    losing = False
    started = False
    while flag:
        pygame.time.delay(10)           
        clock.tick(30)
        circle.changeSpeed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not losing:
                            started = True
                            k.moving = True
                    if event.key == pygame.K_TAB:
                        main()



        if k.moving == True:  
            knifes.append(k)
            k = Knife()

        

        for kn in knifes:
            if kn.moving == True and kn.y == circle_pos[0]: 
                kn.moving = False
                kn.rotating = True
                score += 1

            if kn.moving:
                kn.move()

            if kn.rotating:    
                kn.rotate()

        redrawWin(win)




main()