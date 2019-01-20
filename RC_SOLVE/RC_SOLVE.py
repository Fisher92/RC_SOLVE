#import Cube

import Cube2
import tkinter as Tk
import kociemba as kc

class CubeGUI:
    def __init__(self,window,Cube):           
        self.cube = Cube
        self.steplist = []
        self.step=0
        self.canvas = Tk.Canvas(window,width=1000,height=1000)
        self.canvas.pack()
        self.px = 425 #Starting X Position
        self.py= 50 #Starting Y Position
        self.sz = 25
        self.cUp_xi=[self.sz + self.px+self.sz*i for i in range(3)]
        self.cUp_yi=[self.py+self.sz*i for i in range(3)]
        self.cFt_xi=[self.sz + self.px+self.sz*i for i in range(3)]
        self.cFt_yi=[4*self.sz+self.py+self.sz*i for i in range(3)]
        self.cLe_xi=[self.px+self.sz*i-3*self.sz for i in range(3)]
        self.cLe_yi=[4*self.sz+self.py+self.sz*i for i in range(3)]
        self.cRi_xi=[self.px+self.sz*i+5*self.sz for i in range(3)]
        self.cRi_yi=[4*self.sz+self.py+self.sz*i for i in range(3)]
        self.cDn_xi=[self.sz + self.px+self.sz*i for i in range(3)]
        self.cDn_yi=[2*self.sz+2*3*self.sz+self.py+self.sz*i for i in range(3)]
        self.cBk_xi=[self.px+self.sz*i+9*self.sz for i in range(3)]
        self.cBk_yi=[4*self.sz+self.py+self.sz*i for i in range(3)]
        self.cUp = []
        self.cFt = []
        self.cDn = []
        self.cBk = []
        self.cRi = []
        self.cLe = []
        for j in range(3):
            for i in range(3):
                self.cUp.append(self.canvas.create_rectangle(self.cUp_xi[i],self.cUp_yi[j],self.cUp_xi[i]+self.sz,self.cUp_yi[j]+self.sz,fill='white'))
                self.cFt.append(self.canvas.create_rectangle(self.cFt_xi[i],self.cFt_yi[j],self.cFt_xi[i]+self.sz,self.cFt_yi[j]+self.sz,fill='green'))
                self.cDn.append(self.canvas.create_rectangle(self.cDn_xi[i],self.cDn_yi[j],self.cDn_xi[i]+self.sz,self.cDn_yi[j]+self.sz,fill='yellow'))  
                self.cBk.append(self.canvas.create_rectangle(self.cBk_xi[i],self.cBk_yi[j],self.cBk_xi[i]+self.sz,self.cBk_yi[j]+self.sz,fill='blue'))
                self.cRi.append(self.canvas.create_rectangle(self.cRi_xi[i],self.cRi_yi[j],self.cRi_xi[i]+self.sz,self.cRi_yi[j]+self.sz,fill='red'))
                self.cLe.append(self.canvas.create_rectangle(self.cLe_xi[i],self.cLe_yi[j],self.cLe_xi[i]+self.sz,self.cLe_yi[j]+self.sz,fill='orange'))                                                                                           
                
        self.faces = {'Up':self.cUp,'Dn':self.cDn,'Ri':self.cRi,'Le':self.cLe,'Ft':self.cFt,'Bk':self.cBk}                
                
        self.next = Tk.Button(text ="Next", command = self.Next)
        self.next.pack()
        self.solve = Tk.Button(text ="Solve", command = self.Solve)
        self.solve.pack()

        self.lbl_sol = Tk.Label(text = "Solution")

        self.lbl_sol.pack()

        self.step = 0
        self.face_colours = {"U":'white',"D":'yellow',"B":'blue',"F":'green',"R":'red',"L":'orange'}
        self.map_face()

    def Solve(self):
        self.steplist = kc.solve(self.cube.kociemba()).split()
        print(self.steplist)
        self.lbl_sol.config(text = ''.join(self.steplist))

    def Next(self):
        if self.step<len(self.steplist):                       
            self.cube.Turn(self.steplist[self.step])         
            print(self.step)
            self.step+=1
        self.map_face()
    
    def map_face(self):
        #Array Order: U0,D1,R2,L3,F4,B5,
        
        cube_list = []
        cube_list = self.cube.definition()
        
        for index, cubit in enumerate(self.faces['Up']):
            self.canvas.itemconfig(cubit,fill=self.face_colours[cube_list[index]])
        for index, cubit in enumerate(self.faces['Ri']):
            self.canvas.itemconfig(cubit,fill=self.face_colours[cube_list[index+9]])
        for index, cubit in enumerate(self.faces['Ft']):
            self.canvas.itemconfig(cubit,fill=self.face_colours[cube_list[index+18]])
        for index, cubit in enumerate(self.faces['Dn']):
            self.canvas.itemconfig(cubit,fill=self.face_colours[cube_list[index+27]])
        for index, cubit in enumerate(self.faces['Le']):
            self.canvas.itemconfig(cubit,fill=self.face_colours[cube_list[index+36]])
        for index, cubit in enumerate(self.faces['Bk']):
            self.canvas.itemconfig(cubit,fill=self.face_colours[cube_list[index+45]])    

    
Cube = Cube2.Cube()
Cube.Turn("R")
Cube.Turn("R")
Cube.Turn("U")
Cube.Turn("F'")
Cube.Turn("R'")
Cube.Turn("U")
Cube.Turn("L")
window = Tk.Tk()
window.title("Rubiks Cube Solver")
CubeG = CubeGUI(window,Cube)

window.mainloop()

