from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
from ophyd.sim import det
import inspect
from itertools import dropwhile
import textwrap
from .CodeObject import CodeObject
from ophyd.ophydobj import OphydObject

def isOphyd(obj):
	return issubclass(obj, OphydObject)

class TextUpdateBase2(CodeObject):
	def __init__(self, parent=None,*,sig=""):
		#self.parent = parent
		#super().__init__(parent)
		#QLabel.__init__(self, parent)
		CodeObject.__init__(self, parent)
		self._source = ""
		self._source1 = ""
		self.source = sig
		self._source1 = sig
		self.timer_update_time = QtCore.QTimer(self) 
		self.timer_update_time.setInterval(1500)
		#self.timer_update_time.timeout.connect(self.runCode)
		self.timer_update_time.timeout.connect(self.timeout)
		self.timer_update_time.start()

	def timeout(self):
		self.runCode()

	def updateText(self, val):
		try:
			self.setText(val)
		except:
			self.setText("unknown")
	

	def default_code(self):
		return """
			from bsstudio.functions import widgetValue
			ui = self.ui
			self.updateText(str(widgetValue(eval(self.source))))
			"""[1:]

	@Property(str, designable=True)
	def source(self):
		return self._source

	@source.setter
	def source(self, val):
		self._source = val

	@Property(str, designable=True)
	def source1(self):
		return self._source1

	@source1.setter
	def source1(self, val):
		self._source1 = val




	def pause_widget(self):
		self.timer_update_time.stop()

	def resume_widget(self):
		self._paused = False
		#self.timer_update_time.start()


class TextUpdate2(QLabel, TextUpdateBase2):
	def __init__(self, parent=None,*,sig=""):
		#self.parent = parent
		#super().__init__(parent)
		QLabel.__init__(self, parent)
		TextUpdateBase2.__init__(self, parent)
