import pygame
import neat
import time
import os
import random


WIN_HEIGHT=800
WIN_WIDTH=500

BIRD_IMG=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png")))
    ,pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png")
    )),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]

PIPE_IMG=[pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))]
BASE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))


class Bird:
    IMGS=BIRD_IMG
    MAX_ROTATION=25
    ROT_VEL=20  #how much we rotate on each frame
    ANIMATION_TIME=5

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.frame_move=0
        self.vel=0
        self.height=self.y
        self.img_count=0        #which image we are showing
        self.img=self.IMGS[0]

    def jump(self):
        self.vel=-10.5    #going up is negative, going down is positive
        self.frame_move=0
        self.height=self.y

    def move(self):
        self.frame_move+=1
        displacement=self.vel*self.frame_move+1.5*self.frame_move**2

        if displacement>=16:
            displacement=16

        if displacement<0:
            displacement-=2

        self.y=self.y+displacement

        if displacement<0 or self.y<self.height+50:
            if self.tilt<self.MAX_ROTATION:
                self.tilt=self.MAX_ROTATION
        else:
            if self.tilt>-90:
                self.tilt=-90

    def draw(self,window):
        self.img_count+=1     #to keep a track of the frames

        if self.img_count<self.ANIMATION_TIME:
            self.img=self.IMGS[0]
        elif self.img_count<self.ANIMATION_TIME*2:
            self.img=self.IMGS[1]
        elif self.img_count<self.ANIMATION_TIME*3:
            self.img=self.IMGS[2]
        elif self.img_count<self.ANIMATION_TIME*4:
            self.img=self.IMGS[1]
        elif self.img_count==self.ANIMATION_TIME*4+1:
            self.img=self.IMGS[0]
            self.img_count=0

        if self.tilt<=-80:
            self.img=self.IMGS[1]
            self.img_count=self.ANIMATION_TIME*2

        rotated_image=pygame.transform.rotate(self.img,self.tilt)
        new_rect=rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        window.blit(rotated_image,new_rect.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)

def draw_window(window,bird):
    window.blit(BG_IMG,(0,0))
    bird.draw(window)
    pygame.display.update()


def main():
    bird=Bird(200,200)
    window=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock=pygame.time.Clock()

    run=True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        bird.move()
        draw_window(window,bird)

    pygame.quit()
    quit()


main()