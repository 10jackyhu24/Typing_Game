import pygame
import random

def centerText(word, color, size, x, y):
    font = pygame.font.SysFont(None, size)
    surface = font.render(word, True, color)
    rect = surface.get_rect()
    rect.centerx = x
    rect.centery = y
    screen.blit(surface, rect)

def leftText(word, color, size, x, y):
    font = pygame.font.SysFont(None, size)
    surface = font.render(word, True, color)
    rect = surface.get_rect()
    rect.x = x
    rect.y = y
    screen.blit(surface, rect)

def draw_score():
    global score, HEIGHT
    word = 'Score: ' + str(score)
    leftText(word, (0, 0, 0), 32, 10, HEIGHT - 30)

def draw_time():
    global WIDTH, HEIGHT, time
    word = 'Time: ' + str(time)
    leftText(word, (0, 0, 0), 32, 10, HEIGHT - 60)

def draw_drop_cd():
    global WIDTH, HEIGHT, delay
    word = 'Drop CD: ' + format(delay, '.0f')
    leftText(word, (0, 0, 0), 32, WIDTH / 2 - 50, HEIGHT - 30)

def draw_drop_speed():
    global WIDTH, HEIGHT, speed
    word = 'Drop Speed: ' + str(format(speed, '.2f'))
    leftText(word, (0, 0, 0), 32, WIDTH / 2 - 50, HEIGHT - 60)

def init_screen():
    global score, time
    screen.fill(WHITE)
    word = 'Last score: ' + str(score)
    centerText(word, (0, 0, 0), 32, WIDTH / 2, 20)
    word_2 = 'Last play time: ' + str(time)
    centerText(word_2, (0, 0, 0), 32, WIDTH / 2, 50)
    centerText('Press the space bar to', (0, 0, 0), 32, WIDTH / 2, HEIGHT / 2 - 30)
    centerText('start the game', (0, 0, 0), 32, WIDTH / 2, HEIGHT / 2 + 30)

def updateGameStage(mode):
    global  speed, delay, time, score
    now_delay = delay
    if mode == 0:
        if time % 10 == 0:
            speed *= 1.03
            delay *= 0.9
    elif mode == 1:
        delay *= 0.9
    if now_delay != delay:
        pygame.time.set_timer(UPDATE, int(delay))

class Letter():
    def __init__(self):
        self.letter = chr(self.getRandomLetter())
        self.x = self.getRandomCoordinate()
        self.y = -10
        self.color = 0, 0, 0
        self.size = 64
        self.red_color = 0
        self.red_turn_on_off = 12

    def getRandomLetter(self):
        return random.randint(65, 90)

    def getRandomCoordinate(self):
        offset = 20
        return random.randint(0 + offset, WIDTH - offset)

    def update(self):
        self.y += speed

    def draw(self):
        centerText(self.letter, self.color, self.size, self.x, self.y)

    def drawFlashing(self):
        self.red_color += self.red_turn_on_off
        if self.red_color > 255:
            self.red_turn_on_off = -12
            self.red_color = 255
        elif self.red_color < 0:
            self.red_turn_on_off = 12
            self.red_color = 0
        R = self.red_color
        color = R, 0, 0
        centerText(self.letter, color, self.size, self.x, self.y)


if __name__ == '__main__':
    pygame.init()

    WIDTH = 400
    HEIGHT = 800
    WHITE = 255, 255, 255
    CLOCK = pygame.time.Clock()
    FPS = 60
    UPDATE = pygame.USEREVENT
    TIME = pygame.USEREVENT + 1
    SIZE = WIDTH, HEIGHT
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Typing Game')
    show_init = True
    running = True
    score = 0
    time = 0
    while running:
        # init
        if show_init:
            init_screen()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        letters = []
                        speed = 2
                        score = 0
                        delay = 1000
                        pygame.time.set_timer(UPDATE, delay)
                        pygame.time.set_timer(TIME, 1000)
                        time = 0
                        show_init = False
        else:
        # get input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if 97 <= event.key <= 122 and len(letters) > 0:
                        pressed_letter = chr(event.key - 32)
                        if pressed_letter == letters[0].letter:
                            score += 1
                            updateGameStage(0)
                            letters.pop(0)
                        else:
                            score -= 1
                            updateGameStage(1)
                if event.type == UPDATE:
                    letters.append(Letter())
                if event.type == TIME:
                    time += 1

            # game update
            CLOCK.tick(FPS)
            for letter in letters:
                if letter.y > HEIGHT:
                    show_init = True
                letter.update()

            # screen output
            screen.fill(WHITE)
            for i in range(len(letters) - 1, -1, -1):
                if i == 0:
                    letters[i].drawFlashing()
                else:
                    letters[i].draw()

            draw_score()
            draw_time()
            draw_drop_cd()
            draw_drop_speed()
            pygame.display.update()
    pygame.quit()