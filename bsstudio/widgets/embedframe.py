from .CodeObject import CodeObject
from PyQt5.QtWidgets import QFrame, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import QFile, QFileSelector, QUrl, QVariant, pyqtSignal, QDir
from PyQt5.QtCore import pyqtProperty as Property
from .REButton import makeProperty
from .CodeButton import CodeButton
from .Base import BaseWidget
from bsstudio.functions import openFileAsString, getTopObject
import os


def relPath(selfPath, filePath):
	cp = os.path.commonpath([selfPath, filePath])
	try:
		path = os.path.relpath(filePath, cp)
	except:
		path = ""
	return path

def absPath(selfPath, relFilePath):
	prefix = os.path.dirname(selfPath)
	return os.path.join(prefix, relFilePath)

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
	if self.windowFileName() is None:
		#self._fileName=val
		#return None
		return val
	rp = relPath(self.windowFileName(), valPath)
	ap = absPath(self.windowFileName(), rp)
	if toRelative:
		return QUrl("file:"+rp)
	else:
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
		self._paused = False
		self.runCode()
		


class EmbedFrame(QFrame, CodeObject):

	fileChanged = pyqtSignal()



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
			self.updateUi()
		self.resizeEvent = resizeEvent
	
	def updateUi(self):
		from PyQt5.QtWidgets import QWidget
		from PyQt5.QtWidgets import QVBoxLayout
		ui = self.ui

		from PyQt5 import uic
		import io
		if hasattr(self,"subWindow"):
			self.subWindow.setParent(None)
			for c in self.subWindow.children():
				c.deleteLater()
			self.subWindow.deleteLater()

		self.subWindow = QWidget(self)
		
		self.subWindow.isTopLevel = True
		filename = self.fileName.toLocalFile()
		#if filename=="" or filename==None:
		#	return
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
			print("Error opening file "+filename)
			return
		self.subWindow.resize(self.size())
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
		self._paused = False
		self.runCode()
		#self.resume_children()
		

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
			self._fileName=path
		return
			
			

	@Property(bool)
	def useRelativePath(self):
		return self._useRelativePath

	@useRelativePath.setter
	def useRelativePath(self, val):
		self._useRelativePath = val
		self.fileName = self._fileName


	#useRelativePath = makeProperty("useRelativePath", bool)


class OpenWindowButton(CodeButton):

	def __init__(self, parent=None):
		super().__init__(parent)
		self._fileName = QUrl()
		self._macros = []
		self._useRelativePath = True
	
	def default_code(self):
		return """
			from PyQt5.QtWidgets import QDialog
			from PyQt5 import uic
			from PyQt5.QtCore import QDir
			from bsstudio.functions import openFileAsString
			from bsstudio.widgets.embedframe import absPath
			import io
			ui = self.ui
			self.subWindow = QDialog(self)
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
		"""
		path = convertPath(self, val, toRelative=self._useRelativePath)
		if path is None:
			self._fileName=val
		else:
			self._fileName=path
		return
		"""
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

