#Program to reannotate the images 
#Essential imports
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty,BooleanProperty
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle
from os import listdir, remove,walk
from os.path import dirname as os_dirname
from os.path import exists as os_exists
from os import makedirs as os_makedirs
from shutil import copyfile, move
import cv2
import numpy as np
from functools import partial
#-------------------------------------------------------------------------------------------
class ImageButton(ButtonBehavior, Image):
	pass
class HomeScreen(Screen):
	
	def __init__(self,**kwargs):
		super(HomeScreen,self).__init__(**kwargs)
		self.LoadImageList()
		self.DefineImageView()
		self.DefineButtonView()
	
	def LoadImageList(self):
		self.image_length = 704                    #Enter the dimentions of the image
		self.image_breadth =  1280
		self.LoadDataDir = "./images/"
		self.LoadGtDir = "./labels/"
		self.SaveDataDir = "./final_images/"
		self.SaveGtDir = "./final_labels/"
		self.ensure_dir("./.temp/")
		folders = self.get_folders(self.LoadDataDir)
		self.DataList = self.get_files(folders,".jpg")
		# self.DataList = ([(self.LoadDataDir + i) for i in listdir(self.LoadDataDir) if (".jpg" in i)])
		self.DataList.sort()
		self.CurrentID = 0
		self.class_color = {0:0,1:0,2:250}
		for i in range(3,256):
			self.class_color[i] = 0
		self.NowEdit = 0
	
	def DefineImageView(self):
		#Position and dimention of the image and ground truth
		self.DataW, self.DataH = 0.5, 2.0/3.0
		self.DataX, self.DataY = 0.25, 2.0/3.0
		self.GtW, self.GtH = 0.5, 2.0/3.0
		self.GtX, self.GtY = 0.75, 2.0/3.0
	
	def DefineButtonView(self):
		#Dimention and position of the buttons
		self.CorrectW, self.CorrectH = 0.24, 0.1
		self.CorrectX, self.CorrectY = 0.125, 0.15
		self.WrongW, self.WrongH = 0.24, 0.1
		self.WrongX, self.WrongY = 0.375, 0.15
		self.UndoW, self.UndoH = 0.24, 0.1
		self.UndoX, self.UndoY = 0.875, 0.15
	
	def on_pre_enter(self):
		self.clear_widgets()
		if self.CurrentID > (len(self.DataList)-1):
			print ("All Done :)")
			App.get_running_app().stop()
			return 0

		self.DataImageSource = self.DataList[self.CurrentID]
		self.GtImageSource = self.LoadGtDir + self.DataList[self.CurrentID][len(self.LoadDataDir):-3] + "png" #Did not understand
		self.NowGtImage = "./.temp/" + str(self.NowEdit) + ".png"
		self.RootGtImage = self.NowGtImage[:-4]+"root.png"
		self.img = cv2.imread(self.GtImageSource,0)
		self.RootImg = cv2.imread(self.GtImageSource)
		#self.img = np.vectorize(self.class_color.get, otypes=[np.float])(self.img)
		#lower = np.array([245,245,245])
		#upper = np.array([255,255,255])
		#mask = cv2.inRange(self.img,lower,upper)
		_,self.contours,_ = cv2.findContours(self.img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		cv2.drawContours(self.img,self.contours, -1, (0,255,0), 2)
		cv2.imwrite(self.NowGtImage,self.img)
		cv2.imwrite(self.RootGtImage,self.RootImg)
		self.ShowWindow()
	
	def ShowWindow(self):
		self.ShowImages()
		self.ShowButtons()

	def on_touch_down(self,touch):
		#On mouse click 
		x = int((touch.spos[0]-0.5)*(self.image_breadth*2))
		y = int((1.0-touch.spos[1])*(self.image_length*(3.0/2.0)))
		# The click is getting detected
		# Check whether the contours are getting generated or not. 
		for contour in self.contours:
			dist = cv2.pointPolygonTest(contour,(x,y),True)
			if(dist>=0):
				cv2.fillPoly(self.img, pts =[contour], color=(0,0,0))
				cv2.fillPoly(self.RootImg, pts =[contour], color=(0,0,0))
				self.NowEdit += 1
				self.NowGtImage = "./.temp/" + str(self.NowEdit) + ".png"
				self.RootGtImage = self.NowGtImage[:-4]+"root.png"
				cv2.imwrite(self.NowGtImage, self.img)
				cv2.imwrite(self.RootGtImage, self.RootImg)
				self.GtImage.source = self.NowGtImage
				self.GtImage.reload()
				self.ShowImages()
		super(HomeScreen, self).on_touch_down(touch)	
	
	def ShowImages(self):
		# To display the images for the tweaking purposes
		# DataImageGrid = GridLayout(cols=1)
		source = self.DataImageSource
		self.DataImage = ImageButton(source=source,size_hint=(self.DataW,self.DataH),pos_hint={"center_x":self.DataX,"center_y":self.DataY},keep_ratio=False,allow_stretch=True)
		self.add_widget(self.DataImage)
		source = self.NowGtImage
		self.GtImage = ImageButton(source=source,size_hint=(self.GtW,self.GtH),pos_hint={"center_x":self.GtX,"center_y":self.GtY},keep_ratio=False,allow_stretch=True)
		self.add_widget(self.GtImage)
		self.GtImage.reload()
	
	def ShowButtons(self):
		#Displaying the buttons on the screen
		CorrectBtn = Button(text="CORRECT",font_size=25,size_hint=(self.CorrectW,self.CorrectH),pos_hint={"center_x":self.CorrectX,"center_y":self.CorrectY},valign="center",halign="center",on_press=partial(self.NextImage,True))
		self.add_widget(CorrectBtn)
		WrongBtn = Button(text="WRONG",font_size=25,size_hint=(self.WrongW,self.WrongH),pos_hint={"center_x":self.WrongX,"center_y":self.WrongY},valign="center",halign="center",on_press=partial(self.NextImage,False))
		self.add_widget(WrongBtn)
		UndoBtn = Button(text="UNDO",font_size=25,size_hint=(self.UndoW,self.UndoH),pos_hint={"center_x":self.UndoX,"center_y":self.UndoY},valign="center",halign="center",on_press=partial(self.MakeUndo,"1"))
		self.add_widget(UndoBtn)
	
	def MakeUndo(self,x=0,_="_"):
		if(self.NowEdit>0):
			self.NowEdit -= 1
			self.NowGtImage = "./.temp/" + str(self.NowEdit) + ".png"
			self.RootGtImage = self.NowGtImage[:-4]+"root.png"
			self.img = cv2.imread(self.NowGtImage)
			self.RootImg = cv2.imread(self.RootGtImage)
			self.GtImage.source = self.NowGtImage
			self.GtImage.reload()
			self.on_pre_enter()
	
	def NextImage(self,ImageVal=False,_="_"):
		#Moving to the next image
		if(ImageVal):
			remove(self.GtImageSource)
			self.ensure_dir(self.SaveDataDir + self.DataImageSource[len(self.LoadDataDir):])
			self.ensure_dir(self.SaveGtDir + self.GtImageSource[len(self.LoadGtDir):])
			move(self.DataImageSource,self.SaveDataDir + self.DataImageSource[len(self.LoadDataDir):])
			move(self.RootGtImage,self.SaveGtDir + self.GtImageSource[len(self.LoadGtDir):])
			#So that the next image can load successfully
			self.NowEdit = 0
			self.CurrentID += 1
			self.on_pre_enter()
		else:
			remove(self.DataImageSource)
			remove(self.GtImageSource)
			self.NowEdit = 0
			self.CurrentID += 1
			self.on_pre_enter()

#Code for file traversal and ensuring that the folders exist
	def ensure_dir(self,file_path):
		if '/' in file_path:
			directory = os_dirname(file_path)
		if not os_exists(directory):
			os_makedirs(directory)
	def get_folders(self,root_folder):
		folders = []
		folders.append(root_folder)
		for (dirpath, dirnames, filenames) in walk(root_folder):
			for fold in dirnames:
				folders.append(dirpath + fold + '/')
		return(folders)
	def get_files(self,folders,ext):
		files = []
		for folder in folders:
			files_fold = ([(folder+i) for i in listdir(folder) if i.endswith(ext)])
			files_fold.sort()
			for filename in files_fold:
				files.append(filename)
		return(files)

class MainClass(App):
	def build(self):
		ScreenMan = ScreenManagerbuild()
		ScreenMan.add_widget(HomeScreen(name='home_window'))
		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass

if __name__ == '__main__':
	MainClass().run()