#game
import numpy as np
import GameSetup

class chessBoard:
    
    #create variables
    def fresh(self):
        #the board
        self.mate = False
        
        self.board = np.array([['wrh','wng','wbf',"wke",'wqd','wbc','wnb','wra'],
                          ['wph','wpg','wpf','wpe','wpd','wpc','wpb','wpa'],["000","000","000","000","000","000","000","000"],["000","000","000","000","000","000","000","000"],["000","000","000","000","000","000","000","000"],["000","000","000","000","000","000","000","000"],
                          ['bph','bpg','bpf','bpe','bpd','bpc','bpb','bpa'],
                          ["brh","bng",'bbf','bke','bqd','bbc','bnb','bra']])
        
        #check status
        self.check_white = False
        self.check_black = False
        
        #castling rights
        self.castle_kingside_white = True
        self.castle_queenside_white = True
        self.castle_kingside_black = True
        self.castle_queenside_black = True
        
        #initialize movements for pieces
        self.wrh = self.wbf = self.wke = self.wqd = self.wbc = self.wra = []
        
        self.wph = ["h3","h4"]
        self.wpg = ["g3","g4"]
        self.wpf = ["f3","f4"]
        self.wpe = ["e3","e4"]
        self.wpd = ["d3","d4"]
        self.wpc = ["c3","c4"]
        self.wpb = ["b3","b4"]
        self.wpa = ["a3","a4"]
        self.wng = ["h3","f3"]
        self.wnb = ["c3","a3"]
        
        self.brh = self.bbf = self.bke = self.bqd = self.bbc = self.bra = []
        
        self.bph = ["h6","h5"]
        self.bpg = ["g6","g5"]
        self.bpf = ["f6","f5"]
        self.bpe = ["e6","e5"]
        self.bpd = ["d6","d5"]
        self.bpc = ["c6","c5"]
        self.bpb = ["b6","b5"]
        self.bpa = ["a6","a5"]
        self.bng = ["h6","f6"]
        self.bnb = ["c6","a6"]
        
        self.en_passant_target = ""
        
        return
    
    def refresh_illegal_check(self):
        #illegal check lists the moves that, while legal based on piece movement, are not legal because they put you in check
        #so the legal moves are really the above lists minus these variables
        self.illegal_check_white = list([])
        self.illegal_check_black = list([])
        
#        #update white
#        for x1 in range(0,6):#pieces
#            for x2 in range(0,8):#files of pieces
#                piece_name = "w" + GameSetup.list_pieces.get(x1) + GameSetup.number_to_file.get(x2)
#                self.legal_check_white.append(getattr(self,piece_name))
#        
#        #update black
#        for x1 in range(0,6):#pieces
#            for x2 in range(0,8):#files of pieces
#                piece_name = "b" + GameSetup.list_pieces.get(x1) + GameSetup.number_to_file.get(x2)
#                self.legal_check_black.append(getattr(self,piece_name))
    
    def generated(self):
        self.f_rank = 0
        self.f_file = 0
        self.t_rank = 0
        self.t_file = 0
        
        self.search_level = 1
        
        self.score = 0

def fresh_board():
    new = chessBoard()
    new.fresh()
    return new      
        

Master = fresh_board()

#currently manipulated board
cMan = fresh_board()