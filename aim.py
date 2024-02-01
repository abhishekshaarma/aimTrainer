import math
import random
import time

import pygame
pygame.init()
TOP_BAR = 50
LABEL_FONT  = pygame.font.SysFont("karmafuture", 24)
LIVES = 3
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30 
BG = (23,50 ,50 )
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

class Target:
    MAX_S = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    COLOR2 = "white"

    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.s = 0
        self.grow = True

    
    def update(self):
        if self.s + self.GROWTH_RATE >= self.MAX_S:
            self.grow = False
        if self.grow:
            self.s += self.GROWTH_RATE
        else:
            self.s -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win , self.COLOR, (self.x, self.y) , self.s )
        pygame.draw.circle(win , self.COLOR2, (self.x, self.y) , self.s * 0.8)
        pygame.draw.circle(win , self.COLOR, (self.x, self.y) , self.s * 0.6)
        pygame.draw.circle(win , self.COLOR2, (self.x, self.y) , self.s * 0.4)

    def collide(self , x , y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)  
        return dis <= self.s 

def draw1(win, targets):
    win.fill(BG)

    for target in targets:
        target.draw(win)


def format_time(secs):
    seconds = int(round(secs % 60, 1))
    mins = int(secs//60)
    return f"{mins:02d}:{seconds:02d}"

 
def draw_top(win, elasped_time, target_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH,TOP_BAR))
    time_label = LABEL_FONT.render(f"Time: {format_time(elasped_time)}", 1, "black")

    speed = round(target_pressed / elasped_time, 1)
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", 1 , 'black')
    score_label = LABEL_FONT.render(f"Score : {target_pressed} t/s", 1 , 'black')
    lives_label = LABEL_FONT.render(f"Lives : {LIVES - misses} ", 1 , 'black')

    

    win.blit(time_label, (5, 5))
    
    win.blit(speed_label, (200, 5))

    win.blit(score_label, (450, 5))
    win.blit(lives_label, (670, 5))

def endScreen(win, elasped_time, target_pressed, clicks):
    win.fill(BG)
    a = round(target_pressed/ clicks * 100 , 1)
    time_label = LABEL_FONT.render(f"Time: {format_time(elasped_time)}", 1, "black")
    speed = round(target_pressed / elasped_time, 1)
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", 1 , 'black')
    score_label = LABEL_FONT.render(f"Score : {target_pressed} t/s", 1 , 'black')
    accuracy_label = LABEL_FONT.render(f"Accuracy : {a}% ", 1 , 'black')

    win.blit(time_label, (get_mid(time_label), 100))
    win.blit(speed_label, (get_mid(speed_label), 200))
    win.blit(score_label, (get_mid(score_label), 300))
    win.blit(accuracy_label, (get_mid(accuracy_label), 400))

    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT  or event.type == pygame.KEYDOWN:
                quit()


def get_mid(surface):
    return WIDTH / 2 - surface.get_width() / 2
def main():
    run = True
    target_pressed = 0
    clicks = 0 
    start_time = time.time()
    misses = 0

    clock = pygame.time.Clock()

    targets = []
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        mouse_pos = pygame.mouse.get_pos()

        clock.tick(60)
        elasped_time = time.time() - start_time

        click = False    
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break
        
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING + TOP_BAR, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.s <= 0:
                targets.remove(target)
                misses += 1
            
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES:
            endScreen(WIN, elasped_time, target_pressed, clicks)
        

        draw1(WIN, targets)
        draw_top(WIN, elasped_time, target_pressed, misses)

        pygame.display.update()

    pygame.quit()   

if __name__ == "__main__":
    main()
