from .CodeObject import CodeObject
from PyQt5.QtWidgets import QFrame, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import QFile, QFileSelector, QUrl, QVariant, pyqtSignal, QDir
from PyQt5.QtCore import pyqtProperty as Property
from .REButton import makeProperty
from .CodeButton import CodeButton
from .Base import BaseWidget
from bsstudio.functions import openFileAsString, getTopObject
import os
import time

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def relPath(selfPath, filePath):
	selfDir = os.path.dirname(selfPath)
	try:
		path = os.path.relpath(filePath, selfDir)
	except:
		path = ""
	return path

def absPath(selfPath, relFilePath):
	prefix = os.path.dirname(selfPath)
	ap = os.path.join(prefix, relFilePath)
	return ap

def convertPath(w, fileUrl,*,toRelative):
	val = fileUrl
	valPath = val.toLocalFile()
	self = w
	if self.windowFileName()=="":
		alert = QMessageBox(self)
		alert.setText("Current file has no name. Please save the current file first and try again.")
		alert.show()
		return None
	if valPath=="":
		alert = QMessageBox(self)
		alert.setText("Empty filename")
		alert.show()
		return None
	if self.windowFileName() is None or toRelative!=os.path.isabs(valPath):
		logger.info("self.windowFileName is None")
		return val
	if toRelative:
		rp = relPath(self.windowFileName(), valPath)
		return QUrl("file:"+rp)
	else:
		ap = absPath(self.windowFileName(), valPath)
		return QUrl("file:"+ap)


def wait_until_unpaused(obj):
	while obj._paused:
		time.sleep(.1)

def wait_until_all_children_unpaused(obj):
	for c in obj.children():
		if hasattr(c, "_paused"):
			wait_until_unpaused(obj)
			print(obj, obj._paused)

class CodeContainer(QFrame, CodeObject):
	def __init__(self, parent=None):
		QFrame.__init__(self,parent)
		CodeObject.__init__(self,parent)
		self.pauseWidget()
		original = self.resizeEvent
		#def resizeEvent(event):
		#	#print("codecontainer resize")
		#	original(event)
		#	if not self._paused:
		#		self.resumeChildren()
		#	#self.runCode()
		#	if self._paused:
		#		self.runPaused()
		#self.resizeEvent = resizeEvent

	
	@Property(bool, designable=True)
	def runInThread(self):
		return self._useThreading

	@runInThread.setter
	def runInThread(self, val):
		self._useThreading = val


	def default_code(self):
		return """
			ui = self.ui
			"""[1:]

	def resumeWidget(self):
		#if not self._paused:
		#	return
		CodeObject.resumeWidget(self)
		#wait_until_all_children_unpaused(self)
		self.resumeChildren()
		self.runCode()
		

from ..functions import deleteWidgetAndChildren

class EmbedFrame(QFrame, CodeObject):

	fileChanged = pyqtSignal()

	def deleteSubWindow(self):
		if hasattr(self,"subWindow"):
			#self.subWindow.setParent(None)
			#for c in self.subWindow.children():
			#	c.deleteLater()
			#self.subWindow.deleteLater()
			deleteWidgetAndChildren(self.subWindow)
		else:
			logger.info("no existing subwindow")



	def __init__(self, parent=None):
		QFrame.__init__(self,parent)
		CodeObject.__init__(self,parent)
		self._fileName = QUrl()
		self._macros = []
		self._useRelativePath = True
		self.fileChanged.connect(self.updateUi)
		original = self.resizeEvent
		def resizeEvent(event):
			original(event)
			#self.runCode()
			if hasattr(self, "subWindow"):
				self.subWindow.resize(self.size())

			if self._paused:
				self.runPaused()
		self.resizeEvent = resizeEvent

	def runPaused(self):
		self.updateUi()

	def getAbsPath(self):
		filename = self.fileName.toLocalFile()
		if not QDir.isAbsolutePath(filename):
			filename = absPath(self.windowFileName(), filename)
		return filename

	def frameUi(self):
		return self.subWindow

	def updateUi(self):
		from PyQt5.QtWidgets import QWidget
		from PyQt5.QtWidgets import QVBoxLayout
		ui = self.ui

		from PyQt5 import uic
		import io
		self.deleteSubWindow()

		self.subWindow = QWidget(self)
		
		self.subWindow.isTopLevel = True
		filename = self.fileName.toLocalFile()
		if self.windowFileName() is None:
			return
		if not QDir.isAbsolutePath(filename):
			filename = absPath(self.windowFileName(), filename)
		self.subWindow.uiFilePath = filename
		fileContents = openFileAsString(filename, self.macros)
		fileObject = io.StringIO(fileContents)
		try:
			uic.loadUi(fileObject, self.subWindow)
		except:
			logger.info("Error opening file "+filename)
			return
		self.subWindow.resize(self.size())
		self.subWindow.show()
		if not self._paused:
			self.resumeChildren()

		

	

	def default_code(self):
		return """
			from PyQt5.QtWidgets import QWidget
			from PyQt5 import uic
			import io
			ui = self.ui
			self.updateUi()
			"""[1:]

	def resumeWidget(self):
		if not self._paused:
			return
		CodeObject.resumeWidget(self)
		self.runCode()

	#def resumeFrame(self):
	#	#BaseWidget.resumeChildren(self.frameUi())
	#	children = self.findChildren(BaseWidget)
	#	for c in children:
	#		c.resumeWidget()


		

	#fileName = makeProperty("fileName", QUrl, notify=fileChanged)
	macros = makeProperty("macros", "QStringList")
	@Property("QUrl")
	def fileName(self):
		return self._fileName

	@fileName.setter
	def fileName(self, val):
			
		path = convertPath(self, val, toRelative=self._useRelativePath)
		if path is not None:
			#print("path",path)
			self._fileName=path
			self.fileChanged.emit()
		return
			
			

	@Property(bool)
	def useRelativePath(self):
		return self._useRelativePath

	@useRelativePath.setter
	def useRelativePath(self, val):
		self._useRelativePath = val
		self.fileName = self._fileName

	def __copy__(self):
		ef = EmbedFrame(self.parent())
		ef.macros = self.macros
		ef.fileName = self.fileName
		ef.useRelativePath = self.useRelativePath
		return ef




class OpenWindowButton(CodeButton):

	runInThread = Property(bool, designable=False) # Disabling property

	def deleteSubWindow(self):
		if hasattr(self,"subWindow"):
			deleteWidgetAndChildren(self.subWindow)
		else:
			logger.info("no existing subwindow")




	def __init__(self, parent=None):
		super().__init__(parent)
		self._fileName = QUrl()
		self._macros = []
		self._useRelativePath = True
		self._useThreading = False
	
	def default_code(self):
		return """
			from PyQt5.QtWidgets import QDialog, QFrame, QWidget, QApplication
			from PyQt5 import uic, QtCore
			from PyQt5.QtCore import QDir
			from PyQt5.Qt import Qt
			from bsstudio.functions import openFileAsString
			from bsstudio.widgets.embedframe import absPath, EmbedFrame
			import time
			import io
			ui = self.ui
			#if hasattr(self, "subWindow"):
			#	print("already has subwindow")
			#	self.subWindow.close()
			#self.deleteSubWindow()
			#self.subWindow = QDialog(self)
			self.subWindow = EmbedFrame(self)
			self.subWindow.setWindowFlags(Qt.Window)
			#self.subWindow = QDialog(self)
			self.subWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)

			self.subWindow.isTopLevel = True
			filename = self.fileName.toLocalFile()
			if not QDir.isAbsolutePath(filename):
				filename = absPath(self.windowFileName(), filename)
			self.subWindow.uiFilePath = filename
			fileContents = openFileAsString(filename, self.macros)
			fileObject = io.StringIO(fileContents)
			uic.loadUi(fileObject, self.subWindow)
			#self.resize(self.subWindow.size())
			self.subWindow.show()
			self.subWindow.update()
			self.subWindow.repaint()
			#QApplication.instance().processEvents()
			self.resumeChildren()
			"""[1:]

	def resumeWidget(self):
		self._paused = False
	

	@Property("QUrl")
	def fileName(self):
		return self._fileName

	@fileName.setter
	def fileName(self, val):
		path = convertPath(self, val, toRelative=self._useRelativePath)
		if path is not None:
			self._fileName=path

	@Property(bool)
	def useRelativePath(self):
		return self._useRelativePath

	@useRelativePath.setter
	def useRelativePath(self, val):
		self._useRelativePath = val
		self.fileName = self._fileName

		

	#fileName = makeProperty("fileName", QUrl)
	macros = makeProperty("macros", "QStringList")

