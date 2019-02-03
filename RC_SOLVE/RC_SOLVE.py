#import Cube
import Cube2
import math
import tkinter as Tk
import kociemba as kc
#import threading
import imutils as imu
import PIL.Image, PIL.ImageTk
import cv2

class CubeGUI:
    def __init__(self,Cube,video_source):           
        self.window = Tk.Tk()
        self.config= Tk.Tk()
        self.cube = Cube
        self.video_source = video_source
        self.steplist = []
        self.cal_RGB = []
        self.step=0
        self.canvas = Tk.Canvas(self.window,width=800,height=400)
        self.canvas.pack(anchor = 'nw')
        self.px = 100 #Starting X Position
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
                
        lbl_cR = Tk.Label(self.config,text="R  ")
        lbl_cR.grid(row=0,column=1,sticky='e')
        lbl_cG = Tk.Label(self.config,text="G  ")
        lbl_cG.grid(row=0,column=2,sticky='e')
        lbl_cB = Tk.Label(self.config,text="B  ")
        lbl_cB.grid(row=0,column=3,sticky='e')
        lbl_fU = Tk.Label(self.config,text="Up (W)")
        lbl_fU.grid(row=1,column=0,sticky='ns')
        for i in range(18):
            self.cal_RGB.append(Tk.Scale(self.config,from_=0,to=255,orient = "vertical"))
        for idx,item in enumerate(self.cal_RGB):
            item.grid(row=math.floor(idx/3)+1,column = idx%3+1)

        self.next = Tk.Button(text ="Next", command = self.Next)
        self.next.pack()

        self.solve = Tk.Button(text ="Solve", command = self.Solve)
        self.solve.pack()

        self.lbl_sol = Tk.Label(text = "Solution")
        self.lbl_sol.pack()

        self.step = 0
        self.face_colours = {"U":'white',"D":'yellow',"B":'blue',"F":'green',"R":'red',"L":'orange'}
        
        
        self.vid = MyVideoCapture(video_source)
        
        
        
        self.delay = 15
        
        self.map_face()
        self.update()
        self.window.mainloop()

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

    def update(self):

        ret, frame = self.vid.get_frame()
        frame = imu.resize(frame,300,300)
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(500, self.py, image = self.photo, anchor = Tk.NW)
 
        self.window.after(self.delay, self.update)    
           
        #self.window.after(self.delay, self.update)
            
class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
 
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.mainloop()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

Cube = Cube2.Cube()
Cube.Turn("R")
#Cube.Turn("L")
Cube.Turn("U")
Cube.Turn("F'")
Cube.Turn("R'")
Cube.Turn("U")
Cube.Turn("L")
#window = Tk.Tk()
#config = Tk.Tk()
#window.title("Rubiks Cube Solver")
CubeG = CubeGUI(Cube,0)

#window.mainloop()

