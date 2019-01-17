
import numpy as np
from copy import deepcopy as dc
#http://studentnet.cs.manchester.ac.uk/resources/library/3rd-year-projects/2015/aryeh.grosskopf.pdf
#http://lghttp.38568.nexcesscdn.net/8013252/pdf/uploads/general_content/Rubiks_cube_3x3_solution-en.pdf
#https://github.com/hkociemba/RubiksCube-TwophaseSolver
#https://pypi.org/project/kociemba/

class Cube(object):
    """
    Cube State and Operations
            Cube Structure
    --- [UP[W,W,W,W,W,W]
         DN[Y,Y,Y,Y,Y,Y]
         RI[R,R,R,R,R,R]
         LE[O,O,O,O,O,O]
         FN[G,G,G,G,G,G]
         BA[B,B,B,B,B,B]] ---
    
            kociemba Structure
    --- U1, U2, U3, U4, U5, U6, U7, U8, U9,
        R1, R2, R3, R4, R5, R6, R7, R8, R9, 
        F1, F2, F3, F4, F5, F6, F7, F8, F9, 
        D1, D2, D3, D4, D5, D6, D7, D8, D9, 
        L1, L2, L3, L4, L5, L6, L7, L8, L9, 
        B1, B2, B3, B4, B5, B6, B7, B8, B9. ---
    
        
        
        Cube Turns
    """
    def __init__(self,istate = None):
        self.cube = ""
        self.coldic = {"U":'white',"D":'yellow',"B":'blue',"F":'green',"R":'red',"L":'orange'}
        self.kocdic = {"U":'W',"D":'Y',"B":'B',"F":'G',"R":'R',"L":'O'}
        self.kociemba = ""
        
        if istate:
            self.cube = istate
        else:        
            for face in "URFDLB":
                self.cube +=(face*9)
                
        print(self.cube)
   
    def colour_map(self):
        """Return Array of Length 9 with face Colours"""
        #Array Order: U0,D1,R2,L3,F4,B5,
        col_up = []
        col_dn = []
        col_ri = []
        col_le = []
        col_fn = []
        col_ba = []
        colour_map=[[],[],[],[],[],[],[]]
        for i in range(9):
            col_up.append(self.coldic[self.cube[i]])
        for i in range(9,18):
            col_dn.append(self.coldic[self.cube[i]])
        for i in range(18,27):
            col_ri.append(self.coldic[self.cube[i]])   
        for i in range(27,36):
            col_le.append(self.coldic[self.cube[i]])
        for i in range(36,45):
            col_fn.append(self.coldic[self.cube[i]])
        for i in range(45,54):
            col_ba.append(self.coldic[self.cube[i]])  

        colour_map[0]=col_up
        colour_map[1]=col_dn
        colour_map[2]=col_ri
        colour_map[3]=col_le
        colour_map[4]=col_fn
        colour_map[5]=col_ba
        return(colour_map)

    def ret_koc(self):
        """Return kociemba Equivalent of Colour Map. Sinlge String denoting URFDLB
        order   U1, U2, U3, U4, U5, U6, U7, U8, U9,
                R1, R2, R3, R4, R5, R6, R7, R8, R9,
                F1, F2, F3, F4, F5, F6, F7, F8, F9, 
                D1, D2, D3, D4, D5, D6, D7, D8, D9, 
                L1, L2, L3, L4, L5, L6, L7, L8, L9, 
                B1, B2, B3, B4, B5, B6, B7, B8, B9."""
        
                #U0,D1,R2,L3,F4,B5,
        
        kocstr=""
        
        for face in self.cube:
            for row in face:  
                for i in row:
                    kocstr+=self.kocdic[i]
        self.kociemba = kocstr[0:9] #U
        self.kociemba += kocstr[18:27] #R
        self.kociemba += kocstr[36:45] #F
        self.kociemba += kocstr[9:18] #D
        self.kociemba += kocstr[27:36] #L
        self.kociemba += kocstr[45:54]#[::-1] #B
        print(kocstr)
        return(self.kociemba)



            



