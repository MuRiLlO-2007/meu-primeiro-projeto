import random

class MineGame:
    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.visible = [['.' for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
        self._place_mines()
        self._count_neighbors()
        self.game_over = False
        self.win = False

    def _place_mines(self):
        positions = random.sample(range(self.rows * self.cols), self.mines)
        self.mine_locations = set()
        for pos in positions:
            r, c = divmod(pos, self.cols)
            self.board[r][c] = 'M'
            self.mine_locations.add((r, c))

    def _count_neighbors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'M':
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc] == 'M':
                                count += 1
                self.board[r][c] = str(count)

    def display(self):
        header = '   ' + ' '.join(f'{c:2}' for c in range(self.cols))
        print(header)
        for r in range(self.rows):
            row = f'{r:2} ' + ' '.join(self._cell_display(r, c) for c in range(self.cols))
            print(row)

    def _cell_display(self, r, c):
        if self.flags[r][c]:
            return 'F '
        return self.visible[r][c] + ' '

    def reveal(self, r, c):
        if self.flags[r][c] or self.visible[r][c] != '.':
            return
        if self.board[r][c] == 'M':
            self.game_over = True
            self._reveal_all_mines()
            return
        self._flood_fill(r, c)
        if self._check_win():
            self.win = True
            self.game_over = True

    def _reveal_all_mines(self):
        for (r, c) in self.mine_locations:
            self.visible[r][c] = 'M'

    def _flood_fill(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        if self.visible[r][c] != '.' or self.flags[r][c]:
            return
        self.visible[r][c] = self.board[r][c]
        if self.board[r][c] == '0':
            self.visible[r][c] = ' '
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr != 0 or dc != 0:
                        self._flood_fill(r + dr, c + dc)

    def flag(self, r, c):
        if self.visible[r][c] == '.' and not self.game_over:
            self.flags[r][c] = not self.flags[r][c]

    def _check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 'M' and self.visible[r][c] == '.':
                    return False
        return True


def read_command():
    try:
        command = input('Digite comando (r row col = revelar, f row col = marcar): ').strip().split()
    except EOFError:
        return None
    return command


def main():
    print('Bem-vindo ao Mine Game!')
    rows = 9
    cols = 9
    mines = 10
    game = MineGame(rows, cols, mines)
    while not game.game_over:
        game.display()
        command = read_command()
        if not command:
            break
        if len(command) != 3 or command[0] not in ('r', 'f'):
            print('Comando inválido. Use r row col ou f row col.')
            continue
        action, rs, cs = command
        if not (rs.isdigit() and cs.isdigit()):
            print('Linha e coluna devem ser números.')
            continue
        r, c = int(rs), int(cs)
        if not (0 <= r < rows and 0 <= c < cols):
            print('Coordenadas fora do intervalo.')
            continue
        if action == 'r':
            game.reveal(r, c)
        else:
            game.flag(r, c)
    game.display()
    if game.win:
        print('Parabéns! Você venceu!')
    elif game.game_over:
        print('Game over! Você pisou em uma mina.')
    else:
        print('Fim do jogo.')

if __name__ == '__main__':
    main()
