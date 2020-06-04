from PyQt5.QtWidgets import QWidget, QComboBox

def defaultValueField(w):
	if isinstance(w, QComboBox):
		return "currentText"
	return None

def fieldValue(w, field):
	ip = get_ipython()
	ns = ip.user_ns.copy()
	ns['self'] = w
	#return eval(getattr(w, field)(), ns)
	return eval(w.property(field), ns)

def widgetValue(w):
	"""
	prop = w.property("valueField")
	if prop != None:
		valueField = prop
	elif hasattr(w, "valueField"):
		valueField = w.valueField()
	else:
		valueField = defaultValueField(w)
	return fieldValue(w, valueField)
	"""
	prop = w.property("valueField")
	if prop==None:
		prop = defaultValueField(w)
	return fieldValue(w, prop)
	
		

def isWidget(obj):
	return issubclass(obj.__class__, QWidget)
	
