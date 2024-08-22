import copy

import random
def print_board(lst):
  print("+-------"*4 + "+")
  for row in lst:
      print("|" + "".join(f" {str(item).ljust(6)}|" for item in row))
      print("+-------"*4 + "+")
      
def add_random_tile(board):
    # Create a deep copy to avoid modifying the original board
    board = copy.deepcopy(board)
    # Find all empty positions
    empty_positions = [i for i, x in enumerate(flatten(board)) if x is None]
    
    if empty_positions:
        # Choose a random empty position
        position = random.choice(empty_positions)
        # Place a tile with value 2 in the chosen empty position
        board = create(board, position, 2)  # Explicitly placing tile with value 2
    
    return board

def X(num):
    return num % 4

def Y(num):
    return num // 4

def create(board, num, value):
    row = X(num)
    col = Y(num)
    # Check if the position is empty before placing the value
    if board[row][col] is None:
        board[row][col] = value
    return board

def init():
    board = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
    # Generate the first tile
    board = create(board, random.randint(0, 15), 2)  # Choose a position between 0 and 15 inclusive

    # Find the second position where the tile should be placed
    empty_positions = [i for i, x in enumerate(flatten(board)) if x is None]
    if empty_positions:
        board = create(board, random.choice(empty_positions), 2)

    return board
  

def flatten(lst):
    lst = copy.deepcopy(lst)
    return [item for sublist in lst for item in sublist]
def gen(board):
  return create(board, random.randint(0, flatten(board).count(None)))
def shift_up(board):
    board = copy.deepcopy(board)
    for j in range(4):
        new_column = [board[i][j] for i in range(4) if board[i][j] is not None]
        for i in range(1, len(new_column)):
            if new_column[i] == new_column[i - 1]:
                new_column[i - 1] *= 2
                new_column[i] = None
        new_column = [value for value in new_column if value is not None]
        while len(new_column) < 4:
            new_column.append(None)
        for i in range(4):
            board[i][j] = new_column[i]
    return board
def shift_down(board):
    board = copy.deepcopy(board)
    for j in range(4):
        new_column = [board[i][j] for i in range(3, -1, -1) if board[i][j] is not None]
        for i in range(1, len(new_column)):
            if new_column[i] == new_column[i - 1]:
                new_column[i - 1] *= 2
                new_column[i] = None
        new_column = [value for value in new_column if value is not None]
        while len(new_column) < 4:
            new_column.append(None)
        for i in range(4):
            board[3 - i][j] = new_column[i]
    return board
def shift_right(board):
    board = copy.deepcopy(board)
    for i in range(4):
        new_row = [board[i][j] for j in range(3, -1, -1) if board[i][j] is not None]
        for j in range(1, len(new_row)):
            if new_row[j] == new_row[j - 1]:
                new_row[j - 1] *= 2
                new_row[j] = None
        new_row = [value for value in new_row if value is not None]
        while len(new_row) < 4:
            new_row.append(None)
        for j in range(4):
            board[i][3 - j] = new_row[j]
    return board
def shift_left(board):
    board = copy.deepcopy(board)
    for i in range(4):
        new_row = [board[i][j] for j in range(4) if board[i][j] is not None]
        for j in range(1, len(new_row)):
            if new_row[j] == new_row[j - 1]:
                new_row[j - 1] *= 2
                new_row[j] = None
        new_row = [value for value in new_row if value is not None]
        while len(new_row) < 4:
            new_row.append(None)
        for j in range(4):
            board[i][j] = new_row[j]
    return board
def game_over(board):
  return None not in flatten(board)
def think(board, depth):
  if depth == 2:
    return depth*10 + flatten(board).count(None)
  best = -1
  #print_board(board)
  for i, item in enumerate(flatten(board)):
    if item == None:
      aval_move = []
      for fx in [shift_up, shift_down, shift_right, shift_left]:
        if flatten(fx(board)) != flatten(board):
          aval_move.append(fx)
      if aval_move == []:
        return depth*10
      for fx in aval_move:
        val = think(fx(create(copy.deepcopy(board), i, 2)), depth+1)
        if val > best:
          best = val
  return best
def initialize_specific_board():
    # Create a board where a specific move is necessary to avoid losing
    board = [
        [2, 16, 4, None],
        [8, 4, 16, 8],
        [16, 8, 4, 64],
        [8, 16, 32, 8]
    ]
    return board
def decide(board):
  best = -1
  best_move = None
  aval_move = []
  for index, fx in enumerate([shift_up, shift_down, shift_right, shift_left]):
    #print_board(fx(board))
    if flatten(fx(board)) != flatten(board):
        aval_move.append((fx, index))
  if aval_move == []:
    return None
  for fx in aval_move:
    val = think(fx[0](board), 0)
    if val > best:
      best = val
      best_move = fx[1]
  return best, best_move

#board = initialize_specific_board()
board =init()
print_board(board)
while True:
  tmp = decide(board)
  if tmp == None:
    print("game over")
    break
  print(tmp)
  board = [shift_up, shift_down, shift_right, shift_left][tmp[1]](board)
  print_board(board)
  board = add_random_tile(board)
  print_board(board)
