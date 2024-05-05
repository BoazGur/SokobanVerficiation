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
        self.n, self.m = len(self.board), len(self.board[0])
        self.__add_define()
        self.__add_var()
        self.__add_assign()
        self.__add_specs()

    def __add_specs(self):
        for spec in self.specs:
            self.content += f'\n{spec}'

    def __add_assign(self):
        self.content += f'\nASSIGN'

        for i in range(self.n):
            for j in range(self.m):
                self.content += f'\n\tinit(v_{i}{j}) := {dictonary.get(self.board[i][j])};'
        self.content += '\n'

        self.content += f'\n\tinit(possible_up) := '
        if self.y == 0:
            self.content += 'FALSE;'
        elif self.y == 1:
            self.content += f'!(v_{self.y-1}{self.x} = solamit);'
        else:
            self.content += f'!((v_{self.y-1}{self.x} = solamit) | (((v_{self.y-1}{self.x} = dollar) | (v_{self.y-1}{self.x} = dollar)) & ((v_{self.y-2}{self.x} = dollar) | (v_{self.y-2}{self.x} = dollar) | (v_{self.y-2}{self.x} = solamit))));'
        
        self.content += f'\n\tinit(possible_down) := '
        if self.y == self.n - 1:
            self.content += 'FALSE;'
        elif self.y == self.n - 2:
            self.content += f'!(v_{self.y+1}{self.x} = solamit);'
        else:
            self.content += f'!((v_{self.y+1}{self.x} = solamit) | (((v_{self.y+1}{self.x} = dollar) | (v_{self.y+1}{self.x} = dollar)) & ((v_{self.y+2}{self.x} = dollar) | (v_{self.y+2}{self.x} = dollar) | (v_{self.y+2}{self.x} = solamit))));'

        self.content += f'\n\tinit(possible_right) := '
        if self.x == self.m - 1:
            self.content += 'FALSE;'
        elif self.x == self.m - 2:
            self.content += f'!(v_{self.y}{self.x+1} = solamit);'
        else:
            self.content += f'!((v_{self.y}{self.x+1} = solamit) | (((v_{self.y}{self.x+1} = dollar) | (v_{self.y}{self.x+1} = dollar)) & ((v_{self.y}{self.x+2} = dollar) | (v_{self.y}{self.x+2} = dollar) | (v_{self.y}{self.x+2} = solamit))));'

        self.content += f'\n\tinit(possible_left) := '
        if self.x == 0:
            self.content += 'FALSE;'
        elif self.x == 1:
            self.content += f'!(v_{self.y}{self.x-1} = solamit);'
        else:
            self.content += f'!((v_{self.y}{self.x-1} = solamit) | (((v_{self.y}{self.x-1} = dollar) | (v_{self.y}{self.x-1} = dollar)) & ((v_{self.y}{self.x-2} = dollar) | (v_{self.y}{self.x-2} = dollar) | (v_{self.y}{self.x-2} = solamit))));'

        self.content += f'\n\tinit(turn) := none;'\
                        f'\n\tinit(x) := {self.x};'\
                        f'\n\tinit(y) := {self.y};\n'

        self.__add_transitions()

    def __add_transitions(self):
        self.__add_possible_transition()
        self.__add_turn_transition()
        self.__add_x_transition()
        self.__add_y_transition()
        self.__add_board_transition()

    def __add_board_transition(self):
        for i in range(self.n):
            for j in range(self.m):
                self.content += f'\n\tnext(v_{i}{j}) := case'\
                                f'\n\t\t(y = {i}) & (x = {j}) & (v_{i}{j} = shtrudel) & (next(turn) != none) : minus;'\
                                f'\n\t\t(y = {i}) & (x = {j}) & (v_{i}{j} = plus) & (next(turn) != none) : dot;'
                if j > 0:
                    self.content += f'\n\t\t(y = {i}) & (x = {j-1}) & ((v_{i}{j} = minus) | (v_{i}{j} = dollar)) & (next(turn) = r) : shtrudel;'\
                                    f'\n\t\t(y = {i}) & (x = {j-1}) & ((v_{i}{j} = dot) | (v_{i}{j} = star)) & (next(turn) = r) : plus;'
                if j > 1:
                    self.content += f'\n\t\t(y = {i}) & (x = {j-2}) & ((v_{i}{j-1} = star) | (v_{i}{j-1} = dollar)) & (v_{i}{j} = minus) & (next(turn) = r) : dollar;'\
                                    f'\n\t\t(y = {i}) & (x = {j-2}) & ((v_{i}{j-1} = star) | (v_{i}{j-1} = dollar)) & (v_{i}{j} = dot) & (next(turn) = r) : star;'
                if j < self.m - 1:
                    self.content += f'\n\t\t(y = {i}) & (x = {j+1}) & ((v_{i}{j} = minus) | (v_{i}{j} = dollar)) & (next(turn) = l) : shtrudel;'\
                                    f'\n\t\t(y = {i}) & (x = {j+1}) & ((v_{i}{j} = dot) | (v_{i}{j} = star)) & (next(turn) = l) : plus;'
                if j < self.m - 2:
                    self.content += f'\n\t\t(y = {i}) & (x = {j+2}) & ((v_{i}{j+1} = star) | (v_{i}{j+1} = dollar)) & (v_{i}{j} = minus) & (next(turn) = l) : dollar;'\
                                    f'\n\t\t(y = {i}) & (x = {j+2}) & ((v_{i}{j+1} = star) | (v_{i}{j+1} = dollar)) & (v_{i}{j} = dot) & (next(turn) = l) : star;'
                if i > 0:
                    self.content += f'\n\t\t(y = {i-1}) & (x = {j}) & ((v_{i}{j} = minus) | (v_{i}{j} = dollar)) & (next(turn) = d) : shtrudel;'\
                                    f'\n\t\t(y = {i-1}) & (x = {j}) & ((v_{i}{j} = dot) | (v_{i}{j} = star)) & (next(turn) = d) : plus;'
                if i > 1:
                    self.content += f'\n\t\t(y = {i-2}) & (x = {j}) & ((v_{i-1}{j} = star) | (v_{i-1}{j} = dollar)) & (v_{i}{j} = minus) & (next(turn) = d) : dollar;'\
                                    f'\n\t\t(y = {i-2}) & (x = {j}) & ((v_{i-1}{j} = star) | (v_{i-1}{j} = dollar)) & (v_{i}{j} = dot) & (next(turn) = d) : star;'
                if i < self.n - 1:
                    self.content += f'\n\t\t(y = {i+1}) & (x = {j}) & ((v_{i}{j} = minus) | (v_{i}{j} = dollar)) & (next(turn) = u) : shtrudel;'\
                                    f'\n\t\t(y = {i+1}) & (x = {j}) & ((v_{i}{j} = dot) | (v_{i}{j} = star)) & (next(turn) = u) : plus;'
                if i < self.n - 2:
                    self.content += f'\n\t\t(y = {i+2}) & (x = {j}) & ((v_{i+1}{j} = star) | (v_{i+1}{j} = dollar)) & (v_{i}{j} = minus) & (next(turn) = u) : dollar;'\
                                    f'\n\t\t(y = {i+2}) & (x = {j}) & ((v_{i+1}{j} = star) | (v_{i+1}{j} = dollar)) & (v_{i}{j} = dot) & (next(turn) = u) : star;'

                self.content += f'\n\t\tTRUE : v_{i}{j};'\
                                f'\n\tesac;\n'

    def __add_x_transition(self):
        self.content += f'\n\tnext(x) := case'\
                        f'\n\t\t(next(turn) = r) & (x < m - 1) : x + 1;'\
                        f'\n\t\t(next(turn) = l) & (x > 0) : x - 1;'\
                        f'\n\t\tTRUE : x;'\
                        f'\n\tesac;\n'

    def __add_y_transition(self):
        self.content += f'\n\tnext(y) := case'\
                        f'\n\t\t(next(turn) = d) & (y < n - 1) : y + 1;'\
                        f'\n\t\t(next(turn) = u) & (y > 0) : y - 1;'\
                        f'\n\t\tTRUE : y;'\
                        f'\n\tesac;\n'

    def __add_turn_transition(self):
        self.content += f'\n\tnext(turn) := case'\
                        f'\n\t\tdone : none;'

        turns = ['u', 'd', 'r', 'l']
        for i in range(4, 0, -1):
            for combination in list(combinations(turns, i)):
                flag = False
                if 'u' in combination:
                    self.content += f'\n\t\tnext(possible_up) '
                    flag = True
                
                if 'd' in combination:
                    if flag:
                        self.content += f'& '
                    else:
                        self.content += f'\n\t\t'
                    
                    flag = True
                    self.content += f'next(possible_down) '
                
                if 'r' in combination:
                    if flag:
                        self.content += f'& '
                    else:
                        self.content += f'\n\t\t'

                    flag = True
                    self.content += f'next(possible_right) '
                
                if 'l' in combination:
                    if flag:
                        self.content += f'& '
                    else:
                        self.content += f'\n\t\t'

                    flag = True
                    self.content += f'next(possible_left) '

                self.content += ': {' + ', '.join(combination) + ', none};'
        
        self.content += f'\n\t\tTRUE : none;'

        self.content += f'\n\tesac;\n'
    
    def __add_possible_transition(self):
        self.content += f'\n\tnext(possible_up) := case'
        for i in range(self.n):
            for j in range(self.m):
                if i == 0:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : FALSE;'
                elif i == 1:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : !((v_{i-1}{j} = solamit));'
                else:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : !((v_{i-1}{j} = solamit) | (((v_{i-1}{j} = dollar) | (v_{i-1}{j} = star)) & ((v_{i-2}{j} = dollar) | (v_{i-2}{j} = star) | (v_{i-2}{j} = solamit))));'
        self.content += f'\n\t\tTRUE : FALSE;'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(possible_down) := case'     
        for i in range(self.n):
            for j in range(self.m):
                if i == self.n - 1:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : FALSE;'
                elif i == self.n - 2:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : !((v_{i+1}{j} = solamit));'
                else:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : !((v_{i+1}{j} = solamit) | (((v_{i+1}{j} = dollar) | (v_{i+1}{j} = star)) & ((v_{i+2}{j} = dollar) | (v_{i+2}{j} = star) | (v_{i+2}{j} = solamit))));'
        self.content += f'\n\t\tTRUE : FALSE;'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(possible_right) := case'
        for i in range(self.n):
            for j in range(self.m):
                if j == self.m - 1:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : FALSE;'
                elif j == self.m - 2:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : !((v_{i}{j+1} = solamit));'
                else:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : !((v_{i}{j+1} = solamit) | (((v_{i}{j+1} = dollar) | (v_{i}{j+1} = star)) & ((v_{i}{j+2} = dollar) | (v_{i}{j+2} = star) | (v_{i}{j+2} = solamit))));'
        self.content += f'\n\t\tTRUE : FALSE;'\
                        f'\n\tesac;\n'
        
        self.content += f'\n\tnext(possible_left) := case'
        for i in range(self.n):
            for j in range(self.m):
                if j == 0:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : FALSE;'
                elif j == 1:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : !((v_{i}{j-1} = solamit));'
                else:
                    self.content += f'\n\t\t(y = {i}) & (x = {j}) : !((v_{i}{j-1} = solamit) | (((v_{i}{j-1} = dollar) | (v_{i}{j-1} = star)) & ((v_{i}{j-2} = dollar) | (v_{i}{j-2} = star) | (v_{i}{j-2} = solamit))));'
        self.content += f'\n\t\tTRUE : FALSE;'\
                        f'\n\tesac;\n'
        
    def __add_var(self):
        self.content += f'\nVAR'\
                        f'\n\tturn: {{u, d, r, l, none}};'\
                        f'\n\tpossible_up: boolean;'\
                        f'\n\tpossible_down: boolean;'\
                        f'\n\tpossible_right: boolean;'\
                        f'\n\tpossible_left: boolean;'
        self.content += '\n\ty: {'
        for i in range(self.n):
            if i:
                self.content += f', {i}'
            else:
                self.content += f'{i}'
        self.content += '};'
        self.content += '\n\tx: {'
        for i in range(self.m):
            if i:
                self.content += f', {i}'
            else:
                self.content += f'{i}'
        self.content += '};'
        
        for i in range(self.n):
            for j in range(self.m):
                self.content += f'\n\tv_{i}{j}: {{shtrudel, plus, dollar, star, solamit, dot, minus}};'
        self.content += '\n'

    def __add_define(self):
        self.content += f'\nDEFINE'\
                        f'\n\tn := {self.n}; m := {self.m};'

        self.content += f'\n\tdone :='
        for i in range(self.n):
            for j in range(self.m):
                self.content += f' (v_{i}{j} != dollar)'
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