import numpy as np
#http://studentnet.cs.manchester.ac.uk/resources/library/3rd-year-projects/2015/aryeh.grosskopf.pdf
#http://lghttp.38568.nexcesscdn.net/8013252/pdf/uploads/general_content/Rubiks_cube_3x3_solution-en.pdf
#https://github.com/hkociemba/RubiksCube-TwophaseSolver

class cube(object):
    """
    Cube State and Operations
    """
    def __init__(self,istate = None):
        self.coldic = {"W":'white',"Y":'yellow',"B":'blue',"G":'green',"R":'red',"O":'orange'}

        if istate:
            self.cube = istate
        else:
            #Array Order: U0,D1,R2,L3,F4,B5,
            self.cube = np.array([[["W"]*3]*3,[["Y"]*3]*3,[["B"]*3]*3,[["G"]*3]*3,[["R"]*3]*3,[["O"]*3]*3], copy = True)
            #self.cube = {'Top':np.array(['W']*9),'Bot':np.array(["Y"]*9),'Bak':np.array(["R"]*9),'Fnt':np.array(["O"]*9),'SiL':np.array(["B"]*9),'SiR':np.array(["G"]*9)}
        self.valid = False
        self.__isvalid()
        #print(self.cube)
       # self.tempcube=np.copy(self.cube)

    def turn_Y(self,edge,direction="CCW"):
        #Array Order: U0,D1,R2,L3,F4,B5,
        self.tempcube = np.copy(self.cube)
        if edge == "R":
        #1 CCW Up Gets Backs RHS|CW Up gets Fronts RHS
        #2 CCW Down Gets Fronts RHS|CW Down Gets Back RHS
        #3Right Rotated 90 CW / CCW
        #4Left NA
        #5 CCW Front face Gets Ups RHS|CW Front face Gets Dows RHS
        #6 CCW Back gets Downs RHS|CW Back Gets Ups RHS                
        #Array Order: U0,D1,R2,L3,F4,B5,   
            #print("Turning Right Face Clockwise")
            #1
            for i in range(3):
                if direction == "CCW":
                    self.cube[0][i][2] = np.copy(self.tempcube[5][i][2])
                else:
                    self.cube[0][i][2] = np.copy(self.tempcube[4][i][2])   
            #2
            #for i in range(3):
                if direction == "CCW":
                    self.cube[1][i][2] = np.copy(self.tempcube[4][i][2])
                else:
                    self.cube[1][i][2] = np.copy(self.tempcube[5][i][2])
            #3
            #for i in range(3): 
                if direction == "CCW":
                    self.cube[2][0][i]=np.copy(self.tempcube[2][i][0])
                    self.cube[2][2][i]=np.copy(self.tempcube[2][i][2])
                    self.cube[2][0][i]=np.copy(self.tempcube[2][2][i])
                    self.cube[2][i][2]=np.copy(self.tempcube[2][0][i])
                else:
                    self.cube[2][0][i]=np.copy(self.tempcube[2][i][2])
                    self.cube[2][2][i]=np.copy(self.tempcube[2][i][0])
                    self.cube[2][0][i]=np.copy(self.tempcube[2][0][i])
                    self.cube[2][i][2]=np.copy(self.tempcube[2][2][i])
            #4
            #Nothing
            #5
            #for i in range(3):
                if direction == "CCW":
                    self.cube[4][i][2] = np.copy(self.tempcube[0][i][2])
                else:
                    self.cube[4][i][2] = np.copy(self.tempcube[1][i][2])   
            #6
            #for i in range(3):
                if direction == "CCW":
                    self.cube[5][i][2] = np.copy(self.tempcube[1][i][2])                                                                                                                                              
                else:
                    self.cube[5][i][2] = np.copy(self.tempcube[0][i][2])  
            print(self.cube)

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


            



