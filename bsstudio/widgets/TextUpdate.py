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

class TextUpdate(QLabel, CodeObject):
	def __init__(self, parent=None):
		self.parent = parent
		#super().__init__(self.parent)
		QLabel.__init__(self, self.parent)
		CodeObject.__init__(self, self.parent)
		self._source = ""
		self.timer_update_time = QtCore.QTimer(self) 
		self.timer_update_time.setInterval(1500)
		self.timer_update_time.timeout.connect(self.run_code)
		self.timer_update_time.start()
	
	def default_code(self):
		return """
			from bsstudio import ui
			self.setText(str(eval(self.source)))
			"""[1:]

	@Property(str, designable=True)
	def source(self):
		return self._source

	@source.setter
	def source(self, val):
		self._source = val

	def print_hi(self):
		print("hi")
	
	def pause_widget(self):
		self.timer_update_time.stop()
