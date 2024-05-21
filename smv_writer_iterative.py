from smv_writer import SMVWriter, dictonary

class SMVWriterIterative(SMVWriter):
    def __init__(self, board_path=None, specs_path=None, board=None):
        super().__init__(board_path, specs_path, board)

        self.box_y, self.box_x = self.get_first_box()

    def add_var(self):
        super().add_var()

        self.content += f'\n\tbox_y: 0..{self.n - 1};'\
                        f'\n\tbox_x: 0..{self.m - 1};'

    def add_init(self):
        super().add_init()

        self.content += f'\n\tinit(box_y) := {self.box_y};'\
                        f'\n\tinit(box_x) := {self.box_x};'

    def add_transitions(self):
        super().add_transitions()

        self.content += f'\n\tnext(box_x) := case'\
                        f'\n\t\t(next(turn) = r) & (x = box_x - 1) & (y = box_y) & (box_x < m - 1) : box_x + 1;'\
                        f'\n\t\t(next(turn) = l) & (x = box_x + 1) & (y = box_y) & (box_x > 0) : box_x - 1;'\
                        f'\n\t\tTRUE : box_x;'\
                        f'\n\tesac;\n'

        self.content += f'\n\tnext(box_y) := case'\
                        f'\n\t\t(next(turn) = u) & (y = box_y + 1) & (x = box_x) & (box_y > 0) : box_y - 1;'\
                        f'\n\t\t(next(turn) = d) & (y = box_y - 1) & (x = box_x) & (box_y < n - 1) : box_y + 1;'\
                        f'\n\t\tTRUE : box_y;'\
                        f'\n\tesac;\n'

    def add_done(self):
        self.content += f'\n\tdone := '
        for i in range(self.n):
            for j in range(self.m):
                self.content += f'((box_x = {j}) & (box_y = {i}) & (v_{i}{j} = star))'
                if (i != self.n - 1) | (j != self.m - 1):
                    self.content += f' | '
                else:
                    self.content += ';\n'

    def get_first_box(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == '$':
                    return (i, j)
                    
        return (-1, -1)