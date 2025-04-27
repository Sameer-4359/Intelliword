import pygame
from game import Game
from ui import draw_grid, draw_word_list, get_cell_under_mouse, get_random_color, draw_lines, show_victory_screen
from menu import select_difficulty, back_button
import random
from pygame import mixer


def load_words_from_file(filename="words.txt", count=8):
    try:
        with open(filename, 'r') as file:
            all_words = [word.strip().upper() for word in file.readlines() if word.strip()]
            return random.sample(all_words, min(count, len(all_words)))
    except FileNotFoundError:
        print(f"Warning: {filename} not found, using default words")
        return ["CAT", "DOG", "SUN", "SHARK", "TIGER", "BIRD", "LION", "ZEBRA"]


def run_game():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    
    CELL_SIZE = 60
    FONT = pygame.font.SysFont('consolas', 28)
    big_font = pygame.font.SysFont('Arial', 80, bold=True)
    WINDOW_SIZE = 1200
    WORDS = load_words_from_file()

    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE -400))

    pygame.display.set_caption("IntelliWord")
    icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(icon)

    #music
    mixer.music.load("music/background.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    #initialize the background
    background = pygame.image.load("images/background.png")
    newsize = (WINDOW_SIZE,WINDOW_SIZE-400)
    background = pygame.transform.scale(background, newsize)  
      
     

    #bomb
    time_bomb_icon = pygame.image.load("images/time-bomb.png")
    time_bomb_icon = pygame.transform.scale(time_bomb_icon, (24, 24))  # adjust size if needed
    
    GRID_SIZE, max_word_length, selected_mode = select_difficulty(screen)
    

    game = Game(size=GRID_SIZE, words=WORDS, mode=selected_mode)
    start_ticks = pygame.time.get_ticks()
    font = pygame.font.SysFont('consolas', 24)
    overFont = pygame.font.SysFont('consolas', 54, bold=True)

    def showGameOver():
        game_over = overFont.render("GAME OVER", True, (255, 80, 80))
        mixer.Sound("music/gameover.mp3").play()
        screen.blit(game_over, (WINDOW_SIZE // 2 - 170, 250))



    running = True
    button_rect = pygame.Rect(20, 20, 100, 30) # (x, y, width, height)
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
        draw_grid(screen, game.grid_manager.grid, CELL_SIZE, FONT, game)
        

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
            bomb_icon=time_bomb_icon if bomb_word else None,
            chain_word=game.word_chain[game.chain_index] if game.mode == "Word Chain" else None,
            reveal_points=game.reveal_points if game.mode == "Fog of War" else None
        )

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mixer.Sound("music/click.mp3").play()
                pos = pygame.mouse.get_pos()
                result = get_cell_under_mouse(pos, CELL_SIZE, GRID_SIZE, screen)
                if button_rect.collidepoint(event.pos):
                    
                    print("Back button clicked!")
                    running = False
                
                if result:
                    row, col = result
                    if game.mode == "Fog of War":
                        if game.reveal_area(row, col):
                            print(f"Revealed area around ({row}, {col}). Reveals left: {game.reveal_points}")
                            mixer.Sound("music/fog.mp3").play()
                        elif (row, col) in game.revealed_cells:
                            selected_start = result
                    else:
                        selected_start = result

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                result = get_cell_under_mouse(pos, CELL_SIZE, GRID_SIZE, screen)
                if result:
                    selected_end = result

                    if selected_start and selected_end:
                        word, positions = game.grid_manager.get_word_from_coords(
                            selected_start, selected_end, game
                        )
                        # Only proceed if we got a valid word and positions
                        if word and positions:
                            if game.check_and_update_word(word, positions):
                                print(f"✔ You found: {word}")
                                mixer.Sound("music/wordfound.mp3").play()
                                # Add all positions to revealed cells in Fog of War mode
                                if game.mode == "Fog of War":
                                    for pos in positions:
                                        game.revealed_cells.add(pos)
                                found_lines.append({
                                    'positions': list(positions),
                                    'progress': 0.0,
                                    'color': get_random_color(),
                                    'opacity': 150
                                })
                            else:
                                print("✘ Not a valid word.")
                                mixer.Sound("music/incorrect.mp3").play()
                        selected_start = selected_end = None

        # Draw the back button
        back_button(screen, font, button_rect)

        # AI Move
        # AI Move (only in non-Word Bomb modes)
        now = pygame.time.get_ticks()
        if not game_completed and game.mode == "Grid Shuffle" and now - ai_timer > ai_delay:
            ai_word, ai_path = game.ai_turn()
            ai_timer = now
            if ai_word:
                print(f"🤖 AI found: {ai_word}")
                mixer.Sound("music/aifound.mp3").play()
                found_lines.append({
                    'positions': list(ai_path),
                    'progress': 0.0,
                    'color': get_random_color(),
                    'opacity': 100
                })


        if game.is_game_over():
            game_completed = True

        draw_lines(screen, found_lines, CELL_SIZE, GRID_SIZE,game)

        # Timer + Score (Dark UI)
        if game.mode == "Grid Shuffle":
            cols = GRID_SIZE
            if cols <= 6:
                origin_x = (screen.get_width()) //cols
            elif cols <= 8:
                origin_x = (screen.get_width()) //cols
            else:
                origin_x = (screen.get_width()) //cols 

            origin_y = 50
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            timer_text = font.render(f"Time: {elapsed_seconds}s", True, (180, 180, 180))
            screen.blit(timer_text, (screen.get_width() - 140, 20))

            human_score = game.get_score("human")
            ai_score = game.get_score("ai")
            score_text = font.render(f"You: {human_score}   AI: {ai_score}", True, (180, 180, 180))
            screen.blit(score_text, (origin_x, origin_y))

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

        if  game_completed and game.mode == "Grid Shuffle":
            human_score = game.get_score("human")
            ai_score = game.get_score("ai")

            if human_score > ai_score:
                show_victory_screen(screen)
            elif human_score < ai_score:
                showGameOver()
            else:
                draw_lines(screen, found_lines, CELL_SIZE, GRID_SIZE,game)
                tie_text = big_font.render("It's a Tie!", True, (255, 255, 255))
                screen.blit(tie_text, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 50))

            pygame.display.flip()
            end_time = pygame.time.get_ticks() + 1500
            while pygame.time.get_ticks() < end_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                pygame.time.delay(1000)
            running = False

        if game.bomb_failed:
            pygame.time.delay(300)
            showGameOver()
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False


        if game_completed and all(line['progress'] >= 1.0 for line in found_lines):
            pygame.time.delay(100)
            show_victory_screen(screen)

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
