from .CodeObject import CodeObject
from PyQt5.QtWidgets import QFrame, QWidget, QLabel
from PyQt5.QtCore import QFile, QFileSelector, QUrl, QVariant, pyqtSignal, QDir
from PyQt5.QtCore import pyqtProperty as Property
from .REButton import makeProperty
from .CodeButton import CodeButton
from .Base import BaseWidget
from bsstudio.functions import openFileAsString
import os


def relPath(selfPath, filePath):
	print(selfPath, filePath)
	print(type(filePath))
	cp = os.path.commonprefix([selfPath, filePath])
	try:
		path = os.path.relpath(filePath, cp)
	except:
		path = ""
	return path

def absPath(selfPath, relFilePath):
	prefix = os.path.dirname(selfPath)
	return os.path.join(prefix, relFilePath)


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
		self.run_code()
		


class EmbedFrame(QFrame, CodeObject):

	fileChanged = pyqtSignal()

	def windowFileName(self):
		ui = self.ui
		#self.subWindow.uiFilePath = filename
		#fileName = self.core.formWindowManager().activeFormWindow().fileName()
		print(self._paused)
		if not self._paused:
			print("ui", ui())
			fileName = ui().uiFilePath
		else:
			try:
				fileName = self.core.formWindowManager().activeFormWindow().fileName()
			except:
				fileName=""
		return fileName


	def __init__(self, parent=None):
		#super().__init__(parent)
		QFrame.__init__(self,parent)
		CodeObject.__init__(self,parent)
		self._fileName = QUrl()
		#self.pause_widget()
		self._macros = []
		self._useRelativePath = True
		self.fileChanged.connect(self.updateUi)
		original = self.resizeEvent
		def resizeEvent(event):
			print("resizing")
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
			#del self.subWindow

		self.subWindow = QWidget(self)
		
		self.subWindow.isTopLevel = True
		filename = self.fileName.toLocalFile()
		print("here")
		print("filename", filename)
		if filename=="" or filename==None:
			return
		if not QDir.isAbsolutePath(filename):
			print("if block",self.windowFileName(), filename)
			filename = absPath(self.windowFileName(), filename)
		if filename=="":
			return
		print("opening filename", filename)
		fileContents = openFileAsString(filename, self.macros)
		fileObject = io.StringIO(fileContents)
		try:
			uic.loadUi(fileObject, self.subWindow)
		except:
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

	#def pause_widget(self):
	#	#self._paused = True
	#	pass
	
	

	def resume_widget(self):
		self._paused = False
		self.run_code()
		#self.resume_children()
		

	#fileName = makeProperty("fileName", QUrl, notify=fileChanged)
	macros = makeProperty("macros", "QStringList")
	@Property("QUrl")
	def fileName(self):
		return self._fileName

	@fileName.setter
	def fileName(self, val):
		print("type", type(val))
		print("dir", dir(val))
		#w = val
		#print("w", w.toLocalFile())
		print("val", val.toLocalFile())
		valPath = val.toLocalFile()
		if self.windowFileName()=="":
			self._fileName=val
			return
		rp = relPath(self.windowFileName(), valPath)
		print("relpath", rp)
		#self._fileName=QUrl(path)
		print(self.windowFileName(), rp)
		ap = absPath(self.windowFileName(), rp)
		print("absPath", ap)
		#val.setPath("file://"+ap)
		#val.setPath(ap)
		if rp=="":
			self._fileName=val
			print("HERE")
			return
		#val.setPath(rp)
		#self._fileName=val
		self._fileName=QUrl("file:"+rp)
		#self._fileName=QUrl("file://"+val.toLocalFile())
		print(self._fileName, val, ap)
		self.fileChanged.emit()

	useRelativePath = makeProperty("useRelativePath", bool)


class OpenWindowButton(CodeButton):

	def __init__(self, parent=None):
		super().__init__(parent)
		self._fileName = QUrl()
		self._macros = []
	
	def default_code(self):
		return """
			from PyQt5.QtWidgets import QDialog
			from PyQt5 import uic
			from bsstudio.functions import openFileAsString
			import io
			ui = self.ui
			self.subWindow = QDialog(self)
			self.subWindow.isTopLevel = True
			filename = self.fileName.toLocalFile()
			fileContents = openFileAsString(filename, self.macros)
			fileObject = io.StringIO(fileContents)
			uic.loadUi(fileObject, self.subWindow)
			#self.resize(self.subWindow.size())
			self.subWindow.show()
			self.resume_children()
			"""[1:]

	def resume_widget(self):
		self._paused = False
		#self.run_code()
		#self.resume_children()
		

	fileName = makeProperty("fileName", QUrl)
	macros = makeProperty("macros", "QStringList")

