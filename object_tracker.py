#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  cv, cv2, math
import numpy as np
import time
import gc

class ColorTracker:
	def __init__(self, camera_num, width, height, scale):
		self.camera_num = camera_num
		self.width = width
		self.height = height
		self.camera = None
		self.frame_count = 0
		self.recovery_count = 0		
		self.frame = None
		self.capture_time = 0.0
		self.scale_down = scale
		self.sensitivity = 300 #higher is less sensitive i.e. objects most be closer to recognize at higher setting
		self.hsv = None
		#pink ball lower_HSV: [130   3 248]  upper_HSV: [162  54 255]
		self.hue_high = 165
		self.hue_low = 135
		self.sat_high = 55
		self.sat_low = 3
		self.val_high = 255
		self.val_low = 245

		#self.hue_high = 0
		#self.hue_low = 180
		#self.sat_high = 0
		#self.sat_low = 255
		#self.val_high = 0
		#self.val_low = 255
		
		self.lower_HSV = np.array([self.hue_low, self.sat_low, self.val_low])
		self.upper_HSV = np.array([self.hue_high, self.sat_high, self.val_high])
		print self.lower_HSV , self.upper_HSV
		cv2.namedWindow("threshold")
		cv2.namedWindow("ColorTrackerWindow" , cv2.CV_WINDOW_AUTOSIZE)
		

	def on_mouse(self, event,x,y,flag,param):
		if (event==cv.CV_EVENT_LBUTTONDOWN): 
			print x,y
			hsv_color = self.hsv[y][x]
			rgb_color = self.frame[y][x]
			print "H:",hsv_color[0],"      S:",hsv_color[1],"       V:",hsv_color[2]
			print "R:",rgb_color[2],"      B:",rgb_color[0],"       G:",rgb_color[1]
			if hsv_color[0] > self.hue_high: self.hue_high = hsv_color[0] 
			if hsv_color[0] < self.hue_low: self.hue_low = hsv_color[0] 
			if hsv_color[1] > self.sat_high: self.sat_high = hsv_color[1]
			if hsv_color[1] < self.sat_low: self.sat_low = hsv_color[1]
			if hsv_color[2] > self.val_high: self.val_high = hsv_color[2]
			if hsv_color[2] < self.val_low: self.val_low = hsv_color[2]
			self.lower_HSV = np.array([self.hue_low, self.sat_low, self.val_low], np.uint8)
			self.upper_HSV = np.array([self.hue_high, self.sat_high, self.val_high],np.uint8)
			print "lower_HSV:", self.lower_HSV, " upper_HSV:" , self.upper_HSV

		if (event==cv.CV_EVENT_MBUTTONDOWN):
			#on middle mouse button reset all values
			print "resetting values"
			self.hue_high = 0
			self.hue_low = 180
			self.sat_high = 0
			self.sat_low = 255
			self.val_high = 0
			self.val_low = 255
			print self.lower_HSV , self.upper_HSV
			self.lower_HSV = np.array([self.hue_low, self.sat_low, self.val_low])
			self.upper_HSV = np.array([self.hue_high, self.sat_high, self.val_high])

	def initialize_camera(self):
			if self.camera_num <> "":
				self.camera = cv2.VideoCapture(self.camera_num)
				self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.width) 
				self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.height) 
				#self.camera1.set(cv2.cv.CV_CAP_PROP_FPS, 10)
				#self.camera.set(cv2.cv.CV_CAP_PROP_EXPOSURE, 10)
				self.camera.set(cv2.cv.CV_CAP_PROP_CONTRAST,0.70)
				self.camera.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS,0.1)
				#self.camera.set(cv2.cv.CV_CAP_PROP_GAIN,0.1)
				self.camera.set(cv2.cv.CV_CAP_PROP_HUE,0.2)
				self.camera.set(cv2.cv.CV_CAP_PROP_SATURATION ,0.8)
				print "contrast:", self.camera.get(cv2.cv.CV_CAP_PROP_CONTRAST)
				print "brightness:", self.camera.get(cv2.cv.CV_CAP_PROP_BRIGHTNESS)
				print "gain:", self.camera.get(cv2.cv.CV_CAP_PROP_GAIN)
				print "hue:", self.camera.get(cv2.cv.CV_CAP_PROP_HUE)
				print "satuation:", self.camera.get(cv2.cv.CV_CAP_PROP_SATURATION )

	def grab_frame(self):
		now = time.time()
		local_frame = None
		try:
			ret, local_frame = self.camera.read()
		except:
			pass
		self.capture_time = (time.time()-now)
		if self.capture_time > 0.4 or local_frame == None:
			#time.sleep(1)
			print "camera fault: recovering...", self.recovery_count
			self.recovery_count += 1
			try:
				if self.camera != None:
					self.camera.release	
				gc.enable()
				gc.collect()			
				self.initialize_camera()
			except:
				#time.sleep(.1)
				pass
			self.grab_frame()
		else:
			self.frame_count += 1		
			self.frame = local_frame

	def run(self):
		self.initialize_camera()
		cv.SetMouseCallback("ColorTrackerWindow",self.on_mouse);
		while True:
			time.sleep(0.001)
			self.grab_frame()

			#flip image to give correct prospective
			#self.frame = cv2.flip(self.frame, 1)
		
			#scale
			self.frame = cv2.resize(self.frame, (len(self.frame[0]) / self.scale_down, len(self.frame) / self.scale_down))
			
            #blur the source image to reduce color noise 
   			#self.frame = cv2.blur(self.frame,(3,3))
			#self.frame = cv2.GaussianBlur(self.frame, (9,9), 0)

			#split color channels		
			#r,g,b = cv2.split(self.frame)
			# create a CLAHE object (Arguments are optional).
			#clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
			#r = clahe.apply(r)
			#g = clahe.apply(g)
			#b = clahe.apply(b)
			#self.frame = cv2.merge([r,g,b])

			# convert to hsv and find range of colors
			self.hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)
			#print self.hsv, self.lower_HSV, self.upper_HSV
			thresh = cv2.inRange(self.hsv ,self.lower_HSV , self.upper_HSV )
			
			#brightness = np.mean(self.hsv[[[2]]])
			#print "mean brightness:", brightness 

			#thresh = cv2.GaussianBlur(thresh, (5,5), 0)

			dilation = np.ones((12, 12), "uint8")
			thresh  = cv2.dilate(thresh , dilation)

			# find contours in the threshold image
			contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

			#contours, hierarchy = cv2.findContours(thresh,cv.CV_RETR_TREE ,cv.CV_CHAIN_APPROX_NONE)
			max_area = 0
			largest_contour = None
			for idx, contour in enumerate(contours):
				area = cv2.contourArea(contour)
				if area > max_area:
					max_area = area
					largest_contour = contour

			if largest_contour == None:
				print "No Target Object in Frame"
				cv2.putText(self.frame, "No Target Object in Frame",(0,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0) )		

			if not largest_contour == None:
				moment = cv2.moments(largest_contour)
				if moment["m00"] > self.sensitivity / self.scale_down:
					rect = cv2.minAreaRect(largest_contour)
					rect = ((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), rect[2])
					box = cv2.cv.BoxPoints(rect)
					box = np.int0(box)
					cv2.drawContours(self.frame,[box], 0, (0, 0, 255), 2)

					#draw circle in center of mass
					cx,cy = int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])
					cv2.circle(self.frame,(cx,cy),3,255,-1)

					#cv2.drawContours(self.frame,[largest_contour],0, (0,0,0),  thickness=3)
					#send out center of mass coordinates and area size
					st = "Target X:" + str(cx) + ' Y:' + str(cy) + "   Area:" + str(moment["m00"])
					print st
					cv2.putText(self.frame, st ,(0,50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0) )
					approx = cv2.approxPolyDP(largest_contour,0.01*cv2.arcLength(largest_contour,True),True)
					'''
					print "# of Corners:", len(approx)
					if len(approx)==5:
						print "pentagon"
					if len(approx)==3:
						print "triangle"
					if len(approx)==4:
						print "square"
					if len(approx) >= 9 and len(approx) <= 11:
						print "half-circle"
					if len(approx) >= 9 and len(approx) <= 17:
						print "circle"
					'''
			cv2.imshow("ColorTrackerWindow", self.frame)
			cv2.imshow("threshold", thresh)

			# Clean up everything before leaving
			if cv2.waitKey(10) == 27 or cv2.waitKey(10) == 1048603:
				cv2.destroyWindow("ColorTrackerWindow")
				self.capture.release()
				break

if __name__ == "__main__":

	#color_tracker = ColorTracker("20131125_103550.mp4",640,480, 2)
	color_tracker = ColorTracker(0,640,480,1)
	color_tracker.run()


