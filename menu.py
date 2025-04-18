import pygame
import sys

def select_difficulty(screen):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)

    difficulties = [("Easy", 5, 5), ("Medium", 8, 8), ("Hard", 10, 10)]
    button_rects = []

    screen.fill((30, 30, 30))
    title = font.render("Select Difficulty", True, (255, 255, 255))
    screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))

    for i, (label, grid_size, max_word_len) in enumerate(difficulties):
        rect = pygame.Rect(screen.get_width()//2 - 100, 150 + i*100, 200, 60)
        button_rects.append((rect, grid_size, max_word_len))
        pygame.draw.rect(screen, (70, 130, 180), rect)
        text = small_font.render(label, True, (255, 255, 255))
        screen.blit(text, (rect.x + 70, rect.y + 15))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, grid_size, max_word_len in button_rects:
                    if rect.collidepoint(mouse_pos):
                        return grid_size, max_word_len
                    

