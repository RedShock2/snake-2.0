import sys
import argparse
import random
import pygame

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
FPS = 10

UP = pygame.Vector2(0, -1)
DOWN = pygame.Vector2(0, 1)
LEFT = pygame.Vector2(-1, 0)
RIGHT = pygame.Vector2(1, 0)

class Snake:
    def __init__(self, color, start_pos):
        self.body = [pygame.Vector2(start_pos)]
        self.direction = RIGHT
        self.color = color
        self.grow_pending = 0

    def handle_input(self, keys, up, down, left, right):
        if keys[up] and self.direction != DOWN:
            self.direction = UP
        elif keys[down] and self.direction != UP:
            self.direction = DOWN
        elif keys[left] and self.direction != RIGHT:
            self.direction = LEFT
        elif keys[right] and self.direction != LEFT:
            self.direction = RIGHT

    def move(self):
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)
        if self.grow_pending:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending += 1

    def hits_itself(self):
        return self.body[0] in self.body[1:]

    def draw(self, surface):
        for cell in self.body:
            rect = pygame.Rect(cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.color, rect)


def spawn_food(*snakes):
    while True:
        pos = pygame.Vector2(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        occupied = any(pos in snake.body for snake in snakes if snake)
        if not occupied:
            return pos


def check_collision(snake, other_snake=None):
    head = snake.body[0]
    if head.x < 0 or head.x >= GRID_WIDTH or head.y < 0 or head.y >= GRID_HEIGHT:
        return True
    if snake.hits_itself():
        return True
    if other_snake and head in other_snake.body:
        return True
    return False


def draw_food(surface, pos):
    rect = pygame.Rect(pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, (255, 255, 0), rect)


def main():
    parser = argparse.ArgumentParser(description="Simple Snake Game")
    parser.add_argument('--mode', choices=['solo', 'multi'], default='solo', help='Game mode')
    parser.add_argument('--p1', default='Player 1', help='Name of player 1')
    parser.add_argument('--p2', default='Player 2', help='Name of player 2 (multiplayer)')
    args = parser.parse_args()

    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    snake1 = Snake((0, 255, 0), (GRID_WIDTH // 4, GRID_HEIGHT // 2))
    snake2 = None
    if args.mode == 'multi':
        snake2 = Snake((255, 0, 0), (3 * GRID_WIDTH // 4, GRID_HEIGHT // 2))

    food = spawn_food(snake1, snake2)
    scores = {args.p1: 0}
    if snake2:
        scores[args.p2] = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        snake1.handle_input(keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
        if snake2:
            snake2.handle_input(keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

        snake1.move()
        if snake2:
            snake2.move()

        if snake1.body[0] == food:
            snake1.grow()
            scores[args.p1] += 1
            food = spawn_food(snake1, snake2)
        elif snake2 and snake2.body[0] == food:
            snake2.grow()
            scores[args.p2] += 1
            food = spawn_food(snake1, snake2)

        if check_collision(snake1, snake2):
            running = False
        if snake2 and check_collision(snake2, snake1):
            running = False

        screen.fill((0, 0, 0))
        draw_food(screen, food)
        snake1.draw(screen)
        if snake2:
            snake2.draw(screen)

        score_text = " | ".join(f"{name}: {score}" for name, score in scores.items())
        text_surf = font.render(score_text, True, (255, 255, 255))
        screen.blit(text_surf, (10, 5))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
