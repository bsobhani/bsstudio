from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
import inspect
from itertools import dropwhile
import textwrap
from .CodeButton import CodeButton

class REAbortButton(CodeButton):
	def default_code(self):

		return """
		ui = self.ui
		RE.abort()
		"""[1:]
	
