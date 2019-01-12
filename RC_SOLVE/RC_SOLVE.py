import Cube
import tkinter as Tk

x=Cube.cube()




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
        for i in range(3):
            for j in range(3):
                self.cUP.append(self.canvas.create_rectangle(self.cUP_xi[i],self.cUP_yi[j],self.cUP_xi[i]+self.sz,self.cUP_yi[j]+self.sz,fill='white'))
                self.cFT.append(self.canvas.create_rectangle(self.cFT_xi[i],self.cFT_yi[j],self.cFT_xi[i]+self.sz,self.cFT_yi[j]+self.sz,fill='red'))
                self.cDN.append(self.canvas.create_rectangle(self.cDN_xi[i],self.cDN_yi[j],self.cDN_xi[i]+self.sz,self.cDN_yi[j]+self.sz,fill='yellow'))
                self.cBK.append(self.canvas.create_rectangle(self.cBK_xi[i],self.cBK_yi[j],self.cBK_xi[i]+self.sz,self.cBK_yi[j]+self.sz,fill='orange'))
                self.cLe.append(self.canvas.create_rectangle(self.cLe_xi[i],self.cLe_yi[j],self.cLe_xi[i]+self.sz,self.cLe_yi[j]+self.sz,fill='green'))
                self.cRi.append(self.canvas.create_rectangle(self.cRi_xi[i],self.cRi_yi[j],self.cRi_xi[i]+self.sz,self.cRi_yi[j]+self.sz,fill='blue'))

window = Tk.Tk()
window.title("GUI")

geeks_bro = CubeGUI(window)
window.mainloop()

#while True:
#    test = input("direction")
#    if int(test) == 0:
#        print("Turning CLowckwise")
#        x.turn_Y("R","CW")
#    if int(test) == 1:
#        print("Turning CounterCLowckwise")
#        x.turn_Y("R","CCW")