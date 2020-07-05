from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import Qt
from .TextUpdate import TextUpdateBase
class BooleanLED(QWidget, TextUpdateBase):
	def setColor(self, color):
		p = self.palette()
		p.setColor(self.backgroundRole(), color)
		self.setPalette(p)
	def setVal(self, val):
		if val:
			self.setColor(Qt.green)
		else:
			self.setColor(Qt.black)
	def __init__(self, parent=None):
		super().__init__(parent)
		p = self.palette()
		self.setVal(False)
		self.setAutoFillBackground(True)
	def default_code(self):
		return """
		from bsstudio.functions import widgetValue
		ui = self.ui
		if self.source != "":
			b = widgetValue(eval(self.source))
			self.setVal(b)
		"""[1:]
