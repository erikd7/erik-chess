#this is the gameplay file

#import ancillary files
import GameSetup
import Human, Game

#run the game
color_human = "w"
color_pc = "b"

#create the master board


while Game.Master.mate == False:
    GameSetup.print_board()
    
    Human.human_move(color_human)
    
    if(Game.Master.mate==True): break
    print("- - - - - ")
    
    GameSetup.print_board()
    
    Human.human_move(color_pc)
    
#if you're in check, only allowable moves are into the check vector or move the king
#if you're not in check, only allowable moves are not out of the check vector
#in other words, can only move into the opposing check vector, not out of