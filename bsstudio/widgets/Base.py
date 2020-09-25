from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
from PyQt5.QtCore import pyqtSignal
from ophyd.sim import det
from ..functions import getTopObject
import inspect
from itertools import dropwhile
import textwrap
import time
import logging

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARN)

all_bss_widgets = []

class BaseWidget:
	signal = pyqtSignal()

	def __init__(self, parent=None):
		self.parent = parent
		global all_bss_widgets
		all_bss_widgets.append(self)
		self.isTopLevel = False

	def initialize(self):
		pass

	def pause_widget(self):
		pass

	def resume_widget(self):
		pass


	def windowFileName(self):
		fileName = None
		if not self._paused:
			fileName = getTopObject(self).uiFilePath
		else:
			try:
				fileName = self.core.formWindowManager().activeFormWindow().fileName()
			except:
				logger.info("Error getting window filename in designer")
		return fileName


	def ui(self):
		from ..functions import makeUiFunction
		_ui = makeUiFunction(self)
		return _ui()

	def resume_children(self):
		children = self.findChildren(BaseWidget)
		for c in children:
			c.resume_widget()

	def closeEvent(self, evt):
		logger.info("close Event")
		self.hide()
		#self.worker.cancel()
		for child in self.findChildren(QWidget):
			try:
				child.close()
			except:
				None
		#super().closeEvent(self)


