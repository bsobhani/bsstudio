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
from functools import partial

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CodeButton(QPushButton, CodeObject):
	def __init__(self, parent=None):
		self.parent = parent
		QPushButton.__init__(self, parent)
		CodeObject.__init__(self, parent)
		self.clicked.connect(self.runCode)
		#self._useThreading = True
		self.threadType = "qthread"

	def default_code(self):

		code_string = """
		ui = self.ui
		print(self.objectName()+" pressed...")
		"""[1:]
		return code_string

	def runCode(self):
		if self.threadpool.waitForDone(0):
			CodeObject.runCode(self)
		else:
			logger.info("Thread still running for CodeButton")
	
