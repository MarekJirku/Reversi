from copy import deepcopy
import random

class MyPlayer:
    '''Hrac je chudak velmi hloupy a umi hrat pouze nahodny tah :( '''
    def __init__(self, my_color, opponent_color):
        self.name = 'jirkuma4'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.value_matrix =[[120,-20, 20,  5,  5, 20,-20,120],
                            [-20,-40, -5, -5, -5, -5,-40,-20],
                            [ 20, -5, 15,  3,  3, 15, -5, 20],
                            [  5, -5,  3,  3,  3,  3, -5,  5],
                            [  5, -5,  3,  3,  3,  3, -5,  5],
                            [ 20, -5, 15,  3,  3, 15, -5, 20],
                            [-20,-40, -5, -5, -5, -5,-40,-20],
                            [120,-20, 20,  5,  5, 20,-20,120]
                            ]
                             
    def move(self, board):
        valid_moves = self.find_valid_moves(board, self.my_color)
        if len(valid_moves) == 0: # return none if there are no valid moves
            return None
        self.best_score = -100000
        for i in range(len(valid_moves)):
            self.score = 0
            self.simulate_next_rounds(40, valid_moves[i], board, self.my_color)
            print("score: ", self.score)
            if(self.score > self.best_score):
                my_move = valid_moves[i]
                self.best_score = self.score
        #my_move = self.select_final_move(valid_moves, board)
        return my_move
    
    def find_valid_moves(self, board, p1_color):
        valid_moves = []
        for r in range(len(board)): #check every tile if its valid
            for c in range(len(board[r])):
                if self.is_tile_valid(p1_color,board, r, c): #returs True or false for each tile
                    valid_moves.append((r,c)) # create a list of valid tiles
        return valid_moves

    def is_tile_valid(self,p1_color, board, r, c):
        if(p1_color == 1):
            p2_color = 0
        else:
            p2_color = 1
        if board[r][c] != -1:
            return False
        for i in range(-1,2):
            for j in range(-1,2):       # first two for cycles check all directions
                if r+i >= 0 and r+i < len(board) and c+j >= 0 and c+j < len(board):  #chcek if there is a tile in selected direction 
                    if board[r+i][c+j] == p2_color: 
                        for k in range(1,len(board)): # check all tiles in selected dierction
                            if (r+i*k) >= 0 and (r+i*k) < len(board) and (c+j*k) >= 0 and (c+j*k) < len(board): #chcek if there is a chceckable tile on the board
                                if board[r+i*k][c+j*k] == p2_color: # if there is an opponent tile continue to the next one
                                    continue
                                elif board[r+i*k][c+j*k] == p1_color: #if the line ends with my tile methond returns true
                                    return True
                                elif board[r+i*k][c+j*k] == -1: #if the line ends with an empty tile, check the next direction
                                    break
        return False
    
    def lowest_opponent_moves(self, valid_moves, board):
        amount_of_opponent_moves = 100
        for i in range(len(valid_moves)):
            opponent_valid_moves = []
            new_board = board
            new_board[valid_moves[i][0]][valid_moves[i][1]] = self.my_color
            for r in range(len(board)):
                for c in range(len(board)):
                    validity = self.is_tile_valid_for_opponent(new_board, r, c)
                    if validity == True:
                        opponent_valid_moves.append((r,c))
            if (len(opponent_valid_moves) < amount_of_opponent_moves):
                amount_of_opponent_moves = len(opponent_valid_moves)
                final_move = valid_moves[i]
        return final_move

    def is_tile_valid_for_opponent(self, board, r, c):
        if board[r][c] != -1:
            return False
        for i in range(-1,2):
            for j in range(-1,2):       # first two for cycles check all directions
                if r+i >= 0 and r+i < len(board) and c+j >= 0 and c+j < len(board):  #chcek if there is a tile in selected direction 
                    if board[r+i][c+j] == self.my_color: 
                        for k in range(1,len(board)): # check all tiles in selected dierction
                            if (r+i*k) >= 0 and (r+i*k) < len(board) and (c+j*k) >= 0 and (c+j*k) < len(board): #chcek if there is a chceckable tile on the board
                                if board[r+i*k][c+j*k] == self.my_color: # if there is an opponent tile continue to the next one
                                    continue
                                elif board[r+i*k][c+j*k] == self.opponent_color: #if the line ends with my tile methond returns true
                                    return True
                                elif board[r+i*k][c+j*k] == -1: #if the line ends with an empty tile, check the next direction
                                    break
        return False
    
    def count_tiles_on_board(self, board):
        tile_counter = 0
        for r in range(len(board)):
            for c in range(len(board)):
                if(board[r][c] == 1 or board[r][c] == 0):
                    tile_counter += 1
        return tile_counter
    
    def rank_valid_tiles(self, valid_moves, board):
        max_value = -100
        for i in range (len(valid_moves)):
            if (self.value_matrix[valid_moves[i][0]][valid_moves[i][1]] > max_value):
                final_move = valid_moves[i]
        return final_move
    
    def select_final_move(self, valid_moves, board):
        mega_score = -10000
        for i in range(len(valid_moves)):
            best_score = -10000000
            board1 = self.play_move_on_board(board, valid_moves[i], self.my_color)
            opponent_valid_moves = self.find_valid_moves(board1, self.opponent_color)
            if(len(opponent_valid_moves) == 0):
                return valid_moves[i]
            opponent_move = self.opponent_plays_move(board1, opponent_valid_moves)
            board2 = self.play_move_on_board(board, opponent_move, self.opponent_color)
            valid_moves1 = self.find_valid_moves(board2, self.my_color)
            Jscore = 0
            for j in range (len(valid_moves1)):
                board3 = self.play_move_on_board(board, valid_moves1[j], self.my_color)
                curr_score = self.evaluate_board(board3, self.my_color)
                Jscore += curr_score
            if (Jscore > best_score):
                best_score = Jscore
                final_move = valid_moves[i]
            
        
        return final_move
    
    def opponent_plays_move(self, board, valid_moves):
        best_tile_sum = -1000
        for i in range(len(valid_moves)):
            current_tile_sum = 0
            new_board = self.play_move_on_board(board,valid_moves[i], self.opponent_color)
            for r in range(len(board)):
                for c in range(len(board)):
                    if (new_board[r][c] == self.opponent_color):
                        current_tile_sum += self.value_matrix[r][c]
                    elif (new_board[r][c] == self.my_color):
                        current_tile_sum -= self.value_matrix[r][c]
            if (current_tile_sum > best_tile_sum):
                final_move = valid_moves[i]
                best_tile_sum = current_tile_sum
        return final_move

    def simulate_next_rounds(self,depth, move, board, p1_color):
        if(p1_color == 1):
            p2_color = 0
        else:
            p2_color = 1
        if depth == 0:
            return
        if(move == None):
            return
        else:
            new_board = self.play_move_on_board(board, move, p1_color)
            if (depth == 1):
                if(self.evaluate_board(new_board, self.my_color) > self.score):
                    self.score = self.evaluate_board(new_board, self.my_color)
            valid_moves = self.find_valid_moves(new_board, p2_color)
            best_move = self.find_best_move_by_board_eval(new_board, valid_moves, p2_color)
            self.print_board_w_num(new_board)
            print("depth: ", depth)

            self.simulate_next_rounds(depth - 1, best_move, new_board, p2_color)

    def find_best_move_by_board_eval(self,board,moves,p1_color):
        if (len(moves)) == 0:
            return None
        move_values = []
        for i in range(len(moves)):
            new_board = self.play_move_on_board(board, moves[i], p1_color)
            move_values.append( (moves[i] , self.evaluate_board(new_board, p1_color)) )

        sorted_values = sorted(move_values,key=lambda x: x[1])
        best_move = sorted_values[-1][0]

        return best_move

    def simulate_all_oponent_moves(self, valid_moves, board, p1_color):
        all_possible_boards = []
        for i in range (len(valid_moves)):
            new_board = self.play_move_on_board(board, valid_moves[i], p1_color)
            all_possible_boards.append(new_board)
        return all_possible_boards
    
    def evaluate_board(self, board, p1_color):
        if(p1_color == 1):
            p2_color = 0
        else:
            p2_color = 1
        score = 0
        for r in range(len(board)):
            for c in range(len(board)):
                if (board[r][c] == p1_color):
                    score += self.value_matrix[r][c]
                elif (board[r][c] == p2_color):
                    score -= self.value_matrix[r][c]
        return score
        
    def play_move_on_board(self, board, move, p1_color):
        new_board = deepcopy(board)
        for i in range(-1,2):
            for j in range(-1,2):
                if self.check_direction(board,move,i,j,p1_color):
                    new_board = self.flip_tiles_in_direction(new_board, move,i,j,p1_color)
        return new_board

    def check_direction(self, board, move,dx,dy,p1_color):
        if(p1_color == 1):
            p2_color = 0
        else:
            p2_color = 1

        curr_x = move[0]+dx
        curr_y = move[1]+dy

        if (curr_x>=0) and (curr_x<len(board)) and (curr_y>=0) and (curr_y<len(board)):
            if board[curr_x][curr_y] == p2_color:
                while (curr_x>=0) and (curr_x<len(board)) and (curr_y>=0) and (curr_y<len(board)):
                    curr_x += dx
                    curr_y += dy
                    if (curr_x>=0) and (curr_x<len(board)) and (curr_y>=0) and (curr_y<len(board)):
                        if (board[curr_x][curr_y] == p1_color):
                            return True
                        if (board[curr_x][curr_y] == -1):
                            return False
        return False
    
    def flip_tiles_in_direction(self, board, move, dx, dy, p1_color):
        if(p1_color == 1):
            p2_color = 0
        else:
            p2_color = 1
        board[move[0]][move[1]] = p1_color
        curr_x = move[0]+dx
        curr_y = move[1]+dy
        while(board[curr_x][curr_y] == p2_color):
            board[curr_x][curr_y] = p1_color
        return board

    def print_board_w_num(self, board):
            print("X  0  1  2  3  4  5  6  7")
            for r in range(8):
                for c in range(-1,8):
                    if c == -1:
                        print(r, end="")
                    elif board[r][c] == -1:
                        x = "-"
                        print(f"{x:>3}", end="")
                    else:
                        print(f"{board[r][c]:>3}", end="")
                    # print(self.board[r][c], end=" ")
                print()

if __name__ == "__main__":
    board = \
	    [[-1,-1,-1,-1,-1,-1,-1,-1], # created this testing board so its easily changeble
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1, 1, 0,-1,-1,-1,-1],
         [-1,-1,-1, 1, 0,-1,-1,-1],
         [-1,-1,-1, 0, 0, 0,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         ]
    board2 = [[random.choice([-1,0,1]) for i in range(8)] for j in range(8)] #create a board full of random 0,1,-1

    player = MyPlayer(1,0)
    print(player.move(board))
 

        