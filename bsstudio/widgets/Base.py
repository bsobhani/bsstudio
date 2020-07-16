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
logger.setLevel(logging.DEBUG)

all_bss_widgets = []

global_id = 1
"""
class dotdict(dict):
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__
"""
class BaseWidget:
	signal = pyqtSignal()

	def __init__(self, parent=None):
		self.parent = parent
		global global_id
		#self._id = global_id
		self.id = global_id
		self.id = 22
		self.id = 25
		#self.setProperty("id", 26)
		#self.setVa
		global all_bss_widgets
		all_bss_widgets.append(self)
		global_id += 1
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
				print("Error getting window filename in designer")
		return fileName

	"""
	def ui(self):
		from ..window import isMainWindow
		obj = self.parentWidget()
		while True:
			if hasattr(obj, "isTopLevel"):
				if obj.isTopLevel==True:
					#return obj
					break
			if isMainWindow(obj):
				#print(obj.findChildren(QWidget))
				#return obj
				break
			obj = obj.parentWidget()
		#return None
		children = obj.findChildren(QWidget)
		d = {c.objectName(): c for c in children}

		d = dotdict(d)
		return d
	"""

	def ui(self):
		from ..functions import makeUiFunction
		_ui = makeUiFunction(self)
		return _ui()

	def resume_children(self):
		children = self.findChildren(BaseWidget)
		for c in children:
			c.resume_widget()

	@Property(int, designable=True, notify=signal, stored=True, final=True, constant=True)
	def id(self):
		return self._id

	@id.setter
	def id(self, val):
		self._id = val
		self.signal.emit()

	def closeEvent(self, evt):
		logger.info("close Event")
		self.hide()
		#self.worker.cancel()
		for child in self.findChildren(QWidget):
			child.close()
		#super().closeEvent(self)


