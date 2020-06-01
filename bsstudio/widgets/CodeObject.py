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

	def __init__(self, parent=None):
		self.parent = parent
		code = textwrap.dedent(self.default_code())
		self._code = bytes(code, "utf-8")

	@Property("QByteArray", designable=True)
	def code(self):
		return self._code

	@code.setter
	def code(self, new_severity):
		self._code = new_severity
	
	def default_code(self):
		return ""

	def run_code(self):
		ns = vars(sys.modules[self.__class__.__module__])
		exec(self._code, ns)
	

