from PyQt5.QtWidgets import QWidget, QComboBox, QSpinBox, QDoubleSpinBox
from bluesky.callbacks import LivePlot, LiveGrid
import matplotlib.pyplot as plt
from collections import Iterable
import time


class dotdict(dict):
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__

def getTopObject(w):
	from .window import isMainWindow
	obj = w.parentWidget()
	while True:
		if hasattr(obj, "isTopLevel"):
			if obj.isTopLevel==True:
				#return obj
				break
		if isMainWindow(obj):
			if not obj.isLoaded:
				time.sleep(1)
			#print(obj.findChildren(QWidget))
			#return obj
			break
		obj = obj.parentWidget()
	return obj


def makeUiFunction(self):
	def ui():
		"""
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
		"""
		obj = getTopObject(self)
		children = obj.findChildren(QWidget)
		d = {c.objectName(): c for c in children}

		d = dotdict(d)
		return d
	return ui

def defaultValueField(w):
	if isinstance(w, QComboBox):
		return "currentText"
	if isinstance(w, QSpinBox):
		return "value"
	if isinstance(w, QDoubleSpinBox):
		return "value"

	return None

def fieldValueAsString(w, field):
	prop = w.property(field)
	print(prop)
	if prop == None:
		return str(getattr(w, field)())
	return str(w.property(field))

def evalInNs(w, cmd):
	ip = get_ipython()
	ns = ip.user_ns.copy()
	ns['self'] = w
	if "ui" not in ns.keys():
		ui = makeUiFunction(w)
		ns["ui"] = ui
	return eval(cmd, ns)


def fieldValue(w, field):
	"""
	ip = get_ipython()
	ns = ip.user_ns.copy()
	ns['self'] = w
	if "ui" not in ns.keys():
		ui = makeUiFunction(w)
		ns["ui"] = ui
	return eval(fieldValueAsString(w, field), ns)
	"""
	return evalInNs(w, fieldValueAsString(w, field))

def comboBoxValue(w):
	key = w.currentText()
	prop = w.property(key)
	if prop == None:
		key = "currentText"
	return fieldValue(w, key)
	
	
"""
def widgetValueString(w_string, continuous=True):
	#ui = makeUiFunction(w)
	w = evalInNs(w, w_string)
	if type(w) is list:
		return [widgetValueString(x, continuous) for x in w]
	if not isWidget(w):
		return w_string
	if isinstance(w, QComboBox):
		wv = comboBoxValue(w)
	prop = w.property("valueField")
	if prop == None:
		prop = defaultValueField(w)
	#wv = fieldValue(w, prop)
	wv_string = fieldValueAsString(w, prop)
	if continuous:
		return widgetValueString(wv_string, True)
	return wv_string
"""

def widgetValueString(self, w_string, continuous=True):
	#ui = makeUiFunction(w)
	w = evalInNs(self, w_string)
	if type(w) is list:
		return [widgetValueString(x, continuous) for x in w]
	if not isWidget(w):
		return w_string
	return widgetValue(w, continuous, asString=True)


def widgetValue(w, continuous=True,*,asString=False):
	if type(w) is list:
		return [widgetValue(x, continuous) for x in w]
	if not isWidget(w):
		return w
	if isinstance(w, QComboBox):
		wv = comboBoxValue(w)
	prop = w.property("valueField")
	if prop == None:
		prop = defaultValueField(w)
	wv = fieldValue(w, prop)
	wv_string = fieldValueAsString(w, prop)
	if continuous:
		return widgetValue(wv, True, asString=asString)
	return wv



def isWidget(obj):
	return issubclass(obj.__class__, QWidget)
	
"""
def makePlots(plotFields, plotKwargsList, cls):
	livePlots = []
	for i in range(len(plotKwargsList)):
		p = plotFields[i]
		plotKwargs = plotKwargsList[i]
		if cls==LivePlot:
			lp = cls(*p, **plotKwargs)
		else:
			lp = plotKwargsList[i]["Figure"].plot(*p)
		livePlots.append(lp)
	return livePlots

def makeLivePlots(plots, plotFields, plotKwargsList):
	plotKwargsList = plotKwargsList + [{}]*(len(plots)-len(plotKwargsList))
	for i in range(len(plots)):
		plotKwargsList[i]["ax"] = plots[i].canvas.ax
	return makePlots(plotFields, plotKwargsList, LivePlot)
	

def makeMplPlots(plots, plotFields, plotKwargsList):
	plotKwargsList = plotKwargsList + [{}]*(len(plots)-len(plotKwargsList))
	for i in range(len(plots)):
		plotKwargsList[i]["Figure"] = plots[i].canvas.ax
	makePlots(plotFields, plotKwargsList, plt.plot)
	
"""

def makeLivePlots(plots, plotFields, plotKwargsList):
	plotKwargsList = plotKwargsList + [{}]*(len(plots)-len(plotKwargsList))
	livePlots = []
	for i in range(len(plots)):
		plot_tuple = plots[i]
		if not isinstance(plot_tuple, Iterable):
			plot_tuple = (plot_tuple, "LivePlot")
		plotWidget,cls = plot_tuple
		if cls == "LiveGrid":
			plotWidget.canvas.wipe()
		p = plotFields[i]
		plotKwargs = plotKwargsList[i]
		plotKwargs["ax"] = plotWidget.canvas.ax
		lp = eval(cls)(*p, **plotKwargs)
		livePlots.append(lp)
	return livePlots

"""
def makeLivePlots(plots, plotFields, plotKwargsList):
	plotKwargsList = plotKwargsList + [{}]*(len(plots)-len(plotKwargsList))
	for i in range(len(plots)):
		plotKwargsList[i]["ax"] = plots[i].canvas.ax
	return makePlots(plots, plotFields, plotKwargsList)
"""

def plotHeader(livePlot, header):
	livePlot.start(header.start)
	for e in header.events():
		livePlot.event(e)

def openFileAsString(filename, macros=[]):
	try:
		fileContents = open(filename).read()
	except:
		print("Read error")
		return

	for m in macros:
		left, right = m.split(":")
		fileContents = fileContents.replace("$("+left+")", right)
	return fileContents


