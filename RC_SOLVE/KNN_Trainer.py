import cv2
import tkinter as Tk
import PIL.Image, PIL.ImageTk
import numpy as np
import time as time
import csv
import random
import math
import operator
#import KNNT as KNNT
from scipy.spatial import distance
import os

class Cube_Trainer:
    def __init__(self,video_source,RParam =(30,10,45,65),**kwargs):
        self.__CFS()
        self.window = Tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self._delete_window)
        self.canvas = Tk.Canvas(self.window,width=600,height=480)
        self.canvas.grid(row=0,column=0,columnspan=10)
        self.delay = 15
        self.video_source = video_source
        self.CV_RParam = RParam
        self.Face_Rectangles = self.CV_rectangles(self.CV_RParam)
        self.NPI_Rectangles = [None,None,None,None,None,None,None,None,None]
        self.S_TI = Tk.Button(self.window,text ="Save Training Images", command = self.TI_save)
        self.S_TI.grid(row=1,column=0,padx=10,sticky="ew")
        self.S_Tr = Tk.Button(self.window,text ="Train", command = lambda: (self.__train(),self.__load_data()))
        self.S_Tr.grid(row=1,column=1,padx=10,sticky="ew")
        self.run = False
        self.S_GC = Tk.Button(self.window,text ="Run", command = lambda: self.GC_Toggle())
        self.S_GC.grid(row=1,column=3,padx=10,sticky="ew")

        #self.S_Te = Tk.Button(self.window,text ="Test", command = lambda: (self.__load_data()))
        #self.S_Te.grid(row=1,column=2,padx=10,sticky="ew")
        self.Pu_Btn = Tk.Button(self.window,text ="Purge", command = lambda: (self.__Purge()))
        self.Pu_Btn.grid(row=1,column=2,padx=10,sticky="ew")
        self.console = Tk.Label(self.window,text = "Console")
        self.console.grid(row=1,column=4, rowspan = 5)
        self.color = Tk.IntVar()
        self.lst_colors = ('white','red','green','orange','blue','yellow')
        self.trained_data = []       
        for n,color in enumerate(self.lst_colors):
            rbtn = Tk.Radiobutton(self.window,text=color,variable = self.color,value = n)
            rbtn.grid(row=2+n,column=0,sticky='w')
        self.test = 0
        self.__load_data()
        self.vid = MyVideoCapture(video_source)
        self.update()        
        self.window.mainloop()

    def __CFS(self):
        """Check the required files exist and create them if they dont"""
        if os.path.isdir('./Images'):
            for dir in('yellow','white','red','orange','green','blue'):
                if not os.path.isdir('./Images/'+dir):
                    os.mkdir('./Images/'+dir)
        else:
            os.mkdir('./Images')
            for dir in('yellow','white','red','orange','green','blue'):
                    os.mkdir('./Images/'+dir)
        if not os.path.isfile('./training.data'):
            open('training.data', 'w').close()

    def GC_Toggle(self):
        
        print('here')
        if self.run ==True:
            self.S_GC.config(text = "Run")
            self.run = False
        else:
            self.S_GC.config(text = "Stop")
            self.run = True
    def __Purge(self):
        """Delete All Training Data and Training Images"""
        for f in os.listdir('./Images/red'):
            os.remove('./Images/red/' + f)            
        for f in os.listdir('./Images/yellow'):
            os.remove('./Images/yellow/' + f)
        for f in os.listdir('./Images/green'):
            os.remove('./Images/green/' + f)
        for f in os.listdir('./Images/orange'):
            os.remove('./Images/orange/' + f)
        for f in os.listdir('./Images/white'):
            os.remove('./Images/white/' + f)
        for f in os.listdir('./Images/blue'):
            os.remove('./Images/blue/' + f)
        open('training.data', 'w').close()

    def CV_rectangles(self,XYSP):
        """Generate Rectangles For Face Colour Detection
        X,Y Start Coords - relative to frame size
        rectangel size"""
        X,Y,S,P = XYSP
        rectangles=[]
        for j in range(3):
            for i in range(3):
                rectangles.append([(X+i*S+i*P,Y+j*S+j*P),\
                                       (X+i*S+i*P+S,Y+j*S+j*P+S)])
        return rectangles
    
    def TI_save(self):
        #cv2.imsave
        #name = ''
        ts = str(time.time())
        for n, item in enumerate(self.NPI_Rectangles):
            name = 'C:\\Users\\Patrick\\source\\repos\\KNN_Trainer\\KNN_Trainer\\Images\\'+self.lst_colors[self.color.get()]+'\\'+ts+'_'+self.lst_colors[self.color.get()]+str(n)+'.jpg'            
            cv2.imwrite(name,cv2.cvtColor(item, cv2.COLOR_BGR2RGB))

    def update(self):
        cubits = [None,None,None,None,None,None,None,None,None]
        text = ''
        ret, frame = self.vid.get_frame()
        #if self.test <3:
        raw = np.copy(frame)
        #self.test += 1
        for n,item in enumerate(self.Face_Rectangles):
            cv2.rectangle(frame,item[0],item[1],(0,255,0),1)
            #self.NPI_Rectangles[n] = frame[item[0][1]:item[0][1]+self.CV_RParam[2],item[0][0]:item[0][0]+self.CV_RParam[2]]
            self.NPI_Rectangles[n] = raw[item[0][1]:item[1][1],item[0][0]:item[1][0]]
        if self.run == True:
            for i,item in enumerate(self.NPI_Rectangles):
                t=((self.frame_mean(item)))
                cubits[i]=[t[0],t[1][0]]
            for item in cubits:
                text += 'Colour Detected: {:<6}, Distance: {:4.1f}\n'.format(item[1],item[0])
            self.console.config(text=text)
        if ret:

            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            #self.canvas.config(width=480,height = 640)
            self.canvas.create_image(0, 0, image = self.photo, anchor = Tk.NW)
        
        self.window.after(self.delay, self.update)
    
    def __load_data(self):
        """Load trained data and map for use"""
        data = []
        with open('C:\\Users\\Patrick\\source\\repos\\KNN_Trainer\\KNN_Trainer\\training.data', 'r') as myfile:
            lines = myfile.readlines()
            
        for line in lines:
            line = line.rstrip()
            data.append([line.split(',')[0],tuple((map(int,line.split(',')[1:4])))])
        self.trained_data = [x for x in data]
             
    def frame_mean(self,hframe):
        minDist = (np.inf, None)
        mask = cv2.erode(hframe, None, iterations=2)
        b,g,r,_=np.uint8(cv2.mean(mask))
        for (i, row) in enumerate(self.trained_data):
            rgb = row[1]
            d = distance.euclidean(rgb[0:3], [b,g,r])
            if d < minDist[0]:
                        minDist = (d, self.trained_data[i])
        return minDist

    def color_mean(self,img_name):
        if 'red' in img_name:
            data_source = 'red'
        elif 'yellow' in img_name:
            data_source = 'yellow'
        elif 'green' in img_name:
            data_source = 'green'
        elif 'orange' in img_name:
            data_source = 'orange'
        elif 'white' in img_name:
            data_source = 'white'
        elif 'blue' in img_name:
            data_source = 'blue'

        image = cv2.imread(img_name)
        mask = cv2.erode(image, None, iterations=2)
        b,g,r,_=np.uint8(cv2.mean(mask))
        mean = cv2.mean(mask)
        feature_data = str(r) + ',' + str(g) + ',' + str(b)
        with open('training.data', 'a') as myfile:
            myfile.write(data_source + ',' + feature_data + '\n')

    def __train(self):
        # red color training images
        for f in os.listdir('./Images/red'):
            self.color_mean('./Images/red/' + f)
            
        # yellow color training images
        for f in os.listdir('./Images/yellow'):
            self.color_mean('./Images/yellow/' + f)

        # green color training images
        for f in os.listdir('./Images/green'):
            self.color_mean('./Images/green/' + f)

        # orange color training images
        for f in os.listdir('./Images/orange'):
            self.color_mean('./Images/orange/' + f)
        # white color training images
        for f in os.listdir('./Images/white'):
            self.color_mean('./Images/white/' + f)

        # blue color training images
        for f in os.listdir('./Images/blue'):
            self.color_mean('./Images/blue/' + f)

        
    def _delete_window(self):
        print("closing")
       #pickle.dump(self.colours,open("colours.p","wb"))
        #pickle.dump(self.cubestring,open("cubestring.p","wb"))
        try:
            del(self.vid)
            self.window.destroy()
        except:
            pass

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        #self.vid.set(cv2.CAP_PROP_EXPOSURE,-4); 
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


test = Cube_Trainer(0,(20,5,90,100))