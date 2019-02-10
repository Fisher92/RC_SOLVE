#import Cube
import Cube2
import math
import tkinter as Tk
import kociemba as kc
#import threading
import imutils as imu
import PIL.Image, PIL.ImageTk
import cv2
import numpy as np
from imutils.video import VideoStream
from scipy.spatial import distance as dist
from collections import OrderedDict

class CubeGUI:
    def __init__(self,Cube,video_source):           
        self.window = Tk.Tk()
        #self.config= Tk.Tk()
        #self.c_win = None
        self.cube = Cube
        self.cubestring = list("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
        Cube.set(self.cubestring)
        self.video_source = video_source
        self.steplist = []
        self.calibration_RGB = []
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
        self.cal_var = []
        self.cubits = [None]*9
        self.cubits_mean=[None]*9
        #self.cur_var = []
        for i in range(18):
            self.cal_var.append(Tk.IntVar())
            #self.cur_var.append(0)
        self.detect_colour = True
        #self.nearest = [Tk.StringVar()]*9
      
        self.refPt = []

        self.Face_Rectangles = []
        self.start = (20,30)
        self.size = 50
        self.space = 50
        for i in range(3):
            for j in range(3):
                self.Face_Rectangles.append([(self.start[0]+i*self.size+i*self.space,self.start[1]+j*self.size+j*self.space),\
                                       (self.start[0]+i*self.size+i*self.space+self.size,self.start[1]+j*self.size+j*self.space+self.size)])

        self.colors = OrderedDict({
			        "red": [230, 80, 60],
			        "green": [30, 200, 120],
			        "blue": [0, 0, 255],
			        "orange":[255,165,40],
			        "white":[200,200,200],
			        "yellow":[250,250,100]})

        self.rgb = np.zeros((len(self.colors), 1, 3), dtype="uint8")
        self.colorNames = []

        # loop over the colors dictionary
        for (i, (name, val)) in enumerate(self.colors.items()):
	        # update the L*a*b* array and the color names list
            self.rgb[i] = val
            self.colorNames.append(name)


        for j in range(3):
            for i in range(3):
                self.cUp.append(self.canvas.create_rectangle(self.cUp_xi[i],self.cUp_yi[j],self.cUp_xi[i]+self.sz,self.cUp_yi[j]+self.sz,fill='white'))
                self.cFt.append(self.canvas.create_rectangle(self.cFt_xi[i],self.cFt_yi[j],self.cFt_xi[i]+self.sz,self.cFt_yi[j]+self.sz,fill='green'))
                self.cDn.append(self.canvas.create_rectangle(self.cDn_xi[i],self.cDn_yi[j],self.cDn_xi[i]+self.sz,self.cDn_yi[j]+self.sz,fill='yellow'))  
                self.cBk.append(self.canvas.create_rectangle(self.cBk_xi[i],self.cBk_yi[j],self.cBk_xi[i]+self.sz,self.cBk_yi[j]+self.sz,fill='blue'))
                self.cRi.append(self.canvas.create_rectangle(self.cRi_xi[i],self.cRi_yi[j],self.cRi_xi[i]+self.sz,self.cRi_yi[j]+self.sz,fill='red'))
                self.cLe.append(self.canvas.create_rectangle(self.cLe_xi[i],self.cLe_yi[j],self.cLe_xi[i]+self.sz,self.cLe_yi[j]+self.sz,fill='orange'))                                                                                           
                
        self.faces = {'Up':self.cUp,'Dn':self.cDn,'Ri':self.cRi,'Le':self.cLe,'Ft':self.cFt,'Bk':self.cBk}                
        self.console = Tk.Text(self.window,height = 10,width =45)
        self.console.pack(anchor = 'e')
       

        self.next = Tk.Button(text ="Next", command = self.Next)
        self.next.pack()

        self.config = Tk.Button(text ="Config", command = self.Config_Window)
        self.config.pack()

        self.solve = Tk.Button(text ="Solve", command = self.Solve)
        self.solve.pack()

        self.map_cface = Tk.Button(text ="Map", command = self.map_to_face)
        self.map_cface.pack(anchor = 'ne')

        self.lbl_sol = Tk.Label(text = "Solution")
        self.lbl_sol.pack()

        self.step = 0
        self.face_colours = {"U":'white',"D":'yellow',"B":'blue',"F":'green',"R":'red',"L":'orange'}
        self.colours_face = {"white":('Up',(0,9)),'yellow':('Down',(27,36)),'blue':('Back',(45,54)),'green':("Front",(18,27)),'red':("Right",(9,18)),'orange':("L",(36,45))}
        
        self.vid = MyVideoCapture(video_source)
        
        
        
        self.delay = 15
        
        self.map_face()
        self.update()
        self.window.mainloop()

    def Config_Window(self):
        
        try:
            c_win.destroy()
        except:
            pass
        
        c_win = Tk.Toplevel(self.window)
        c_win_svar = []
        cal_RGB = []

        lbl_cR = Tk.Label(c_win,text="R  ")
        lbl_cR.grid(row=0,column=1,sticky='e')
        lbl_cG = Tk.Label(c_win,text="G  ")
        lbl_cG.grid(row=0,column=2,sticky='e')
        lbl_cB = Tk.Label(c_win,text="B  ")
        lbl_cB.grid(row=0,column=3,sticky='e')
        #URFDLB
        for i , face in enumerate("URFDLB"):
            Tk.Label(c_win,text = self.face_colours[face]+" ("+face+")").grid(row = i+1,column=0,sticky="ns")
        
        
        for i in range(18):
            cal_RGB.append(Tk.Scale(c_win,from_=0,to=255,orient = "vertical",variable = self.cal_var[i]))
            #c_win_svar.append(Tk.StringVar())
        for idx,item in enumerate(cal_RGB):
            item.grid(row=math.floor(idx/3)+1,column = idx%3+1)
            item.bind("<ButtonRelease-1>",self.SetValue)
        

        for i,item in enumerate(self.colors.get('white')):
            self.cal_var[i+0].set(item)
        for i,item in enumerate(self.colors.get('red')):
            self.cal_var[i+3].set(item)
        for i,item in enumerate(self.colors.get('green')):
            self.cal_var[i+6].set(item)
        for i,item in enumerate(self.colors.get('yellow')):
            self.cal_var[i+9].set(item)
        for i,item in enumerate(self.colors.get('orange')):
            self.cal_var[i+12].set(item)
        for i,item in enumerate(self.colors.get('blue')):
            self.cal_var[i+15].set(item)
            
        Btn_Quit = Tk.Button(c_win, text="Quit", command=c_win.destroy)
        Btn_Quit.grid(row=10,column=2)

    def SetValue(self,event):
        for i in range(3):
            self.colors.get('white')[i]=self.cal_var[i].get()
        for i in range(3):
            self.colors.get('red')[i]=self.cal_var[i+3].get()
        for i in range(3):
            self.colors.get('green')[i]=self.cal_var[i+6].get()
        for i in range(3):
            self.colors.get('yellow')[i]=self.cal_var[i+9].get()
        for i in range(3):
            self.colors.get('orange')[i]=self.cal_var[i+12].get()
        for i in range(3):
            self.colors.get('blue')[i]=self.cal_var[i+15].get()

        for (i, (name, val)) in enumerate(self.colors.items()):
	        # update the L*a*b* array and the color names list
            self.rgb[i] = val
    def map_to_face(self):
        temp = []
        #print(self.colours_face[self.cubits[4]][1][0]:self.colours_face[self.cubits[4]][1][1]])
        print(self.cubestring)
        for item in self.cubits:
            temp.append(self.colours_face[item][0][0])
        self.cubestring[self.colours_face[self.cubits[4]][1][0]:self.colours_face[self.cubits[4]][1][1]] =\
        temp[:]
        print(self.cubestring)
        #print(temp)
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

    def update(self):

        ret, frame = self.vid.get_frame()
        frame = imu.resize(frame,400,400)


        mask = np.zeros(frame.shape[:2], dtype="uint8")
        test = np.copy(frame)

        for item in self.Face_Rectangles:
            cv2.rectangle(frame,item[0],item[1],(0,255,0),3)

        if self.detect_colour:
            for number, item in enumerate(self.Face_Rectangles):
                minDist = (np.inf, None)
                #mask = cv2.erode(test[150:210,200:260], None, iterations=2)
                mask = cv2.erode(test[item[0][0]:item[1][0],item[0][1]:item[1][1]], None, iterations=2)
                b,g,r,_=np.uint8(cv2.mean(mask))
                mean = cv2.mean(mask)

                for (i, row) in enumerate(self.rgb):
    
                    d = dist.euclidean(row[0], mean[:3])

                    if d < minDist[0]:
                        minDist = (d, i)

                self.cubits[number] = self.colorNames[minDist[1]]
                self.cubits_mean[number]=[r,g,b]
                #cv2.putText(frame,str(number)+':'+self.colorNames[minDist[1]][:3],(item[0][0],item[0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        
        console_text =''
        for number, item in enumerate(self.cubits_mean):
            console_text += 'Cube('+str(number)  +") {:<7}: - R:{:03d} - G:{:03d} - B:{:03d}\n".format(self.cubits[number], item[2],item[1],item[1])
            #cv2.putText(frame,str(number)+':'+self.cubits[number],(self.Face_Rectangles[number][0][0],self.Face_Rectangles[number][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
            #array index all fucked
        cv2.putText(frame,'0',(self.Face_Rectangles[0][0][0]+int(self.size/2)-10,self.Face_Rectangles[0][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'1',(self.Face_Rectangles[3][0][0]+int(self.size/2)-10,self.Face_Rectangles[3][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'2',(self.Face_Rectangles[6][0][0]+int(self.size/2)-10,self.Face_Rectangles[6][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'3',(self.Face_Rectangles[1][0][0]+int(self.size/2)-10,self.Face_Rectangles[1][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'4',(self.Face_Rectangles[4][0][0]+int(self.size/2)-10,self.Face_Rectangles[4][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'5',(self.Face_Rectangles[7][0][0]+int(self.size/2)-10,self.Face_Rectangles[7][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'6',(self.Face_Rectangles[2][0][0]+int(self.size/2)-10,self.Face_Rectangles[2][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'7',(self.Face_Rectangles[5][0][0]+int(self.size/2)-10,self.Face_Rectangles[5][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'8',(self.Face_Rectangles[8][0][0]+int(self.size/2)-10,self.Face_Rectangles[8][0][1]+int(self.size/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        self.console.delete('1.0', Tk.END)
        self.console.insert('1.0',console_text)#str(b)+','+str(g)+','+str(r)+'\n') 
        self.console.insert(Tk.END,'Face Detected:'+self.colours_face[self.cubits[4]][0]) 
                # return the name of the color with the smallest distance
                #print(self.colorNames[minDist[1]])
            
                #self.nearest[number].set(self.colorNames[minDist[1]])
                #self.detect_colour = False
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

