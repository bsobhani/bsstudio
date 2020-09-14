from .CodeObject import CodeObject
from PyQt5.QtWidgets import QFrame, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import QFile, QFileSelector, QUrl, QVariant, pyqtSignal, QDir
from PyQt5.QtCore import pyqtProperty as Property
from .REButton import makeProperty
from .CodeButton import CodeButton
from .Base import BaseWidget
from bsstudio.functions import openFileAsString, getTopObject
import os

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def relPath(selfPath, filePath):
	#cp = os.path.commonpath([selfPath, filePath])
	#print("rel ins:",selfPath, filePath)
	selfDir = os.path.dirname(selfPath)
	try:
		path = os.path.relpath(filePath, selfDir)
	except:
		path = ""
	#print("rel out:",path)
	return path

def absPath(selfPath, relFilePath):
	#print("selfpath", selfPath)
	#print("relfilepath",relFilePath)
	prefix = os.path.dirname(selfPath)
	ap = os.path.join(prefix, relFilePath)
	#print("abs path", ap)
	return ap

def convertPath(w, fileUrl,*,toRelative):
	val = fileUrl
	valPath = val.toLocalFile()
	self = w
	if self.windowFileName()=="":
		alert = QMessageBox(self)
		alert.setText("Current file has no name. Please save the current file first and try again.")
		alert.show()
		#self._fileName=val
		return None
	if valPath=="":
		alert = QMessageBox(self)
		alert.setText("Empty filename")
		alert.show()
		#self._fileName=val
		return None
	if self.windowFileName() is None or toRelative!=os.path.isabs(valPath):
		#self._fileName=val
		#return None
		logger.info("self.windowFileName is None")
		#return None
		return val
	if toRelative:
		rp = relPath(self.windowFileName(), valPath)
		#print("w rp", rp)
		return QUrl("file:"+rp)
	else:
		ap = absPath(self.windowFileName(), valPath)
		#print("w ap", ap)
		return QUrl("file:"+ap)



class CodeContainer(QFrame, CodeObject):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.pause_widget()
	

	def default_code(self):
		return """
			ui = self.ui
			"""[1:]

	def resume_widget(self):
		#self._paused = False
		CodeObject.resume_widget(self)
		self.runCode()
		

def deleteWidgetAndChildren(w):
	w.setParent(None)
	for c in w.children():
		c.deleteLater()
	w.deleteLater()


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
		#super().__init__(parent)
		QFrame.__init__(self,parent)
		CodeObject.__init__(self,parent)
		self._fileName = QUrl()
		self._macros = []
		self._useRelativePath = True
		self.fileChanged.connect(self.updateUi)
		original = self.resizeEvent
		def resizeEvent(event):
			original(event)
			#self.updateUi()
			self.runCode()
		self.resizeEvent = resizeEvent

	def runPaused(self):
		self.updateUi()

	def getAbsPath(self):
		filename = self.fileName.toLocalFile()
		if not QDir.isAbsolutePath(filename):
			filename = absPath(self.windowFileName(), filename)
		return filename
	
	def updateUi(self):
		from PyQt5.QtWidgets import QWidget
		from PyQt5.QtWidgets import QVBoxLayout
		ui = self.ui

		from PyQt5 import uic
		import io
		#if hasattr(self,"subWindow"):
		#	self.subWindow.setParent(None)
		#	for c in self.subWindow.children():
		#		c.deleteLater()
		#	self.subWindow.deleteLater()
		self.deleteSubWindow()

		self.subWindow = QWidget(self)
		
		self.subWindow.isTopLevel = True
		filename = self.fileName.toLocalFile()
		#if filename=="" or filename==None:
		#	return
		if self.windowFileName() is None:
			return
		if not QDir.isAbsolutePath(filename):
			filename = absPath(self.windowFileName(), filename)
		self.subWindow.uiFilePath = filename
		#if filename=="":
		#	return
		fileContents = openFileAsString(filename, self.macros)
		fileObject = io.StringIO(fileContents)
		try:
			uic.loadUi(fileObject, self.subWindow)
		except:
			logger.info("Error opening file "+filename)
			return
		self.subWindow.resize(self.size())
		#print("subwindow show")
		self.subWindow.show()
		if not self._paused:
			self.resume_children()

		

	

	def default_code(self):
		return """
			from PyQt5.QtWidgets import QWidget
			from PyQt5 import uic
			import io
			ui = self.ui
			self.updateUi()
			"""[1:]

	def resume_widget(self):
		#self._paused = False
		CodeObject.resume_widget(self)
		self.runCode()
		

	#fileName = makeProperty("fileName", QUrl, notify=fileChanged)
	macros = makeProperty("macros", "QStringList")
	@Property("QUrl")
	def fileName(self):
		return self._fileName

	@fileName.setter
	def fileName(self, val):
		"""
		valPath = val.toLocalFile()
		if self.windowFileName() is None:
			self._fileName=val
			return
		rp = relPath(self.windowFileName(), valPath)
		ap = absPath(self.windowFileName(), rp)
		if self._useRelativePath:
			self._fileName=QUrl("file:"+rp)
		else:
			self._fileName=QUrl("file:"+ap)
		self.fileChanged.emit()
		"""
		
			
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


	#useRelativePath = makeProperty("useRelativePath", bool)


class OpenWindowButtonOld(CodeButton):

	def __init__(self, parent=None):
		super().__init__(parent)
		self._fileName = QUrl()
		self._macros = []
		self._useRelativePath = True
		self._useThreading = False
	
	def default_code(self):
		return """
			from PyQt5.QtWidgets import QDialog
			from PyQt5 import uic, QtCore
			from PyQt5.QtCore import QDir
			from bsstudio.functions import openFileAsString
			from bsstudio.widgets.embedframe import absPath
			import io
			ui = self.ui
			self.subWindow = QDialog(self)
			self.subWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)

			self.subWindow.isTopLevel = True
			filename = self.fileName.toLocalFile()
			if not QDir.isAbsolutePath(filename):
				filename = absPath(self.windowFileName(), filename)
			fileContents = openFileAsString(filename, self.macros)
			fileObject = io.StringIO(fileContents)
			uic.loadUi(fileObject, self.subWindow)
			#self.resize(self.subWindow.size())
			self.subWindow.show()
			
			self.resume_children()
			"""[1:]

	def resume_widget(self):
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

class OpenWindowButton(CodeButton):


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
			self.resume_children()
			"""[1:]

	def resume_widget(self):
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

