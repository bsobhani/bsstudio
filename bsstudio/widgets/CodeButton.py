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

class CodeButton(QPushButton, CodeObject):
	def __init__(self, parent=None):
		self.parent = parent
		QPushButton.__init__(self, parent)
		CodeObject.__init__(self, parent)
		self.clicked.connect(self.run_code)

	def default_code(self):

		return """
		print("Button pressed...")
		"""[1:]
	
