from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit, QComboBox
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
from ophyd.sim import det
import inspect
from itertools import dropwhile
import textwrap
from .CodeButton import CodeButton
from .CodeObject import CodeObject

class WorkerSignals(QtCore.QObject):
	trigger = QtCore.pyqtSignal(object, list)


class Worker(QtCore.QRunnable):
	signals = WorkerSignals()
	def __init__(self, fn, *args, **kwargs):
		super(Worker, self).__init__()
		self.fn = fn
		self.args = args
		self.kwargs = kwargs

	@QtCore.pyqtSlot()
	def run(self):
		self.fn(*self.args, **self.kwargs)


def parseField(field):
	ip = get_ipython()
	#obj = eval(field, ip.user_ns)
	#obj = eval(field)
	obj = field
	if isinstance(obj, QComboBox):
		obj = eval(obj.currentText(), ip.user_ns)
		#obj = eval(obj.currentText())
	return obj
		


class REButton(CodeButton):
	def default_code(self):

		return """
		ip = get_ipython()
		RE = ip.user_ns["RE"]
		det = ip.user_ns["det"]
		motor = ip.user_ns["motor"]
		scan = ip.user_ns["scan"]
		#RE(scan([det], motor, -1, 1, 10))
		plan = scan([det], motor, -1, 1, 10)
		Worker.signals.trigger.emit(RE, [plan])
		"""[1:]
	
	#def run_code(self):
	#	print(globals())
	#	g = globals()
	#	CodeObject.run_code(self, g)

class Scan1DButton(REButton):
	def __init__(self, parent):
		super().__init__(parent)
		self._motor = ""
	def default_code(self):

		return """
		ip = get_ipython()
		RE = ip.user_ns["RE"]
		det = ip.user_ns["det"]
		motor = ip.user_ns["motor"]
		scan = ip.user_ns["scan"]
		#RE(scan([det], motor, -1, 1, 10))
		plan = scan([det], motor, -1, 1, 10)
		Worker.signals.trigger.emit(RE, [plan])
		"""[1:]

	@Property(str)
	def motor(self):
		return self._motor

	@motor.setter
	def motor(self, val):
		self._motor = val
