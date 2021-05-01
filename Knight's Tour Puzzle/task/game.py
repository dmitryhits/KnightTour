# Write your code here
def get_board_size():
    message = 'Invalid dimensions!'
    while True:
        try:
            col, row = (int(x) for x in input("Enter your board dimensions:").split())
            if col > 0 and row > 0:
                return col, row
            else:
                print(message)
        except ValueError:
            print(message)


class Chess:
    def __init__(self):
        # first determine the size of the board which determines most of the display parameters
        self.cols, self.rows = get_board_size()
        # variable for displaying board
        self.cell_width = len(str(self.rows * self.cols))
        self.left_width = len(str(self.cols))
        self.cell = ' ' + '_' * self.cell_width
        self.knight_cell = " " * self.cell_width + 'X'
        self.move_cell = " " * self.cell_width + 'O'
        self.visited_cell = " " * self.cell_width + '*'
        self.left_cells = [f"{n:>{self.left_width}}|" for n in reversed(list(range(1, self.rows + 1)))]
        self.right_cells = [" |"]
        self.bottom_cells = [f" {n:>{self.cell_width}}" for n in range(1, self.cols + 1)]
        border_length = ((self.cell_width + 1) * self.cols + 3)
        self.border = "-" * border_length
        # initialize the containers
        self.current_moves = []
        self.visited_cells = {}
        self.moves = ((-2, -1), (-1, -2), (-2, 1), (1, -2), (-1, 2), (2, -1), (2, 1), (1, 2))
        self.steps = {}
        # initialize the control variable
        self.user_plays = False
        self.rewind = False
        self.no_solution = False
        self.start = True
        # initialize counters
        self.step_number = 0
        self.rewind_count = 0
        self.knight_position = self.get_knight_starting_position()
        self.board = self.reset_board()

    def number_cell(self, x):
        return f' {x:>{self.cell_width}}'

    def reset_board(self):
        """every cell is assigned empty cell view"""
        # print('board reset')
        return [[self.cell for _ in range(self.cols)] for _ in range(self.rows)]

    def get_knight_starting_position(self):
        message = 'Invalid position!'
        while True:
            try:
                col, row = (int(x) for x in input("Enter the knight's starting position:").split())
                if 1 <= col <= self.cols and 1 <= row <= self.rows:
                    # self.get_possible_moves(col, row)
                    self.visited_cells[self.step_number] = (col, row)
                    return col, row
                else:
                    print(message)
            except ValueError:
                print(message)

    def who_plays(self):
        while True:
            answer = input("Do you want to try the puzzle? (y/n):")
            if answer == 'y':
                self.user_plays = True
                break
            elif answer == 'n':
                self.user_plays = False
                self.start = False
                break
            else:
                print("invalid input")

    def solution_search(self):
        if self.rewind:
            self.rewind_count += 1
            self.step_number, current_step = self.steps.popitem()
            popped_item = self.visited_cells.popitem()
            self.rewind = False
        else:
            # First pass
            self.current_moves.clear()
            n_moves = self.get_possible_moves(*self.knight_position)
            current_step = {}
            if len(self.current_moves) > 0:
                for (col, row) in self.current_moves:
                    cell_score = self.get_possible_moves(col, row)
                    current_step[(col, row)] = cell_score
                # sort current step in order of decreasing cell_score, remove cells with a score 0
                if len(current_step) > 1:
                    current_step = {cell: current_step[cell]
                                    for cell in sorted(current_step, key=current_step.get, reverse=True)
                                    if current_step[cell] > 0}
            elif len(self.visited_cells) == self.rows * self.cols:
                self.no_solution = False
                return True
            elif self.steps:
                self.rewind = True
                self.solution_search()
            else:
                self.no_solution = True
                return 0

        if current_step:
            self.knight_position = current_step.popitem()[0]
            self.steps[self.step_number] = current_step
            self.step_number += 1
            self.visited_cells[self.step_number] = self.knight_position
            self.solution_search()

        elif len(self.visited_cells) == self.rows * self.cols:
            self.no_solution = False
            return True
        elif self.steps:
            self.rewind = True
            self.solution_search()
        else:
            self.no_solution = True
            return False

    def move_knight(self):
        message = 'Invalid move!'
        while True:
            try:
                col, row = (int(x) for x in input("Enter your next move:").split())
                if 1 <= col <= self.cols and 1 <= row <= self.rows \
                        and (col, row) not in self.visited_cells.values() \
                        and (col, row) != self.knight_position\
                        and (col, row) in self.current_moves:
                    self.visited_cells[self.step_number] = self.knight_position
                    self.knight_position = (col, row)
                    self.get_possible_moves(col, row)
                    self.step_number += 1
                    break
                else:
                    print(message, end=' ')
            except ValueError:
                print(message, end=' ')

    def mark_visited_cells(self):
        # print('visited', end=': ')
        for (col, row) in self.visited_cells.values():
            # print(f'[{col}:{row}]', end=' ')
            self.board[-row][col - 1] = self.visited_cell

    def mark_knight_position(self):
        col, row = self.knight_position
        # print(f'marking knight [{col}, {row}]')
        self.board[-row][col - 1] = self.knight_cell
        # print(self.board['rows'])

    def mark_number_cells(self):
        # print('current', self.current_moves)
        # print('marking number cells', end=': ')
        for (col, row) in self.current_moves:
            # print(f'[{col}:{row}]', end=' ')
            self.board[-row][col - 1] = self.number_cell(self.get_possible_moves(col, row))

    def mark_solution(self):
        # print(f'self.visited_cells: {self.visited_cells}')
        for step_number, cell in self.visited_cells.items():
            # print(f'step_number: {step_number},cell: {cell}')
            (col, row) = cell
            self.board[-row][col - 1] = self.number_cell(step_number + 1)

    def reset_visited(self):
        self.knight_position = self.visited_cells[0]
        self.visited_cells = {}

    def set_board(self):
        self.board = self.reset_board()
        if self.user_plays:
            self.mark_visited_cells()
            self.mark_knight_position()
            self.mark_number_cells()
        elif self.start:
            self.mark_knight_position()
        else:
            self.mark_solution()

    def get_possible_moves(self, col, row):
        current_col, current_row = self.knight_position
        current_moves = []
        # print('pos', current_moves)
        for i, j in self.moves:
            new_col = col + i
            new_row = row + j
            if 1 <= new_col <= self.cols and 1 <= new_row <= self.rows \
                    and (new_col != current_col or new_row != current_row) \
                    and (new_col, new_row) not in self.visited_cells.values():
                current_moves.append((new_col, new_row))

        if (col, row) == (current_col, current_row):
            self.current_moves = current_moves
            # print('current possible', self.current_moves)
        # print(col, row, current_moves)
        # print("Here are the possible moves:")
        return len(current_moves)

    def display_board(self):
        self.set_board()
        print(" " * self.left_width + self.border)
        for start, row in zip(self.left_cells, self.board):
            print(start + ''.join(row) + ' |')
        print(" " * self.left_width + self.border)
        print(" " * self.left_width + " " + "".join(self.bottom_cells))


# -------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000)
    board = Chess()
    #board.display_board()
    board.who_plays()
    if board.user_plays:
        board.solution_search()
        if not board.no_solution:
            board.reset_visited()
            board.get_possible_moves(*board.knight_position)
            board.start = False
            while True:
                board.display_board()
                board.move_knight()
                if board.get_possible_moves(*board.knight_position) == 0:
                    print("No more possible moves!")
                    print(f"Your knight visited {len(board.visited_cells) + 1} squares!")
                    if len(board.visited_cells) + 1 == board.rows * board.cols:
                        print("What a great tour! Congratulations!")
                    break
        else:
            print("No solution exists!")
    else:
        board.solution_search()
        if board.no_solution:
            print(board.visited_cells)
            print("No solution exists!")
        else:
            print("\nHere's the solution!")
            board.display_board()
