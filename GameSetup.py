#setup for the game
import numpy as np
import Game,copy



color_display = {
    "b": "Black",
    "w": "White",
}

color_opponent = {
    "b": "w",
    "w": "b",
        }
        
#convert file to number dictionary. backwards because i built the game with the wrong rank/file setup
file_to_number = {
    "h": 1,
    "g": 2,
    "f": 3,
    "e": 4,
    "d": 5,
    "c": 6,
    "b": 7,
    "a": 8,}

number_to_file = {n: f for f, n in file_to_number.items()}

list_pieces = {
    0:"r",
    1:"n",
    2:"b",
    3:"q",
    4:"p",
    5:"k",
        }

def rf_to_square(rank,file):#takes two numbers and returns a rank and a file
    #*rank is 1-8, which is why we have to add 1. file is 1-8 with letters h-a, which is why we have to subtract 1
    return number_to_file.get(file+1) + str(rank+1)

def piece_to_rf(piece,board=Game.Master.board):
    r = np.where(board == piece)
    return r[0][0],r[1][0]

def square_to_nums(square):#rank and file 0-7
    
    return int(square[1])-1,int(file_to_number.get(square[0]))-1

#print a pretty board
def print_board():
    display_board=copy.deepcopy(Game.Master.board)
    np.place(display_board, display_board == "000","___")
    for r in range(0,8):
        for f in range(0,8):
            display_board[r,f]=display_board[r,f][:-1]#replace third char
    print(np.append([[" "],[1],[2],[3],[4],[5],[6],[7],[8]],np.append([["h ","g ","f ","e ","d ","c ","b ","a "]],display_board,axis=0),axis=1))
    
    return

#get a movement vector of a to b
def movement_vector(a_rank,a_file,b_rank,b_file,board=Game.Master.board):
    #right and down is increasing
    r=f=1#moves right and down
   
    if(a_file>b_file):#goes left
        f=-1
    #elif(a_file < b_file]):#goes right
        #x=1         --- comment out -- captured in initialization
    elif(a_file==b_file):#same file
        f=0
    if(a_rank>b_rank):#goes up
        r=-1
   # elif(a_rank>b_rank):#goes up
       # y=1
    elif(a_rank==b_rank):#same rank
        r = 0
    #if((y != 0) and abs((a_file - b_file)/(a_rank - b_rank)) == 1):
        #same_diag = 1
    
    return r,f

def add_possible_move(piece,r,f):
    current = getattr(Game.cMan,piece)
    new = rf_to_square(r,f)
    
    #do a quick call out for if the list is empty--empty list is boolean False, cannot append
    if(not current):
        setattr(Game.cMan,piece,[new])
        
    elif(new not in current):
        current.append(new)
        setattr(Game.cMan,piece,current)


    #print(f"adding {new} to {piece}")
    return

def subtract_possible_move(piece,r,f):
    current = getattr(Game.cMan,piece)
    new = rf_to_square(r,f)
    
    #do a quick call out for if the list is empty--empty list is boolean False, no action needed
    if(not current):
        return
    
    if(new in current):
        current.remove(new)
        setattr(Game.cMan,piece,current)
    
    #print(f"removing {new} from {piece}")
    return

def clear_all_moves(piece):
    current = getattr(Game.cMan,piece)
    
    #do a quick call out for if the list is empty--empty list is boolean False, no action needed
    if(not current):
        return
    else:
        current.clear()
        setattr(Game.cMan,piece,current)
    
    #print(f"clearing {piece}")
    return