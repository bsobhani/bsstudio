from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit, QComboBox
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
import inspect
from itertools import dropwhile
import textwrap
from .CodeButton import CodeButton
from .CodeObject import CodeObject
from ..worker import Worker, WorkerSignals
from IPython import get_ipython


def parseField(field):
	ip = get_ipython()
	#obj = eval(field, ip.user_ns)
	#obj = eval(field)
	obj = field
	if isinstance(obj, QComboBox):
		obj = eval(obj.currentText(), ip.user_ns)
		#obj = eval(obj.currentText())
	return obj



def makeProperty(name, propertyType=str, **kwargs):
	storageVarName = "_"+name
	def g(self):
		return eval("self."+storageVarName)

	def s(self, val):
		exec("self."+storageVarName+"=val")	
		if "notify" in kwargs.keys():
			kwargs["notify"].emit()
	
	return Property(propertyType, g, s)


	
		


class REButton(CodeButton):

	runInThread = Property(bool, designable=False) # Disabling property

	def __init__(self, parent):
		super().__init__(parent)
		self._plots = "[]"
		self._plotFields = "[[]]"
		self._plotKwargsList = "[{}]"
		self._RunEngine = "RE"
	plots = makeProperty("plots")
	plotFields = makeProperty("plotFields")
	plotKwargsList = makeProperty("plotKwargsList")
	RunEngine = makeProperty("RunEngine")


class RECustomPlan(REButton):
	def __init__(self, parent):
		super().__init__(parent)
		self._arguments = []
		self._plan = ""

	arguments = makeProperty("arguments", "QStringList")
	plan = makeProperty("plan")
	def default_code(self):
		return """
			from bsstudio.functions import widgetValue, makeLivePlots
			from bluesky.callbacks import LiveGrid
			from bluesky.plans import grid_scan
			ui = self.ui
			args = []
			kwargs = {}
			for arg in self.arguments:
				sp = arg.split("=")
				left = sp[0]
				right = widgetValue(eval(sp[-1]))
				if len(sp)==1:
					args.append(right)
				else:
					kwargs[left] = right
			RE = widgetValue(eval(self.RunEngine))
			plots = widgetValue(eval(self.plots)[:])
			plotFields = widgetValue(eval(self.plotFields)[:])
			plotKwargsList = eval(self.plotKwargsList)[:]
			livePlots = makeLivePlots(plots, plotFields, plotKwargsList)
			if livePlots is None:
				livePlots = []
			ts = [RE.subscribe(lp) for lp in livePlots]
	
			plan = widgetValue(eval(self.plan))
			#RE(plan(*args,**kwargs),LiveGrid((6, 10), 'det4'))
			RE(plan(*args,**kwargs))
			for p in plots:
				try:
					x = p[0]
				except:
					x = p
				x.canvas.draw()
			for t in ts:
				RE.unsubscribe(t)
			"""[1:]
			



class Scan1DButton(REButton):
	def __init__(self, parent):
		super().__init__(parent)
		self._motor = ""
		self._detector_list = "[]"
		self._startPosition = "-1"
		self._endPosition = "1"
		self._numSteps = "10"

	def default_code(self):

		return """
		from bsstudio.functions import isWidget, widgetValue, makeLivePlots
		ui = self.ui

		detector_list = eval(self.detectorList)[:]
		motor = eval(self.motor)
		endPosition = eval(self.endPosition)
		startPosition = eval(self.startPosition)
		numSteps = eval(self.numSteps)
		RE = eval(self.RunEngine)

		ophyd_detector_list = [widgetValue(w) for w in detector_list]

		motor = widgetValue(motor)
		endPosition = widgetValue(endPosition)
		startPosition = widgetValue(startPosition)
		numSteps = widgetValue(numSteps)
		RE = widgetValue(RE)

		plots = eval(self.plots)[:]
		plotFields = eval(self.plotFields)[:]
		plotKwargsList = eval(self.plotKwargsList)[:]
		livePlots = makeLivePlots(plots, plotFields, plotKwargsList)
		if livePlots is None:
			livePlots = []
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

	@Property(str)
	def detectorList(self):
		return self._detector_list

	@detectorList.setter
	def detectorList(self, val):
		self._detector_list = val[:]
