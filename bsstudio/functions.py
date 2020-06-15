from PyQt5.QtWidgets import QWidget, QComboBox, QSpinBox
from bluesky.callbacks import LivePlot

def defaultValueField(w):
	if isinstance(w, QComboBox):
		return "currentText"
	if isinstance(w, QSpinBox):
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
	
def makeLivePlots(plots, plotFields, plotKwargsList):
	livePlots = []
	plotKwargsList = plotKwargsList + [{}]*(len(plots)-len(plotKwargsList))
	print(plotKwargsList)
	for i in range(len(plots)):
		p = plotFields[i]
		plotKwargs = plotKwargsList[i]
		plotKwargs['ax'] = plots[i].canvas.ax
		lp = LivePlot(*p, **plotKwargs)
		livePlots.append(lp)
	return livePlots

