from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
import inspect
from itertools import dropwhile
import textwrap
from .CodeObject import CodeObject
from functools import partial
import time

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CodeButton(QPushButton, CodeObject):
	def __init__(self, parent=None):
		QPushButton.__init__(self, parent)
		CodeObject.__init__(self, parent)
		self.clicked.connect(self.runCode)

	@Property(bool, designable=True)
	def runInThread(self):
		return self._useThreading

	@runInThread.setter
	def runInThread(self, val):
		self._useThreading = val


	def default_code(self):

		code_string = """
		ui = self.ui
		print(self.objectName()+" pressed...")
		"""[1:]
		return code_string
	
