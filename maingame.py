import sys

import pygame
import combat_client
import gamedata

pygame.init()

# define font style and size
font = pygame.font.Font('Assets/slkscr.ttf', gamedata.FONTSIZE)
font_special = pygame.font.Font('Assets/slkscr.ttf', int(gamedata.FONTSIZE * 1.5))

# define main windows framework
# set resolution
WIN = pygame.display.set_mode((gamedata.WIDTH, gamedata.HEIGHT))
# set title
pygame.display.set_caption("Hyper Typer")


# display waiting text
def waiting_for_another_player():
    waiting_text = font.render('Waiting for another player...', False, (200, 200, 200), (50, 50, 50))
    WIN.blit(waiting_text, (
        gamedata.WIDTH // 2 - waiting_text.get_width() // 2, gamedata.HEIGHT // 2 - waiting_text.get_height() // 2))


# read txt into TXT list
def read_txt():
    file = open("Assets/1.txt")
    line = file.readline()

    while line:
        line = line[:-1]
        gamedata.TXT.append(line)
        line = file.readline()

    file.close()


# clear the scene
def initial_draw():
    WIN.fill((66, 66, 66))
    pygame.display.update()


def draw_window(current_index, current_word, score_me, score_opponent):
    WIN.fill((66, 66, 66))
    # set rope positon
    gamedata.image_x = -gamedata.WIDTH // 2 - (int(score_me) - int(score_opponent)) * gamedata.SCORE_MUL
    gamedata.image_y = gamedata.HEIGHT // 5
    # draw the rope
    WIN.blit(gamedata.IMAGE1, (gamedata.image_x, gamedata.image_y))

    # word I am inputting
    TXT_NOW = gamedata.TXT[current_index][0:current_word + 1]
    # word I have inputted
    TXT_CORRECT = gamedata.TXT[current_index][0:current_word]

    combo_text = font_special.render('COMBO x ' + str(gamedata.combo), False, (220, 120, 100), (50, 50, 50))
    score_text_me = font.render('My Score: ' + str(score_me) + ' (+' + str(gamedata.combo // 5 + 1) + ')', False,
                                (200, 200, 200), (50, 50, 50))
    score_text_opponent = font.render("Opponent's Score: " + str(score_opponent), False, (200, 200, 200), (50, 50, 50))

    # combo score display
    WIN.blit(combo_text,
             (gamedata.WIDTH // 2 - combo_text.get_width() // 2, gamedata.HEIGHT // 1.5 - combo_text.get_height() // 2))
    # my score display
    WIN.blit(score_text_me, (20, 20))
    # opponent's score display
    WIN.blit(score_text_opponent, (gamedata.WIDTH - score_text_opponent.get_width() - 20, 20))

    text = font.render(gamedata.TXT[current_index], False, (200, 200, 200), (50, 50, 50))
    current_text = font.render(TXT_NOW, False, (220, 220, 220), (80, 80, 80))
    correct_text = font.render(TXT_CORRECT, False, (200, 200, 200), (50, 150, 50))

    # black
    WIN.blit(text, (gamedata.WIDTH // 2 - text.get_width() // 2, gamedata.HEIGHT - gamedata.FONTSIZE - 20))
    # grey
    WIN.blit(current_text, (gamedata.WIDTH // 2 - text.get_width() // 2, gamedata.HEIGHT - gamedata.FONTSIZE - 25))
    # green
    WIN.blit(correct_text, (gamedata.WIDTH // 2 - text.get_width() // 2, gamedata.HEIGHT - gamedata.FONTSIZE - 20))

    pygame.display.update()


def analyse_data_from_server():
    # print(gamedata.net_content)
    if gamedata.net_content[0] == '!':
        pass
    else:
        if gamedata.net_content[0] == '1' or gamedata.net_content[0] == '0':
            if str(gamedata.net_index) != gamedata.net_content[0]:
                gamedata.score_opponent = gamedata.net_content[2:]
        else:
            pass


def win_or_lose(clock):
    # if win
    if gamedata.image_x // 2 <= -gamedata.WIDTH // 2:
        combat_client.send('!win')
        initial_draw()

        # show win text
        press_text = font.render('press any key to quit', False, (200, 200, 200), (50, 50, 50))
        waiting_text = font_special.render('YOU WIN!', False, (100, 200, 120), (50, 50, 50))
        WIN.blit(waiting_text, (
            gamedata.WIDTH // 2 - waiting_text.get_width() // 2, gamedata.HEIGHT // 2 - waiting_text.get_height() // 2))
        WIN.blit(press_text, (
            gamedata.WIDTH // 2 - press_text.get_width() // 2, gamedata.HEIGHT // 1.5 - press_text.get_height() // 2))
        pygame.display.update()

        # press any key to quit
        while True:
            clock.tick(gamedata.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()

    # if lost
    elif gamedata.net_content == '!win':
        initial_draw()
        press_text = font.render('press any key to quit', False, (200, 200, 200), (50, 50, 50))
        waiting_text = font_special.render('YOU LOSE!', False, (200, 100, 120), (50, 50, 50))
        WIN.blit(waiting_text, (
            gamedata.WIDTH // 2 - waiting_text.get_width() // 2, gamedata.HEIGHT // 2 - waiting_text.get_height() // 2))
        WIN.blit(press_text, (
            gamedata.WIDTH // 2 - press_text.get_width() // 2, gamedata.HEIGHT // 1.5 - press_text.get_height() // 2))
        pygame.display.update()
        while True:
            clock.tick(gamedata.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()
    else:
        pass


def main():
    initial_draw()

    # get my index in server clients list
    combat_client.send('!index')

    # get how many clients have connected
    combat_client.send('!count')

    read_txt()
    # current line index in TXT (TXT[current_index])
    current_index = 0
    # current word index in this line (TXT[current_index][current word])
    current_word = 0

    clock = pygame.time.Clock()
    # 200 ms a response if holding a key
    pygame.key.set_repeat(200)

    # display waiting text
    if gamedata.client_count < 2:
        waiting_for_another_player()
        pygame.display.update()

    # constantly check if there is another player
    while gamedata.client_count < 2:
        clock.tick(gamedata.FPS)  # equal to time.sleep(1//gamedata.FPS)
        combat_client.send('!count')

        # check pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    run = True
    while run:
        clock.tick(gamedata.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # key detect
            if event.type == pygame.KEYDOWN:
                # get key list
                keys_pressed = pygame.key.get_pressed()
                key = ''
                # get key number
                for i in range(len(keys_pressed)):
                    if keys_pressed[i] > 0:
                        key = chr(i)

                # if key matched
                if key.upper() == gamedata.TXT[current_index][current_word] or \
                        key.lower() == gamedata.TXT[current_index][current_word]:
                    gamedata.score_me += 1 + gamedata.combo // 5
                    gamedata.combo += 1
                    # sync my score with the server
                    combat_client.send(f'{gamedata.score_me}')

                    # check if word index should increase
                    if current_word < len(gamedata.TXT[current_index]) - 1:
                        current_word += 1
                    else:
                        current_word = 0
                        # check if line index should increase
                        if current_index < len(gamedata.TXT) - 1:
                            current_index += 1
                        else:
                            current_index = 0
                # if key don't match
                else:
                    gamedata.combo = 0

        analyse_data_from_server()
        draw_window(current_index, current_word, gamedata.score_me, gamedata.score_opponent)
        win_or_lose(clock)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
