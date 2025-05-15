import pygame
import sys
import pyaudio
import numpy as np

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 600, 400
BALL_SIZE = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
FPS = 60

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Paddle(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 5

    def move(self, y):
        self.y = y - self.height / 2
        if self.top < 0:
            self.top = 0
        elif self.bottom > HEIGHT:
            self.bottom = HEIGHT

    def ai_move(self, ball_y):
        if ball_y < self.centery:
            self.y -= self.speed
        elif ball_y > self.centery:
            self.y += self.speed

        if self.top < 0:
            self.top = 0
        elif self.bottom > HEIGHT:
            self.bottom = HEIGHT

class Ball(pygame.Rect):
    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT / 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.top < 0 or self.bottom > HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed_x *= -1

def play_sound(frequency, duration):
    p = pyaudio.PyAudio()
    volume = 1.0
    fs = 44100
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    stream.write(volume * samples)
    stream.stop_stream()
    stream.close()
    p.terminate()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    paddle1 = Paddle(0, HEIGHT / 2 - PADDLE_HEIGHT / 2)
    paddle2 = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT / 2 - PADDLE_HEIGHT / 2)
    ball = Ball()

    score1 = 0
    score2 = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_y:
                    score1 = 0
                    score2 = 0
                    ball.reset()
                    game_over = False
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            mouse_y = pygame.mouse.get_pos()[1]
            paddle1.move(mouse_y)
            paddle2.ai_move(ball.centery)

            ball.move()

            if ball.colliderect(paddle1) or ball.colliderect(paddle2):
                ball.speed_x *= -1
                play_sound(1000, 0.1)

            if ball.left < 0:
                score2 += 1
                ball.reset()
            elif ball.right > WIDTH:
                score1 += 1
                ball.reset()

            if score1 == 5 or score2 == 5:
                game_over = True

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle1)
        pygame.draw.rect(screen, WHITE, paddle2)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
        font = pygame.font.Font(None, 72)
        text = font.render(f"{score1} - {score2}", True, WHITE)
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 10))

        if game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over! Restart? (Y/N)", True, WHITE)
            screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
