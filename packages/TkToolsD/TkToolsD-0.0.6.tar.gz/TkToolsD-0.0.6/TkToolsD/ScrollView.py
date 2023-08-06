# -*- coding:utf-8 -*- 
# Date: 2018-03-08 10:27:20
# Author: dekiven

import os
from DKVTools.Funcs import *

if isPython3() :
	import tkinter as tk	
else:
	import Tkinter as tk

# test
# from CommonWidgets import *

#import sys 
#reload(sys)
#sys.setdefaultencoding('utf-8')

class ScrollView(tk.Frame):
	'''ScrollView
	'''
	# scrollbar orientation vertical
	BarDir_V = 0b0001
	# scrollbar orientation horizontal
	BarDir_H = 0b0010
	# scrollbar orientation both vertical and horizontal
	BarDir_B = 0b0011

	__keySetLeft = ('Left')
	__keySetRight = ('Right')
	__keySetUp = ('Up')
	__keySetDown = ('Down')

	def __init__(self, *args, **dArgs) :
		tk.Frame.__init__(self, *args, **dArgs)
		self.scrollbarV = None
		self.scrollbarH = None
		self.mouseIn = False
		self.focus = False
		self.size = (dArgs.get('width') or 0, dArgs.get('height') or 0)

		# 设置canvas所在单元格(0, 0)可缩放
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		
		# 创建canvas，随单元格大小缩放
		# canvas = tk.Canvas(self,width=200, height=200, bd=0, highlightthickness=0)
		canvas = tk.Canvas(self, bd=0, highlightthickness=0, takefocus=1)
		canvas.grid(column=0, row=0, sticky=tk.N+tk.W+tk.S+tk.E)
		# 设置canvas中放内容的单元格可缩放
		# canvas.columnconfigure(0, weight=1)
		# canvas.rowconfigure(0, weight=1)

		self.canvas = canvas

		# 创建frame放置要显示的额内容，随单元格缩放
		frame = tk.Frame(canvas)
		frame.grid(sticky=(tk.N, tk.W, tk.S, tk.E))
		canvas.create_window(0, 0, anchor=tk.N+tk.W, window=frame, tags='content')
		self.contentFrame = frame

		# 默认显示两个方向的滚动条
		self.setBarOrientation(self.BarDir_B)

		self.__registEvents()

		# self.updateContentSize()


	def getCanvas(self):
		return self.canvas

	def getContentFrame(self):
		return self.contentFrame

	def setBarOrientation(self, orientation):
		self.barOrient = orientation
		canvas = self.canvas

		# 有竖直方向的滚动条
		scrollbar = self.scrollbarV
		frame = self.contentFrame

		if orientation & self.BarDir_V > 0:
			if scrollbar is None:
				scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
				scrollbar.configure(command=self.__yview)
				canvas.configure(yscrollcommand=scrollbar.set)
				self.scrollbarV = scrollbar
				scrollbar.grid(column=1, row=0,sticky=tk.N+tk.S)
			else :
				config = scrollbar.grid_info()
				# scrollbar.grid()
				scrollbar.grid(**config)
		elif scrollbar is not None:
			scrollbar.grid_remove()

		# 有水平方向的滚动条
		scrollbar = self.scrollbarH
		if orientation & self.BarDir_H > 0:
			if scrollbar is None:
				scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
				scrollbar.configure(command=self.__xview)
				canvas.configure(xscrollcommand=scrollbar.set)
				self.scrollbarH = scrollbar
				scrollbar.grid(column=0, row=1, sticky=tk.W+tk.E)
			else :
				config = scrollbar.grid_info()
				# scrollbar.grid()
				scrollbar.grid(**config)
		elif scrollbar is not None:
			scrollbar.grid_remove()

	def movetoPercentV(self, percent) :
		self.canvas.yview('moveto', str(percent/100.0))

	def movetoPercentH(self, percent) :
		self.canvas.xview('moveto', str(percent/100.0))

	def moveToTop(self) :
		self.movetoPercentV(0)

	def moveToBottom(self) :
		self.movetoPercentV(100)

	def movetToLeft(self) :
		self.movetoPercentH(0)

	def movetToRight(self) :
		self.movetoPercentH(100)

	def moveUpOneStep(self) :
		self.canvas.yview(tk.SCROLL, -1, tk.UNITS)

	def moveDownOneStep(self) :
		self.canvas.yview(tk.SCROLL, 1, tk.UNITS)

	def moveLeftOneStep(self) :
		self.canvas.xview(tk.SCROLL, -1, tk.UNITS)

	def moveRightOneStep(self) :
		self.canvas.xview(tk.SCROLL, 1, tk.UNITS)

	def updateLayout(self) :
		'''在修改了frame中的显示内容后需要调用一次
		'''
		self.contentFrame.update_idletasks()
		self.updateContentSize()

	def __yview(self, *args, **dArgs) :
		# print('yview', args, dArgs)
		self.canvas.yview(*args, **dArgs)

	def __xview(self, *args, **dArgs) :
		# print('xview', args, dArgs)
		self.canvas.xview(*args, **dArgs)

	def __registEvents(self) :
		# self.tag_configure("overstrike", overstrike=True)
		# 注册控件大小改变事件监听
		self.bind('<Configure>', self.__on_configure)
		# TODO:注册鼠标中键滑动监听
		self.bind('<MouseWheel>', self.__on_mouseWheel)
		# TODO:注册鼠标进入退出监听
		self.bind('<Enter>', self.__on_mouseEnter)
		self.bind('<Leave>', self.__on_mouseLeave)

		self.bind('<FocusIn>', self.__on_focusIn)
		self.bind('<FocusOut>', self.__on_focusOut)
		# TODO:注册键盘按键监听
		self.bind('<Key>', self.__on_key)

	def updateContentSize(self, w=None, h=None) :
		w = w or self.size[0]
		h = h or self.size[1]
		# print(w, h)

		canv = self.canvas
		frame = self.contentFrame

		natural = frame.winfo_reqwidth()
		canv.itemconfigure('content', width= w if w>natural else natural)
		natural = frame.winfo_reqheight()
		canv.itemconfigure('content', height= h if h>natural else natural)
		canv.configure(scrollregion=canv.bbox('all'))


	# TODO:事件处理
	def __on_configure(self, event) :
		'''在窗口大小改变时，保证显示内容的窗口（不是freme，frame只是显示内容的容器）的大小跟canvas一样大
		'''
		self.size = (event.width, event.height)
		self.updateContentSize()

	def __on_key(self, event) :
		if self.focus :		
			key = event.keysym
			# print(key)
			if key in self.__keySetUp :
				self.moveUpOneStep()
				# return
			elif key in self.__keySetDown :
				self.moveDownOneStep()
				# return
			elif key in self.__keySetLeft :
				self.moveLeftOneStep()
				# return
			elif key in self.__keySetRight :
				self.moveRightOneStep()
				# return

		# return 'break'

	def __on_mouseEnter(self, event) :
		# self.pass
		# print('enter')
		if not self.focus and not self.mouseIn:
			self.focus_set()
		self.mouseIn = True

	def __on_mouseLeave(self, event) :
		# print('leave')
		self.mouseIn = False
		# self.focus_set()

	def __on_mouseWheel(self, event) :
		# print(event.delta)
		if self.focus :
			if event.delta > 0 :
				self.moveUpOneStep()
			else :
				self.moveDownOneStep()

	def __on_focusIn(self, event) :
		# print('in')
		# if not self.focus :
		# 	ShowChooseFileDialog()
		self.focus = True

	def __on_focusOut(self, event) :
		# print('out')
		self.focus = False

def main():
	# help(ScrollView)
	s = ScrollView(None)
	master = s.master
	master.columnconfigure(0, weight=1)
	master.rowconfigure(0, weight=1)
	s.setBarOrientation(3)
	s.grid(sticky=tk.N+tk.W+tk.S+tk.E)
	__test(s)
	s.mainloop()

# test ================================begin====
def getCounter(start=0) :
	c = [start]
	def count() :
		c[0] += 1
		return c[0]
	return count

def __test(s) :
	# test
	frame = s.getContentFrame()
	for i in range(20):
		m = __MessageItem(frame, 'Something Profound', bd=2, bg='black')
		m.grid(row=i, column=0, sticky='nsew', padx=2, pady=2)
	s.updateLayout()


class __MessageItem(tk.Frame):
	"""A message to be contained inside a scrollableContainer"""
	def __init__(self, master, message, **kwds):
		tk.Frame.__init__(self, master, **kwds)
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.text = tk.Label(self, text=message, anchor='w', bg='gold')
		self.text.grid(row=0, column=0, sticky='nsew')

# test ===================================end=======


if __name__ == '__main__':
	main()