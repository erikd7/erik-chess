#make the actual move or a test move
import copy
import Game,Pieces

#FINAL MAKE MOVE FUNCTION SHOULD JUST UPDATE TEMPS TO GLOBALS

def real(f_rank,f_file,t_rank,t_file):
    
    #updates Game.cMan
    pre(f_rank,f_file,t_rank,t_file)
    
    #just update the master board with the board that's being passed in
    Game.Master = copy.deepcopy(Game.cMan)
    
    #check
    if(Game.Master.check_white == True): print("White is in check.")
    elif(Game.Master.check_black == True): print("Black is in check.")
    
    #update currently manipulated board for next turn
    #Game.cMan = copy.deepcopy(Game.Master)
        
    return


def just_piece(f_rank,f_file,t_rank,t_file,test_board = Game.cMan.board):
    
    test_board = copy.deepcopy(test_board)#necessary to make sure the board is separate, since python ties array data together
    test_board[t_rank,t_file] = test_board[f_rank,f_file]#piece goes to new square
    test_board[f_rank,f_file] = "000"#existing square is cleared
    
    print("well now then")
    if(test_board[t_rank,t_file][1]=="p" and abs(t_rank-f_rank)==2):
        Game.cMan.en_passant_target = t_file
        print(f"up {Game.cMan.en_passant_target}")
    
    return test_board


def test(f_rank,f_file,t_rank,t_file,test_board=Game.cMan.board):
    
    pre(f_rank,f_file,t_rank,t_file)
    
    return

def pre(f_rank,f_file,t_rank,t_file):
    Game.cMan.board[t_rank,t_file] =  Game.cMan.board[f_rank,f_file]#piece goes to new square
    Game.cMan.board[f_rank,f_file] = "000"#existing square is cleared
    
    #if it's a king or a rook, need some additional code for castling
    if(Game.cMan.board[t_rank,t_file][1] == "k" or Game.cMan.board[t_rank,t_file][1] == "r"):
        turn_castle(f_rank,f_file,t_rank,t_file)
    
    #en passant
    Game.cMan.en_passant_target = ""#reset--lasts only one move
    if(Game.cMan.board[t_rank,t_file][1]=="p" and abs(t_rank-f_rank)==2):
        Game.cMan.en_passant_target = t_file

    return

def turn_castle(f_rank,f_file,t_rank,t_file):
    #special for castle--2 pieces move
    if(Game.cMan.board[t_rank,t_file][1]=="k" and abs(t_file-f_file)>1):#to rank/file bc we already updated the board
        #white castle-kingside then queenside
        if(f_rank == 0 and t_file==1):
            #now need to update possible moves
            Pieces.update_pieces(0,0,0,2,"w",Game.cMan.board)
            #now make the second move (rook)
            Game.cMan.board = just_piece(0,0,0,2)
        if(f_rank == 0 and t_file==5):
            #now need to update possible moves
            Pieces.update_pieces(0,7,0,4,"w",Game.cMan.board)
            #now make the second move (rook)
            Game.cMan.board = just_piece(0,7,0,4)
        #black castle-kingside then queenside
        if(f_rank == 7 and t_file==1):
            #now need to update possible moves
            Pieces.update_pieces(7,0,7,2,"b",Game.cMan.board)
            #now make the second move (rook)
            Game.cMan.board = just_piece(7,0,7,2)
        if(f_rank == 7 and t_file==5):
            #now need to update possible moves
            Pieces.update_pieces(7,7,7,4,"b",Game.cMan.board)
            #now make the second move (rook)
            Game.cMan.board = just_piece(7,7,7,4)
    
        #update castling rights. in this block, we actually castled
        if(Game.cMan.board[t_rank,t_file]=="wke"):
            Game.cMan.castle_kingside_white = Game.cMan.castle_queenside_white = False
        elif(Game.cMan.board[t_rank,t_file]=="bke"):
            Game.cMan.castle_kingside_black = Game.cMan.castle_queenside_black = False
        
    #more updates to castle rights. here, we did not castle but the king moved    
    if(Game.cMan.board[f_rank,f_file] == "wke"):
        Game.cMan.castle_kingside_white = Game.cMan.castle_queenside_white = False
        return #saves us from checking rooks if it we already know a king was moved
    if(Game.cMan.board[f_rank,f_file] == "bke"):
        Game.cMan.castle_kingside_black = Game.cMan.castle_queenside_black = False
        return #saves us from checking rooks if it we already know a king was moved
    
    #rooks moving
    if(Game.cMan.board[f_rank,f_file] == "wrh" and Game.cMan.castle_kingside_white == True): Game.cMan.castle_kingside_white = False
    if(Game.cMan.board[f_rank,f_file] == "wra" and Game.cMan.castle_queenside_white == True): Game.cMan.castle_queenside_white = False
    if(Game.cMan.board[f_rank,f_file] == "brh" and Game.cMan.castle_kingside_black == True): Game.cMan.castle_kingside_black = False
    if(Game.cMan.board[f_rank,f_file] == "bra" and Game.cMan.castle_queenside_black == True): Game.cMan.castle_queenside_black = False

    return