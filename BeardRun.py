
#gain access to the pygame library
import pygame, sys, random
pygame.init()
pygame.font.init()
#size of screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Flappy Beard'
#colours according to RGB codes
WHITE_COLOUR = (255,255,255)
BLACK_COLOUR = (0,0,0)
RED_COLOUR = (255, 0, 0)
GREEN_COLOUR = (0, 255, 0)
BLUE_COLOUR = (0, 0, 255)
#clock used to update game events and frames
clock = pygame.time.Clock()



class Game:

    #equivalent to fps
    TICK_RATE = 120
    print(pygame.get_init())
    

    def __init__(self, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        #Create window of specified size in white to display the game
        self.game_screen = pygame.display.set_mode((width,height))
        #set the game window colour to black
        self.game_screen.fill(BLACK_COLOUR)
        pygame.display.set_caption(title)
    

    def run_game_loop(self, high_score):
        game_active = True
        game_screen_over = False
        direction = 0
        score = 0


        player_character = PlayerCharacter('Images/jharden.png', 300, 380, 100, 100)
        ground = GroundMovement('Images/ground.png',0, 700, 1600, 100)
        game_over_face = GameObject('Images/BeardlessJHarden.png', 250, 200, 300, 300)

        razor_surface = RazorMovement('Images/good_razor.png')
        razor_list = []

        game_score = DisplayScore(700, 50, score, high_score)

        SPAWNRAZOR = pygame.USEREVENT
        pygame.time.set_timer(SPAWNRAZOR, 2200)
        #Main game loop, used to update all gameplay such as movement, checks, and graphics
        #Runs until is_game_over = True
        while not game_screen_over:

            #A loop to get all of the events occuring at any given time
            #Events are most often mouse movement, mouse and button clicks, or exit events
            for event in pygame.event.get():
                 #If we have a quit type of event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    game_screen_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and game_active:
                        direction = 1
                    elif event.key == pygame.K_DOWN and game_active:
                        direction = -1
                    if event.key == pygame.K_SPACE and game_active == False:
                        razor_list.clear()
                        player_character.rect.center = (350, 430)
                        game_score.score = 0
                        new_game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
                        new_game.run_game_loop(high_score)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = -1
                
                if event.type == SPAWNRAZOR:
                    razor_list.append(razor_surface.create_razor())
                    print(razor_list)
                print(event)

            #Redraw the screen to black
            self.game_screen.fill(BLACK_COLOUR)
            if game_active:
                #Harden
                player_character.move(direction)
                player_character.draw(self.game_screen)
                game_active = player_character.check_collision(razor_list)

                #razors
                razor_list = razor_surface.move_razors(razor_list)
                razor_surface.draw_razors(self.game_screen, razor_list)
                game_score.score += 0.01
                game_score.display_score(self.game_screen, 'game_on')
            else:
                game_score.high_score = game_score.update_score()
                game_score.display_score(self.game_screen, 'game_over')
                game_over_face.draw(self.game_screen)
            #Floor
            ground.move()
            ground.draw(self.game_screen)

            #Update game graphics        
            pygame.display.update()
            #Tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)

class GameObject:

    def __init__(self, image_path, x, y, width, height):

        object_image = pygame.image.load(image_path)
        #scale image up
        self.image = pygame.transform.scale(object_image, (width, height))

        if image_path == 'Images/jharden.png':
            self.rect = self.image.get_rect(center = (350, 430))
            self.harden = 1
        else:
            self.harden = 0
        
        self.x_pos = x
        self.y_pos = y

        self.width = width 
        self.height = height 
        
    def draw(self, background):
        if self.harden == 1:
            background.blit(self.image, self.rect)
        else:   
            background.blit(self.image, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):

    SPEEDUP = 18
    SPEEDDOWN = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction):
        if direction > 0:
            self.rect.centery -= self.SPEEDUP
        elif direction < 0:
            self.rect.centery += self.SPEEDDOWN
    
    def check_collision(self, razors):
        for r in razors:
            if self.rect.colliderect(r):
                return False
        
        if self.rect.top <= -200 or self.rect.bottom >= 800:
            return False
        
        return True

class GroundMovement(GameObject):
    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self):
        if self.x_pos > -800:
            self.x_pos -= 1
        else:
            self.x_pos = 0

class RazorMovement:

    def __init__(self, image_path):
        object_image = pygame.image.load(image_path)
        object_image = pygame.transform.scale(object_image, (100, 350) )
        self.image = object_image
    

    def create_razor(self):
        razor_height = [50, 150, 250, 350]
        random_razor_pos = random.choice(razor_height)
        razor = self.image.get_rect(midtop = (1000,random_razor_pos) )
        return razor
    
    def move_razors(self, razors):
        for r in razors:
            r.centerx -= 5
        return razors
    
    def draw_razors(self, background, razors):
        for r in razors:
            background.blit(self.image, r)
            
class DisplayScore():

    def __init__(self,x, y, score, high_score):
        self.x_pos = x
        self.y_pos = y
        self.score = score
        self.high_score = high_score

    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
        return self.high_score
    
    def display_score(self, background, game_state):
        game_font = pygame.font.Font('Fonts/04B_19.ttf',40)
        if game_state == 'game_on':
            score_surface = game_font.render(str(int(self.score)), True, WHITE_COLOUR)
            score_rect = score_surface.get_rect(center = (self.x_pos, self.y_pos))
            background.blit(score_surface, score_rect)
        if game_state == 'game_over':
            score_surface = game_font.render(f'Score: {int(self.score)}', True, WHITE_COLOUR)
            score_rect = score_surface.get_rect(center = (self.x_pos - 300, self.y_pos))
            background.blit(score_surface, score_rect)

            high_score_surface = game_font.render(f'High Score: {int(self.high_score)}', True, WHITE_COLOUR)
            high_score_rect = high_score_surface.get_rect(center = (self.x_pos - 300, self.y_pos + 500))
            background.blit(high_score_surface, high_score_rect)

            game_over_surface = game_font.render('Press Space to Try Again', True, WHITE_COLOUR)
            game_over_rect = game_over_surface.get_rect(center = (self.x_pos - 300, 650))
            background.blit(game_over_surface, game_over_rect)

        



new_game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(0)

#Quit pygame and the program
pygame.quit()
quit()







