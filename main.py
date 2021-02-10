import pygame
import random
import data
import sys
import datetime
import time
import math
import copy

blank_sudoku = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def drawGrid(surface, dark_info):
    if dark_info:
        colo = (255, 255, 255)
    else:
        colo = (0, 0, 0)
    x = 0
    y = 0
    w = 1
    for i in range(10):
        if i % 3 == 0:
            w = 3
        pygame.draw.line(surface, colo, (x, 0), (x, cell_size * 9), width=w)
        pygame.draw.line(surface, colo, (0, y), (cell_size * 9, y), width=w)
        x += cell_size
        y += cell_size
        w = 1


def displayText(surface, dark_info, txt, x, y, size, start=True):
    if dark_info:
        if start:
            colo = (255, 255, 255)
        else:
            colo = (51, 207, 255)
    else:
        if start:
            colo = (0, 0, 0)
        else:
            colo = (51, 207, 255)
    comic_sans = pygame.font.SysFont('calibri', size)
    txt_surface = comic_sans.render(txt, False, colo)
    txt_rect = txt_surface.get_rect(topleft=(x, y))
    surface.blit(txt_surface, (x, y))
    surface.blit(txt_surface, txt_rect)
    pygame.display.update()
    return txt_rect


def drawMenu(surface, dark_info, t_easy, t_medium, t_hard, t_expert):
    displayText(surface, dark_info, 'Difficulty', cell_size, cell_size * 0.2, font_size_big)
    easy_r = displayText(surface, dark_info, 'Easy', cell_size, cell_size * 2, font_size_default)
    medium_r = displayText(surface, dark_info, 'Medium', cell_size, cell_size * 4, font_size_default)
    hard_r = displayText(surface, dark_info, 'Hard', cell_size, cell_size * 6, font_size_default)
    expert_r = displayText(surface, dark_info, 'Very Hard', cell_size, cell_size * 8, font_size_default)
    displayText(surface, dark_info, 'Record', cell_size * 5, cell_size * 0.2, font_size_big)
    displayText(surface, dark_info, str(t_easy), cell_size * 5, cell_size * 2, font_size_default)
    displayText(surface, dark_info, str(t_medium), cell_size * 5, cell_size * 4, font_size_default)
    displayText(surface, dark_info, str(t_hard), cell_size * 5, cell_size * 6, font_size_default)
    displayText(surface, dark_info, str(t_expert), cell_size * 5, cell_size * 8, font_size_default)
    displayText(surface, dark_info, 'Theme:', cell_size, cell_size * 9.75, font_size_small)
    dark_info_rect = displayText(surface, dark_info, 'Dark', cell_size * 4, cell_size * 9.75, font_size_small)
    bright_r = displayText(surface, dark_info, 'Bright', cell_size * 6, cell_size * 9.75, font_size_small)
    displayText(surface, dark_info, 'For the Sudokus:', cell_size, cell_size * 11, font_size_very_small)
    displayText(surface, dark_info, '© Memory-Improvement-Tips.com. Used by Permission.', cell_size, cell_size * 11.5,
                font_size_very_small)
    return easy_r, medium_r, hard_r, expert_r, dark_info_rect, bright_r


def displaySudoku(surface, dark_info, sudoku, start):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                displayText(surface, dark_info, str(sudoku[i][j]), cell_size * (j + 0.32), cell_size * (i + 0.17),
                            font_size_big, start=start)
            else:
                continue


def markCells(surface, number, sudoku, sudoku_start, empt, x_p, y_p, colo=(166, 255, 184)):
    if not empt:
        if number != 0:
            for i in range(9):
                for j in range(9):
                    if sudoku[i][j] == number or sudoku_start[i][j] == number:
                        x = cell_size * j + 1
                        y = cell_size * i + 1
                        width = cell_size - 1
                        height = cell_size - 1
                        if j % 3 == 0:
                            x += 1
                            width -= 1
                        if j % 3 == 2:
                            width -= 1
                        if i % 3 == 0:
                            y += 1
                            height -= 1
                        if i % 3 == 2:
                            height -= 1
                        pygame.draw.rect(surface, colo, (x, y, width, height))
    else:
        i = y_p // cell_size
        j = x_p // cell_size
        x_p = j * cell_size + 1
        y_p = i * cell_size + 1
        width = cell_size - 1
        height = cell_size - 1
        if j % 3 == 0:
            x_p += 1
            width -= 1
        if j % 3 == 2:
            width -= 1
        if i % 3 == 0:
            y_p += 1
            height -= 1
        if i % 3 == 2:
            height -= 1
        pygame.draw.rect(surface, colo, (x_p, y_p, width, height))


def insertNum(surface, num, current_s, current_s_s, r, c, dark_info):
    current_s[r][c] = num
    moves.append((r, c, num))
    surface.fill(color=bg_col)
    drawGrid(surface, dark_info)
    displaySudoku(win, dark_info, current_s_s, True)
    displaySudoku(win, dark_info, current_s, False)


pygame.font.init()


def markCellsLogic(x_p, y_p, empt):
    global saved_num, marked_num
    if empty:
        if dark:
            colo = (40, 40, 40)
        else:
            colo = (230, 230, 230)
    else:
        if dark:
            colo = (0, 108, 36)
        else:
            colo = (166, 255, 184)
    if 0 <= x_p <= cell_size * 9 and 0 <= y_p <= cell_size * 9:
        if (current_sudoku[y_pos // cell_size][x_pos // cell_size] != 0) or empt:
            win.fill(color=bg_col)
            drawGrid(win, dark)
            marked_num = current_sudoku[y_pos // cell_size][x_pos // cell_size]
            if (marked_num != 0 and marked_num != saved_num) or empt:
                markCells(win, marked_num, current_sudoku, current_sudoku_start, empt, x_p, y_p, colo=colo)
                markCells(win, marked_num, current_sudoku, current_sudoku_start, empt, x_p, y_p, colo=colo)
                saved_num = current_sudoku[y_pos // cell_size][x_pos // cell_size]
            displaySudoku(win, dark, current_sudoku_start, True)
            displaySudoku(win, dark, current_sudoku, False)
        elif (current_sudoku_start[y_pos // cell_size][x_pos // cell_size] != 0) or empt:
            win.fill(color=bg_col)
            drawGrid(win, dark)
            marked_num = current_sudoku_start[y_p // cell_size][x_p // cell_size]
            if (marked_num != 0 and marked_num != saved_num) or empt:
                markCells(win, marked_num, current_sudoku, current_sudoku_start, empt, x_p, y_p, colo=colo)
                markCells(win, marked_num, current_sudoku, current_sudoku_start, empt, x_p, y_p, colo=colo)
                saved_num = current_sudoku_start[y_pos // cell_size][x_pos // cell_size]
            else:
                saved_num = 0
            displaySudoku(win, dark, current_sudoku_start, True)
            displaySudoku(win, dark, current_sudoku, False)


def displayNumbers(surface):
    n1_rect = displayText(surface, dark, '1', cell_size * 0.5, cell_size * 9.3, font_size_big)
    n2_rect = displayText(surface, dark, '2', cell_size * 1.3, cell_size * 9.3, font_size_big)
    n3_rect = displayText(surface, dark, '3', cell_size * 2.1, cell_size * 9.3, font_size_big)
    n4_rect = displayText(surface, dark, '4', cell_size * 2.9, cell_size * 9.3, font_size_big)
    n5_rect = displayText(surface, dark, '5', cell_size * 3.7, cell_size * 9.3, font_size_big)
    n6_rect = displayText(surface, dark, '6', cell_size * 0.9, cell_size * 10.3, font_size_big)
    n7_rect = displayText(surface, dark, '7', cell_size * 1.7, cell_size * 10.3, font_size_big)
    n8_rect = displayText(surface, dark, '8', cell_size * 2.5, cell_size * 10.3, font_size_big)
    n9_rect = displayText(surface, dark, '9', cell_size * 3.3, cell_size * 10.3, font_size_big)
    return n1_rect, n2_rect, n3_rect, n4_rect, n5_rect, n6_rect, n7_rect, n8_rect, n9_rect


if __name__ == '__main__':
    dark = False
    playing = True
    FPS = 90
    cell_size = 55
    font_size_very_small = 18
    font_size_small = 27
    font_size_default = 35
    font_size_big = 45
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
                if medium_rect.collidepoint(mouse_pos):
                    difficulty = 2
                if hard_rect.collidepoint(mouse_pos):
                    difficulty = 3
                if expert_rect.collidepoint(mouse_pos):
                    difficulty = 4
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
        first = True
        current_sudoku = copy.deepcopy(blank_sudoku)
        current_sudoku_start = copy.deepcopy(blank_sudoku)
        current_solution = copy.deepcopy(blank_sudoku)
        marked_num = 0
        saved_num = 0
        play_pause = 'Pause'
        start_time = time.time()
        dt = 0
        play = True
        moves = []
        marked_cell = (-1, -1)
        empty = False
        if difficulty != 0:
            win.fill(color=bg_col)
        while difficulty != 0:
            if first:
                sudokus_list = data.sudokus[difficulty]
                solutions_list = data.solutions[difficulty]
                rand_num = random.randint(0, len(sudokus_list) - 1)
                current_sudoku_start = sudokus_list[rand_num].copy()
                current_sudoku = copy.deepcopy(blank_sudoku)
                current_solution = solutions_list[rand_num].copy()
                drawGrid(win, dark)
                displaySudoku(win, dark, current_sudoku_start, True)
                displaySudoku(win, dark, current_sudoku, False)
            num1, num2, num3, num4, num5, num6, num7, num8, num9 = displayNumbers(win)
            displayText(win, dark, 'Time:', cell_size * 4.5, cell_size * 9.8, font_size_default)
            if dark:
                col = 'black'
            else:
                col = 'white'
            pygame.draw.rect(win, col, (
                math.floor(cell_size * 6.25), math.floor(cell_size * 9.8), math.floor(cell_size * 3), cell_size))
            displayText(win, dark, time.strftime('%H:%M:%S', time.gmtime(dt)), cell_size * 6.25, cell_size * 9.8,
                        font_size_default)
            play_pause_rect = displayText(win, dark, play_pause, cell_size * 7.5, cell_size * 9.2, font_size_small)
            menu_rect = displayText(win, dark, 'Menu', cell_size * 0.5, cell_size * 11.2, font_size_small)
            undo_rect = displayText(win, dark, 'Undo', cell_size * 2.5, cell_size * 11.2, font_size_small)
            redo_rect = displayText(win, dark, 'Redo', cell_size * 3.75, cell_size * 11.2, font_size_small)
            hint_rect = displayText(win, dark, 'Hint', cell_size * 5.75, cell_size * 11.2, font_size_small)
            solution_rect = displayText(win, dark, 'Solution', cell_size * 7, cell_size * 11.2, font_size_small)
            pygame.display.update()
            if play:
                dt += time.time() - start_time
                start_time = time.time()
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
                        difficulty = 0
                        win.fill(color=bg_col)
                        # TODO: fix the changing of blank_sudoku
                    x_pos = mouse_pos[0]
                    y_pos = mouse_pos[1]
                    if 0 <= x_pos <= cell_size * 9 and 0 <= y_pos <= cell_size * 9:
                        if current_sudoku_start[y_pos // cell_size][x_pos // cell_size] == 0:
                            empty = True
                            marked_cell = (y_pos // cell_size, x_pos // cell_size)
                        else:
                            empty = False
                        markCellsLogic(x_pos, y_pos, empty)
                    row = marked_cell[0]
                    col = marked_cell[1]
                    if empty and current_sudoku_start[row][col] == 0 and current_sudoku[row][col] == 0:
                        if num1.collidepoint(mouse_pos):
                            insertNum(win, 1, current_sudoku, current_sudoku_start, row, col, dark)
                        if num2.collidepoint(mouse_pos):
                            insertNum(win, 2, current_sudoku, current_sudoku_start, row, col, dark)
                        if num3.collidepoint(mouse_pos):
                            insertNum(win, 3, current_sudoku, current_sudoku_start, row, col, dark)
                        if num4.collidepoint(mouse_pos):
                            insertNum(win, 4, current_sudoku, current_sudoku_start, row, col, dark)
                        if num5.collidepoint(mouse_pos):
                            insertNum(win, 5, current_sudoku, current_sudoku_start, row, col, dark)
                        if num6.collidepoint(mouse_pos):
                            insertNum(win, 6, current_sudoku, current_sudoku_start, row, col, dark)
                        if num7.collidepoint(mouse_pos):
                            insertNum(win, 7, current_sudoku, current_sudoku_start, row, col, dark)
                        if num8.collidepoint(mouse_pos):
                            insertNum(win, 8, current_sudoku, current_sudoku_start, row, col, dark)
                        if num9.collidepoint(mouse_pos):
                            insertNum(win, 9, current_sudoku, current_sudoku_start, row, col, dark)
                    if play_pause_rect.collidepoint(mouse_pos):
                        if dark:
                            col = 'black'
                        else:
                            col = 'white'
                        if play_pause == 'Play':
                            play_pause = 'Pause'
                            play = True
                            start_time = time.time()
                            pygame.draw.rect(win, col, (
                                math.floor(cell_size * 7.5), math.floor(cell_size * 9.2), math.floor(cell_size * 2),
                                math.floor(cell_size * 0.75)))
                        elif play_pause == 'Pause':
                            play_pause = 'Play'
                            play = False
                            pygame.draw.rect(win, col, (
                                math.floor(cell_size * 7.5), math.floor(cell_size * 9.2), math.floor(cell_size * 2),
                                math.floor(cell_size * 0.75)))
            first = False
            # TODO: white box when stop, undo & redo logic, hint & solution logic, ending
            #  screen, updating record time (with text file), design and set icon 211

