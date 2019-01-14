#import numpy as np
from copy import deepcopy as dc
#http://studentnet.cs.manchester.ac.uk/resources/library/3rd-year-projects/2015/aryeh.grosskopf.pdf
#http://lghttp.38568.nexcesscdn.net/8013252/pdf/uploads/general_content/Rubiks_cube_3x3_solution-en.pdf
#https://github.com/hkociemba/RubiksCube-TwophaseSolver
#https://pypi.org/project/kociemba/

class cube(object):
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
        self.coldic = {"W":'white',"Y":'yellow',"B":'blue',"G":'green',"R":'red',"O":'orange'}
        self.kocdic = {"W":'U',"Y":'D',"B":'B',"G":'F',"R":'R',"O":'L'}
        self.kociemba = ""
        
        if istate:
            self.cube = istate
        else:        
            self.cube = [[["W"]*3]*3,[["Y"]*3]*3,[["R"]*3]*3,[["O"]*3]*3,[["G"]*3]*3,[["B"]*3]*3]    
        self.valid = False
        self.__isvalid()



    def RC_Turn(self,Turn = "F"):
        """Turn the Rubiks Cube According to the Standard Notation
        Clockwise
        F
        R
        U
        L
        B
        D
        CounterClockwise (Add Prime Notation ')       
        https://ruwix.com/the-rubiks-cube/notation/
        """
    #Array Order: U0,D1,R2,L3,F4,B5,

        CCW=False

        if "FRULBD".find(Turn[0]) != -1:
            #"Valid"
            pass
        else:
            return

        
        self.tempcube = dc(self.cube)
       
        if len(Turn)>1:
            if Turn[1] == "'":
                CCW = True
                
        if Turn[0] == "U":
            print(CCW)
        #1 CCW Up Gets Rotated 90
        #2 Down is Unchanged
        #3 Right Top Row Gets Backs Top Row
        #4 Left Top Row Gets Fronts Top Row
        #5 Front Top Row Gets Rights Top Row
        #6 Back Gets Lefts Top Row             
        #Array Order: U0,D1,R2,L3,F4,B5,
        #
            for i in range(3):
            #1 Rotate Top
                if CCW:
                    self.cube[0][0][i]=dc(self.tempcube[0][i][2]) #Row 0.
                    self.cube[0][2][i]=dc(self.tempcube[0][i][0]) #Row 2
                    self.cube[0][1][0]=dc(self.tempcube[0][0][1]) #Column 0  
                    self.cube[0][1][2]=dc(self.tempcube[0][2][1]) #Column 2
                    
                else:
                    self.cube[0][0][i]=dc(self.tempcube[0][i][0]) #Row 0.
                    self.cube[0][2][i]=dc(self.tempcube[0][i][2]) #Row 2
                    self.cube[0][1][0]=dc(self.tempcube[0][2][1]) #Column 0  
                    self.cube[0][1][2]=dc(self.tempcube[0][0][1]) #Column 2
            #2
            #3 Right Top Row Gets Backs Top Row               
            if CCW:
                self.cube[2][0] = dc(self.tempcube[4][0])
                                   
            else:
                self.cube[2][0] = dc(self.tempcube[5][0])   
                
            #4 Left Top Row Gets Fronts Top Row
            
            if CCW:
                self.cube[3][0] = dc(self.tempcube[5][0])                   
            else:
                self.cube[3][0] = dc(self.tempcube[4][0])
            #5 Front Top Row Gets Rights Top Row
            if CCW:
                self.cube[4][0] = dc(self.tempcube[3][0])                   
            else:
                self.cube[4][0] = dc(self.tempcube[2][0])  
            #6 Back Gets Lefts Top Row    
            if CCW:
                self.cube[5][0] = dc(self.tempcube[2][0])                   
            else:
                self.cube[5][0] = dc(self.tempcube[3][0])  

        if Turn[0] == "R":
        #1 CCW Up Gets Backs RHS|CW Up gets Fronts RHS
        #2 CCW Down Gets Fronts RHS|CW Down Gets Back RHS
        #3Right Rotated 90 CW / CCW
        #4Left NA
        #5 CCW Front face Gets Ups RHS|CW Front face Gets Dows RHS
        #6 CCW Back gets Downs RHS|CW Back Gets Ups RHS                
        #Array Order: U0,D1,R2,L3,F4,B5,   
            print(self.tempcube[5])
            print(self.tempcube[5][2][0])
            print(self.tempcube[5][1][0])
            print(self.tempcube[5][0][0])
            
            #for i in range(3):
            if CCW:
                print(self.cube[5] == self.cube[4])
                #self.cube[0][i][2] = dc(self.tempcube[5][i][2]) #Backwards for Repr
                self.cube[0][0][2] = "O"#dc(self.tempcube[5][2][0])
                #self.cube[0][1][2] = dc(self.tempcube[5][1][0])
                #self.cube[0][2][2] = dc(self.tempcube[5][0][0])
                #print(self.tempcube[5][2-i])
            else:
                #self.cube[0][i][2] = dc(self.tempcube[4][i][2])  
                pass 
            #2
            #for i in range(3):
        print(self.cube[0][0][2])
        print(self.cube[0][1][2])
        print(self.cube[0][2][2])
        if False:
                if CCW:
                    self.cube[1][i][2] = dc(self.tempcube[4][i][2])
                else:
                    self.cube[1][i][2] = dc(self.tempcube[5][i][2])
            #3
            #for i in range(3): 
                if CCW:
                    self.cube[2][0][i]=dc(self.tempcube[2][i][2])
                    self.cube[2][2][i]=dc(self.tempcube[2][i][0])
                    self.cube[2][1][0]=dc(self.tempcube[2][0][1])
                    self.cube[2][1][2]=dc(self.tempcube[2][2][1])
                else:
                    self.cube[2][0][i]=dc(self.tempcube[2][i][0])
                    self.cube[2][2][i]=dc(self.tempcube[2][i][2])
                    self.cube[2][1][0]=dc(self.tempcube[2][2][1])
                    self.cube[2][1][2]=dc(self.tempcube[2][0][1])
            #4
            #Nothing
            #5
            #for i in range(3):
                if CCW:
                    self.cube[4][i][2] = dc(self.tempcube[0][i][2])
                else:
                    self.cube[4][i][2] = dc(self.tempcube[1][i][2])   
            #6
            #for i in range(3):         
                if CCW:
                    self.cube[5][i][0] = dc(self.tempcube[1][i][2])    #Backwards Repr                                                                                                                                          
                else:
                    self.cube[5][i][0] = dc(self.tempcube[0][2][2])    #Backwards Repr 
        
                    
                    


    def __isvalid(self):
        """Cube is Valid if 9 of every color exists"""
        self.valid = True
        #print(np.where(self.cube == "W"))
        #if self.cube.where(x="W") != 9: 
        #    self.valid = False
        
        #print(self.valid)
   
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
        for i in range(3):
            for item in self.cube[0][i]:
                col_up.append(self.coldic[item])
            for item in self.cube[1][i]:
                col_dn.append(self.coldic[item])
            for item in self.cube[2][i]:
                col_ri.append(self.coldic[item])
            for item in self.cube[3][i]:
                col_le.append(self.coldic[item])
            for item in self.cube[4][i]:
                col_fn.append(self.coldic[item])
            for item in self.cube[5][i]:
                col_ba.append(self.coldic[item])
       
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



            



