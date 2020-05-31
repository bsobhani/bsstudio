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
from bsstudio.widgets import REButton, CodeButton, TextUpdate, MplWidget

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
			w.pause_widget()
			return w


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

pCodeButton = plugin_factory(CodeButton)
pREButton = plugin_factory(REButton)
pTextUpdate = plugin_factory(TextUpdate)
pMplWidget = plugin_factory(MplWidget)
