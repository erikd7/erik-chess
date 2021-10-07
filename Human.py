#human move file

import GameSetup
import ValidMove
import Pieces
import MakeMove
import copy
import Game


def human_move(c):    
    valid = False
    while not valid:
        move_input = input(f"{GameSetup.color_display.get(c,c)} - enter move: ")
        
        #skip nonsensical input
        try:
            #split input
            f_rank = int(move_input[1])-1
            f_file = GameSetup.file_to_number.get(move_input[0], "Invalid File - Must be A-H")-1
            t_rank = int(move_input[4])-1
            t_file = GameSetup.file_to_number.get(move_input[3], "Invalid File - Must be A-H")-1
        
        except:
            print("Invalid entry. Try again.")
            continue#go back to top of loop
            
         #are moves in valid range
        if(not (0 <= f_rank <= 7 and 0 <= f_file <= 7 and 0 <= t_rank <= 7 and 0 <= t_file <= 7)):
            print("Invalid entry. Rank must be 1-8 and file must be A-H.")
            return 0
    
        #is move legal
        valid = ValidMove.valid_move(f_rank,f_file,t_rank,t_file,c,Game.cMan)
        
    #now that we know it's legal, make the move
    Pieces.update_pieces(f_rank,f_file,t_rank,t_file,c,Game.cMan.board)
    MakeMove.real(f_rank,f_file,t_rank,t_file)
    
            
    return
    