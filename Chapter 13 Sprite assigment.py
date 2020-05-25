#######################
###Chapter 13 Sprite###
##### By William ######
#######################

import sys
import pygame
import time

WHITE = (255,255,255)
BLACK = (0,0,0)

class Cat(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()

        # load the sprite sheet
        sheet=pygame.image.load("Cat sprite.png").convert() 

        self.frame=[]
        for i in range(9):
           self.frame.append(pygame.Surface([33,37]).convert())
           #starting xpoint + width*(i%amountofColoum),starting ypoint + length*(i//AmountofColoum),width,lenght)
           patch = (0+33*(i%9),7+37*(i//9),33,37)
           self.frame[i].blit(sheet,(0,0), patch)
           self.frame[i].set_colorkey(BLACK)
           

        self.anim_frame=0
        self.image=self.frame[0]                            
        self.rect=self.image.get_rect()

        self.rect.x=x
        self.rect.y=y                             
        self.deltax=0
        self.deltay=0
        self.face = 1



    def update(self,index):
        self.anim_frame = (self.anim_frame+index)%9

        if (self.deltax<0) or (self.face == 2):
            self.image=pygame.transform.flip(self.frame[self.anim_frame],True,False)
            
        else:
            self.image=self.frame[self.anim_frame]

        self.rect.x += self.deltax
        self.rect.y += self.deltay
                             
                             


def main():

    pygame.init()


    main_surface = pygame.display.set_mode((960,580))
    background=pygame.image.load("Backgroundmap.jpg").convert()
    


    cat=Cat(533, 317)
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(cat)
    index = 0
    
                            
    while True:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key = event.dict['key']
                if key == 32:
                    cat.accel=-500
                elif key == pygame.K_LEFT:
                   cat.deltax=-3
                   cat.face = 2
                elif key == pygame.K_RIGHT:
                   cat.deltax=3
                   cat.face = 1
                elif key == pygame.K_UP:
                    cat.deltay=-3
                elif key == pygame.K_DOWN:
                   cat.deltay=3
                else:
                   cat.deltax=0
                   cat.deltay=0
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    cat.deltax=0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    cat.deltay=0
                    
            if (cat.deltax != 0) or (cat.deltay != 0):
                index = 1
                
            else:
                index = 0

        all_sprites.update(index)
        
        main_surface.blit(background,(0,0))
        all_sprites.draw(main_surface)

        pygame.display.flip()

        time.sleep(0.01)  

if __name__=='__main__':    
    main()
