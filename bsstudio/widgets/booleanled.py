from PyQt5.QtWidgets import QWidget, QFrame
from PyQt5.Qt import Qt
from .TextUpdate import TextUpdateBase
class BooleanLED(QFrame, TextUpdateBase):
	def setColor(self, color):
		p = self.palette()
		p.setColor(self.backgroundRole(), color)
		self.setPalette(p)
	def setVal(self, val):
		if val:
			self.setColor(self.onColor)
		else:
			self.setColor(self.offColor)
	def __init__(self, parent=None):
		super().__init__(parent)
		p = self.palette()
		self.offColor = Qt.black
		self.onColor = Qt.green
		self.setVal(False)
		self.setAutoFillBackground(True)
		#self.setStyleSheet("border: 1px solid black;")
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
