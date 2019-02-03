import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
from scipy.spatial import distance as dist
from collections import OrderedDict

def click(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, New
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		New = True
		#print(refPt)




vs = cv2.VideoCapture(0)#VideoStream(src=0).start()

cv2.namedWindow("image")
cv2.setMouseCallback("image", click)

refPt = []
New = False

Face_Rectangles = []
start = (10,10)
size = 60
space = 60
for j in range(3):
	for i in range(3):
		Face_Rectangles.append([(start[0]+i*size+i*space,start[1]+j*size+j*space),(start[0]+i*size+i*space+size,start[1]+j*size+j*space+size)])
print(Face_Rectangles)



colors = OrderedDict({
			"red": (230, 80, 60),
			"green": (30, 200, 120),
			"blue": (0, 0, 255),
			"orange":(255,165,40),
			"white":(200,200,200),
			"yellow":(250,250,100)})

lab = np.zeros((len(colors), 1, 3), dtype="uint8")
colorNames = []

# loop over the colors dictionary
for (i, (name, rgb)) in enumerate(colors.items()):
	# update the L*a*b* array and the color names list
	lab[i] = rgb
	colorNames.append(name)

# convert the L*a*b* array from the RGB color space
# to L*a*b*
lab = cv2.cvtColor(lab, cv2.COLOR_RGB2BGR)#LAB)
print(lab)
while True:
	
	
	ret,frame = vs.read()
	
	#frame = frame[1] if args.get("video", False) else frame
	
	if frame is None:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	
	resized = imutils.resize(frame, width=600)
	
	
		#print(refPt)
		#try:
		#	pass
			#a,b =refPt[0][1],refPt[0][0]
			#x= frame[]
			#print(a,b)
			#x= frame[a,b]
			#B,G,R = frame[a,b]
			#print(B,G,R )
		##except:
			#pass
		#print(frame[refPt[0],refPt[1]])
		
	mask = np.zeros(frame.shape[:2], dtype="uint8")
	#c = np.array([[200,150],[260,210]])
	#cv2.drawContours(mask, c, -1, 255, -1)
	test = np.copy(frame)
	#test = cv2.cvtColor(test, cv2.COLOR_RGB2LAB)
	#test = test
	if New:
		print("New")
		New = False
		for item in Face_Rectangles:
			minDist = (np.inf, None)
			#mask = cv2.erode(test[150:210,200:260], None, iterations=2)
			mask = cv2.erode(test[item[0][0]:item[1][0],item[0][1]:item[1][1]], None, iterations=2)
			b,g,r,_=np.uint8(cv2.mean(mask))
			mean = cv2.mean(mask)
	#print(mean[:3])
	#mean = cv2.mean(frame, mask=([150:210,200:260]))[:3]
	#print(b,g,r)
	# initialize the minimum distance found thus far
	
	#if New:
			#a,b =refPt[0][1],refPt[0][0]
			#x= frame[a,b]
			#B,G,R = frame[a,b]
			##print(R,G,B )
			#New = False
			#print(lab)
				# loop over the known L*a*b* color values
			for (i, row) in enumerate(lab):
				#print(i,row)
				# compute the distance between the current L*a*b*
				# color value and the mean of the image
				pass
				#print(row[0])
				d = dist.euclidean(row[0], mean[:3])
				#print(d)
				# if the distance is smaller than the current distance,
				# then update the bookkeeping variable
				if d < minDist[0]:
					minDist = (d, i)

				# return the name of the color with the smallest distance
			print(colorNames[minDist[1]])

	
	
	for item in Face_Rectangles:
		#cv2.rectangle(frame,(200,150),(260,210),(0,255,0),3)
		cv2.rectangle(frame,item[0],item[1],(0,255,0),3)
	cv2.imshow("image", frame)


	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("q"):
		
		break
		
vs.release()
# close all windows
cv2.destroyAllWindows()