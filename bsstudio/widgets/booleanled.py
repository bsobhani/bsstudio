from PyQt5.QtWidgets import QWidget, QFrame
from PyQt5.Qt import Qt
from .TextUpdate import TextUpdateBase
from PyQt5.QtCore import pyqtSignal
class BooleanLED(QFrame, TextUpdateBase):
	valChanged = pyqtSignal()
	def setColor(self, color):
		p = self.palette()
		p.setColor(self.backgroundRole(), color)
		self.setPalette(p)
	def setVal(self, val):
		oldVal = self.val
		self.val = val
		if val:
			newColor = self.onColor
		else:
			newColor = self.offColor
		self.setColor(newColor)
		if val != oldVal:
			self.valChanged.emit()
	def __init__(self, parent=None):
		super().__init__(parent)
		p = self.palette()
		self.offColor = Qt.black
		self.onColor = Qt.green
		self.val = False
		self.setVal(False)
		self.setAutoFillBackground(True)
		#self.setStyleSheet("border: 1px solid black;")
	#def timeout(self):
	#	return
	def default_code(self):
		return """
		from PyQt5.Qt import Qt
		from bsstudio.functions import widgetValue
		self.offColor = Qt.black
		self.onColor = Qt.green
		ui = self.ui
		if self.source != "":
			b = widgetValue(eval(self.source))
			self.setVal(b)
		"""[1:]
