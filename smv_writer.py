from itertools import combinations

class SMVWriter:
    def __init__(self, board_path, specs_path):
        self.board = self.__get_board(board_path)
        self.specs = self.__get_specs(specs_path)

        self.x, self.y = -1, -1
        self.n, self.m = -1, -1

        self.content = ''

    def export_smv(self, path):
        with open(path, 'w') as f:
            f.write(self.content)

    def write_smv(self):
        self.content += 'MODULE main\n'

        self.x, self.y = self.__get_coords()
        self.n, self.m = len(self.board), len(self.board[0]) - 1
        self.__add_define()
        self.__add_var()
        self.__add_assign()

    def __add_assign(self):
        self.content += f'\nASSIGN'\
                        f'\n\tinit(turn) := none;'\
                        f'\n\tinit(x) := {self.x};'\
                        f'\n\tinit(y) := {self.y};\n'

        for i in range(self.n):
            for j in range(self.m):
                self.content += f'\n\tinit(board[{i}][{j}]) := {self.board[i][j]};'

        self.content += '\n'

        self.__add_transitions()

    def __add_transitions(self):
        self.content += f'\n\tnext(turn) := case'

        turns = ['up', 'down', 'right', 'left']
        for i in range(1, 5):
            for combination in list(combinations(turns, i)):
                print(combination) # TODO: ADD ALL COMBINATIONS TO ADD TURN TRANSITION

    def __add_var(self):
        self.content += f'\nVAR'\
                        f'\n\tboard: array 0..{self.n - 1} of array 0..{self.m - 1} of {{@, +, $, *, #, ., _}};'\
                        f'\n\tturn: {{u, d, r, l, none}};'\
                        f'\n\tx: int;'\
                        f'\n\ty: int;\n'

    def __add_define(self):
        self.content += f'\nDEFINE n := {self.n}; m := {self.m};'\
                        f'\n\tpossible_up := !((y = 0) or (board[y-1][x] = #) or (((board[y-1][x] = $) or (board[y-1][x] = $)) and ((board[y-2][x] = $) or (board[y-2][x] = $) or (board[y-2][x] = #))));'\
                        f'\n\tpossible_down := !((y = n-1) or (board[y+1][x] = #) or (((board[y+1][x] = $) or (board[y+1][x] = $)) and ((board[y+2][x] = $) or (board[y+2][x] = $) or (board[y+2][x] = #))));'\
                        f'\n\tpossible_right := !((x = m-1) or (board[y][x+1] = #) or (((board[y][x+1] = $) or (board[y][x+1] = $)) and ((board[y][x+2] = $) or (board[y][x+2] = $) or (board[y][x+2] = #))));'\
                        f'\n\tpossible_left := !((x = 0) or (board[y][x-1] = #) or (((board[y][x-1] = $) or (board[y][x-1] = $)) and ((board[y][x-2] = $) or (board[y][x-2] = $) or (board[y][x-2] = #))));\n'\


    def __get_coords(self):
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if col in ['@', '+']:
                    return (x, y)

        return (-1, -1)

    def __get_specs(self, path):
        with open(path, 'r') as f:
            specs = f.readlines()

        return specs

    def __get_board(self, path):
        board = []
        with open(path, 'r') as f:
            for line in f.readlines():
                row = list(line)
                board.append(row)

        return board


def main():
    writer = SMVWriter('board.txt', 'specs.txt')
    writer.write_smv()
    writer.export_smv('sokoban.smv')


if __name__ == '__main__':
    main()
