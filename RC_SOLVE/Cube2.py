
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
    
            kociemba Structure
    --- U1, U2, U3, U4, U5, U6, U7, U8, U9,
        R1, R2, R3, R4, R5, R6, R7, R8, R9, 
        F1, F2, F3, F4, F5, F6, F7, F8, F9, 
        D1, D2, D3, D4, D5, D6, D7, D8, D9, 
        L1, L2, L3, L4, L5, L6, L7, L8, L9, 
        B1, B2, B3, B4, B5, B6, B7, B8, B9. ---
    
        
        
        Cube Turns
        FRULBD
    """

#|--------|0, 1, 2 |--------|--------|  
#|--------|3, 4, 5 |--------|--------|
#|--------|6, 7, 8 |--------|--------|
#------------------------------------
#|36,37,38|18,19,20|9, 10,11|45,46,47|
#|39,40,41|21,22,23|12,13,14|48,49,50|
#|42,43,44|24,25,26|15,16,17|51,52,53|
#------------------------------------
#|--------|27,28,29|--------|--------|  
#|--------|30,31,32|--------|--------|  
#|--------|33,34,35|--------|--------| 

    def __init__(self,istate = None):
        self.cube = []
        #self.face={'U'}
        self.coldic = {"U":'white',"D":'yellow',"B":'blue',"F":'green',"R":'red',"L":'orange'}
        self.kocdic = {"U":'W',"D":'Y',"B":'B',"F":'G',"R":'R',"L":'O'}
        self.kocdic2 = {"U":'U',"D":'D',"B":'B',"F":'F',"R":'R',"L":'L'}
        self.TurnList = {'R':[[2,20],[5,23],[8,26],[20,29],
                              [23,32],[26,35],[29,51],[32,48],
                              [35,45],[45,8],[48,5],[51,2],
                              [9,15],[10,12],[11,9],[12,16],[14,10],[15,17],[16,14],[17,11]],
                         'U':[[18,9],[9,45],[45,36],[36,18],
                              [19,10],[10,46],[46,37],[37,19],
                              [20,11],[11,47],[47,38],[38,20],
                              [0,6],[1,3],[2,0],[3,7],[5,1],[6,8],[7,5],[8,2]],
                         'F':[[6,44],[44,29],[29,9],[9,6],
                              [7,41],[41,28],[28,12],[12,7],
                              [8,38],[38,27],[27,15],[15,8],
                              [18,24],[19,21],[20,18],[21,25],[23,19],[24,26],[25,23],[26,20]]}
        self.kociemba = ""
        
        if istate:
            self.cube = istate
        else:        
            for face in "URFDLB":
                for i in range(9):
                    self.cube.append(face)
                
        print(self.cube)
        self.Turn("R")
        self.Turn("U",False)
        self.Turn("F")
        self.Turn("R")
        self.Turn("F",False)
        self.Turn("R")
        self.Turn("F",False)
        self.Turn("R",False)
        self.Turn("U",False)
        self.Turn("F")
        self.Turn("R")
        self.Turn("F")
        self.Turn("R",False)
        self.Turn("F")
       
    def Turn(self,Type,CW=True):
        tCube=[self.kocdic2[x] for x in self.cube]
        print(tCube)
        if CW:
            for swap in self.TurnList[Type]:
                print(swap)
                self.cube[swap[0]] = self.kocdic2[tCube[swap[1]]]
        else:
            for swap in self.TurnList[Type]:
                print(swap)
                self.cube[swap[1]] = self.kocdic2[tCube[swap[0]]]
        del(tCube)
        
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
        testdtr = ''.join(map(str, self.cube))
        for i in range(9):
            col_up.append(self.coldic[testdtr[i]])
        for i in range(9,18):
            col_ri.append(self.coldic[testdtr[i]])
        for i in range(18,27):
            col_fn.append(self.coldic[testdtr[i]])   
        for i in range(27,36):
            col_dn.append(self.coldic[testdtr[i]])
        for i in range(36,45):
            col_le.append(self.coldic[testdtr[i]])
        for i in range(45,54):
            col_ba.append(self.coldic[testdtr[i]])  

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
        self.kociemba=''.join(map(str, self.cube))
        #for face in self.cube:
        #    for row in face:  
        #        for i in row:
       #             kocstr+=self.kocdic[i]
       # self.kociemba = kocstr[0:9] #U
       # self.kociemba += kocstr[18:27] #R
       # self.kociemba += kocstr[36:45] #F
       # self.kociemba += kocstr[9:18] #D
       # self.kociemba += kocstr[27:36] #L
       # self.kociemba += kocstr[45:54]#[::-1] #B
       # print(kocstr)
        return(self.kociemba)



            



