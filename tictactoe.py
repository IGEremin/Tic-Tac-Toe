from random import randint


class Player:
    def __init__(self, mark, opp_mark):
        self.mark = mark
        self.opp_mark = opp_mark


class User(Player):
    def move(self, field):
        coord = self.coordinates(field)
        field[coord[0]][coord[1]] = self.mark
        return field

    def coordinates(self, field):
        coord = input("Enter the coordinates: ").split()
        if not coord[0].isnumeric() or not coord[1].isnumeric():
            print("You should enter numbers!")
            return self.coordinates(field)

        coord = [int(n) - 1 for n in coord]

        if coord[0] > 2 or coord[1] > 2:
            print("Coordinates should be from 1 to 3!")
            return self.coordinates(field)

        elif field[coord[0]][coord[1]] in Game.mark:
            print("This cell is occupied! Choose another one!")
            return self.coordinates(field)
        return coord


class Robot(Player):
    def move(self, field):
        print(f'Making move level "{self.__class__.__name__.lower()}"')
        coord = self.coordinates(field)
        field[coord[0]][coord[1]] = self.mark
        return field

    def random_coord(self, field):
        coord = [randint(0, 2), randint(0, 2)]
        if field[coord[0]][coord[1]] in Game.mark:
            return self.random_coord(field)
        return coord


class Easy(Robot):
    def coordinates(self, field):
        return self.random_coord(field)


class Medium(Robot):
    def coordinates(self, field):
        coord = self.two_row_check(field)
        if not coord:
            coord = self.random_coord(field)
        return coord

    def two_row_check(self, field):
        transposed_field = [[field[m][n] for m in range(len(field))] for n in range(len(field[0]))]

        if Game.mark[0] == self.mark:
            mark_list = Game.mark
        else:
            mark_list = Game.mark.copy()
            mark_list.reverse()

        for mark in mark_list:
            for n, column in enumerate(field):  # Checking column of field for 2-in-row
                if column.count(mark) == 2 and column.count('_'):
                    return [n, column.index('_')]
            for m, row in enumerate(transposed_field):  # Checking row of field for 2-in-row
                if row.count(mark) == 2 and row.count('_'):
                    return [row.index('_'), m]

            # Checking main diagonal of field for 2-in-row
            main_diagonal = [field[n][abs(n - 2)] for n in range(len(field))]
            if main_diagonal.count(mark) == 2 and main_diagonal.count('_'):
                return [main_diagonal.index('_'), abs(main_diagonal.index('_') - 2)]

            # Checking side diagonal of field for 2-in-row
            side_diagonal = [field[n][n] for n in range(len(field))]
            if side_diagonal.count(mark) == 2 and side_diagonal.count('_'):
                return [side_diagonal.index('_'), side_diagonal.index('_')]
        return None


class Hard(Robot):
    def coordinates(self, field):
        (m, col, row) = self.maximum(field, -2, 2)
        coord = [col, row]
        return coord

    def maximum(self, field, alpha, beta):
        max_value = -2
        p_row = None
        p_col = None

        result = Game.checker(field)

        if result == self.mark:
            return 1, 0, 0
        elif result == self.opp_mark:
            return -1, 0, 0
        elif result == "Draw":
            return 0, 0, 0

        for col in range(len(field)):
            for row in range(len(field[0])):
                if field[col][row] == '_':
                    field[col][row] = self.mark
                    (m, min_col, min_row) = self.minimum(field, alpha, beta)
                    if m > max_value:
                        max_value = m
                        p_col = col
                        p_row = row
                    field[col][row] = '_'

                    if max_value >= beta:
                        return max_value, p_col, p_row
                    if max_value > alpha:
                        alpha = max_value

        return max_value, p_col, p_row

    def minimum(self, field, alpha, beta):
        min_value = 2
        q_row = None
        q_col = None

        result = Game.checker(field)

        if result == self.mark:
            return 1, 0, 0
        elif result == self.opp_mark:
            return -1, 0, 0
        elif result == "Draw":
            return 0, 0, 0

        for col in range(len(field)):
            for row in range(len(field[0])):
                if field[col][row] == '_':
                    field[col][row] = self.opp_mark
                    (m, max_col, max_row) = self.maximum(field, alpha, beta)
                    if m < min_value:
                        min_value = m
                        q_col = col
                        q_row = row
                    field[col][row] = '_'

                    if min_value <= alpha:
                        return min_value, q_col, q_row
                    if min_value < beta:
                        beta = min_value

        return min_value, q_col, q_row


class Game:
    command = {'user': User, 'easy': Easy, 'medium': Medium, 'hard': Hard, 'start': None, 'exit': exit}
    mark = ['X', 'O']

    def __init__(self):
        self.field = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
        self.start()
        print(self)
        self.process()

    def __str__(self):
        result = f"---------\n" \
                 f"| {self.field[0][2]} {self.field[1][2]} {self.field[2][2]} |\n" \
                 f"| {self.field[0][1]} {self.field[1][1]} {self.field[2][1]} |\n" \
                 f"| {self.field[0][0]} {self.field[1][0]} {self.field[2][0]} |\n" \
                 f"---------"
        return result

    def start(self):
        user_command = input("Input command: ").split()
        if user_command[0] == 'exit' and len(user_command) == 1:
            exit()
        elif user_command[0] == 'start' and len(user_command) == 3:
            if user_command[1] in Game.command and user_command[2] in Game.command:
                self.first = Game.command[user_command[1]]('X', 'O')
                self.second = Game.command[user_command[2]]('O', 'X')
        else:
            print("Bad parameters!")
            self.start()

    def process(self):
        while True:
            for player in [self.first, self.second]:
                self.field = player.move(self.field)
                print(self)
                result = self.checker(self.field)
                if result:
                    if result == "Draw":
                        print("Draw\n")
                    else:
                        print(result, 'wins\n')
                    return

    @staticmethod
    def checker(field):
        result = ''
        for check in Game.mark:
            if field[1][1] == check:
                if (field[1][0] == field[1][2] == check or
                        field[0][1] == field[2][1] == check or
                        field[0][0] == field[2][2] == check or
                        field[0][2] == field[2][0] == check):
                    result = check
            if field[0][0] == check:
                if (field[1][0] == field[2][0] == check or
                        field[0][1] == field[0][2] == check):
                    result = check
            if field[2][2] == check:
                if (field[1][2] == field[0][2] == check or
                        field[2][1] == field[2][0] == check):
                    result = check

        if not result and not (field[0].count('_') or field[1].count('_') or field[2].count('_')):
            result = "Draw"

        return result


# -------------MAIN-------------
while True:
    session = Game()
    del session
