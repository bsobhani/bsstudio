from . TextUpdate import TextUpdateBase
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import Q_ENUMS
from .REButton import makeProperty
import math
from enum import Enum

class ScaleType:
	Linear = 1
	Logarithmic = 2

class BarUpdate(TextUpdateBase, QProgressBar, ScaleType):
	Q_ENUMS(ScaleType)
	ScaleType=ScaleType
	def __init__(self, parent):
		QProgressBar.__init__(self, parent)
		TextUpdateBase.__init__(self, parent)
		self._scientificNotation = False
		self._scale = ScaleType.Linear
		self.N = 100
		self.setMinimum(0)
		self.setMaximum(self.N)
		self._minimumValue = "0"
		self._maximumValue = "100"
	def setBarValue(self, val):
		low = eval(self._minimumValue)
		high = eval(self._maximumValue)
		barPercent = (val - low)/(high - low)
		self.setValue(barPercent*self.N)
	def setBarValueLog(self, val):
		low = math.log10(eval(self._minimumValue))
		high = math.log10(eval(self._maximumValue))
		val = math.log10(val)
		barPercent = (val - low)/(high - low)
		self.setValue(barPercent*self.N)
	def default_code(self):
		return """
			ui = self.ui
			from bsstudio.functions import widgetValue
			value = widgetValue(eval(self.source))
			if self.scale == self.ScaleType.Linear:
				self.setBarValue(value)
			elif self.scale == self.ScaleType.Logarithmic:
				self.setBarValueLog(value)
			if self.scientificNotation:
				self.setFormat("%.02E" % value) 
			else:
				self.setFormat("%.02f" % value) 
			"""[:-1]

	minimumValue = makeProperty("minimumValue")
	maximumValue = makeProperty("maximumValue")
	scientificNotation = makeProperty("scientificNotation", bool)
	scale = makeProperty("scale", ScaleType)
	
