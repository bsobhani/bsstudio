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
from .Base import BaseWidget
import sys


class CodeObject(BaseWidget):

	def __init__(self, parent=None, copyNameSpace=True):
		self.parent = parent
		super().__init__(parent)
		code = textwrap.dedent(self.default_code())
		self._code = bytes(code, "utf-8")
		self._paused = True
		self._copyNameSpace = copyNameSpace

	@Property("QByteArray", designable=True)
	def code(self):
		return self._code

	@code.setter
	def code(self, val):
		self._code = val
	
	def default_code(self):
		return ""

	def pause_widget(self):
		self._paused = True

	def resume_widget(self):
		self._paused = False

	def runCode(self):
		if self._paused:
			return
		#ns = vars(sys.modules[self.__class__.__module__])
		ip = get_ipython()
		if self._copyNameSpace:
			ns = ip.user_ns.copy()
		else:
			ns = ip.user_ns
			
		ns['self'] = self
		try:
			exec(self._code, ns)
		except BaseException as e:
			additional_info = " Check code in "+self.objectName()+" widget"
			raise type(e)(str(e) + additional_info).with_traceback(sys.exc_info()[2])

