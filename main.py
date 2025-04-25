import pygame
from game import Game
from ui import draw_grid, draw_word_list, get_cell_under_mouse, get_random_color, draw_lines
from menu import select_difficulty
import random


def run_game():
    pygame.init()
    pygame.font.init()

    CELL_SIZE = 60
    FONT = pygame.font.SysFont('consolas', 28)
    WINDOW_SIZE = 600
    WORDS = ["CAT", "DOG", "SUN", "SHARK", "ELEPHANT", "TIGER", "BIRD", "LION", "ZEBRA"]

    pygame.display.set_caption("IntelliWord")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    #bomb
    time_bomb_icon = pygame.image.load("time-bomb.png")
    time_bomb_icon = pygame.transform.scale(time_bomb_icon, (24, 24))  # adjust size if needed


    # Dark mode background
    background = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE + 100))
    background.fill((30, 30, 30))

    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
    GRID_SIZE, max_word_length, selected_mode = select_difficulty(screen)


    game = Game(size=GRID_SIZE, words=WORDS, mode=selected_mode)

    start_ticks = pygame.time.get_ticks()
    font = pygame.font.SysFont('consolas', 24)
    overFont = pygame.font.SysFont('consolas', 54, bold=True)

    def showGameOver():
        game_over = overFont.render("GAME OVER", True, (255, 80, 80))
        screen.blit(game_over, (WINDOW_SIZE // 2 - 170, 250))

    running = True
    selected_start = None
    selected_end = None
    found_lines = []
    game_completed = False

    ai_timer = pygame.time.get_ticks()
    ai_delay = 6500

    bomb_interval = 5000  # 30 seconds
    last_bomb_time = pygame.time.get_ticks()

    while running:
        screen.blit(background, (0, 0))
        draw_grid(screen, game.grid_manager.grid, CELL_SIZE, FONT)
        # if game.bomb_word:
        #     bomb_path = game.ai.find_word(game.grid_manager.grid, game.bomb_word)
        #     if bomb_path:
        #         draw_lines(screen, [{
        #             'positions': list(bomb_path),
        #             'progress': 1.0,
        #             'color': (255, 0, 0),
        #             'opacity': 80
        #          }], CELL_SIZE, GRID_SIZE)

        bomb_word = game.bomb_word if game.mode == "Word Bomb" else None

        draw_word_list(
            screen,
            game.found_words,
            game.words,
            FONT,
            CELL_SIZE,
            GRID_SIZE,
            text_color=(200, 200, 200),
            bomb_word=bomb_word,
            bomb_icon=time_bomb_icon if bomb_word else None
        )



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                result = get_cell_under_mouse(pos, CELL_SIZE, GRID_SIZE, screen)
                if result:
                    selected_start = result

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                result = get_cell_under_mouse(pos, CELL_SIZE, GRID_SIZE, screen)
                if result:
                    selected_end = result

                    if selected_start and selected_end:
                        word, positions = game.grid_manager.get_word_from_coords(
                            selected_start, selected_end
                        )
                        if game.check_and_update_word(word, positions):
                            print(f"✔ You found: {word}")
                            positions = list(positions)
                            found_lines.append({
                                'positions': positions,
                                'progress': 0.0,
                                'color': get_random_color(),
                                'opacity': 150
                            })
                        else:
                            print("✘ Not a valid word.")
                        selected_start = selected_end = None

        # AI Move
        # AI Move (only in non-Word Bomb modes)
        now = pygame.time.get_ticks()
        if not game_completed and game.mode == "Grid Shuffle" and now - ai_timer > ai_delay:
            ai_word, ai_path = game.ai_turn()
            ai_timer = now
            if ai_word:
                print(f"🤖 AI found: {ai_word}")
                found_lines.append({
                    'positions': list(ai_path),
                    'progress': 0.0,
                    'color': get_random_color(),
                    'opacity': 100
                })


        if game.is_game_over():
            game_completed = True

        draw_lines(screen, found_lines, CELL_SIZE, GRID_SIZE)

        # Timer + Score (Dark UI)
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        timer_text = font.render(f"Time: {elapsed_seconds}s", True, (180, 180, 180))
        screen.blit(timer_text, (screen.get_width() - 140, 20))

        human_score = game.get_score("human")
        ai_score = game.get_score("ai")
        score_text = font.render(f"You: {human_score}   AI: {ai_score}", True, (180, 180, 180))
        screen.blit(score_text, (20, 20))

        # Word Bomb mode
        if game.mode == "Word Bomb":
            if not game.bomb_word and now - last_bomb_time >= bomb_interval:
                game.pick_random_unfound_word()
                last_bomb_time = now

            if game.bomb_word:
                new_now = pygame.time.get_ticks()  # Ensure you get this in the same place
                time_left = max(0, 10 - (new_now - game.bomb_start_time) // 1000)

                if time_left == 0:
                    game.handle_bomb_failure()
                    last_bomb_time = new_now

                bomb_text = FONT.render(f"⏳ {time_left}s", True, (255, 0, 0))
                screen.blit(bomb_text, (screen.get_width() // 2 - 120, screen.get_height() - 40))

        if game.bomb_failed:
            showGameOver()
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False


        if game_completed and all(line['progress'] >= 1.0 for line in found_lines):
            showGameOver()
            pygame.display.flip()
            end_time = pygame.time.get_ticks() + 1500
            while pygame.time.get_ticks() < end_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                pygame.time.delay(10)
            running = False

        pygame.time.delay(10)
        pygame.display.flip()


while 1:
    run_game()
