from PyQt5.QtWidgets import QWidget, QComboBox, QSpinBox, QDoubleSpinBox
from bluesky.callbacks import LivePlot, LiveGrid
import matplotlib.pyplot as plt
from collections import Iterable

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


def fieldValue(w, field):
	ip = get_ipython()
	ns = ip.user_ns.copy()
	ns['self'] = w
	return eval(fieldValueAsString(w, field), ns)

def comboBoxValue(w):
	key = w.currentText()
	prop = w.property(key)
	if prop == None:
		key = "currentText"
	return fieldValue(w, key)
	
	

def widgetValue(w, continuous=True):
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
	if continuous:
		return widgetValue(wv, True)
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


