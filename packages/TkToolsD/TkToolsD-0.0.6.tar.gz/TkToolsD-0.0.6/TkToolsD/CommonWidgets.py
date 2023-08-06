# -*- coding:utf-8 -*- 
# Date: 2018-03-07 16:41:50
# Author: dekiven

import os
from DKVTools.Funcs import *

if isPython3() :
	from tkinter import *
	import tkinter.filedialog as fileDialog
	import tkinter.messagebox as messageBox
else:
	from Tkinter import *
	import tkFileDialog as fileDialog
	import tkMessageBox as messageBox


Pathjoin = os.path.join
PathExists = os.path.exists
# curDir = os.getcwd()
curDir = os.path.split(sys.argv[0])[0]

def GetDirWidget(root, title, pathDefault, pathSaved = None, callback = None, enableEmpty = False):
	widget = Frame(root)

	strTitle = StringVar()
	strTitle.set(title)
	Label(widget, textvariable = strTitle, width = 20).grid(row = 1, column = 0)

	strPathD = StringVar()
	strPathD.set(pathDefault)
	Label(widget, textvariable = strPathD).grid(row = 0, column = 1)

	strTitle = StringVar()
	strTitle.set(title)
	et = StringVar()
	if pathSaved :
		et.set(pathSaved)

	Entry(widget, textvariable = et, width = 90).grid(row = 1, column = 1)

	def btnCallback():
		def onChoosen(path):
			if path is not None and path != '' or enableEmpty :
				setValue(path)
				if callback is not None :
					if not isinstance(path, str):
						path = path
					callback(path)
		ShowChooseDirDialog(onChoosen, initialdir=et.get())


	Button(widget, text = u'Search', command = btnCallback, width = 15).grid(row = 1, column = 2)

	widget.strTitle = strTitle
	widget.strPathD = strPathD
	widget.et = et

	def setValue(value):
		et.set(value)
	widget.setValue = setValue

	return widget

def ShowChooseDirDialog(callback=None, **options):	
	'''options = {
	'defaultextension' : '.txt',
	'filetypes' : [('all files', '.*'), ('text files', '.txt')],
	'initialdir' : initDir,
	'initialfile' : 'myfile.txt',
	'parent' : root,
	'title' : 'This is a title',
}
可部分或全部不设置	
	'''
	# def funcTemp():
	path = fileDialog.askdirectory(**options)
	if callback is not None :
		if not isinstance(path, str):
			path = path
		callback(path)
	# return funcTemp


def ShowChooseFileDialog(callback=None, **options):	
	'''options = {
	'defaultextension' : '.txt',
	'filetypes' : [('all files', '.*'), ('text files', '.txt')],
	'initialdir' : initDir,
	'initialfile' : 'myfile.txt',
	'parent' : root,
	'title' : 'This is a title',
}
可部分或全部不设置
	'''

	# def funcTemp():
	path = fileDialog.askopenfilename(**options)
	if callback is not None :
		if not isinstance(path, str):
			path = path
		callback(path)
	# return funcTemp

def ShowInfoDialog(msg, title = u'Tips'):
	return messageBox.showinfo(title = title, message = msg)

def ShowAskDialog(msg, title = u'Asking'):
	return messageBox.askokcancel(title = title, message = msg)


def main():
	# GetDirWidget(None,None,None)
	# ShowInfoDialog('t')
	# ShowAskDialog('T')
	# def test(p) :
	# 	print(p)
	# ShowChooseDirDialog(test, initialdir='')
	help(ShowChooseDirDialog)


if __name__ == '__main__':
	main()
