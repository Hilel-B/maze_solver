import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    def test_maze_create_cells_neg_size(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(100, 100, num_rows, num_cols, -10, -10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    def test_maze_create_cells_zero_vals(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 0, 0)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_entrance_and_exit(self):
        num_cols = 5
        num_rows = 7
        m1 = Maze(100, 100, num_rows, num_cols, 50, 50)
        m1._break_entrance_and_exit()
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False
        )
        self.assertEqual(
            m1._cells[4][6].has_bottom_wall,
            False
        )
        

    def test_maze_entrance_is_exit(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(100, 100, num_rows, num_cols, 50, 50)
        m1._break_entrance_and_exit()
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False
        )
        self.assertEqual(
            m1._cells[0][0].has_bottom_wall,
            False
        )

    def test_visited_after_break(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(100, 100, num_rows, num_cols, 50, 50)
        m1._break_entrance_and_exit()
        for i in range(len(m1._cells)):
            for j in range(len(m1._cells[i])):
                self.assertEqual(
                m1._cells[i][j]._visited,
                False
                )
    

if __name__ == "__main__":
    unittest.main()