from .CodeObject import CodeObject
from PyQt5.QtWidgets import QFrame, QWidget, QLabel
from PyQt5.QtCore import QFile, QFileSelector, QUrl, QVariant, pyqtSignal
from PyQt5.QtCore import pyqtProperty as Property
from .REButton import makeProperty
from .CodeButton import CodeButton
from .Base import BaseWidget
from bsstudio.functions import openFileAsString

class CodeContainer(QFrame, CodeObject):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.pause_widget()
	

	def default_code(self):
		return """
			ui = self.ui
			"""[1:]

	def pause_widget(self):
		pass
	

	def resume_widget(self):
		self._paused = False
		self.run_code()
		


class EmbedFrame(QFrame, CodeObject):

	fileChanged = pyqtSignal()

	def __init__(self, parent=None):
		#super().__init__(parent)
		QFrame.__init__(self,parent)
		CodeObject.__init__(self,parent)
		self._fileName = QUrl()
		#self.pause_widget()
		self._macros = []
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
		if filename=="":
			return
		fileContents = openFileAsString(filename, self.macros)
		fileObject = io.StringIO(fileContents)
		uic.loadUi(fileObject, self.subWindow)
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
		self._fileName=val
		self.fileChanged.emit()


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

