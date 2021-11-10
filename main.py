import pygame
import random
import sudoku_data
import sys
import os
import time
import math
import copy
import calendar

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


def getPath(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def drawGrid(surface, dark_info):
    if grid:
        if dark_info:
            colo = (255, 255, 255)
        else:
            colo = (0, 0, 0)
        x = 0
        y = 0
        w = 1
        for n in range(10):
            if n % 3 == 0:
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
            colo = (3, 132, 252)
    else:
        if start:
            colo = (0, 0, 0)
        else:
            colo = (3, 132, 252)
    comic_sans = pygame.font.SysFont('calibri', size)
    txt_surface = comic_sans.render(txt, False, colo)
    txt_rect = txt_surface.get_rect(topleft=(x, y))
    surface.blit(txt_surface, (x, y))
    surface.blit(txt_surface, txt_rect)
    pygame.display.update()
    return txt_rect


def drawMenu(surface, dark_info, ti_easy, ti_medium, ti_hard, ti_very_hard):
    displayText(surface, dark_info, 'Difficulty', cell_size, cell_size * 0.2, font_size_big)
    easy_r = displayText(surface, dark_info, 'Easy', cell_size, cell_size * 2, font_size_default)
    medium_r = displayText(surface, dark_info, 'Medium', cell_size, cell_size * 4, font_size_default)
    hard_r = displayText(surface, dark_info, 'Hard', cell_size, cell_size * 6, font_size_default)
    very_hard_r = displayText(surface, dark_info, 'Very Hard', cell_size, cell_size * 8, font_size_default)
    displayText(surface, dark_info, 'Record', cell_size * 5, cell_size * 0.2, font_size_big)
    displayText(surface, dark_info, str(ti_easy), cell_size * 5, cell_size * 2, font_size_default)
    displayText(surface, dark_info, str(ti_medium), cell_size * 5, cell_size * 4, font_size_default)
    displayText(surface, dark_info, str(ti_hard), cell_size * 5, cell_size * 6, font_size_default)
    displayText(surface, dark_info, str(ti_very_hard), cell_size * 5, cell_size * 8, font_size_default)
    displayText(surface, dark_info, 'Theme:', cell_size, cell_size * 9.75, font_size_small)
    dark_info_rect = displayText(surface, dark_info, 'Dark', cell_size * 4, cell_size * 9.75, font_size_small)
    bright_r = displayText(surface, dark_info, 'Bright', cell_size * 6, cell_size * 9.75, font_size_small)
    displayText(surface, dark_info, 'For the Sudokus:', cell_size, cell_size * 11, font_size_very_small)
    displayText(surface, dark_info, '© Memory-Improvement-Tips.com. Used by Permission.', cell_size, cell_size * 11.5,
                font_size_very_small)
    return easy_r, medium_r, hard_r, very_hard_r, dark_info_rect, bright_r


def displaySudoku(surface, dark_info, sudoku, start):
    for n in range(9):
        for k in range(9):
            if sudoku[n][k] != 0:
                displayText(surface, dark_info, str(sudoku[n][k]), cell_size * (k + 0.32), cell_size * (n + 0.17),
                            font_size_big, start=start)
                if start and first:
                    time.sleep(0.04)
            else:
                continue


def markCells(surface, number, sudoku, sudoku_start, empt, x_p, y_p, colo=(166, 255, 184)):
    if not empt:
        if number != 0:
            for n in range(9):
                for k in range(9):
                    if sudoku[n][k] == number or sudoku_start[n][k] == number:
                        x = cell_size * k + 1
                        y = cell_size * n + 1
                        width = cell_size - 1
                        height = cell_size - 1
                        if k % 3 == 0:
                            x += 1
                            width -= 1
                        if k % 3 == 2:
                            width -= 1
                        if n % 3 == 0:
                            y += 1
                            height -= 1
                        if n % 3 == 2:
                            height -= 1
                        pygame.draw.rect(surface, colo, (x, y, width, height))
    else:
        n = y_p // cell_size
        k = x_p // cell_size
        x_p = k * cell_size + 1
        y_p = n * cell_size + 1
        width = cell_size - 1
        height = cell_size - 1
        if k % 3 == 0:
            x_p += 1
            width -= 1
        if k % 3 == 2:
            width -= 1
        if n % 3 == 0:
            y_p += 1
            height -= 1
        if n % 3 == 2:
            height -= 1
        pygame.draw.rect(surface, colo, (x_p, y_p, width, height))


def insertNum(surface, num, current_s, current_s_s, r, c, dark_info):
    current_s[r][c] = num
    moves.append((r, c, num))
    redo.clear()
    surface.fill(color=bg_col)
    drawGrid(surface, dark_info)
    displaySudoku(win, dark_info, current_s_s, True)
    displaySudoku(win, dark_info, current_s, False)


pygame.font.init()


def markCellsLogic(x_p, y_p, empt):
    global saved_num, marked_num
    if not solved:
        if empt:
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
            if (current_sudoku[y_p // cell_size][x_p // cell_size] != 0) or empt:
                win.fill(color=bg_col)
                drawGrid(win, dark)
                marked_num = current_sudoku[y_p // cell_size][x_p // cell_size]
                if (marked_num != 0 and marked_num != saved_num) or empt:
                    markCells(win, marked_num, current_sudoku, current_sudoku_start, empt, x_p, y_p, colo=colo)
                    markCells(win, marked_num, current_sudoku, current_sudoku_start, empt, x_p, y_p, colo=colo)
                    saved_num = current_sudoku[y_p // cell_size][x_p // cell_size]
            elif (current_sudoku_start[y_p // cell_size][x_p // cell_size] != 0) or empt:
                win.fill(color=bg_col)
                drawGrid(win, dark)
                marked_num = current_sudoku_start[y_p // cell_size][x_p // cell_size]
                if (marked_num != 0 and marked_num != saved_num) or empt:
                    markCells(win, marked_num, current_sudoku, current_sudoku_start, empt, x_p, y_p, colo=colo)
                    markCells(win, marked_num, current_sudoku, current_sudoku_start, empt, x_p, y_p, colo=colo)
                    saved_num = current_sudoku_start[y_p // cell_size][x_p // cell_size]
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
    cell_size = 59
    font_size_very_small = math.floor(cell_size * 0.35)
    font_size_small = math.floor(cell_size * 0.50)
    font_size_default = math.floor(cell_size * (8 / 12))
    font_size_big = math.floor(cell_size * 0.80)
    first_loop = True
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((cell_size * 9, cell_size * 12))
    pygame.display.set_caption('Sudoku')
    ICON_SURFACE = pygame.image.load(getPath('sudoku_icon_2.png')).convert_alpha()
    pygame.display.set_icon(ICON_SURFACE)
    if dark:
        bg_col = 'black'
    else:
        bg_col = 'white'
    win.fill(color=bg_col)
    while playing:
        difficulty = 0
        global t_easy, t_medium, t_hard, t_very_hard, times
        if first_loop:
            t_easy = t_medium = t_hard = t_very_hard = time.gmtime(86399)
            times = {1: t_easy, 2: t_medium, 3: t_hard, 4: t_very_hard}
            first_loop = False
            with open(getPath('records.txt'), 'r') as file:
                lines = file.readlines()
                t_easy = time.gmtime(int(lines[0][:-1]))
                t_medium = time.gmtime(int(lines[1][:-1]))
                t_hard = time.gmtime(int(lines[2][:-1]))
                t_very_hard = time.gmtime(int(lines[3]))
        time_easy = time.strftime('%H:%M:%S', times[1])
        time_medium = time.strftime('%H:%M:%S', times[2])
        time_hard = time.strftime('%H:%M:%S', times[3])
        time_very_hard = time.strftime('%H:%M:%S', times[4])
        easy_rect, medium_rect, hard_rect, very_hard_rect, dark_rect, bright_rect = drawMenu(win, dark, time_easy,
                                                                                             time_medium, time_hard,
                                                                                             time_very_hard)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if easy_rect.collidepoint(mouse_pos):
                    difficulty = 1
                if medium_rect.collidepoint(mouse_pos):
                    difficulty = 2
                if hard_rect.collidepoint(mouse_pos):
                    difficulty = 3
                if very_hard_rect.collidepoint(mouse_pos):
                    difficulty = 4
                if dark_rect.collidepoint(mouse_pos):
                    dark = True
                    if dark:
                        bg_col = 'black'
                    else:
                        bg_col = 'white'
                    win.fill(color=bg_col)
                    easy_rect, medium_rect, hard_rect, very_hard_rect, dark_rect, bright_rect = drawMenu(win, dark,
                                                                                                         time_easy,
                                                                                                         time_medium,
                                                                                                         time_hard,
                                                                                                         time_very_hard)
                if bright_rect.collidepoint(mouse_pos):
                    dark = False
                    if dark:
                        bg_col = 'black'
                    else:
                        bg_col = 'white'
                    win.fill(color=bg_col)
                    easy_rect, medium_rect, hard_rect, very_hard_rect, dark_rect, bright_rect = drawMenu(win, dark,
                                                                                                         time_easy,
                                                                                                         time_medium,
                                                                                                         time_hard,
                                                                                                         time_very_hard)
            if event.type == pygame.QUIT:
                playing = False
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
        dt = 0
        play = True
        moves = []
        redo = []
        cheated = False
        marked_cell = (-1, -1)
        empty = False
        display_end_screen = True
        global start_time, solved, grid
        global num1, num2, num3, num4, num5, num6, num7, num8, num9
        global menu_rect, undo_rect, redo_rect, solution_rect, hint_rect, play_pause_rect
        if difficulty != 0:
            win.fill(color=bg_col)
        while difficulty != 0:
            if first:
                solved = False
                grid = True
                sudokus_list = sudoku_data.sudokus[difficulty]
                solutions_list = sudoku_data.solutions[difficulty]
                rand_num = random.randint(0, len(sudokus_list) - 1)
                current_sudoku_start = sudokus_list[rand_num].copy()
                current_sudoku = copy.deepcopy(blank_sudoku)
                current_solution = solutions_list[rand_num].copy()
                drawGrid(win, dark)
                displaySudoku(win, dark, current_sudoku_start, True)
                displaySudoku(win, dark, current_sudoku, False)
                first = False
                start_time = time.time()
            if not solved:
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
            if play and not first:
                dt += time.time() - start_time
                start_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
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
                        grid = False
                        display_end_screen = False
                        difficulty = 0
                        current_sudoku = copy.deepcopy(blank_sudoku)
                        current_sudoku_start = copy.deepcopy(blank_sudoku)
                        current_solution = copy.deepcopy(blank_sudoku)
                        win.fill(color=bg_col)
                    x_pos = mouse_pos[0]
                    y_pos = mouse_pos[1]
                    if undo_rect.collidepoint(mouse_pos):
                        if len(moves) != 0:
                            last_move = moves.pop(-1)
                            redo.append(last_move)
                            current_sudoku[last_move[0]][last_move[1]] = 0
                            win.fill(color=bg_col)
                            drawGrid(win, dark)
                            displaySudoku(win, dark, current_sudoku_start, True)
                            displaySudoku(win, dark, current_sudoku, False)
                    if redo_rect.collidepoint(mouse_pos):
                        if len(redo) != 0:
                            next_move = redo.pop(-1)
                            moves.append(next_move)
                            current_sudoku[next_move[0]][next_move[1]] = next_move[2]
                            win.fill(color=bg_col)
                            drawGrid(win, dark)
                            displaySudoku(win, dark, current_sudoku_start, True)
                            displaySudoku(win, dark, current_sudoku, False)
                    if 0 <= x_pos <= cell_size * 9 and 0 <= y_pos <= cell_size * 9:
                        if current_sudoku_start[y_pos // cell_size][x_pos // cell_size] == 0 and \
                                current_sudoku[y_pos // cell_size][x_pos // cell_size] == 0:
                            empty = True
                            marked_cell = (y_pos // cell_size, x_pos // cell_size)
                        else:
                            empty = False
                        markCellsLogic(x_pos, y_pos, empty)
                    row = marked_cell[0]
                    col = marked_cell[1]
                    if hint_rect.collidepoint(mouse_pos):
                        if empty:
                            solution_number = current_solution[row][col]
                            moves.append((row, col, solution_number))
                            current_sudoku[row][col] = solution_number
                            win.fill(color=bg_col)
                            drawGrid(win, dark)
                            displaySudoku(win, dark, current_sudoku_start, True)
                            displaySudoku(win, dark, current_sudoku, False)
                            cheated = True
                    if solution_rect.collidepoint(mouse_pos) and not solved:
                        for i in range(9):
                            for j in range(9):
                                if current_sudoku_start[i][j] == 0:
                                    current_sudoku[i][j] = current_solution[i][j]
                        cheated = True
                        solved = True
                        play = False
                        win.fill(color=bg_col)
                        drawGrid(win, dark)
                        displaySudoku(win, dark, current_sudoku_start, True)
                        displaySudoku(win, dark, current_sudoku, False)
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
                        markCellsLogic(col * cell_size, row * cell_size, False)
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
                            win.fill(color=bg_col)
                            drawGrid(win, dark)
                            displaySudoku(win, dark, current_sudoku_start, True)
                            displaySudoku(win, dark, current_sudoku, False)
                        elif play_pause == 'Pause':
                            play_pause = 'Play'
                            play = False
                            pygame.draw.rect(win, col, (
                                math.floor(cell_size * 7.5), math.floor(cell_size * 9.2), math.floor(cell_size * 2),
                                math.floor(cell_size * 0.75)))
                            pygame.draw.rect(win, bg_col, (0, 0, cell_size * 9, cell_size * 9 + 2))
            solved = True
            for i in range(9):
                for j in range(9):
                    if current_sudoku_start[i][j] == 0 and current_sudoku[i][j] != current_solution[i][j]:
                        solved = False
            if solved and display_end_screen:
                pygame.draw.rect(win, bg_col, (0, cell_size * 9, cell_size * 9, cell_size * 3))
                menu_rect = displayText(win, dark, 'Menu', cell_size * 7, cell_size * 11, font_size_default)
                play = False
                if cheated:
                    displayText(win, dark, 'This is the solution. Try again?', cell_size * 0.25, cell_size * 9.5,
                                font_size_small)
                    displayText(win, dark, ', but you used some help.', cell_size * 4.5, cell_size * 10.5,
                                font_size_very_small)
                else:
                    if time.gmtime(dt) < times[difficulty]:
                        displayText(win, dark, 'You\'ve broke the record!', cell_size * 4.5, cell_size * 10.5,
                                    font_size_very_small)
                        if difficulty == 1:
                            t_easy = time.gmtime(dt)
                        if difficulty == 2:
                            t_medium = time.gmtime(dt)
                        if difficulty == 3:
                            t_hard = time.gmtime(dt)
                        if difficulty == 4:
                            t_very_hard = time.gmtime(dt)
                        times = {1: t_easy, 2: t_medium, 3: t_hard, 4: t_very_hard}
                        with open(getPath('records.txt'),
                                  'w') as file:
                            file.write(
                                f'{calendar.timegm(times[1])}\n{calendar.timegm(times[2])}\n{calendar.timegm(times[3])}'
                                f'\n{calendar.timegm(times[4])}')
                    displayText(win, dark, 'Congrats, you solved the Sudoku!', cell_size * 0.25, cell_size * 9.5,
                                font_size_small)
                displayText(win, dark, f'Your time: {time.strftime("%H:%M:%S", time.gmtime(dt))}', cell_size * 0.25,
                            cell_size * 10.5,
                            font_size_small)
                display_end_screen = False

# IMPORTANT CHANGE: seperate file for functions
# BUG: anti virus detections shows alarm (after download)
# BUG: .exe failed to execute after download
# TODO: cleaner code: Display class & more
# TODO: deleting a number in a specific cell

            
