from cell import Cell
import random
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)

        self._create_cells()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)

        last_col = self._num_cols - 1
        last_row = self._num_rows - 1
        self._cells[last_col][last_row].has_bottom_wall = False
        self._draw_cell(last_col,last_row)

    def _knock_between(self, c1i, c1j, c2i, c2j):
        if (abs(c1i - c2i) > 1 and abs(c1j - c2j) > 1) or (c1i == c2i and c1j == c2j):
            return
        
        if c1i != c2i:
            if c1i < c2i:
                self._cells[c1i][c1j].has_right_wall = False
                self._cells[c2i][c2j].has_left_wall = False
            else:
                self._cells[c1i][c1j].has_left_wall = False
                self._cells[c2i][c2j].has_right_wall = False
            self._draw_cell(c1i,c1j)
            self._draw_cell(c2i,c2j)
        if c1j != c2j:
            if c1j < c2j:
                self._cells[c1i][c1j].has_bottom_wall = False
                self._cells[c2i][c2j].has_top_wall = False
            else:
                self._cells[c1i][c1j].has_top_wall = False
                self._cells[c2i][c2j].has_bottom_wall = False
            
            self._draw_cell(c1i,c1j)
            self._draw_cell(c2i,c2j)


    def _break_walls_r(self, i=0, j=0):
        self._cells[i][j]._visited = True
        while True:
            dirs = []
            if j > 0 and self._cells[i][j-1]._visited == False:
                dirs.append([i, j-1])
            if j < len(self._cells[i])-1 and self._cells[i][j+1]._visited == False:
                dirs.append([i, j+1])
            if i > 0 and self._cells[i-1][j]._visited == False:
                dirs.append([i-1, j])
            if i < len(self._cells)-1 and self._cells[i+1][j]._visited == False:
                dirs.append([i+1, j])
            
            if len(dirs) == 0:
                return

            dir = random.randint(0, len(dirs)-1)
            self._knock_between(i, j, dirs[dir][0], dirs[dir][1])
            self._break_walls_r(dirs[dir][0], dirs[dir][1])

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j]._visited = False
                

    def _solve(self):
        return self._solve_r()
    
    def _solve_r(self, i=0, j=0):
        self._animate()
        self._cells[i][j]._visited = True
        if i == self._num_cols -1 and j == self._num_rows -1:
            return True
        dirs = []
        if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j-1]._visited:
            dirs.append([i, j-1])
        if j < len(self._cells[i])-1 and not self._cells[i][j].has_bottom_wall and self._cells[i][j+1]._visited == False:
            dirs.append([i, j+1])
        if i > 0 and not self._cells[i][j].has_left_wall and self._cells[i-1][j]._visited == False:
            dirs.append([i-1, j])
        if i < len(self._cells)-1 and not self._cells[i][j].has_right_wall and self._cells[i+1][j]._visited == False:
            dirs.append([i+1, j])

        for dir in dirs:
            self._cells[i][j].draw_move(self._cells[dir[0]][dir[1]])
            found = self._solve_r(dir[0], dir[1])
            if found:
                return True
            self._cells[i][j].draw_move(self._cells[dir[0]][dir[1]], undo=True)
        return False





    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.02)