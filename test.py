board =     [
0,0,0,0,0,0,0,
0,0,0,0,0,0,0,
0,0,0,1,0,0,0,
0,1,0,1,0,2,2,
0,2,2,2,2,1,2,
2,1,2,2,1,2,1]

def check_game_status(board):

    for color_code in [1, 2]:
        for col in range(0, 42, 7): # check rows by looking through each column
            left_most = col + 4
            for i in range(col, left_most):
                if board[i : i+4] == [color_code] * 4:
                    return str(color_code) + "Horizontal" + str(col) + str(i)

        for row in range(0, 7): # check columns by looking through each row
            for j in range(row, row+21, 7):
                if [board[j], board[j+7], board[j + 14], board[j+21]] == [color_code] * 4:
                    return str(color_code) + "Vertical"

        for piece in range(42): # check diagonals using integer div. and mod.
            LEFT = False
            RIGHT = False
            UP = False
            DOWN = False

            if piece // 7 in [0,1,2]: # check if 4 spaces are available in each direction
                DOWN = True
            if piece // 7 in [3,4,5]:
                UP = True

            if piece % 7 in [0,1,2,3]:
                RIGHT = True
            if piece % 7 in [3,4,5,6]:
                LEFT = True

            if RIGHT and UP:
                if [board[piece], board[piece - 6], board[piece - 12], board[piece - 18]] == [color_code] * 4:
                    return str(color_code) + "RIGHTUP"
            if RIGHT and DOWN:
                if [board[piece], board[piece + 8], board[piece + 16], board[piece + 24]] == [color_code] * 4:
                    return str(color_code) + "RIGHTDOWN"
            if LEFT and UP:
                if [board[piece], board[piece - 8], board[piece - 16], board[piece - 24]] == [color_code] * 4:
                    return str(color_code) + "LEFTUP"
            if LEFT and DOWN:
                if [board[piece], board[piece + 6], board[piece + 12], board[piece + 18]] == [color_code] * 4:
                    return str(color_code) + "LEFTDOWN"

    for x in range(42): # check for draw state
        if board[x] == 0:
            # still playing
            return -1

    # draw game
    return 0

print (check_game_status(board))