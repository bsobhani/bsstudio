from .CodeObject import CodeObject
from PyQt5.QtWidgets import QFrame, QWidget
from PyQt5.QtCore import QFile, QFileSelector, QUrl, QVariant
from .REButton import makeProperty

class EmbedFrame(QFrame, CodeObject):
	def __init__(self, parent=None):
		super().__init__(parent)
		#self._fileName = QFileSelector("/home/bsobhani/bsw/bss_test3.ui")
		self._fileName = QUrl()
		self.pause_widget()
		self._macros = []

	def default_code(self):
		return """
			from PyQt5 import uic
			from PyQt5.QtWidgets import QWidget
			import io
			ui = self.ui
			self.subWindow = QWidget(self)
			self.subWindow.topLevel = True
			fileContents = open(self.fileName.toLocalFile()).read()
			
			for m in self.macros:
				left, right = m.split(":")
				fileContents = fileContents.replace("$("+left+")", right)

			fileObject = io.StringIO(fileContents)
				
			uic.loadUi(fileObject, self.subWindow)
			self.resize(self.subWindow.size())
			self.subWindow.show()
			"""[1:]

	def resume_widget(self):
		self._paused = False
		print("resuming")
		self.run_code()
		

	fileName = makeProperty("fileName", QUrl)
	macros = makeProperty("macros", "QStringList")
