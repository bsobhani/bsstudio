from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
from PyQt5.QtCore import pyqtSignal
from ophyd.sim import det
import inspect
from itertools import dropwhile
import textwrap

all_bss_widgets = []

global_id = 1

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

	def pause_widget(self):
		pass

	@Property(int, designable=True, notify=signal, stored=True, final=True, constant=True)
	def id(self):
		return self._id

	@id.setter
	def id(self, val):
		self._id = val
		self.signal.emit()


