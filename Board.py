import copy

checkmate = False
winner = None
stalemate = False
ai_color = None

board = [[None for i in range(8)] for j in range(8)]
pieces_checking = []


def evaluate_material_heuristic(grid, color):
    opponentColor = 'W' if color == 'B' else 'B'
    # Firstly Sum Values of Pieces
    score = 0
    piece_weights = {'P': 1, 'B': 3, 'N': 3, 'R': 5, 'Q': 9, 'K': 0}
    for i in range(8):
        for j in range(8):
            if grid[i][j][0] == color and grid[i][j] != "---":
                score = score + piece_weights.get(grid[i][j][1])
            elif grid[i][j][0] == opponentColor and grid[i][j] != "---":
                score = score - piece_weights.get(grid[i][j][1])
    return score


def evaluate_mobility_heuristic(grid, color):
    opponentColor = 'W' if color == 'B' else 'B'
    opponentBoard = copy.deepcopy(grid)
    own_moves = len(get_all_moves(grid, color))
    opponent_moves = len(get_all_moves(opponentBoard, opponentColor))
    return own_moves - opponent_moves


def initialize_board():
    global board
    board = [
        ["BR1", "BN1", "BB1", "BQ1", "BK1", "BB2", "BN2", "BR2"],
        ["BP1", "BP2", "BP3", "BP4", "BP5", "BP6", "BP7", "BP8"],
        ["---", "---", "---", "---", "---", "---", "---", "---"],
        ["---", "---", "---", "---", "---", "---", "---", "---"],
        ["---", "---", "---", "---", "---", "---", "---", "---"],
        ["---", "---", "---", "---", "---", "---", "---", "---"],
        ["WP1", "WP2", "WP3", "WP4", "WP5", "WP6", "WP7", "WP8"],
        ["WR1", "WN1", "WB1", "WQ1", "WK1", "WB2", "WN2", "WR2"]
    ]


def print_board(grid):
    print()
    for indx, row in enumerate(grid):
        print(f"{indx} |", end="")
        for col in row:
            print(col, end="|")
        print()
    print("    0   1   2   3   4   5   6   7")
    print()


def get_pawn_moves(grid, moves, row, col, piece, color):
    if color == "W":
        if row > 0 and grid[row - 1][col] == "---":
            moves.append((piece, (row, col), (row - 1, col)))
            if row == 6 and grid[row - 2][col] == "---":
                moves.append((piece, (row, col), (row - 2, col)))
        if row > 0 and col > 0 and grid[row - 1][col - 1][0] == "B":
            moves.append((piece, (row, col), (row - 1, col - 1)))
        if row > 0 and col < 7 and grid[row - 1][col + 1][0] == "B":
            moves.append((piece, (row, col), (row - 1, col + 1)))
    else:
        if row < 7 and grid[row + 1][col] == "---":
            moves.append((piece, (row, col), (row + 1, col)))
            if row == 1 and grid[row + 2][col] == "---":
                moves.append((piece, (row, col), (row + 2, col)))
        if row < 7 and col > 0 and grid[row + 1][col - 1][0] == "W":
            moves.append((piece, (row, col), (row + 1, col - 1)))
        if row < 7 and col < 7 and grid[row + 1][col + 1][0] == "W":
            moves.append((piece, (row, col), (row + 1, col + 1)))


def get_knight_moves(grid, moves, row, col, piece, color):
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for move in knight_moves:
        new_row = row + move[0]
        new_col = col + move[1]
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if grid[new_row][new_col] == "---" or grid[new_row][new_col][0] != color:
                moves.append((piece, (row, col), (new_row, new_col)))


def get_rook_moves(grid, moves, row, col, piece, color):
    # Checking moves to the right
    for j in range(col + 1, 8):
        if grid[row][j][0] == color:
            break
        if grid[row][j] == "---":
            moves.append((piece, (row, col), (row, j)))
        else:
            if grid[row][j][0] != color:
                moves.append((piece, (row, col), (row, j)))
            break
    # Checking moves to the left
    for j in range(col - 1, -1, -1):
        if grid[row][j][0] == color:
            break
        if grid[row][j] == "---":
            moves.append((piece, (row, col), (row, j)))
        else:
            if grid[row][j][0] != color:
                moves.append((piece, (row, col), (row, j)))
            break
    # Checking the moves upwards
    for i in range(row - 1, -1, -1):
        if grid[i][col][0] == color:
            break
        if grid[i][col] == "---":
            moves.append((piece, (row, col), (i, col)))
        else:
            if grid[i][col][0] != color:
                moves.append((piece, (row, col), (i, col)))
            break
    # Checking the moves downwards
    for i in range(row + 1, 8):
        if grid[i][col][0] == color:
            break
        if grid[i][col] == "---":
            moves.append((piece, (row, col), (i, col)))
        else:
            if grid[i][col][0] != color:
                moves.append((piece, (row, col), (i, col)))
            break


def get_bishop_moves(grid, moves, row, col, piece, color):
    bishop_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for direction in bishop_moves:
        for i in range(1, 8):
            new_row = row + direction[0] * i
            new_col = col + direction[1] * i
            if new_row < 0 or new_row > 7 or new_col < 0 or new_col > 7:
                break
            if grid[new_row][new_col] == "---":
                moves.append((piece, (row, col), (new_row, new_col)))
            elif grid[new_row][new_col][0] != color:
                moves.append((piece, (row, col), (new_row, new_col)))
                break
            else:
                break


def get_queen_moves(grid, moves, row, col, piece, color):
    # Checking Diagonal Moves
    diagonal_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for direction in diagonal_moves:
        for i in range(1, 8):
            new_row = row + direction[0] * i
            new_col = col + direction[1] * i
            if new_row < 0 or new_row > 7 or new_col < 0 or new_col > 7:
                break
            if grid[new_row][new_col] == "---":
                moves.append((piece, (row, col), (new_row, new_col)))
            elif grid[new_row][new_col][0] != color:
                moves.append((piece, (row, col), (new_row, new_col)))
                break
            else:
                break
    # Checking Right,Left,Up, Down moves
    # Checking moves to the right
    for j in range(col + 1, 8):
        if grid[row][j][0] == color:
            break
        if grid[row][j] == "---":
            moves.append((piece, (row, col), (row, j)))
        else:
            if grid[row][j][0] != color:
                moves.append((piece, (row, col), (row, j)))
            break
    # Checking moves to the left
    for j in range(col - 1, -1, -1):
        if grid[row][j][0] == color:
            break
        if grid[row][j] == "---":
            moves.append((piece, (row, col), (row, j)))
        else:
            if grid[row][j][0] != color:
                moves.append((piece, (row, col), (row, j)))
            break
    # Checking the moves upwards
    for i in range(row - 1, -1, -1):
        if grid[i][col][0] == color:
            break
        if grid[i][col] == "---":
            moves.append((piece, (row, col), (i, col)))
        else:
            if grid[i][col][0] != color:
                moves.append((piece, (row, col), (i, col)))
            break
    # Checking the moves downwards
    for i in range(row + 1, 8):
        if grid[i][col][0] == color:
            break
        if grid[i][col] == "---":
            moves.append((piece, (row, col), (i, col)))
        else:
            if grid[i][col][0] != color:
                moves.append((piece, (row, col), (i, col)))
            break


def perform_move(grid, move):
    # move will be like (piece,(row,col),(new_row,new_col))
    (piece, (row, col), (new_row, new_col)) = move
    grid[row][col] = '---'
    grid[new_row][new_col] = piece


def get_king_moves(grid, moves, row, col, piece, color):
    # Returns All the moves of the king
    king = grid[row][col]
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i <= 7 and 0 <= j <= 7 and (i, j) != (row, col):
                if grid[i][j][0] != color:
                    temp_board = copy.deepcopy(grid)
                    perform_move(temp_board, (king, (row, col), (i, j)))
                    if not is_check(temp_board, color):
                        moves.append((king, (row, col), (i, j)))


def get_check_squares(color):
    global pieces_checking
    squares = []
    for piece in pieces_checking:
        if piece[0][0] != color:
            squares.append(piece[1])
    return squares


def get_all_moves(grid, color):
    moves = []
    global checkmate
    global winner
    # Get the King
    King = None
    King_row = None
    King_col = None
    for row in range(8):
        for col in range(8):
            temp = grid[row][col]
            if temp[0] == color and temp[1] == 'K':
                King = temp
                King_row = row
                King_col = col
                break
        if King is not None:
            break

    for row in range(8):
        for col in range(8):
            piece = grid[row][col]
            if piece != "---" and piece[0] == color:
                if piece[1] == "P":
                    # Generate pawn moves
                    get_pawn_moves(grid, moves, row, col, piece, color)
                elif piece[1] == "N":
                    # Generate Knight moves
                    get_knight_moves(grid, moves, row, col, piece, color)
                elif piece[1] == "R":
                    get_rook_moves(grid, moves, row, col, piece, color)
                elif piece[1] == "B":
                    get_bishop_moves(grid, moves, row, col, piece, color)
                elif piece[1] == "Q":
                    get_queen_moves(grid, moves, row, col, piece, color)
                elif piece[1] == "K":
                    get_king_moves(grid, moves, row, col, piece, color)
    if is_check(grid, color):
        # Checking if any piece can capture the piece
        check_squares = get_check_squares(color)
        for move in moves:
            if move[2] in check_squares:
                return [move]
        # if no capture move then return kings moves
        king_moves = []
        get_king_moves(grid, king_moves, King_row, King_col, King, color)
        return king_moves
    else:
        return moves


def is_check(grid, color):
    # getting the position of the king
    opponentColor = "B" if color == "W" else "W"
    king_pos = None
    for i in range(8):
        for j in range(8):
            piece = grid[i][j]
            if piece[0] == color and piece != '---' and piece[1] == 'K':
                king_pos = (i, j)
                break
        if king_pos is not None:
            break

    # checking if any opponent piece attacks the king
    moves = []
    for i in range(8):
        for j in range(8):
            piece = grid[i][j]
            if piece != "---" and piece[0] == opponentColor:
                if piece[1] == "P":
                    # Generate pawn moves
                    get_pawn_moves(grid, moves, i, j, piece, opponentColor)
                elif piece[1] == "N":
                    # Generate Knight moves
                    get_knight_moves(grid, moves, i, j, piece, opponentColor)
                elif piece[1] == "R":
                    get_rook_moves(grid, moves, i, j, piece, opponentColor)
                elif piece[1] == "B":
                    get_bishop_moves(grid, moves, i, j, piece, opponentColor)
                elif piece[1] == "Q":
                    get_queen_moves(grid, moves, i, j, piece, opponentColor)
                for move in moves:
                    if king_pos == move[2]:
                        pieces_checking.append((move[0], move[1]))
                        return True
    pieces_checking.clear()
    return False


def is_check_mate(grid, color):
    moves = []
    global checkmate
    global winner
    # Get the King
    King = None
    King_row = None
    King_col = None
    for row in range(8):
        for col in range(8):
            temp = grid[row][col]
            if temp[0] == color and temp[1] == 'K':
                King = temp
                King_row = row
                King_col = col
                break
        if King is not None:
            break

    # Check for Check on the king then only do the king moves, if no king moves then checkmate
    if is_check(grid, color):
        moves = get_all_moves(grid, color)
        if len(moves) > 0:
            return False
        else:
            print("Checkmate")
            print(f"Possible Moves left: {moves}")
            checkmate = True
            winner = "B" if color == "W" else "W"
            return True


def is_stale_mate(grid, color):
    moves = get_all_moves(grid, color)
    if len(moves) == 0:
        return True
    return False


def alpha_beta_pruining(grid, max_depth, current_depth, alpha, beta, ai_turn):
    if current_depth == max_depth or checkmate:
        return evaluate_material_heuristic(grid, ai_color) + evaluate_mobility_heuristic(grid, ai_color)
    player_color = 'W' if ai_color == 'B' else 'B'
    if ai_turn:
        best_score = float('-inf')
        best_move = None
        actions = get_all_moves(grid, ai_color)
        for action in actions:
            temp_board = copy.deepcopy(grid)
            perform_move(temp_board, action)
            result = alpha_beta_pruining(temp_board, max_depth, current_depth + 1, alpha, beta, False)
            if isinstance(result, tuple):
                score, _ = result
            else:
                score = result
            if score > best_score:
                best_score = score
                best_move = action
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        actions = get_all_moves(grid, player_color)
        for action in actions:
            temp_board = copy.deepcopy(grid)
            perform_move(temp_board, action)
            result = alpha_beta_pruining(temp_board, max_depth, current_depth + 1, alpha, beta, True)
            if isinstance(result, tuple):
                score, _ = result
            else:
                score = result
            if score < best_score:
                best_score = score
                best_move = action
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score, best_move


def get_piece_coordinates(grid, piece):
    for i in range(8):
        for j in range(8):
            current_piece = grid[i][j]
            if current_piece == piece:
                return i, j
    return None, None


def check_move_validity(grid, piece, nr, nc):
    cr = None
    cc = None
    moves = []
    for i in range(8):
        for j in range(8):
            if grid[i][j] == piece:
                cr = i
                cc = j
    if piece[0] == 'W':
        moves = get_all_moves(grid, 'W')
    elif piece[0] == 'B':
        moves = get_all_moves(grid, 'B')
    for move in moves:
        if move[2] == (nr, nc) and piece == move[0]:
            return True
    return False


def play_chess_game():
    alpha = float('-inf')
    beta = float('inf')
    global ai_color, checkmate, stalemate, winner, board
    player_color = None
    while player_color not in ['W', 'B']:
        player_color = input("Enter to Play as 'W' or as 'B': ").upper()
    ai_color = 'W' if player_color == 'B' else 'B'
    ai_turn = False if player_color == 'W' else True
    current_color = 'W'
    print("Welcome to Chess Game!")
    while not is_check_mate(board, current_color):
        if is_stale_mate(board, current_color):
            print("Game is at a StaleMate : It's A draw!")
            stalemate = True
            return
        print_board(board)
        if ai_turn:
            print("-------AI's Turn-------")
            score, action = alpha_beta_pruining(board, 3, 0, alpha, beta, True)
            perform_move(board, action)
            ai_turn = False
            current_color = player_color
        else:
            print("-------Player's Turn------")
            valid_input = False
            while not valid_input:
                curr_row = None
                curr_col = None
                while curr_row is None or curr_col is None:
                    piece = input("Enter Piece to move: ")
                    curr_row, curr_col = get_piece_coordinates(board, piece)
                new_row = int(input("Enter New row number for piece: "))
                new_col = int(input("Enter New col number for piece: "))
                valid_input = check_move_validity(board, piece, new_row, new_col)
                print("----Invalid Input---") if not valid_input else print()
            perform_move(board, (piece, (curr_row, curr_col), (new_row, new_col)))
            ai_turn = True
            current_color = ai_color


initialize_board()
play_chess_game()
print_board(board)
print("-----GAME OVER------")
