import pytest

class tictac:
    def __init__(self):
        self.board = [[None] * 3 for i in range(3)]

    def get_board(self):
        return self.board

    def place_X(self, row, col):
        if not self.board[row][col]:
            self.board[row][col] = 'X'
        else:
            raise Exception('this square already contains a value')

    def place_O(self, row, col):
        if not self.board[row][col]:
            self.board[row][col] = 'O'
        else:
            raise Exception('this square already contains a value')

    def check_win(self):
        # check rows and cols
        for i in range(3):
            check_cell = self.board[i][i]
            # check for none
            if not check_cell:
                continue

            if len(set(self.board[i])) == 1:
                return check_cell

            if len(set([row[i] for row in self.board])) == 1:
                return check_cell

        left_diag = [self.board[i][i] for i in range(3)]
        right_diag = [self.board[2-i][i] for i in range(3)]

        if len(set(left_diag)) == 1 or len(set(right_diag)) == 1:
            return self.board[1][1]

        return None

check_cells = [0, 1, 2]
@pytest.mark.parametrize('check_cell', check_cells)
def test_horizontal_win(check_cell):
    board_X = tictac()
    board_O = tictac()
    for col in range(3):
        board_X.place_X(check_cell, col)
        board_O.place_O(check_cell, col)
        # no win
        if col != 2:
            assert board_X.check_win() == None
            assert board_O.check_win() == None
    assert board_X.check_win() == 'X'
    assert board_O.check_win() == 'O'

@pytest.mark.parametrize('check_cell', check_cells)
def test_vertical_win(check_cell):
    board_X = tictac()
    board_O = tictac()
    for row in range(3):
        board_X.place_X(row, check_cell)
        board_O.place_O(row, check_cell)
        # no win
        if row != 2:
            assert board_X.check_win() == None
            assert board_O.check_win() == None
    assert board_X.check_win() == 'X'
    assert board_O.check_win() == 'O'

def test_diagonal_win():
    # left diagonal
    board_X = tictac()
    board_O = tictac()
    for cell in range(3):
        board_X.place_X(cell, cell)
        board_O.place_O(cell, cell)
        # no win
        if cell != 2:
            assert board_X.check_win() == None
            assert board_O.check_win() == None
    assert board_X.check_win() == 'X'
    assert board_O.check_win() == 'O'

    # right diagonal
    board_X = tictac()
    board_O = tictac()
    for cell in range(3):
        board_X.place_X(cell, 2-cell)
        board_O.place_O(cell, 2-cell)
        # no win
        if cell != 2:
            assert board_X.check_win() == None
            assert board_O.check_win() == None
    assert board_X.check_win() == 'X'
    assert board_O.check_win() == 'O'

def test_exception():
    board_X = tictac()
    board_O = tictac()
    for i in range(3):
        for j in range(3):
            board_X.place_X(i, j)
            board_O.place_O(i, j)

            with pytest.raises(Exception) as e_X:
                board_X.place_X(i, j)
            assert str(e_X.value) == 'this square already contains a value'

            with pytest.raises(Exception) as e_O:
                board_O.place_O(i, j)
            assert str(e_O.value) == 'this square already contains a value'

def test_empty():
    board = tictac()
    board_view = board.get_board()
    for row in board_view:
        assert row == [None, None, None]
    assert board.check_win() == None