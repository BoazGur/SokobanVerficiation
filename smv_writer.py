from itertools import combinations

dictonary = {
    "@": "shtrudel",
    "+": "plus",
    "$": "dollar",
    "*": "star",
    "#": "solamit",
    ".": "dot",
    "-": "minus"
}

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
        self.__add_specs()

    def __add_specs(self):
        for spec in self.specs:
            self.content += f'\n{spec}'

    def __add_assign(self):
        self.content += f'\nASSIGN'\
                        f'\n\tinit(turn) := none;'\
                        f'\n\tinit(x) := {self.x};'\
                        f'\n\tinit(y) := {self.y};\n'

        for i in range(self.n):
            for j in range(self.m):
                self.content += f'\n\tinit(board[{i * self.m + j}]) := {dictonary.get(self.board[i][j])};'

        self.content += '\n'

        self.__add_transitions()

    def __add_transitions(self):
        self.__add_turn_transition()
        self.__add_x_transition()
        self.__add_y_transition()
        self.__add_board_transition()

    def __add_board_transition(self):
        self.content += f'\n\tnext(board[y*m + x]) := case'\
                        f'\n\t\t(board[y*m + x] = shtrudel) & (next(turn) != none) : minus;'\
                        f'\n\t\t(board[y*m + x] = plus) & (next(turn) != none) : dot;'\
                        f'\n\t\tTRUE : board[y*m + x];'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(board[y][x + 1]) := case'\
                        f'\n\t\t((board[y][x + 1] = minus) | (board[y][x + 1] = dollar)) & (next(turn) = r) : shtrudel;'\
                        f'\n\t\t((board[y][x + 1] = dot) | (board[y][x + 1] = star)) & (next(turn) = r) : plus;'\
                        f'\n\t\tTRUE : board[y][x + 1];'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(board[y][x + 2]) := case'\
                        f'\n\t\t((board[y][x + 1] = star) | (board[y][x + 1] = dollar)) & (board[y][x + 2] = minus) & (next(turn) = r) : dollar;'\
                        f'\n\t\t((board[y][x + 1] = star) | (board[y][x + 1] = dollar)) & (board[y][x + 2] = dot) & (next(turn) = r) : star;'\
                        f'\n\t\tTRUE : board[y][x + 2];'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(board[y][x - 1]) := case'\
                        f'\n\t\t((board[y][x - 1] = minus) | (board[y][x - 1] = dollar)) & (next(turn) = l) : shtrudel;'\
                        f'\n\t\t((board[y][x - 1] = dot) | (board[y][x - 1] = star)) & (next(turn) = l) : plus;'\
                        f'\n\t\tTRUE : board[y][x - 1];'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(board[y][x - 2]) := case'\
                        f'\n\t\t((board[y][x - 1] = star) | (board[y][x - 1] = dollar)) & (board[y][x - 2] = minus) & (next(turn) = l) : dollar;'\
                        f'\n\t\t((board[y][x - 1] = star) | (board[y][x - 1] = dollar)) & (board[y][x - 2] = dot) & (next(turn) = l) : star;'\
                        f'\n\t\tTRUE : board[y][x - 2];'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(board[y + 1][x]) := case'\
                        f'\n\t\t((board[y + 1][x] = minus) | (board[y + 1][x] = dollar)) & (next(turn) = d) : shtrudel;'\
                        f'\n\t\t((board[y + 1][x] = dot) | (board[y + 1][x] = star)) & (next(turn) = d) : plus;'\
                        f'\n\t\tTRUE : board[y + 1][x];'\
                        f'\n\tesac;\n'

        self.content += f'\n\tnext(board[y + 2][x]) := case'\
                        f'\n\t\t((board[y + 1][x] = star) | (board[y + 1][x] = dollar)) & (board[y + 2][x] = minus) & (next(turn) = d) : dollar;'\
                        f'\n\t\t((board[y + 1][x] = star) | (board[y + 1][x] = dollar)) & (board[y + 2][x] = dot) & (next(turn) = d) : star;'\
                        f'\n\t\tTRUE : board[y + 2][x];'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(board[y - 1][x]) := case'\
                        f'\n\t\t((board[y - 1][x] = minus) | (board[y - 1][x] = dollar)) & (next(turn) = u) : shtrudel;'\
                        f'\n\t\t((board[y - 1][x] = dot) | (board[y - 1][x] = star)) & (next(turn) = u) : plus;'\
                        f'\n\t\tTRUE : board[y - 1][x];'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(board[y - 2][x]) := case'\
                        f'\n\t\t((board[y - 1][x] = star) | (board[y - 1][x] = dollar)) & (board[y - 2][x] = minus) & (next(turn) = u) : dollar;'\
                        f'\n\t\t((board[y - 1][x] = star) | (board[y - 1][x] = dollar)) & (board[y - 2][x] = dot) & (next(turn) = u) : star;'\
                        f'\n\t\tTRUE : board[y - 2][x];'\
                        f'\n\tesac;\n'

    def __add_x_transition(self):
        self.content += f'\n\tnext(x) := case'\
                        f'\n\t\t(next(turn) = r) : x + 1;'\
                        f'\n\t\t(next(turn) = l) : x - 1;'\
                        f'\n\t\tTRUE : x;'\
                        f'\n\tesac;\n'

    def __add_y_transition(self):
        self.content += f'\n\tnext(y) := case'\
                        f'\n\t\t(next(turn) = d) : y + 1;'\
                        f'\n\t\t(next(turn) = u) : y - 1;'\
                        f'\n\t\tTRUE : y;'\
                        f'\n\tesac;\n'

    def __add_turn_transition(self):
        self.content += f'\n\tnext(turn) := case'

        turns = ['u', 'd', 'r', 'l']
        for i in range(4, 0, -1):
            for combination in list(combinations(turns, i)):
                flag = False
                if 'u' in combination:
                    self.content += f'\n\t\t(possible_up) '
                    flag = True
                
                if 'd' in combination:
                    if flag:
                        self.content += f'& '
                    else:
                        self.content += f'\n\t\t'
                    
                    flag = True
                    self.content += f'(possible_down) '
                
                if 'r' in combination:
                    if flag:
                        self.content += f'& '
                    else:
                        self.content += f'\n\t\t'

                    flag = True
                    self.content += f'(possible_right) '
                
                if 'l' in combination:
                    if flag:
                        self.content += f'& '
                    else:
                        self.content += f'\n\t\t'

                    flag = True
                    self.content += f'(possible_left) '

                self.content += ': {' + ', '.join(combination) + '};'
        
        self.content += f'\n\t\tTRUE : none;'

        self.content += f'\n\tesac;\n'

    def __add_var(self):
        self.content += f'\nVAR'\
                        f'\n\tboard: array 0..{self.n * self.m - 1} of {{shtrudel, plus, dollar, star, solamit, dot, minus}};'\
                        f'\n\tturn: {{u, d, r, l, none}};'\
                        f'\n\tx: integer;'\
                        f'\n\ty: integer;\n'

    def __add_define(self):
        self.content += f'\nDEFINE n := {self.n}; m := {self.m};'\
                        f'\n\tpossible_up := !((y = 0) | (board[(y - 1)*m + x] = solamit) | (((board[(y - 1)*m + x] = dollar) | (board[(y - 1)*m + x] = dollar)) & ((board[(y - 2)*m + x] = dollar) | (board[(y - 2)*m + x] = dollar) | (board[(y - 2)*m + x] = solamit))));'\
                        f'\n\tpossible_down := !((y = n - 1) | (board[(y + 1)*m + x] = solamit) | (((board[(y + 1)*m + x] = dollar) | (board[(y + 1)*m + x] = dollar)) & ((board[(y + 2)*m + x] = dollar) | (board[(y + 2)*m + x] = dollar) | (board[(y + 2)*m + x] = solamit))));'\
                        f'\n\tpossible_right := !((x = m - 1) | (board[y*m + x + 1] = solamit) | (((board[y*m + x + 1] = dollar) | (board[y*m + x + 1] = dollar)) & ((board[y*m + x + 2] = dollar) | (board[y*m + x + 2] = dollar) | (board[y*m + x + 2] = solamit))));'\
                        f'\n\tpossible_left := !((x = 0) | (board[y*m + x - 1] = solamit) | (((board[y*m + x - 1] = dollar) | (board[y*m + x - 1] = dollar)) & ((board[y*m + x - 2] = dollar) | (board[y*m + x - 2] = dollar) | (board[y*m + x - 2] = solamit))));\n'\

        self.content += f'\n\tdone :='
        for i in range(self.n):
            for j in range(self.m):
                self.content += f' (board[{i*self.m + j}] != dollar)'
                if (i != self.n - 1) | (j != self.m - 1):
                    self.content += f' &'
                else:
                    self.content += ';\n'
    
    def __get_coords(self):
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if col in ["@", "+"]:
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
                if line[-1] == "\n":
                    line = line[:-1]
                row = list(line)
                board.append(row)

        return board


def main():
    writer = SMVWriter('boards\\boardEx.txt', 'specs.txt')
    # writer.add_turn_transition()
    writer.write_smv()
    writer.export_smv('sokoban.smv')


if __name__ == '__main__':
    main()