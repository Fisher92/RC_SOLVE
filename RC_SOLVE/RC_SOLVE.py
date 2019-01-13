import Cube
import tkinter as Tk
import kociemba as kc

xx= kc.solve("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
print(xx)

x=Cube.cube()

x.turn_Y("R","CCW")
face = x.colour_map()
print(face)


class CubeGUI:
    def __init__(self,window):
        self.canvas = Tk.Canvas(window,width=1000,height=1000)
        self.canvas.pack()
        self.px = 425 #Starting X Position
        self.py= 50 #Starting Y Position
        self.sz = 25
        self.cUP_xi=[self.px+self.sz*i for i in range(3)]
        self.cUP_yi=[self.py+self.sz*i for i in range(3)]
        self.cFT_xi=[self.px+self.sz*i for i in range(3)]
        self.cFT_yi=[3*self.sz+self.py+self.sz*i for i in range(3)]
        self.cLe_xi=[self.px+self.sz*i-3*self.sz for i in range(3)]
        self.cLe_yi=[3*self.sz+self.py+self.sz*i for i in range(3)]
        self.cRi_xi=[self.px+self.sz*i+3*self.sz for i in range(3)]
        self.cRi_yi=[3*self.sz+self.py+self.sz*i for i in range(3)]
        self.cDN_xi=[self.px+self.sz*i for i in range(3)]
        self.cDN_yi=[2*3*self.sz+self.py+self.sz*i for i in range(3)]
        self.cBK_xi=[self.px+self.sz*i for i in range(3)]
        self.cBK_yi=[3*3*self.sz+self.py+self.sz*i for i in range(3)]
        self.cUP = []
        self.cFT = []
        self.cDN = []
        self.cBK = []
        self.cRi = []
        self.cLe = []
        for j in range(3):
            for i in range(3):
                self.cUP.append(self.canvas.create_rectangle(self.cUP_xi[i],self.cUP_yi[j],self.cUP_xi[i]+self.sz,self.cUP_yi[j]+self.sz,fill='white'))
                self.cFT.append(self.canvas.create_rectangle(self.cFT_xi[i],self.cFT_yi[j],self.cFT_xi[i]+self.sz,self.cFT_yi[j]+self.sz,fill='red'))
                self.cDN.append(self.canvas.create_rectangle(self.cDN_xi[i],self.cDN_yi[j],self.cDN_xi[i]+self.sz,self.cDN_yi[j]+self.sz,fill='yellow'))
                self.cBK.append(self.canvas.create_rectangle(self.cBK_xi[i],self.cBK_yi[j],self.cBK_xi[i]+self.sz,self.cBK_yi[j]+self.sz,fill='orange'))
                self.cLe.append(self.canvas.create_rectangle(self.cLe_xi[i],self.cLe_yi[j],self.cLe_xi[i]+self.sz,self.cLe_yi[j]+self.sz,fill='green'))
                self.cRi.append(self.canvas.create_rectangle(self.cRi_xi[i],self.cRi_yi[j],self.cRi_xi[i]+self.sz,self.cRi_yi[j]+self.sz,fill='blue'))

    def map_face(self,face):
        #Array Order: U0,D1,R2,L3,F4,B5,
        for i, item in enumerate(self.cUP):
            self.canvas.itemconfig(item,fill=face[0][i])
        for i, item in enumerate(self.cDN):
            self.canvas.itemconfig(item,fill=face[1][i])
        for i, item in enumerate(self.cRi):
            self.canvas.itemconfig(item,fill=face[2][i])
        for i, item in enumerate(self.cLe):
            self.canvas.itemconfig(item,fill=face[3][i])
        for i, item in enumerate(self.cFT):
            self.canvas.itemconfig(item,fill=face[4][i])
        for i, item in enumerate(self.cBK):
            self.canvas.itemconfig(item,fill=face[5][i])
       

window = Tk.Tk()
window.title("GUI")

geeks_bro = CubeGUI(window)
geeks_bro.map_face(x.colour_map())
window.mainloop()

#while True:
#    test = input("direction")
#    if int(test) == 0:
#        print("Turning CLowckwise")
#        x.turn_Y("R","CW")
#    if int(test) == 1:
#        print("Turning CounterCLowckwise")
#        x.turn_Y("R","CCW")