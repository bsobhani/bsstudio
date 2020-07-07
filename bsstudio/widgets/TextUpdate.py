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
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def isOphyd(obj):
	return issubclass(obj, OphydObject)

class TextUpdateBase(CodeObject):
	def __init__(self, parent=None,*,sig=""):
		#self.parent = parent
		#super().__init__(parent)
		#QLabel.__init__(self, parent)
		CodeObject.__init__(self, parent)
		self._source = ""
		self.source = sig
		self.timer = QtCore.QTimer(self) 
		self.timer.setInterval(1500)
		#self.timer.timeout.connect(self.runCode)
		self.timer.timeout.connect(self.timeout)
		self.timer.start()

	def timeout(self):
		self.runCode()

	def updateText(self, val):
		if val == None:
			self.setText("unknown")
			logger.info("setting text to unknown")
		else:
			self.setText(val)
	

	def default_code(self):
		return """
			import logging
			from bsstudio.functions import widgetValue, fieldValue
			#logger = logging.getLogger(__name__)
			ui = self.ui
			v = widgetValue(fieldValue(self, "source"))
			#if self.source != "":
			#	try:
			#		v = eval(self.source)
			#		print("able to interpret" + self.source)
			#		logger.info("info:able to interpret" + self.source)
			#	except:
			#		logger.warning("unable to interpret" + self.source)
			#		print("unable to interpret" + self.source)
			#
			if v is not None:
				v = str(v)
			self.updateText(v)
			"""[1:]

	@Property(str, designable=True)
	def source(self):
		return self._source

	@source.setter
	def source(self, val):
		self._source = val

	def pause_widget(self):
		self.timer.stop()

	def resume_widget(self):
		self._paused = False
		#self.timer.start()



class TextUpdate(QLabel, TextUpdateBase):
	def __init__(self, parent=None,*,sig=""):
		#self.parent = parent
		#super().__init__(parent)
		QLabel.__init__(self, parent)
		TextUpdateBase.__init__(self, parent, sig=sig)


	#def runCode(self):
	#	try:
	#		TextUpdateBase.runCode(self)
	#	except:
	#		self.setText("unknown")
	#		logger.warning("unable to run TextUpdate widget with source=" + self.source)
