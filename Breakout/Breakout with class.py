import pygame
import sys

DARK_BLUE = ( 21,  34,  56)
WHITE     = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH  = 850
SCREEN_HEIGHT = 650

class Ball(pygame.sprite.Sprite):
    
     def __init__(self):
        super().__init__()

        # Load & Set Up Image
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = 242
        self.rect.y = 580
        self.speed_x = 10
        self.speed_y = -10

     def update(self):
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <= 0 or self.rect.x >= 830:
            self.speed_x = -1 * self.speed_x
        if self.rect.y <= 70:
            self.speed_y = -1 * self.speed_y

     def reset_position(self):
        
        self.rect.x = 242
        self.rect.y = 580
        self.speed_y = -1 * self.speed_y



class Block(pygame.sprite.Sprite):

    def __init__(self, location_x, location_y):

        super().__init__()

        # Load & Set Up Image
        self.sprite_sheet = pygame.image.load("sprite.png")
        self.image = self.sprite_sheet.subsurface(20,17,170,57)
        self.rect = self.image.get_rect()
        self.rect.x = location_x
        self.rect.y = location_y



class Paddle(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        # Load & Set Up Image
        self.sprite_sheet = pygame.image.load("sprite.png")
        self.image = self.sprite_sheet.subsurface(570,375,216,40)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 190
        self.rect.y = 600

    def update(self):
        
        position = pygame.mouse.get_pos()
        self.rect.x = position[0]

        # Prevent Paddle From Going Off-Screen 
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= SCREEN_WIDTH - 210:
            self.rect.x = SCREEN_WIDTH - 210

    def reset_position(self):

        self.rect.x = 190
        self.rect.y = 600


class Game():

    def __init__(self):

        # Make score meter, life meter, and game over check
        self.game_over = False
        self.life = 3
        self.score = 0

        # Create Sprite
        self.block_group = pygame.sprite.Group()
        self.paddle_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()

        self.ball = Ball()
        self.all_sprites_group.add(self.ball)
        
        for j in range(5):
            for i in range(5):
                block = Block(0 + 170 * i, 75 + 57 * j)
                self.block_group.add(block)
                self.all_sprites_group.add(block)

        # Create Paddle Sprite
        self.paddle = Paddle()
        self.paddle_group.add(self.paddle)
        self.all_sprites_group.add(self.paddle)
            
    def process_events(self):
        
        for event in pygame.event.get():
            # User Clicks Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Player Plays Again
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()
                
    def run_logic(self):

        # Move All Sprites
        self.all_sprites_group.update()

        # Check for Collisions
        if pygame.sprite.spritecollide(self.ball, self.block_group, True):
            self.ball.speed_y = -1 * self.ball.speed_y
            self.score += 10
   
        if pygame.sprite.spritecollide(self.ball, self.paddle_group, False):
            self.ball.speed_y = -1 * self.ball.speed_y

        # Lose Lives, Count Lives
        if self.ball.rect.y >= 800:
            self.ball.reset_position()
            self.paddle.reset_position()
            self.life -= 1


            
        if self.life <= 0:
            self.game_over = True
        
    def display_frame(self, screen):

        screen.fill(DARK_BLUE)

        # Game Over
        if self.game_over:
            font = pygame.font.SysFont("serif", 55)
            text = font.render("GAME OVER", True, WHITE)
            location_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            screen.blit(text, [location_x, 350])

            text = font.render("CLICK TO RESTART", True, WHITE)
            location_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            screen.blit(text, [location_x, 400]) 
        
        if not self.game_over:
            self.all_sprites_group.draw(screen)

            font = pygame.font.SysFont("serif", 23)
            text = font.render("LIVES: " + str(self.life), True, WHITE)
            screen.blit(text, [325, 20])

            font = pygame.font.SysFont("serif", 23)
            text = font.render("SCORE: " + str(self.score), True, WHITE)
            screen.blit(text, [420, 20])

        pygame.display.flip()

# --- Main Function --- #
def main():

    # Initialize Pygame & Set Up Window
    pygame.init()
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("BREAKOUT")

    done = False

    clock = pygame.time.Clock()
    game = Game()



    while not done:
         
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(120)
    
# Call Main Function & Start Game
if __name__=='__main__':
    main()



     
