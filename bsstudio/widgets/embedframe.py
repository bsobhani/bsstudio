from .CodeObject import CodeObject
from PyQt5.QtWidgets import QFrame, QWidget, QLabel
from PyQt5.QtCore import QFile, QFileSelector, QUrl, QVariant, pyqtSignal
from PyQt5.QtCore import pyqtProperty as Property
from .REButton import makeProperty
from .Base import BaseWidget

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
	
	def updateUi(self):
		from PyQt5.QtWidgets import QWidget
		ui = self.ui

		from PyQt5 import uic
		import io
		self.subWindow = QWidget(self)
		self.subWindow.isTopLevel = True
		try:
			fileContents = open(self.fileName.toLocalFile()).read()
		except:
			print("Read error")
			return

		for m in self.macros:
			left, right = m.split(":")
			fileContents = fileContents.replace("$("+left+")", right)

		fileObject = io.StringIO(fileContents)
		uic.loadUi(fileObject, self.subWindow)
		self.resize(self.subWindow.size())
		self.subWindow.show()
		children = self.subWindow.findChildren(QWidget)

		

	

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
	
	def resume_children(self):
		children = self.findChildren(BaseWidget)
		for c in children:
			c.resume_widget()

	def resume_widget(self):
		self._paused = False
		self.run_code()
		self.resume_children()
		

	#fileName = makeProperty("fileName", QUrl, notify=fileChanged)
	macros = makeProperty("macros", "QStringList")
	@Property("QUrl")
	def fileName(self):
		return self._fileName

	@fileName.setter
	def fileName(self, val):
		self._fileName=val
		self.fileChanged.emit()
