from copy import deepcopy
import random


class MyPlayer:
    '''HRACKTERYSIMULUJETAHYDOPREDUJEHLOUPEJSINEZTNEHLETAKZEODEVZADAVAMTUPOUNA'''
    def __init__(self, my_color, opponent_color):
        self.name = 'jirkuma4'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.worst_possible_score = -400
        self.value_matrix =[[120,-20, 20,  5,  5, 20,-20,120], # Tested a bunch of matrixes and this one seemed to to work the best
                            [-20,-40, -5, -5, -5, -5,-40,-20], # it is from here https://github.com/skalahonza/Reversi
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
        my_move = self.select_final_move(valid_moves, board)
        return my_move
    
    def find_valid_moves(self, board, p1_color):
        valid_moves = []
        for r in range(len(board)): #check every tile
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
                            if (r+i*k) >= 0 and (r+i*k) < len(board) and (c+j*k) >= 0 and (c+j*k) < len(board): #chcek if the tile isnt out of range
                                if board[r+i*k][c+j*k] == p2_color: # if there is an opponent tile continue to the next one
                                    continue
                                elif board[r+i*k][c+j*k] == p1_color: #if the line ends with my tile methond returns true
                                    return True
                                elif board[r+i*k][c+j*k] == -1: #if the line ends with an empty tile, check the next direction
                                    break
        return False
    
    def select_final_move(self, valid_moves, board):
        # It tries each valid move and and evaluates the situation if the move was played
        # then it returns the move with the best evaluation score
        best_score = self.worst_possible_score
        for i in range(len(valid_moves)):
            new_board = self.play_move_on_board(board, valid_moves[i], self.my_color)
            current_move_score = self.evaluate_board(new_board, self.my_color)
            if (current_move_score >= best_score):
                final_move = valid_moves[i]
                best_score = current_move_score
        return final_move
        
    def play_move_on_board(self, board, move, p1_color):
        new_board = deepcopy(board)
        for i in range(-1,2):
            for j in range(-1,2):
                if self.check_direction(board,move,i,j,p1_color):
                    new_board = self.flip_tiles_in_direction(new_board, move,i,j,p1_color)
        return new_board

    def check_direction(self, board, move,dx,dy,p1_color):
        # checks if the direction of a selected move move should be flipped
        # it checks it the same way as is_tile_valid
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
        #flips every tile in a direction until it sees the players color
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

    def evaluate_board(self, board, p1_color):
        # return a value that represent how good of a postion a player has on board
        # it adds the value of a tile if the tile is my, and subtracts if it belongs to the opponent
        # empty tiles arent counted
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


if __name__ == "__main__":
    board = \
	    [[-1,-1,-1,-1,-1,-1,-1,-1], # created this testing board so its easily changeble
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1, 0, 1,-1,-1],
         [-1,-1,-1, 0, 1,-1,-1,-1],
         [-1,-1,-1, 0, 0,-1,-1,-1],
         [-1,-1,-1, 0,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         ]
    board2 = [[random.choice([-1,0,1]) for i in range(8)] for j in range(8)] #create a board full of random 0,1,-1

    player = MyPlayer(1,0)
    print(player.move(board))
 

        