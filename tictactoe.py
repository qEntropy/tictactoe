from os import system, name
from random import randint

board = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' '],
]


def copy_game_state(old_state):
    new_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = old_state[i][j]
    return new_state


def print_board():
    print("------------------")
    for line in board:
        print("||", end=" ")
        for val in line:
            print(val, end=" ")
            print("||", end=" ")
        print()
        print("------------------")


def game_won(board_state):

    # rows
    if (board_state[0][0] == board_state[0][1]
        and board_state[0][1] == board_state[0][2]
            and board_state[0][0] != ' '):
        return board_state[0][0]

    if (board_state[1][0] == board_state[1][1]
        and board_state[1][1] == board_state[1][2]
            and board_state[1][0] != ' '):
        return board_state[1][0]

    if (board_state[2][0] == board_state[2][1]
        and board_state[2][1] == board_state[2][2]
            and board_state[2][0] != ' '):
        return board_state[2][0]

    # columns
    if (board_state[0][0] == board_state[1][0]
        and board_state[1][0] == board_state[2][0]
            and board_state[0][0] != ' '):
        return board_state[0][0]

    if (board_state[0][1] == board_state[1][1]
        and board_state[1][1] == board_state[2][1]
            and board_state[0][1] != ' '):
        return board_state[0][1]

    if (board_state[0][2] == board_state[1][2]
        and board_state[1][2] == board_state[2][2]
            and board_state[0][2] != ' '):
        return board_state[0][2]

    # diagonals
    if (board_state[0][0] == board_state[1][1]
        and board_state[1][1] == board_state[2][2]
            and board_state[0][0] != ' '):
        return board_state[0][0]

    if (board_state[0][2] == board_state[1][1]
        and board_state[1][1] == board_state[2][0]
            and board_state[0][2] != ' '):
        return board_state[0][2]

    return "gameon"


def human_prompt():
    try:
        board_val = input("Dear Human, Your turn!, choose where to place (1 to 9): ")
        b_val = int(board_val)
        return b_val
    except:
        board_val = -1
        return board_val


# Just in case the AI algorithm fails
def ai_prompt():
    try:
        board_val = input("Algo failed, Choose for AI (1 to 9): ")
        b_val = int(board_val)
        return b_val
    except:
        board_val = -1
        return board_val


# update board on coordinates (c0, c1)
# player = 'X' or 'O'
def update_board(board_state, c0, c1, player):
    if (board_state[c0][c1] == ' '):
        board_state[c0][c1] = player
        return True
    else:
        return False


def find_coordinate(board_val):
    coords = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    return coords[board_val]


def human_plays():
    board_val = human_prompt()
    if (board_val < 10 and board_val > 0):
        coords = find_coordinate(board_val)
        updated = update_board(board, coords[0], coords[1], 'X')
        return updated
    else:
        print("your board move was out of the board")
        return False


def test_if_player_can_win(b, mark, i, j):
    board_copy = copy_game_state(b)
    board_copy[i][j] = mark
    won = game_won(board_copy)
    if won == 'X' or won == 'O':
        return True
    return False


def test_if_possible_fork(b, mark, i, j):
    board_copy = copy_game_state(b)
    board_copy[i][j] = mark
    winning_moves = 0
    for p in range(3):
        for q in range(3):
            if board_copy[p][q] is ' ' \
                    and test_if_player_can_win(board_copy, mark, p, q):
                winning_moves += 1
    return winning_moves >= 2


def fill_sides_by_AI():
    if board[0][1] == ' ':
        board[0][1] = 'O'
        return 2
    elif board[1][0] == ' ':
        board[1][0] = 'O'
        return 4
    elif board[1][2] == ' ':
        board[1][2] = 'O'
        return 6
    elif board[2][1] == ' ':
        board[2][1] = 'O'
        return 8
    return -1


def auto_ai(board_state):

    board_val = -1
    updated = False

    # check if AI can win in this board position
    # if AI can win, then freaking win the game
    for i in range(3):
        for j in range(3):
            if board_state[i][j] is ' ' \
                    and test_if_player_can_win(board_state, 'O', i, j):
                updated = update_board(board, i, j, 'O')
                value = 3*i + j + 1
                return value

    # check if HUMAN can win in this board position
    # if HUMAN can win, then STOP HUMAN
    for i in range(3):
        for j in range(3):
            if board_state[i][j] is ' ' \
                    and test_if_player_can_win(board_state, 'X', i, j):
                updated = update_board(board, i, j, 'O')
                value = 3*i + j + 1
                return value

    # check AI fork moves
    for i in range(3):
        for j in range(3):
            if board_state[i][j] is ' ' \
                    and test_if_possible_fork(board_state, 'O', i, j):
                updated = update_board(board, i, j, 'O')
                value = 3*i + j + 1
                return value

    # check for fork for players
    player_forks = 0
    for i in range(3):
        for j in range(3):
            if board_state[i][j] is ' ' \
                    and test_if_possible_fork(board_state, 'X', i, j):
                player_forks += 1
                temp_move = 3*i + j + 1
    if player_forks == 1:
        coords = find_coordinate(temp_move)
        updated = update_board(board, coords[0], coords[1], 'O')
        value = 3*i + j + 1
        return value
    elif player_forks == 2:
        return fill_sides_by_AI()

    # if center is empty, have the AI play at center
    if board[1][1] is ' ':
        updated = update_board(board, 1, 1, 'O')
        return 5

    # if corners are empty
    # AI will play at corners
    for i in {0, 2}:
        for j in {0, 2}:
            if board[i][j] is ' ':
                updated = update_board(board, i, j, 'O')
                value = 3*i + j + 1
                return value

    # if sides are empty
    # AI will play at sides
    return fill_sides_by_AI()

    '''
    ideally code below this should NEVER run
    code in this block should never run
    '''
    if (board_val == -1):
        board_val = ai_prompt()

    if (board_val < 10 and board_val > 0):
        coords = find_coordinate(board_val)
        updated = update_board(board, coords[0], coords[1], 'O')
        return updated
    else:
        print("your board move was out of the board")
        return False
    '''
    code in this block should never run
    ideally code above this should NEVER run
    '''


def game_draw(board):
    draw = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                draw = False
                break
    return draw


def play_game():
    system('clear')
    print_board()
    turn = randint(2, 9)
    while(True):

        if (game_won(board) == 'X'):
            print("game won by HUMAN")
            break
        if (game_won(board) == 'O'):
            print("Game won by AI")
            break
        if (game_draw(board)):
            print("GAME DRAWN")
            break

        if (turn % 2):
            if(human_plays() == True):
                system('clear')
                print_board()
            else:
                turn = turn - 1
        else:
            value_by_ai = auto_ai(board)
            if(value_by_ai != -1):
                system('clear')
                print("AI plays move: " + str(value_by_ai))
                print_board()
            else:
                turn = turn - 1
        turn = turn + 1


play_game()
