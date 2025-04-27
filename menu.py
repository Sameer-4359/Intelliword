import pygame
import sys
from pygame import mixer

pygame.init()
pygame.font.init()
pygame.mixer.init()
WINDOW_SIZE = 1200
x = 100
y = 100

def select_difficulty(screen):
    
    
    menu = pygame.image.load("images/menu.png")
    newsize = (WINDOW_SIZE,WINDOW_SIZE-400)
    menu = pygame.transform.scale(menu, newsize)
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)

    modes = ["Classic", "Grid Shuffle", "Word Bomb", "Word Chain", "Fog of War"]  # Added Word Chain
    difficulties = [("Easy", 5, 5), ("Medium", 8, 8), ("Hard", 10, 10)]

    selected_mode = None
    selected_diff = None

    while not selected_mode:
        
        screen.blit(menu, (0, 0))
        title = font.render("Select Game Mode", True, (245, 245, 245))
        screen.blit(title, (x, y))

        mode_rects = []
        for i, mode in enumerate(modes):
            rect = pygame.Rect(x+20, y+y + i*70, 200, 50)
            mode_rects.append((rect, mode))
            pygame.draw.rect(screen, (58, 159, 241), rect)
            text = small_font.render(mode, True, (245, 245, 245))
            screen.blit(text, (rect.x + 50, rect.y + 12))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mixer.Sound("music/click.mp3").play()
                pos = pygame.mouse.get_pos()
                for rect, mode in mode_rects:
                    if rect.collidepoint(pos):
                        selected_mode = mode

    while not selected_diff:
        screen.blit(menu, (0, 0))
        title = font.render("Select Difficulty", True, (245, 245, 245))
        screen.blit(title, (x+20, y))

        diff_rects = []
        for i, (label, grid_size, max_word_len) in enumerate(difficulties):
            rect = pygame.Rect(x+20, y + y + i*80, 200, 50)
            diff_rects.append((rect, grid_size, max_word_len))
            pygame.draw.rect(screen, (58, 159, 241), rect)
            text = small_font.render(label, True, (255, 255, 255))
            screen.blit(text, (rect.x + 70, rect.y + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, grid_size, max_word_len in diff_rects:
                    if rect.collidepoint(pos):
                        selected_diff = (grid_size, max_word_len)

    return (*selected_diff, selected_mode)

# Button settings
button_color = (200, 0, 0)
hover_color = (255, 0, 0)
text_color = (255, 255, 255)


def back_button(screen,font, button_rect):
    mouse_pos = pygame.mouse.get_pos()
    color = hover_color if button_rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, color, button_rect, border_radius=25)  # Rounded corners
    text = font.render("Back", True, text_color)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)