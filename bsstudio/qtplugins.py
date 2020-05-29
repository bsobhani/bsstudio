from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
from ophyd.sim import det
import inspect
from itertools import dropwhile
import textwrap
from bsstudio import shared

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



def get_function_body(func):
	source_lines = inspect.getsourcelines(func)[0]
	source_lines = dropwhile(lambda x: x.startswith('@'), source_lines)
	def_line = next(source_lines).strip()
	if def_line.startswith('def ') and def_line.endswith(':'):
		# Handle functions that are not one-liners  
		first_line = next(source_lines)
		# Find the indentation of the first line    
		indentation = len(first_line) - len(first_line.lstrip())
		return ''.join([first_line[indentation:]] + [line[indentation:] for line in source_lines])
	else:
		# Handle single line functions
		return def_line.rsplit(':')[-1].strip()

def remove_first_char_lines(lines):
	lines = lines.split("\n")
	lines = [line[1:]+"\n" for line in lines]
	return "".join(lines)


#class PyBS(QLabel, QtWidgets.QWidget):
class PyBS(QLabel):
	#def __init__(self, parent=None):
	#	QLabel.__init__(self, parent)
	pass

class PyBSPushButton(QPushButton):
	def __init__(self, parent=None):
		self.parent = parent
		QPushButton.__init__(self, parent)
		self.clicked.connect(self.run_code)
		code = textwrap.dedent(self.default_code())
		self._code = bytes(code, "utf-8")

	@Property("QByteArray", designable=True)
	def code(self):
		return self._code

	@code.setter
	def code(self, new_severity):
		self._code = new_severity
	
	def default_code(self):

		return """
		ip = get_ipython()
		print(self.text())
		print(self.parent.label.text())
		RE = ip.user_ns["RE"]
		det = ip.user_ns["det"]
		motor = ip.user_ns["motor"]
		scan = ip.user_ns["scan"]
		#RE(scan([det], motor, -1, 1, 10))
		plan = scan([det], motor, -1, 1, 10)
		Worker.signals.trigger.emit(RE, [plan])
		"""[1:]

	def run_code(self):
		exec(self._code)
		#ip = get_ipython()
		#print(self.text())
		#print(self.parent.label.text())
		#RE = ip.user_ns["RE"]
		#det = ip.user_ns["det"]
		#motor = ip.user_ns["motor"]
		#scan = ip.user_ns["scan"]
		#RE(scan([det], motor, -1, 1, 10))
		#plan = scan([det], motor, -1, 1, 10)
	
		

class GeoLocationTaskMenuFactory(QExtensionFactory):

  def __init__(self, parent = None):

      QExtensionFactory.__init__(self, parent)

  def createExtension(self, obj, iid, parent):

      if iid != "com.trolltech.Qt.Designer.TaskMenu":
          return None

      if isinstance(obj, GeoLocationWidget):
          return GeoLocationMenuEntry(obj, parent)

      return None

def plugin_factory(cls):
	class PyBSPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
		def __init__(self, cls):
			QtDesigner.QPyDesignerCustomWidgetPlugin.__init__(self)
			print("init")
			self.cls = cls
			self.initialized = False

		def name(self):
			return self.cls.__name__

		def group(self):
			return "group1"

		def isContainer(self):
			return False

		def icon(self):
			return QtGui.QIcon()

		def toolTip(self):
			return "test"

		def includeFile(self):
			#return ""
			#return "QQ_Widgets.geolocationwidget"
			#return None
			#return "QQ_Widgets"
			return self.cls.__module__

		def whatsThis(self):
			return "this"

		def createWidget(self, parent):
			w = self.cls(parent)
			return w


		"""
		def domXml(self):
			return (
			"<widget class=\"{0}\" name=\"{0}\">\n"
			" <property name=\"toolTip\" >\n"
			"  <string>{1}</string>\n"
			" </property>\n"
			" <property name=\"whatsThis\" >\n"
			"  <string>{2}</string>\n"
			" </property>\n"
			"</widget>\n"
			).format(self.name(), self.toolTip(), self.whatsThis())
		"""
		def initialize(self, core):
			if self.initialized:
				return
			self.manager = core.extensionManager()
			if self.manager:
				factory = GeoLocationTaskMenuFactory(parent=self.manager)
				#factory = QExtensionFactory(parent=self.manager)
				self.manager.registerExtensions(factory,'com.trolltech.Qt.Designer.TaskMenu')	
			self.initialized = True


	class Plugin(PyBSPlugin):
		def __init__(self):
			super(Plugin, self).__init__(cls)

	return Plugin

p1 = plugin_factory(PyBS)
p2 = plugin_factory(PyBSPushButton)
