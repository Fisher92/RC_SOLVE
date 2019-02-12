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
    def __init__(self,CubeDef = None):
        print("#|--------|0, 1, 2 |--------|--------|")  
        print("#|--------|3, 4, 5 |--------|--------|")
        print("#|--------|6, 7, 8 |--------|--------|")
        print("#-------------------------------------")
        print("#|36,37,38|18,19,20|9, 10,11|45,46,47|")
        print("#|39,40,41|21,22,23|12,13,14|48,49,50|")
        print("#|42,43,44|24,25,26|15,16,17|51,52,53|")
        print("#-------------------------------------")
        print("#|--------|27,28,29|--------|--------|")  
        print("#|--------|30,31,32|--------|--------|")  
        print("#|--------|33,34,35|--------|--------|")
        #self.kociemba=''
        self.TurnList = {'R':((2,20),(5,23),(8,26),(20,29),
                              (23,32),(26,35),(29,51),(32,48),
                              (35,45),(45,8),(48,5),(51,2),
                              (9,15),(10,12),(11,9),(12,16),(14,10),(15,17),(16,14),(17,11)),
                         'U':((18,9),(9,45),(45,36),(36,18),
                              (19,10),(10,46),(46,37),(37,19),
                              (20,11),(11,47),(47,38),(38,20),
                              (0,6),(1,3),(2,0),(3,7),(5,1),(6,8),(7,5),(8,2)),
                         'F':((6,44),(44,29),(29,9),(9,6),
                              (7,41),(41,28),(28,12),(12,7),
                              (8,38),(38,27),(27,15),(15,8),
                              (18,24),(19,21),(20,18),(21,25),(23,19),(24,26),(25,23),(26,20)),
                         'L':((18,0),(0,53),(53,27),(27,18),
                              (21,3),(3,50),(50,30),(30,21),
                              (24,6),(6,47),(47,33),(33,24),
                              (36,42),(37,39),(38,36),(39,43),(41,37),(42,44),(43,41),(44,38)),
                         'B':((0,11),(11,35),(35,42),(42,0),
                              (1,14),(14,34),(34,39),(39,1),
                              (2,17),(17,33),(33,36),(36,2),
                              (45,51),(46,48),(47,45),(51,53),(52,50),(53,47),(48,52),(50,46)),
                         'D':((24,42),(42,51),(51,15),(15,24),
                              (25,43),(43,52),(52,16),(16,25),
                              (26,44),(44,53),(53,17),(17,26),
                              (29,27),(32,28),(35,29),(27,33),(30,34),(33,35),(28,30),(34,32))}
                              
                
        if CubeDef:
            self.cube = CubeDef
        else: 
            self.cube = list("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
    
    @property
    def cube(self):
        return self.__cube

    @cube.setter
    def cube(self,cube):
        #"URFDLB"

        if (len(cube)==54) and (cube[4]=="U") and (cube[13] =="R") and (cube[22]=="F") and (cube[31]=="D") and (cube[40] == "L") and (cube[49]=="B"):
            self.__cube = cube
        else:
            print("Cant Set invalid cube definition")
            self.__cube = list("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")

    def Face_Counter(self):
        fcounts = []
        ok = "Valid"
        for face in "URFDLB":
            fcounts.append(self.cube.count(face))
        for cnt in fcounts:
            if cnt!=9:
                ok = "Not Valid"
        fcounts.append(ok)
        return fcounts

    def Turn(self,Type):
        tCube=[x for x in self.cube]
        CW = True
        if len(Type) ==2:
            if Type[1] == "'":
                CW = False
        if CW:
            swapi, swapj = 0,1
        else:
            swapi, swapj = 1,0
            
        for swap in self.TurnList[Type[0]]:
            self.cube[swap[swapi]] = tCube[swap[swapj]]
              
    def definition(self):
        definition = [x for x in self.cube]
        return(definition)

    def get_kociemba(self):
        """Return kociemba Equivalent of Colour Map. Sinlge String denoting URFDLB
            U1, U2, U3, U4, U5, U6, U7, U8, U9,
            R1, R2, R3, R4, R5, R6, R7, R8, R9,
            F1, F2, F3, F4, F5, F6, F7, F8, F9, 
            D1, D2, D3, D4, D5, D6, D7, D8, D9, 
            L1, L2, L3, L4, L5, L6, L7, L8, L9, 
            B1, B2, B3, B4, B5, B6, B7, B8, B9."""
        #self.kociemba=''
        #self.kociemba=''.join(map(str, self.cube))
        
        return(''.join(map(str, self.cube)))



            



