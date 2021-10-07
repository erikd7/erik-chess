#is move valid
import GameSetup


def valid_move(f_rank,f_file,t_rank,t_file,c,fullBoard):
    board = fullBoard.board
    
    #are moves legal--basics of moving pieces
    if(not (board[f_rank,f_file][0]==c and board[t_rank,t_file][0]!=c)):#have to move the correct color piece, and the destination square cannot be occupied by your piece
        print("You must move your own piece to an empty square or take an opponent's piece.")
        return 0
        #if(globals()["Globals." + Globals.board[f_rank,f_file]])
    
    
    #are moves possible -- check current list of available moves    
    move = GameSetup.rf_to_square(t_rank,t_file)
    piece = board[f_rank,f_file]
    available = getattr(fullBoard,piece)
    
    if move in available:
        return 1
    
    
    #if it hasn't been met yet, it is an invalid move
    print("Illegal move. Enter another:")
    return 0

