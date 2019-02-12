#import Cube
import Cube2
import math
import tkinter as Tk
import kociemba as kc
import imutils as imu
import PIL.Image, PIL.ImageTk
import cv2
import numpy as np
from imutils.video import VideoStream
from scipy.spatial import distance as dist
from collections import OrderedDict

class CubeGUI:
    def __init__(self,Cube,video_source,**kwargs):           
        self.window = Tk.Tk()
        self.cube = Cube
        #self.cube.cube = list("UUUURUUUURRRURRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
        self.cubestring = self.cube.cube
        self.video_source = video_source
        self.steplist = []
        self.calibration_RGB = []
        self.step=0
        self.canvas = Tk.Canvas(self.window,width=1000,height=800)
        self.canvas.grid(row=0,column=0,columnspan=10)
        self.cmd_box = Tk.Frame(self.window,width = 500,height = 500,bd=1)#, relief=Tk.SUNKEN)
        self.cmd_box.place(x=0,y=400)
        self.GUI_Params_Cube = (100,50,25) #Starting X Position
        self.CV_RParam = [20,30,50,50] #Rectangle Size
        self.cal_var = []
        self.cubits = [None]*9
        self.cubits_mean=[None]*9
        
        for i in range(18):
            self.cal_var.append(Tk.IntVar())
        
        self.detect_colour = True     
        self.refPt = []
        self.Face_Rectangles = self.CV_rectangles(self.CV_RParam)
        f= open('cubecfg.txt',"r")
        lines = f.read().splitlines()
        f.close()
        last_line = lines[-1]
        colcfg = last_line.split(',')
        print(colcfg)
        self.colors = OrderedDict({
			        "red": [230, 80, 60],
			        "green": [30, 200, 120],
			        "blue": [0, 0, 255],
			        "orange":[255,165,40],
			        "white":[200,200,200],
			        "yellow":[250,250,100]})
        if len(last_line)>=18:
            try:
                self.colors['red'] = colcfg[:3]
                self.colors['green'] = colcfg[3:6]
                self.colors['blue'] = colcfg[6:9]
                self.colors['orange'] = colcfg[9:12]
                self.colors['white'] = colcfg[12:15]
                self.colors['yellow'] = colcfg[15:18]
            except:
                print("Failed to import config")

        self.ocol={'red':('green','yellow'),'green':('blue','red'),'blue':('orange','green'),'orange':('white','blue'),'white':('yellow','orange'),'yellow':('red','white')}
        self.face_colours = {"U":'white',"D":'yellow',"B":'blue',"F":'green',"R":'red',"L":'orange'}
        self.colours_face = {"white":('Up',(0,9)),'yellow':('Down',(27,36)),'blue':('Back',(45,54)),'green':("Front",(18,27)),'red':("Right",(9,18)),'orange':("L",(36,45))}

        self.rgb = np.zeros((len(self.colors), 1, 3), dtype="uint8")
        self.colorNames = []

        
        for (i, (name, val)) in enumerate(self.colors.items()):
            self.rgb[i] = val
            self.colorNames.append(name)
       
        self.window.protocol("WM_DELETE_WINDOW", self._delete_window)
        #self.window.bind("<Destroy>", _destroy)
            
        self.faces =  self.GUI_Cube(self.canvas,self.GUI_Params_Cube)              
        for item in self.faces:
            #Bind left and right mouse clicks to CubeGUIs
            self.canvas.tag_bind(item,'<Button-1>', self.Face_Cycle_L)
            self.canvas.tag_bind(item,'<Button-3>', self.Face_Cycle_R)
                    
        self.console = Tk.Text(self.window,height = 10,width =50)
        self.console.place(x=500,y=400)       
        
        self.next = Tk.Button(self.cmd_box,text ="Next", command = self.Next)
        self.next.grid(row=0,column=0,padx=10,sticky="ew")

        self.config = Tk.Button(self.cmd_box,text ="Config", command = self.Config_Window)
        self.config.grid(row=0,column=1,padx=10,sticky="ew")

        self.solve = Tk.Button(self.cmd_box,text ="Solve", command = self.Solve)
        self.solve.grid(row=1,column=0,padx=10,sticky="ew")

        self.map_cface = Tk.Button(self.cmd_box,text ="Map", command = self.map_to_face)
        self.map_cface.grid(row=1,column=1,padx=10,sticky="ew")

        self.R=Tk.Button(self.cmd_box,text ="R", command=lambda: (self.cube.Turn("R"),self.map_face()))
        self.R.grid(row=0,column=2,padx=10,sticky="ew")

        self.Rd=Tk.Button(self.cmd_box,text ="R'", command=lambda: (self.cube.Turn("R'"),self.map_face()))
        self.Rd.grid(row=0,column=3,padx=10,sticky="ew")

        self.U=Tk.Button(self.cmd_box,text ="U", command=lambda: (self.cube.Turn("U"),self.map_face()))
        self.U.grid(row=1,column=2,padx=10,sticky="ew")

        self.Ud=Tk.Button(self.cmd_box,text ="U'", command=lambda: (self.cube.Turn("U'"),self.map_face()))
        self.Ud.grid(row=1,column=3,padx=10,sticky="ew")

        self.F=Tk.Button(self.cmd_box,text ="F", command=lambda: (self.cube.Turn("F"),self.map_face()))
        self.F.grid(row=2,column=2,padx=10,sticky="ew")

        self.Fd=Tk.Button(self.cmd_box,text ="F'", command=lambda: (self.cube.Turn("F'"),self.map_face()))
        self.Fd.grid(row=2,column=3,padx=10,sticky="ew")

        self.L=Tk.Button(self.cmd_box,text ="L", command=lambda: (self.cube.Turn("L"),self.map_face()))
        self.L.grid(row=3,column=2,padx=10,sticky="ew")

        self.Ld=Tk.Button(self.cmd_box,text ="L'", command=lambda: (self.cube.Turn("L'"),self.map_face()))
        self.Ld.grid(row=3,column=3,padx=10,sticky="ew")

        self.B=Tk.Button(self.cmd_box,text ="B", command=lambda: (self.cube.Turn("B"),self.map_face()))
        self.B.grid(row=4,column=2,padx=10,sticky="ew")

        self.Bd=Tk.Button(self.cmd_box,text ="B'", command=lambda: (self.cube.Turn("B'"),self.map_face()))
        self.Bd.grid(row=4,column=3,padx=10,sticky="ew")

        self.D=Tk.Button(self.cmd_box,text ="D", command=lambda: (self.cube.Turn("D"),self.map_face()))
        self.D.grid(row=4,column=2,padx=10,sticky="ew")

        self.Dd=Tk.Button(self.cmd_box,text ="D'", command=lambda: (self.cube.Turn("D'"),self.map_face()))
        self.Dd.grid(row=4,column=3,padx=10,sticky="ew")

        self.lbl_sol = Tk.Label(self.cmd_box,text = "Solution")
        self.lbl_sol.grid(row=5,column=0,sticky="ew",columnspan=10)

        self.lbl_fcnt = Tk.Label(self.cmd_box,text = "Face Counts")
        self.lbl_fcnt.grid(row=6,column=0,sticky="ew",columnspan=10,rowspan =2)
        
        self.step = 0

        self.vid = MyVideoCapture(video_source)
                       
        self.delay = 15
        
        self.map_face()
        self.update()
        self.window.mainloop()

    def CV_rectangles(self,XYSP):
        """Generate Rectangles For Face Colour Detection
        X,Y Start Coords - relative to frame size
        rectangel size"""
        X,Y,S,P = XYSP
        rectangles=[]
        for i in range(3):
            for j in range(3):
                rectangles.append([(X+i*S+i*P,Y+j*S+j*P),\
                                       (X+i*S+i*P+S,Y+j*S+j*P+S)])
        return rectangles

    def GUI_Cube(self,canvas,XYS):
        """Create A Flat Cube for Display
        Cubits Stored in Class List
        Parameters: X Start, Y Start, S Cube Size"""
        X,Y,S = XYS
        cUp = [];cFt = [];cDn = [];cBk = [];cRi = [];cLe = []
        cUp_xi=[S + X+S*i for i in range(3)]
        cUp_yi=[Y+S*i for i in range(3)]
        cFt_xi=[S + X+S*i for i in range(3)]
        cFt_yi=[4*S+Y+S*i for i in range(3)]
        cLe_xi=[X+S*i-3*S for i in range(3)]
        cLe_yi=[4*S+Y+S*i for i in range(3)]
        cRi_xi=[X+S*i+5*S for i in range(3)]
        cRi_yi=[4*S+Y+S*i for i in range(3)]
        cDn_xi=[S + X+S*i for i in range(3)]
        cDn_yi=[2*S+2*3*S+Y+S*i for i in range(3)]
        cBk_xi=[X+S*i+9*S for i in range(3)]
        cBk_yi=[4*S+Y+S*i for i in range(3)]

        x=0
        for j in range(3):
            for i in range(3):
                cUp.append(canvas.create_rectangle(cUp_xi[i],cUp_yi[j],cUp_xi[i]+S,cUp_yi[j]+S,fill='white',tags = ('Up',x+0)))
                cFt.append(canvas.create_rectangle(cFt_xi[i],cFt_yi[j],cFt_xi[i]+S,cFt_yi[j]+S,fill='green',tags = ('Ft',x+18)))
                cDn.append(canvas.create_rectangle(cDn_xi[i],cDn_yi[j],cDn_xi[i]+S,cDn_yi[j]+S,fill='yellow',tags = ('Dn',x+27)))  
                cBk.append(canvas.create_rectangle(cBk_xi[i],cBk_yi[j],cBk_xi[i]+S,cBk_yi[j]+S,fill='blue',tags = ('Bk',x+45)))
                cRi.append(canvas.create_rectangle(cRi_xi[i],cRi_yi[j],cRi_xi[i]+S,cRi_yi[j]+S,fill='red',tags = ('Ri',x+9)))
                cLe.append(canvas.create_rectangle(cLe_xi[i],cLe_yi[j],cLe_xi[i]+S,cLe_yi[j]+S,fill='orange',tags = ('Le',x+36)))                                                                                           
                x+=1

        return {'Up':cUp,'Dn':cDn,'Ri':cRi,'Le':cLe,'Ft':cFt,'Bk':cBk} 

    def Face_Cycle_R(self,event):                
        """Cycle Through Colours on mouse Click except center Cube"""
        t=event.widget.find_closest(event.x, event.y)[0]
        u=int(self.canvas.itemcget(t,"tags").split()[1])
        if u not in [4,13,22,31,40,49]:
            v=self.colours_face[self.ocol[self.canvas.itemcget(t,"fill")][1]][0][0]
            self.cubestring[u]=v
            self.cube.cube = self.cubestring#Cube.set(self.cubestring)
            self.map_face()
        else:
            print("Cant Change Center Cubit")

    def Face_Cycle_L(self,event):                  
        """Cycle Through Colours on mouse Click except center Cube"""
        t=event.widget.find_closest(event.x, event.y)[0]
        u=int(self.canvas.itemcget(t,"tags").split()[1])
        if u not in [4,13,22,31,40,49]:
            v=self.colours_face[self.ocol[self.canvas.itemcget(t,"fill")][0]][0][0]
            self.cubestring[int(u)]=v
            self.cube.cube = self.cubestring#Cube.set(self.cubestring)
            self.map_face()
        else:
            print("Cant Change Center Cubit")

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
        f= open('cubecfg.txt',"a")
        for (i, (name, val)) in enumerate(self.colors.items()):
            self.rgb[i] = val
            
            f.write(','.join(map(str, val))+",")
            
        #f= open('cubecfg.txt',"a")
        #for item in self.colors.items():
        #    f.write(','.join(map(str, item)))
            
        f.write("\n")
        f.close

    def map_to_face(self):
        temp = []
        for item in self.cubits:
            temp.append(self.colours_face[item[0]][0][0])
        self.cubestring[self.colours_face[self.cubits[4][0]][1][0]:self.colours_face[self.cubits[4][0]][1][1]] =\
        temp[:]
        print(self.cubestring)
        self.map_face()

    def Solve(self):
        """Solve the Cube using KC library
        Remove any "2" and replace with doulbe steip for Cube Library"""
        try:
            self.steplist = kc.solve(self.cube.get_kociemba()).split()
        except ValueError as e:
            print(e)
            self.steplist = []
            self.lbl_sol.config(text = "Invalid Cube. Cannot Solve")
        if len(self.steplist) >0:
            for i,step in enumerate(self.steplist):
                if len(step)==2:               
                    if step[1] == '2':
                        self.steplist[i]=self.steplist[i][0]
                        self.steplist.insert(i,self.steplist[i])       
            self.lbl_sol.config(text = ''.join(self.steplist))
        self.step=0
    def Next(self):
        if self.step<len(self.steplist):                       
            self.cube.Turn(self.steplist[self.step])         
            print(self.step)
            self.step+=1
        self.map_face()
    
    def map_face(self):
        """Map Cube Definition to GUI Cube"""
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

                self.cubits[number] = (self.colorNames[minDist[1]],int(minDist[0]))
                self.cubits_mean[number]=[r,g,b]
                       
        console_text =''
        #Generate Console Text
        #Average Colours and Closest Colour match for face cubits
        for number, item in enumerate(self.cubits_mean):
            console_text += 'Cube('+str(number).strip() +") {:<6}(d:{:03d})| R:{:03d} - G:{:03d} - B:{:03d}\n".format(*self.cubits[number], item[2],item[1],item[1])

        cv2.putText(frame,'0',(self.Face_Rectangles[0][0][0]+int(self.CV_RParam[3]/2)-10,self.Face_Rectangles[0][0][1]+int(self.CV_RParam[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'1',(self.Face_Rectangles[3][0][0]+int(self.CV_RParam[3]/2)-10,self.Face_Rectangles[3][0][1]+int(self.CV_RParam[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'2',(self.Face_Rectangles[6][0][0]+int(self.CV_RParam[3]/2)-10,self.Face_Rectangles[6][0][1]+int(self.CV_RParam[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'3',(self.Face_Rectangles[1][0][0]+int(self.CV_RParam[3]/2)-10,self.Face_Rectangles[1][0][1]+int(self.CV_RParam[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'4',(self.Face_Rectangles[4][0][0]+int(self.CV_RParam[3]/2)-10,self.Face_Rectangles[4][0][1]+int(self.CV_RParam[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'5',(self.Face_Rectangles[7][0][0]+int(self.CV_RParam[3]/2)-10,self.Face_Rectangles[7][0][1]+int(self.CV_RParam[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'6',(self.Face_Rectangles[2][0][0]+int(self.CV_RParam[3]/2)-10,self.Face_Rectangles[2][0][1]+int(self.CV_RParam[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'7',(self.Face_Rectangles[5][0][0]+int(self.CV_RParam[3]/2)-10,self.Face_Rectangles[5][0][1]+int(self.CV_RParam[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,'8',(self.Face_Rectangles[8][0][0]+int(self.CV_RParam[3]/2)-10,self.Face_Rectangles[8][0][1]+int(self.CV_RParam[3]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2,cv2.LINE_AA)
        self.console.delete('1.0', Tk.END)
        self.console.insert('1.0',console_text)
        self.console.insert(Tk.END,'Face Detected:'+self.colours_face[self.cubits[4][0]][0]) 
                # return the name of the color with the smallest distance
                #print(self.colorNames[minDist[1]])
            
                #self.nearest[number].set(self.colorNames[minDist[1]])
                #self.detect_colour = False
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(500, self.GUI_Params_Cube[1], image = self.photo, anchor = Tk.NW)

        face_cnt_str = 'Number of Cubits - Up(W):{:0>2d} | Ri(R):{:0>2d} |Fr(G):{:0>2d} |Do(Y):{:0>2d} |Le(O):{:0>2d} |Ba(B):{:0>2d}. \n Number of Cubits {}'.format(*self.cube.Face_Counter())
        self.lbl_fcnt.config(text=face_cnt_str)
 
        self.window.after(self.delay, self.update)    
                
    def _delete_window(self):
        print("closing")
        try:
            del(self.vid)
            self.window.destroy()
        except:
            pass
            
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
CubeG = CubeGUI(Cube,0)


