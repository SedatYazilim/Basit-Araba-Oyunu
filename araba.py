import pygame
import random
import sys


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basit Araba Oyunu")

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Oyuncu arabası
class PlayerCar:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 8
        
    def draw(self, surface):

        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
        
        pygame.draw.rect(surface, BLACK, (self.x + 5, self.y + 5, self.width - 10, 20))
        
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + 10, 5, 20))
        pygame.draw.rect(surface, BLACK, (self.x + self.width, self.y + 10, 5, 20))
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + self.height - 30, 5, 20))
        pygame.draw.rect(surface, BLACK, (self.x + self.width, self.y + self.height - 30, 5, 20))
        
    def move(self, direction):
        if direction == "left" and self.x > 100:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width - 100:
            self.x += self.speed

# Engel arabalar
class ObstacleCar:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = random.randint(100, SCREEN_WIDTH - self.width - 100)
        self.y = -self.height
        self.speed = random.randint(5, 10)
        self.color = GREEN
        
    def draw(self, surface):
        
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        pygame.draw.rect(surface, BLACK, (self.x + 5, self.y + self.height - 25, self.width - 10, 20))
        
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + 10, 5, 20))
        pygame.draw.rect(surface, BLACK, (self.x + self.width, self.y + 10, 5, 20))
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + self.height - 30, 5, 20))
        pygame.draw.rect(surface, BLACK, (self.x + self.width, self.y + self.height - 30, 5, 20))
        
    def move(self):
        self.y += self.speed
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT


class RoadLine:
    def __init__(self, y):
        self.x = SCREEN_WIDTH // 2
        self.y = y
        self.width = 10
        self.height = 50
        self.speed = 7
        
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x - self.width // 2, self.y, self.width, self.height))
        
    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = -self.height


def main():
    clock = pygame.time.Clock()
    
    player = PlayerCar()
    obstacles = []
    road_lines = [RoadLine(i) for i in range(-50, SCREEN_HEIGHT, 100)]
    
    score = 0
    font = pygame.font.SysFont(None, 36)
    
    obstacle_timer = 0
    obstacle_frequency = 60  
    
    running = True
    game_over = False
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_over and event.key == pygame.K_SPACE:
                    
                    player = PlayerCar()
                    obstacles = []
                    score = 0
                    game_over = False
        
        if not game_over:
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move("left")
            if keys[pygame.K_RIGHT]:
                player.move("right")
            
            
            obstacle_timer += 1
            if obstacle_timer >= obstacle_frequency:
                obstacles.append(ObstacleCar())
                obstacle_timer = 0
               
                obstacle_frequency = max(20, obstacle_frequency - 1)
            
           
            for line in road_lines:
                line.move()
            
            for obstacle in obstacles[:]:
                obstacle.move()
                
                if (player.x < obstacle.x + obstacle.width and
                    player.x + player.width > obstacle.x and
                    player.y < obstacle.y + obstacle.height and
                    player.y + player.height > obstacle.y):
                    game_over = True
                
                
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
                    score += 1
        
        
        screen.fill(GRAY)
        
        
        pygame.draw.rect(screen, BLACK, (0, 0, 100, SCREEN_HEIGHT))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 100, 0, 100, SCREEN_HEIGHT))
        
        
        for line in road_lines:
            line.draw(screen)
        
       
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        
        score_text = font.render(f"Skor: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        if game_over:
            game_over_text = font.render("OYUN BİTTİ! Yeniden başlamak için SPACE'e basın", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
      
        pygame.display.flip()
        
       
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
