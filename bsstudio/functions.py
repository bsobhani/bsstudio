from PyQt5.QtWidgets import QWidget, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit
from bluesky.callbacks import LivePlot, LiveGrid
import matplotlib.pyplot as plt
from collections import Iterable
import time
import re
from IPython import get_ipython
from .lib.pydollarmacro import pydollarmacro

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


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
			while not obj.isLoaded:
				time.sleep(1)
				logger.info("sleeping for 1 second")
			#print(obj.findChildren(QWidget))
			#return obj
			break
		obj = obj.parentWidget()
	return obj


def makeUiFunction(self):
	def ui():
		obj = getTopObject(self)
		children = obj.findChildren(QWidget)
		d = {c.objectName(): c for c in children}
		d["parent"] = obj.parent
		def parentUi():
			return obj.parent.ui()
		d["parentUi"] = parentUi
		

		d = dotdict(d)
		return d
	return ui

def defaultValueField(w):
	if isinstance(w, QComboBox):
		return "currentText"
	if isinstance(w, QCheckBox):
		return "isChecked"
	if isinstance(w, QSpinBox):
		return "value"
	if isinstance(w, QDoubleSpinBox):
		return "value"
	if issubclass(w.__class__, QLineEdit):
		return "text"

	return None

def fieldValueAsString_(w, field):
	prop = w.property(field)
	if prop == None:
		return str(getattr(w, field)())
	return str(w.property(field))

def fieldValueAsString(w, field):
	try:
		return fieldValueAsString_(w,field)
	except:
		logger.warn("unable to get value for field "+field+" as string")
		return None

def evalInNs(w, cmd):
	try:
		ip = get_ipython()
		ns = ip.user_ns.copy()
		ns['self'] = w
		ui = makeUiFunction(w)
		ns["ui"] = ui
		logger.info("evaluating command in namespace: "+cmd)
		return eval(cmd, ns)

	except:
		logger.warn("unable to evaluate command "+str(cmd)+" in namespace "+str(ns.keys()))
		return None



def fieldValue(w, field):
	return evalInNs(w, fieldValueAsString(w, field))

def comboBoxValue(w):
	key = w.currentText()
	prop = w.property(key)
	if prop == None:
		key = "currentText"
	return fieldValue(w, key)
	
	
def widgetValueString(self, w_string, continuous=True):
	#ui = makeUiFunction(w)
	w = evalInNs(self, w_string)
	logger.debug("w in widgetValueString", w)
	if type(w) is list:
		return [widgetValueString(x, continuous) for x in w]
	if not isWidget(w):
		return w_string
	return widgetValue(w, continuous, asString=True)


def widgetValue(w, continuous=True,*,asString=False):
	if type(w) is list:
		return [widgetValue(x, continuous) for x in w]
	if type(w) is dict:
		return {k : widgetValue(w[k], continuous) for k in w.keys()}
	if not isWidget(w):
		return w
	prop = w.property("valueField")
	if prop == None:
		prop = defaultValueField(w)
	if isinstance(w, QComboBox):
		wv = comboBoxValue(w)
	else:
		wv = fieldValue(w, prop)
	wv_string = fieldValueAsString(w, prop)
	if not isWidget(wv) and asString:
		return wv_string
	if continuous:
		return widgetValue(wv, True, asString=asString)
	return wv



def isWidget(obj):
	return issubclass(obj.__class__, QWidget)
	
def makeLivePlots(plots, plotFields, plotKwargsList):
	logger.info("plotFields"+str(plotFields))
	if plotFields is None or plotFields == [[]]:
		return None
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

def plotHeader(livePlot, header):
	livePlot.start(header.start)
	for e in header.events():
		livePlot.event(e)

def openFileAsString(filename, macros=[]):
	try:
		fileContents = open(filename).read()
	except:
		logger.error("Read error")
		return

	macro_dict = {}
	for m in macros:
		left, right = m.split(":")
		macro_dict[left] = right
		#fileContents = fileContents.replace("$("+left+")", right)
		#fileContents = fileContents.replace("$("+left+")", right)
	fileContents = pydollarmacro.subst_str_all(fileContents, macro_dict)
	return fileContents


