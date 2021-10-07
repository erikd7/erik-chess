#status of check
import Game,GameSetup
import numpy as np

def check_impacted(p):#receives a piece, updates check status, and returns if that piece is checking the white or black king
    #find king
    wking = GameSetup.rf_to_square(np.where(Game.cMan.board == "wke")[0][0],np.where(Game.cMan.board == "wke")[1][0])
    bking = GameSetup.rf_to_square(np.where(Game.cMan.board == "bke")[0][0],np.where(Game.cMan.board == "bke")[1][0])
    
    moves = getattr(Game.cMan,p)
    if(not moves):#if it's empty, no need for the below
        return
    
    if(p[0]=="w" and bking in moves):
        Game.cMan.check_black=True
        return "b"
    if(p[0]=="b" and wking in moves):
        Game.cMan.check_white=True
        return "w"
        
    #DOESN"T ACCOUNT FOR PAWNS--POSSIBLE MOVES NOT SAME AS DIAG CHECK MOVES
    
    return 0

def check_impacted_illegal(p):#illegal--can't end a turn in check (move into or fail to evade)
    #receives a piece, removes illegal moves, and returns if that piece is effectively moving its own color into check
    #find king
    wking = GameSetup.rf_to_square(np.where(Game.cMan.board == "wke")[0][0],np.where(Game.cMan.board == "wke")[1][0])
    bking = GameSetup.rf_to_square(np.where(Game.cMan.board == "bke")[0][0],np.where(Game.cMan.board == "bke")[1][0])
    
    moves = getattr(Game.cMan,p)
    if(not moves):#if it's empty, no need for the below
        return
    
    if(p[0]=="w" and bking in moves):
        return "b"
    if(p[0]=="b" and wking in moves):
        Game.cMan.check_white=True
        return "w"
        
    #DOESN"T ACCOUNT FOR PAWNS--POSSIBLE MOVES NOT SAME AS DIAG CHECK MOVES
    
    return 0
