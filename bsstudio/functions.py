from PyQt5.QtWidgets import QWidget, QComboBox, QSpinBox

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
	
	

def widgetValue(w, continuous=False):
	if isinstance(w, QComboBox):
		wv = comboBoxValue(w)
	prop = w.property("valueField")
	if prop == None:
		prop = defaultValueField(w)
	wv = fieldValue(w, prop)
	if continuous and isWidget(wv):
		return widgetValue(wv, True)
	return wv
	
		

def isWidget(obj):
	return issubclass(obj.__class__, QWidget)
	
