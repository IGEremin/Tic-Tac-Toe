symbols = " " * 9
field = [[symbols[0], symbols[3], symbols[6]], [symbols[1], symbols[4], symbols[7]],
         [symbols[2], symbols[5], symbols[8]]]


def print_set(field):
    print("---------")
    for n in range(3):
        print("| " + field[0][n] + " " + field[1][n] + " " + field[2][n] + " |")
    print("---------")


def input_coord(field):
    coord = input("Enter the coordinates: ").split()
    global mark

    if not coord[0].isnumeric() or not coord[1].isnumeric():
        print("You should enter numbers!")
        return

    for n in range(len(coord)):
        coord[n] = int(coord[n]) - 1

    if coord[0] > 2 or coord[1] > 2:
        print("Coordinates should be from 1 to 3!")
        return

    elif field[coord[0]][abs(coord[1] - 2)] == "X" or field[coord[0]][abs(coord[1] - 2)] == "O":
        print("This cell is occupied! Choose another one!")
        return

    else:
        field[coord[0]][2 - coord[1]] = mark
        print_set(field)
        if mark == "X":
            mark = "O"
        else:
            mark = "X"

    return field


def checker(mark, field):
    global winner
    if abs(field[0].count("X") + field[1].count("X") + field[2].count("X") - field[0].count("O") - field[1].count("O") -
           field[2].count("O")) > 1:
        winner = "Impossible"
        print(winner)

    else:
        for mark in ['X', 'O']:
            if field[1][1] == mark:
                if (field[0][0] == field[2][2] == mark or
                        field[0][2] == field[2][0] == mark or
                        field[0][1] == field[2][1] == mark or
                        field[1][0] == field[1][2] == mark):
                    winner += mark
            elif field[0][0] == mark:
                if (field[0][1] == field[0][2] == mark or
                        field[1][0] == field[2][0] == mark):
                    winner += mark
            elif field[2][2] == mark:
                if (field[2][0] == field[2][1] == mark or
                        field[1][2] == field[0][2] == mark):
                    winner += mark
        if not winner:
            if field[0].count(" ") or field[1].count(" ") or field[2].count(" ") or field[0].count("_") + field[
                1].count("_") + field[2].count("_"):
                pass
            else:
                winner = "Draw"
                print(winner)
        elif winner.count("X") and winner.count("O"):
            winner = "Impossible"
            print(winner)
        else:
            print(winner[0], "wins")


mark = 'X'
winner = ''
print_set(field)

while True:
    input_coord(field)
    checker(mark, field)
    if winner:
        break
