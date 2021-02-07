import pygame
import data
import sys
import datetime


def drawGrid(surface, dark_info):
    if dark_info:
        col = (255, 255, 255)
    else:
        col = (0, 0, 0)
    x = 0
    y = 0
    w = 1
    for i in range(10):
        if i % 3 == 0:
            w = 3
        pygame.draw.line(surface, col, (x, 0), (x, cell_size * 9), width=w)
        pygame.draw.line(surface, col, (0, y), (cell_size * 9, y), width=w)
        x += cell_size
        y += cell_size
        w = 1


pygame.font.init()


def displayText(surface, dark_info, txt, x, y, size):
    if dark_info:
        col = (255, 255, 255)
    else:
        col = (0, 0, 0)
    comic_sans = pygame.font.SysFont('calibri', size)
    txt_surface = comic_sans.render(txt, False, col)
    txt_rect = txt_surface.get_rect(topleft=(x, y))
    surface.blit(txt_surface, (x, y))
    surface.blit(txt_surface, txt_rect)
    pygame.display.update()
    return txt_rect


def drawMenu(surface, dark_info, t_easy, t_medium, t_hard, t_expert):
    displayText(surface, dark_info, 'Difficulty', cell_size, cell_size, font_size_big)
    easy_r = displayText(surface, dark_info, 'Easy', cell_size, cell_size * 3, font_size_default)
    medium_r = displayText(surface, dark_info, 'Medium', cell_size, cell_size * 5, font_size_default)
    hard_r = displayText(surface, dark_info, 'Hard', cell_size, cell_size * 7, font_size_default)
    expert_r = displayText(surface, dark_info, 'Very Hard', cell_size, cell_size * 9, font_size_default)
    displayText(surface, dark_info, 'Record', cell_size * 5, cell_size, font_size_big)
    displayText(surface, dark_info, str(t_easy), cell_size * 5, cell_size * 3, font_size_default)
    displayText(surface, dark_info, str(t_medium), cell_size * 5, cell_size * 5, font_size_default)
    displayText(surface, dark_info, str(t_hard), cell_size * 5, cell_size * 7, font_size_default)
    displayText(surface, dark_info, str(t_expert), cell_size * 5, cell_size * 9, font_size_default)
    displayText(surface, dark_info, 'Theme:', cell_size, cell_size * 10.5, font_size_small)
    dark_info_rect = displayText(surface, dark_info, 'Dark', cell_size * 4, cell_size * 10.5, font_size_small)
    bright_r = displayText(surface, dark_info, 'Bright', cell_size * 6, cell_size * 10.5, font_size_small)
    displayText(surface, dark_info, '© Memory-Improvement-Tips.com. Used by Permission.', cell_size, cell_size * 11.5, font_size_very_small)
    return easy_r, medium_r, hard_r, expert_r, dark_info_rect, bright_r


if __name__ == '__main__':
    dark = False
    playing = True
    FPS = 60
    cell_size = 60
    font_size_very_small = 18
    font_size_small = 27
    font_size_default = 35
    font_size_big = 43
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((cell_size * 9, cell_size * 12))
    pygame.display.set_caption('Sudoku')
    if dark:
        bg_col = 'black'
    else:
        bg_col = 'white'
    win.fill(color=bg_col)
    # pygame.display.set_icon() TODO: Design and set icon
    while playing:
        difficulty = 0
        time_easy = datetime.timedelta(seconds=0)
        time_medium = datetime.timedelta(seconds=0)
        time_hard = datetime.timedelta(seconds=0)
        time_expert = datetime.timedelta(seconds=0)
        easy_rect, medium_rect, hard_rect, expert_rect, dark_rect, bright_rect = drawMenu(win, dark, time_easy,
                                                                                          time_medium, time_hard,
                                                                                          time_expert)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if easy_rect.collidepoint(mouse_pos):
                    difficulty = 1
                    print(1)
                if medium_rect.collidepoint(mouse_pos):
                    difficulty = 2
                    print(2)
                if hard_rect.collidepoint(mouse_pos):
                    difficulty = 3
                    print(3)
                if expert_rect.collidepoint(mouse_pos):
                    difficulty = 4
                    print(4)
                if dark_rect.collidepoint(mouse_pos):
                    dark = True
                    if dark:
                        bg_col = 'black'
                    else:
                        bg_col = 'white'
                    win.fill(color=bg_col)
                    easy_rect, medium_rect, hard_rect, expert_rect, dark_rect, bright_rect = drawMenu(win, dark,
                                                                                                      time_easy,
                                                                                                      time_medium,
                                                                                                      time_hard,
                                                                                                      time_expert)
                if bright_rect.collidepoint(mouse_pos):
                    dark = False
                    if dark:
                        bg_col = 'black'
                    else:
                        bg_col = 'white'
                    win.fill(color=bg_col)
                    easy_rect, medium_rect, hard_rect, expert_rect, dark_rect, bright_rect = drawMenu(win, dark,
                                                                                                      time_easy,
                                                                                                      time_medium,
                                                                                                      time_hard,
                                                                                                      time_expert)
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(FPS)
        if difficulty != 0:
            win.fill(color=bg_col)
        while difficulty != 0:
            drawGrid(win, dark)
            menu_rect = displayText(win, dark, 'Menu', cell_size, cell_size * 11, font_size_small)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if menu_rect.collidepoint(mouse_pos):
                        if dark:
                            bg_col = 'black'
                        else:
                            bg_col = 'white'
                        win.fill(color=bg_col)
                        difficulty = 0
            # TODO: main solving screen with 9 x 9 grid, time, pause & play, verification-switch
            #  digits 1 to 9 as inputs, undo & redo, hint and show solution button.
