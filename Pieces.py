#where can each piece go
import GameSetup,MakeMove,Game,Check

#get a list of the pieces whose possible squares will be changed by this new move
def impacted_from(f_rank,f_file,t_rank,t_file,c,board=Game.cMan.board):
    
    impacted = list([])#[board[f_rank,f_file]])
    #FOR LATER -- consider limiting search based on the to->from vector (don't need to search for impacted pieces along that)
    
    #diff to/from
    rank = f_rank
    file = f_file
    
    for x in (-1,1):#test files along one rank--only X matters (moved these out of the big loop because was duplicating--when Y is 1 or -1, this block is the same)
        for i in range(1,8):
            if(not (0 <= rank <= 7 and 0 <= file-(i*x) <= 7)):#keep it within the bounds of the board. could one day just incorporate this into the loop conditional but i don't feel like it rn
                break
            if(board[rank,file-(i*x)][1]=="r" or board[rank,file-(i*x)][1]=="q" or (i == 1 and board[rank,file-x][1]=="k")):#if the square is a rook or queen, or it's a king that moved 1 square
                impacted.append(board[rank,file-(i*x)])
                break#break because, if we hit a piece in this direction, shouldn't keep looking in that direction
            if(board[rank,file-(i*x)] != "000"):break #if we hit a piece that can't move to this square
    
    for y in (-1,1):#test ranks along one file--only Y matters
        for i in range(1,8):                
            if(not (0 <= rank-(i*y) <= 7 and 0 <= file <= 7)):#keep it within the bounds of the board. could one day just incorporate this into the loop conditional but i don't feel like it rn
                break#break the loop with i -- stop moving in that direction
            if((i == 1 or (i == 2 and ((c == "w" and f_rank == 1) or (c == "b" and f_rank == 6)))) and ((0 <= rank-(i) <= 7 and board[rank-(i),file][0:2]=="wp") or (0 <= rank+(i) <= 7 and board[rank+(i),file][0:2]=="bp"))):#pawn forward, including double-move from starting squares. does not look at interim square, which should be caught by above code
                if(board[rank-(i),file][0:2]=="wp"): impacted.append(board[rank-i,file])
                if(board[rank+(i),file][0:2]=="bp"): impacted.append(board[rank+i,file])
                break
            if(board[rank-(i*y),file][1]=="r" or board[rank-(i*y),file][1]=="q" or (i == 1 and board[rank-y,file][1]=="k")):#if the square is a rook or queen, or it's a king that moved 1 square
                impacted.append(board[rank-(i*y),file])
                break
            if(board[rank-(i*y),file] != "000"):break
    
    for x in (-1,1):#test moving along both ranks and files
        #diag pawns
        if(c=="w" and 0 <= rank+1 <= 7 and 0 <= file-x <= 7):
            if(board[rank+1,file-x][0:2]=="bp"):#pawn diag if can take
                impacted.append(board[rank+1,file-x])
                continue
        if(c=="b" and 0 <= rank-1 <= 7 and 0 <= file-x <= 7):
            if(board[rank-1,file-x][0:2]=="wp"):#pawn diag if can take
                impacted.append(board[rank-1,file-x])
                continue
        for y in (-1,1):            
        #test along diag--X and Y matter
            for i in range(1,8):
                if(not (0 <= rank-(i*y) <= 7 and 0 <= file-(i*x) <= 7)):#keep it within the bounds of the board. could one day just incorporate this into the loop conditional but i don't feel like it rn
                    break
                if(board[rank-(i*y),file-(i*x)][1]=="b" or board[rank-(i*y),file-(i*x)][1]=="q" or (i == 1 and board[rank-y,file-x][1]=="k")):
                    impacted.append(board[rank-(i*y),file-(i*x)])
                    break
                if(board[rank-(i*y),file-(i*x)] != "000"): break
                
   #knights!
    for x in (-1,1):#test all directions
        for y in (-1,1):
            if(0 <= rank+1*y <= 7 and 0 <= file+2*x <= 7 and board[rank+1*y,file+2*x][1]=="n"):
                impacted.append(board[rank+1*y,file+2*x])
            if(0 <= rank+2*y <= 7 and 0 <= file+1*x <= 7 and board[rank+2*y,file+1*x][1]=="n"):
                impacted.append(board[rank+2*y,file+1*x])
    
#    #en passant
#    for f in (-1,1):
#        if(board[rank,file][1]=="p" and abs(f_rank-t_rank)==2 and 0<=file+f<=7):
#            if(board[rank,file+f][0:2]==GameSetup.color_opponent.get(c)+"p"):
#                impacted.append(board[rank,file+f]) 
                
    #odd case - castling -- kings can move 2 squares
    for x in (-1,1):#test files along one rank--only X matters (moved these out of the big loop because was duplicating--when Y is 1 or -1, this block is the same)
        for i in range(2,4):#already checked 1 space for kings above--now check 2 (kingside) and 3 (queenside)
            if(not (0 <= rank <= 7 and 0 <= file-(i*x) <= 7)):#keep it within the bounds of the board. could one day just incorporate this into the loop conditional but i don't feel like it rn
                continue#continue rather than break--this tests both directions
            if((rank==0 or rank==7) and board[rank,file-i*x][1]=="k"):#if the square is a rook or queen, or it's a king that moved 1 square
                impacted.append(board[rank,file-(i*x)])
                break#break because, if we hit a piece in this direction, shouldn't keep looking in that direction
            if(board[rank,file-(i*x)] != "000"):break #if we hit a piece that can't move to this square
    
    return impacted

def impacted_to(f_rank,f_file,t_rank,t_file,c,board=Game.cMan.board):
    
    impacted = list([])
    #FOR LATER -- consider limiting search based on the to->from vector (don't need to search for impacted pieces along that)
    
    rank = t_rank
    file = t_file
    
    for x in (-1,1):#test files along one rank--only X matters (moved these out of the big loop because was duplicating--when Y is 1 or -1, this block is the same)
        for i in range(1,8):
            if(not (0 <= rank <= 7 and 0 <= file-(i*x) <= 7)):#keep it within the bounds of the board. could one day just incorporate this into the loop conditional but i don't feel like it rn
                continue#continue rather than break--this tests both directions
            if(board[rank,file-(i*x)][1]=="r" or board[rank,file-(i*x)][1]=="q" or (i == 1 and board[rank,file-x][1]=="k")):#if the square is a rook or queen, or it's a king that moved 1 square
                impacted.append(board[rank,file-(i*x)])
                continue#continue because, if we hit a piece in this direction, shouldn't keep looking in that direction
            elif(board[rank,file-(i*x)] != "000"):break #if we hit a piece that can't move to this square
    
    for y in (-1,1):#test ranks along one file--only Y matters
        for i in range(1,8):                
            if(not (0 <= rank-(i*y) <= 7 and 0 <= file <= 7)):#keep it within the bounds of the board. could one day just incorporate this into the loop conditional but i don't feel like it rn
                break#break the loop with i -- stop moving in that direction
            if(board[rank-(i*y),file][1]=="r" or board[rank-(i*y),file][1]=="q" or (i == 1 and board[rank-y,file][1]=="k")):#if the square is a rook or queen, or it's a king that moved 1 square
                impacted.append(board[rank-(i*y),file])
                break
            if((i == 1 or (i == 2 and ((c == "w" and f_rank == 1) or (c == "b" and f_rank == 6)))) and board[rank-(i*y),file][1]=="p"):#pawn forward, including double-move from starting squares. does not look at interim square, which should be caught by above code
                impacted.append(board[rank-(i*y),file])
                break
            elif(board[rank-(i*y),file] != "000"):break
    
    for x in (-1,1):#test moving along both ranks and files
        #diag pawns
        if(c=="w" and 0 <= rank+1 <= 7 and 0 <= file-x <= 7):
            if(board[rank+1,file-x][0:2]=="bp"):#pawn diag if can take
                impacted.append(board[rank+1,file-x])
                continue
        if(c=="b" and 0 <= rank-1 <= 7 and 0 <= file-x <= 7):
            if(board[rank-1,file-x][0:2]=="wp"):#pawn diag if can take
                impacted.append(board[rank-1,file-x])
                continue
                
        for y in (-1,1):            
            
        #test along diag--X and Y matter
            for i in range(1,8):
                if(not (0 <= rank-(i*y) <= 7 and 0 <= file-(i*x) <= 7)):#keep it within the bounds of the board. could one day just incorporate this into the loop conditional but i don't feel like it rn
                    break
                if(board[rank-(i*y),file-(i*x)][1]=="b" or board[rank-(i*y),file-(i*x)][1]=="q" or (i == 1 and board[rank-y,file-x][1]=="k")):
                    impacted.append(board[rank-(i*y),file-(i*x)])
                    break
                elif(board[rank-(i*y),file-(i*x)] != "000"): break
                
   #knights!
    for x in (-1,1):#test all directions
        for y in (-1,1):
            if(0 <= rank+1*y <= 7 and 0 <= file+2*x <= 7 and board[rank+1*y,file+2*x][1]=="n"):
                impacted.append(board[rank+1*y,file+2*x])
            if(0 <= rank+2*y <= 7 and 0 <= file+1*x <= 7 and board[rank+2*y,file+1*x][1]=="n"):
                impacted.append(board[rank+2*y,file+1*x])
        
    #en passant
    for f in (-1,1):
        if(board[f_rank,f_file][1]=="p" and abs(f_rank-t_rank)==2 and 0<=t_file+f<=7):
            if(board[t_rank,t_file+f][0:2]==GameSetup.color_opponent.get(c)+"p"):
                impacted.append(board[t_rank,t_file+f])   
    
    #odd case - castling -- kings can move 2 squares
    for x in (-1,1):#test files along one rank--only X matters (moved these out of the big loop because was duplicating--when Y is 1 or -1, this block is the same)
        for i in range(2,4):#already checked 1 space for kings above--now check 2 (kingside) and 3 (queenside)
            if(not (0 <= rank <= 7 and 0 <= file-(i*x) <= 7)):#keep it within the bounds of the board. could one day just incorporate this into the loop conditional but i don't feel like it rn
                continue#continue rather than break--this tests both directions
            if((rank==0 or rank==7) and board[rank,file-i*x][1]=="k"):#if the square is a rook or queen, or it's a king that moved 1 square
                impacted.append(board[rank,file-(i*x)])
                break#break because, if we hit a piece in this direction, shouldn't keep looking in that direction
            if(board[rank,file-(i*x)] != "000"):break #if we hit a piece that can't move to this square
        
    return impacted

def update_pieces(f_rank,f_file,t_rank,t_file,c,board=Game.cMan.board):
    #impacted_dup = np.append(impacted_from(f_rank,f_file,t_rank,t_file,c,board),impacted_to(f_rank,f_file,t_rank,t_file,c,board))
    imp_f = impacted_from(f_rank,f_file,t_rank,t_file,c,board)
    imp_t = impacted_to(f_rank,f_file,t_rank,t_file,c,board)
    
    #we already know the pieces that need updates, which is all based on to/from square with exceptions for (castling? promotion?)
    
    #before we update the board, save what piece actually moved
    m = board[f_rank,f_file]
    
    board = MakeMove.just_piece(f_rank,f_file,t_rank,t_file,board)

    
    for i in imp_f:
        if i not in board:#if piece has been taken -- clear all moves and go to next piece
            GameSetup.clear_all_moves(i)
            continue
            
        #first convert piece to a rank and a file
        a_rank = GameSetup.piece_to_rf(i,board)[0]
        a_file = GameSetup.piece_to_rf(i,board)[1]
        
        #color of affected piece
        ac = board[a_rank,a_file][0]
        
        #get movement vector-- moved piece to affected piece
        v = GameSetup.movement_vector(f_rank,f_file,a_rank,a_file,board)
        
        moves_subtract(a_rank,a_file,f_rank,f_file,ac,board,i,v,m)
        moves_add(a_rank,a_file,f_rank,f_file,ac,board,i,v,m)
        
        #Check.check_impacted_illegal(i)
        Check.check_impacted(i)
        
        print(i,getattr(Game.cMan,i))
     

    for i in imp_t:
        if i not in board:#if piece has been taken -- clear all moves and go to next piece
            GameSetup.clear_all_moves(i)
            continue
        
        #first convert piece to a rank and a file
        a_rank = GameSetup.piece_to_rf(i,board)[0]
        a_file = GameSetup.piece_to_rf(i,board)[1]
        
        #color of affected piece
        ac = board[a_rank,a_file][0]
        
        #get movement vector-- moved piece to affected piece
        v = GameSetup.movement_vector(t_rank,t_file,a_rank,a_file,board)
        
        #run subtract function before we added moves based on from square so we don't clear out new things
        moves_subtract(a_rank,a_file,t_rank,t_file,ac,board,i,v,m)
        moves_add(a_rank,a_file,t_rank,t_file,ac,board,i,v,m)
        
        #Check.check_impacted_illegal(i)
        Check.check_impacted(i)
        
        print(i,getattr(Game.cMan,i))
            
    return

def moves_add(a_rank,a_file,m_rank,m_file,c,board,p,v,m):
    #a - affected piece; m - moving piece (to or from depending on where it's called from)
    
    #right and down is positive
    r = v[0]
    f = v[1]
    #v is moved piece to affected piece
    piece = p[1]
    
    oc = GameSetup.color_opponent.get(c)
    
    #use d because in some cases, always want to test same direction fro same color. also, if p==m, r=0
    if(p[0]=="w"): d=1
    elif(p[0]=="b"): d=-1 
    
    if(piece == "p"):#note that rank boundary checks done in impacted fx
        if(board[a_rank+d,a_file]=="000"):#forward space is empty
            GameSetup.add_possible_move(p,a_rank+d,a_file)
        
        #special for pawns--can move diags as well
        if(f!=0 and r!=0 and board[a_rank-r,a_file-f][0]==oc):#pawn diag if can take. note: don't need to test bounds here bc this was defined per impacted pieces. others below were not
            GameSetup.add_possible_move(p,a_rank-r,a_file-f)
            
        #if this is the actual moving piece, need to test both diags, since f might be 0
        if(p==m):#if this is the moving piece, have to do a bit more
            if(f!=0 and 0 <= a_file+f <= 7 and board[a_rank+d,a_file+f][0]==oc):#if f is nonzero, meaning we already checked one diag, we just have to check the other
                GameSetup.add_possible_move(p,a_rank+d,a_file+f)
            else:#otherwise, if f is zero, have to check both diags
                if(0 <= a_file+1 <= 7 and board[a_rank+d,a_file+1][0]==oc):
                    GameSetup.add_possible_move(p,a_rank+d,a_file+1)
                if(0 <= a_file-1 <= 7 and board[a_rank+d,a_file-1][0]==oc):
                    GameSetup.add_possible_move(p,a_rank+d,a_file-1)
        #en passant
        print(Game.cMan.en_passant_target)
        if(Game.cMan.en_passant_target!="" and ((m[0]=="w" and a_rank==3) or (m[0]=="b" and a_rank==4))):
            print("well")
            print(a_file)
            if(a_file == Game.cMan.en_passant_target+1):
                GameSetup.add_possible_move(p,a_rank+d,a_file+1)
                print("adding here1")
                print(a_rank,a_file,d)
            elif(a_file == Game.cMan.en_passant_target-1):
                GameSetup.add_possible_move(p,a_rank+d,a_file-1)
                print("adding here")
                print(a_rank,a_file,d)

                
    if(piece == "b" or piece == "q" or piece == "r"):#rook and queen can be included because either r or f will be zero. only need to test 1 direction (per v), so queen is okay
        for i in range(1,8):
            if(not (0 <= a_rank-(i*r) <= 7 and 0 <= a_file-(i*f) <= 7)): break
            if(board[a_rank-(i*r),a_file-(i*f)]=="000"):#if blank, add as possible and keep going
                GameSetup.add_possible_move(p,a_rank-(i*r),a_file-(i*f))
            elif(board[a_rank-(i*r),a_file-(i*f)][0]==oc):#if opposition, add as possible and STOP
                GameSetup.add_possible_move(p,a_rank-(i*r),a_file-(i*f))
                break
            else: break#otherwise, it's your own piece -- STOP
        if(p == m and p[1] == "q"):#if this is the piece that itself moved, test everything a bishop can get to
            for y in (-1,0,1):
                for x in (-1,0,1):
                    for i in range(1,8):
                        if(not (0 <= a_rank-(i*y) <= 7 and 0 <= a_file-(i*x) <= 7)): break
                        if(board[a_rank-i*y,a_file-i*x]=="000"):#if blank, add as possible and keep going
                            GameSetup.add_possible_move(p,a_rank-i*y,a_file-i*x)
                        elif(board[a_rank-i*y,a_file-i*x][0]==oc):#if opposition, add as possible and STOP
                            GameSetup.add_possible_move(p,a_rank-i*y,a_file-i*x)
                            break
                        else: break#otherwise, it's your own piece -- STOP 
        if(p == m and p[1] == "b"):#if this is the piece that itself moved, test everything a bishop can get to
            for y in (-1,1):
                for x in (-1,1):
                    for i in range(1,8):
                        if(not (0 <= a_rank-(i*y) <= 7 and 0 <= a_file-(i*x) <= 7)): break
                        if(board[a_rank-i*y,a_file-i*x]=="000"):#if blank, add as possible and keep going
                            GameSetup.add_possible_move(p,a_rank-i*y,a_file-i*x)
                        elif(board[a_rank-i*y,a_file-i*x][0]==oc):#if opposition, add as possible and STOP
                            GameSetup.add_possible_move(p,a_rank-i*y,a_file-i*x)
                            break
                        else: break#otherwise, it's your own piece -- STOP
        if(p == m and p[1] == "r"):#if this is the piece that itself moved, test everything a bishop can get to
            for y in (-1,0,1):
                x=0
                for i in range(1,8):
                        if(not (0 <= a_rank-(i*y) <= 7 and 0 <= a_file-(i*x) <= 7)): break
                        if(board[a_rank-i*y,a_file-i*x]=="000"):#if blank, add as possible and keep going
                            GameSetup.add_possible_move(p,a_rank-i*y,a_file-i*x)
                        elif(board[a_rank-i*y,a_file-i*x][0]==oc):#if opposition, add as possible and STOP
                            GameSetup.add_possible_move(p,a_rank-i*y,a_file-i*x)
                            break
                        else: break#otherwise, it's your own piece -- STOP 
                for x in (-1,0,1):
                    y=0
                    for i in range(1,8):
                        if(not (0 <= a_rank-(i*y) <= 7 and 0 <= a_file-(i*x) <= 7)): break
                        if(board[a_rank-i*y,a_file-i*x]=="000"):#if blank, add as possible and keep going
                            GameSetup.add_possible_move(p,a_rank-i*y,a_file-i*x)
                        elif(board[a_rank-i*y,a_file-i*x][0]==oc):#if opposition, add as possible and STOP
                            GameSetup.add_possible_move(p,a_rank-i*y,a_file-i*x)
                            break
                        else: break#otherwise, it's your own piece -- STOP 
    
    if(piece == "n"):#since we know direction, there are 2 spots per direction to test
        if(m!=p and board[m_rank,m_file]=="000"):#if something else moved and the knight is affected
            GameSetup.add_possible_move(p,m_rank,m_file)
        if(m==p):#if the knight itself moved, we need to update everything
            for x in (-1,1):
                for y in (-1,1):
                    if(0 <= a_rank+1*y <= 7 and 0 <= a_file+2*x <= 7 and (board[a_rank+1*y,a_file+2*x][0]==oc or board[a_rank+1*y,a_file+2*x]=="000")):
                        GameSetup.add_possible_move(p,a_rank+1*y,a_file+2*x)
                    if(0 <= a_rank+2*y <= 7 and 0 <= a_file+1*x <= 7 and (board[a_rank+2*y,a_file+1*x][0]==oc or board[a_rank+2*y,a_file+1*x]=="000")):
                        GameSetup.add_possible_move(p,a_rank+2*y,a_file+1*x)
  
    if(piece == "k"):
        if(0 <= a_rank-r <= 7 and 0 <= a_file-f <= 7):
            if(board[a_rank-r,a_file-f]=="000" or board[a_rank-r,a_file-f][0]==oc):
                if(not(board[a_rank-r*2,a_file-f*2][0:2]==oc+"k")):#can't move within 1 square of the other king
                    GameSetup.add_possible_move(p,a_rank-r,a_file-f)  
            #bonus round for kings -- castling
            king_moves(a_rank,a_file,m_rank,m_file,c,board,p,v,m)
    
    return


def moves_subtract(a_rank,a_file,m_rank,m_file,c,board,p,v,m):#this could overall be smarter
    #is move legal? just delete anything that's affected (along v), add stuff back in other fx
    #list of currently legal moves for p
    moves = getattr(Game.cMan,p)
    if(not moves):#if it's empty, no need for the below
        return
    
    #clear out the piece that moved. no great way to tell what it should be without testing very thoroughly, which we do in add function anyways
    if(p == m):
        for n in moves:
            rf = GameSetup.square_to_nums(n)
            GameSetup.subtract_possible_move(p,rf[0],rf[1])
    
    r=v[0]
    f=v[1]
    
    #if moved piece is now in a square that is a possible move
    m_square = GameSetup.rf_to_square(m_rank,m_file)
    if(m_square in moves):
        GameSetup.subtract_possible_move(p,m_rank,m_file)
        
    #also need to cover situation where p has a ray of possible moves that should now be erased
    #is move along v
    for i in range(1,8):
        if(not (0<=m_rank-r*i<=7 and 0<=m_file-f*i<=7)):break
        m_square_next = GameSetup.rf_to_square(m_rank-r*i,m_file-f*i)
        if(m_square_next in moves):
            GameSetup.subtract_possible_move(p,m_rank-r*i,m_file-f*i)
        else: break#if the next square in the ray is not movable, nothing else should be either
    
#    #pawns--have to clear behind them since they can't move backwards
    if(p[1] == "p" and p!=m):#this is pretty ugly--just added a bunch of stuff since i was having issues. should clean up--overtesting
        for i in (-1,0,1):
            a_square_next = GameSetup.rf_to_square(a_rank+r,a_file+f*i)
            if(a_square_next in moves):
                GameSetup.subtract_possible_move(p,a_rank+r,a_file+f*i)
                
    #just to check, clear current space from possible moves
    GameSetup.subtract_possible_move(p,a_rank,a_file)

    
    return 

def king_moves(a_rank,a_file,m_rank,m_file,c,board,p,v,m):
    #castle
    if(Game.cMan.castle_kingside_white==True and (GameSetup.rf_to_square(0,1) in Game.cMan.wrh) and (GameSetup.rf_to_square(0,2) in Game.cMan.wrh) and Game.cMan.board[0,0]=="wrh" and Game.cMan.check_white==False):#rights, spaces are free, not in check currently
        if(not (any_possible_check(0,2,"b"))):#intermediate spaces not in check
            GameSetup.add_possible_move(p,0,1)
    if(Game.cMan.castle_queenside_white==True and (GameSetup.rf_to_square(0,4) in Game.cMan.wra) and (GameSetup.rf_to_square(0,5) in Game.cMan.wra) and (GameSetup.rf_to_square(0,6) in Game.cMan.wra) and Game.cMan.board[0,7]=="wra" and Game.cMan.check_white==False):#rights, spaces are free, not in check currently
        if(not (any_possible_check(0,4,"b") or any_possible_check(0,6,"b"))):#intermediate spaces not in check
            GameSetup.add_possible_move(p,0,5)
            
    if(Game.cMan.castle_kingside_black==True and (GameSetup.rf_to_square(7,1) in Game.cMan.brh) and (GameSetup.rf_to_square(7,2) in Game.cMan.brh) and Game.cMan.board[7,0]=="brh" and Game.cMan.check_black==False):#rights, spaces are free, not in check currently
        if(not (any_possible_check(7,2,"w"))):#intermediate spaces not in check
            GameSetup.add_possible_move(p,7,1)
    if(Game.cMan.castle_queenside_black==True and (GameSetup.rf_to_square(7,4) in Game.cMan.bra) and (GameSetup.rf_to_square(7,5) in Game.cMan.bra) and (GameSetup.rf_to_square(7,6) in Game.cMan.bra) and Game.cMan.board[7,7]=="bra" and Game.cMan.check_black==False):#rights, spaces are free, not in check currently
        if(not (any_possible_check(0,4,"w") or any_possible_check(0,6,"w"))):#intermediate spaces not in check
            GameSetup.add_possible_move(p,7,5)
    
    return

def any_possible_check(rank,file,search_set):
    test = GameSetup.rf_to_square(rank,file)
    
    for r in range(0,8):
        for f in range(0,8):
            if Game.cMan.board[r,f][0]==search_set:
                if(Game.cMan.board[r,f][1]!="p"):
                    moves = getattr(Game.cMan,Game.cMan.board[r,f])
                    if test in moves:
                        return 1
                else:#stupid pawns ruining everything--don't check how they move
                    pawn_rank = 1
                    if(search_set == "w"): pawn_rank = -1
                    for i in (-1,1):
                        if(not (0<=file+i<=7)):continue
                        if(Game.cMan.board[rank+pawn_rank,file+i][0:2]==search_set+"p"):
                            return 1

    return 0
