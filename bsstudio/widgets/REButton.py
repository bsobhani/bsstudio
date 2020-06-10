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
from ..worker import Worker, WorkerSignals


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

def makeProperty(name, propertyType=str):
	storageVarName = "_"+name
	def g(self):
		return eval("self."+storageVarName)

	def s(self, val):
		exec("self."+storageVarName+"=val")	
	
	return Property(propertyType, g, s)




class Scan1DButton(REButton):
	def __init__(self, parent):
		super().__init__(parent)
		self._motor = ""
		self._detector_list = "[]"
		self._startPosition = "-1"
		self._endPosition = "1"
		self._numSteps = "10"
		self._plots = "[]"
		self._plotFields = "[[]]"
	def default_code(self):

		return """
		from bsstudio import ui
		from bsstudio.functions import isWidget, widgetValue, makeLivePlots

		detector_list = eval(self.detectorList)[:]
		motor = eval(self.motor)
		endPosition = eval(self.endPosition)
		startPosition = eval(self.startPosition)
		numSteps = eval(self.numSteps)

		ophyd_detector_list = [widgetValue(w) for w in detector_list]

		motor = widgetValue(motor)
		endPosition = widgetValue(endPosition)
		startPosition = widgetValue(startPosition)
		numSteps = widgetValue(numSteps)

		plots = eval(self.plots)[:]
		plotFields = eval(self.plotFields)[:]
		livePlots = makeLivePlots(plots, plotFields)
		ts = [RE.subscribe(lp) for lp in livePlots]
	
		plan = scan(ophyd_detector_list, motor, startPosition, endPosition, numSteps)
		#Worker.signals.trigger.emit(RE, [plan])
		RE(plan)
		for t in ts:
			RE.unsubscribe(t)
		"""[1:]

	startPosition = makeProperty("startPosition")
	endPosition = makeProperty("endPosition")
	numSteps = makeProperty("numSteps")
	motor = makeProperty("motor")
	plots = makeProperty("plots")
	plotFields = makeProperty("plotFields")

	"""
	@Property(str)
	def motor(self):
		return self._motor

	@motor.setter
	def motor(self, val):
		self._motor = val
	"""

	@Property(str)
	def detectorList(self):
		return self._detector_list

	@detectorList.setter
	def detectorList(self, val):
		self._detector_list = val[:]
