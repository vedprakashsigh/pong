import pygame
pygame.init()
FONT = pygame.font.SysFont('comic sans', 20)

WIDTH, HEIGHT = 1000,500
BLACK = (0,0,0)
WHITE = (255,255,255)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RAD = 7
WINNER = None

class Paddle:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw(self,WIN):
        pygame.draw.rect(WIN, WHITE, (self.x,self.y,self.width,self.height))

class Ball:
    MAX_VEL = 5
    def __init__(self,rad):
        self.rad = rad
        self.x = self.ORIGINAL_X = WIDTH//2
        self.y = self.ORIGINAL_Y = HEIGHT//2
        self.x_vel = 5
        self.y_vel = 0
    def draw(self,WIN):
        ball.move()
        pygame.draw.circle(WIN, WHITE, ((self.x),(self.y)), self.rad)
        pygame.display.update()
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    def reset(self):
        self.x = self.ORIGINAL_X
        self.y = self.ORIGINAL_Y
        self.x_vel *= -1
        self.y_vel = 0
    def vel_change(self,pad):
        d = ((pad.y + PADDLE_HEIGHT//2) - self.y)/(PADDLE_HEIGHT//2)
        self.y_vel = -d * self.MAX_VEL

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")
CLOCK = pygame.time.Clock()

def draw(WIN):
    WIN.fill(BLACK)
    l_pad.draw(WIN)
    r_pad.draw(WIN)
    ball.draw(WIN)
    scr1 = FONT.render(f"PLAYER 1: {l_score}", True, WHITE)
    scr2 = FONT.render(f"PLAYER 2: {r_score}", True, WHITE)
    WIN.blit(scr1, (WIDTH//4 - scr2.get_width()//2,10))
    WIN.blit(scr2, (WIDTH*(3/4) - scr2.get_width()//2,10))
    dash = 0
    for i in range(30):
        pygame.draw.line(WIN, WHITE, (WIDTH//2,dash), (WIDTH//2 , dash + 10))
        dash += 20
    pygame.display.update()

if __name__ == '__main__':
    run = True
    FPS = 60
    l_pad = Paddle(0, (HEIGHT-PADDLE_HEIGHT)//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    r_pad = Paddle(WIDTH-PADDLE_WIDTH, (HEIGHT-PADDLE_HEIGHT)//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    ball = Ball(BALL_RAD)
    l_score, r_score = 0,0
    while run:
        draw(WIN)
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Movement 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and l_pad.y - 5 > 0:
            l_pad.y -= 5
        elif keys[pygame.K_s] and l_pad.y + 5 < HEIGHT - PADDLE_HEIGHT:
            l_pad.y += 5

        if keys[pygame.K_UP] and r_pad.y - 5 > 0:
            r_pad.y -= 5
        elif keys[pygame.K_DOWN] and r_pad.y + 5 < HEIGHT - PADDLE_HEIGHT:
            r_pad.y += 5

        # Collision with Paddles
        if ball.x < PADDLE_WIDTH and ball.y >= l_pad.y and ball.y <= (l_pad.y + PADDLE_HEIGHT):
            ball.x_vel *= -1
            ball.vel_change(l_pad)

        if ball.x > WIDTH - PADDLE_WIDTH and ball.y >= r_pad.y and ball.y <= (r_pad.y + PADDLE_HEIGHT):
            ball.x_vel *= -1 
            ball.vel_change(r_pad)

        # Collision with Roof and Bottom
        if ball.y < 0 or ball.y > HEIGHT:
            ball.y_vel *= -1

        if ball.x > WIDTH:
            l_score += 1
            ball.reset()
        elif ball.x < 0:
            r_score += 1
            ball.reset()

        
        if l_score == 10:
            run = False
            WINNER = "Player 1"

        if r_score == 10:
            run = False    
            WINNER = "Player 2"
        
    if WINNER:
        win_txt = FONT.render(f"The Winner is: {WINNER}", True, WHITE)
        WIN.fill(BLACK)
        WIN.blit(win_txt, ((WIDTH - win_txt.get_width())//2,HEIGHT//2))
        pygame.display.update()
        pygame.time.wait(3000)