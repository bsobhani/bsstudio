from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit, QWidget, QAction
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory, QDesignerPropertyEditorInterface 
from PyQt5.QtCore import pyqtProperty as Property
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSlot, QObject
from ophyd.sim import det
import inspect
from itertools import dropwhile
import textwrap
from .widgets import REButton, RECustomPlan, CodeButton, TextUpdate, MplWidget, Scan1DButton, EmbedFrame, LineInput
from .widgets import Base
from .widgets import CodeContainer
from .widgets import DataBrowser
from .widgets import OphydProperties
from .widgets import OpenWindowButton
from .widgets import ArrayImage
from .widgets import BooleanLED
from PyQt5.QtDesigner import QPyDesignerTaskMenuExtension 

class EditCodeMenuEntry(QPyDesignerTaskMenuExtension):

  def __init__(self, widget, parent):

      QPyDesignerTaskMenuExtension.__init__(self, parent)

      self.widget = widget
      self.editStateAction = QAction(
          self.tr("Edit code..."), self)
      #self.connect(self.editStateAction,
      #    SIGNAL("triggered()"), self.updateLocation)

  def preferredEditAction(self):
      return self.editStateAction

  def taskActions(self):
      return [self.editStateAction]

  def updateLocation(self):
      dialog = GeoLocationDialog(self.widget)
      dialog.exec_()

class GeoLocationTaskMenuFactory(QExtensionFactory):

  def __init__(self, parent = None):

      QExtensionFactory.__init__(self, parent)
      print("factory...", self.createExtension)

  def createExtension(self, obj, iid, parent):
      print("create extensions...")

      if iid != "org.qt-project.Qt.Designer.TaskMenu":
          return None

      if isinstance(obj, CodeButton):
          print("wrhwrt")
          return EditCodeMenuEntry(obj, parent)

      return None

core_initialized = False
def plugin_factory(cls, is_container=False):
	print(cls)
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
			return is_container

		def icon(self):
			return QtGui.QIcon()

		def toolTip(self):
			return "test"

		def includeFile(self):
			return self.cls.__module__

		def whatsThis(self):
			return "this"

		def createWidget(self, parent):
			w = self.cls(parent)
			w.core = self.core
			w.pause_widget()
			return w

		def init_core(self):
			global core_initialized
			if core_initialized:
				return
			core = self.core
			children = core.formWindowManager().children()
			a = QAction("zzz",core.formWindowManager())
			"""
			for c in children:
				if hasattr(c, "iconText"):
					def hi():
						print("aaaaa")
						print(core.actionEditor())
						return "Hello"
			"""

			def preview():
				import os
				print("preview")
				fileName = core.formWindowManager().activeFormWindow().fileName()
				import inspect
				import bsstudio
				path = os.path.dirname(inspect.getfile(bsstudio))
				path_import = "import sys\nsys.path.insert(0, '"+path+"')"

				#cmd = 'ipython --profile=collection --matplotlib=qt5 -c "'+path_import+'\nimport bsstudio\nbsstudio.load(\\"'+fileName+'\\")"'
				cmd = 'bsui -c "'+path_import+'\nimport bsstudio\nbsstudio.load(\\"'+fileName+'\\", False)"'
				os.system(cmd + " &")

				p = core.findChildren(QWidget)
	
				
			p = core.formWindowManager().findChild(QAction, "__qt_default_preview_action")
			p.triggered.disconnect()
			p.triggered.connect(preview)
			
			core_initialized = True

		def initialize(self, core):
			if self.initialized:
				return
			self.core = core
			self.init_core()

			self.manager = core.extensionManager()
			if self.manager:
				factory = GeoLocationTaskMenuFactory(parent=self.manager)
				#self.manager.registerExtensions(factory,'org.qt-project.Qt.Designer.TaskMenu')	
			self.initialized = True


	class Plugin(PyBSPlugin):
		def __init__(self):
			super(Plugin, self).__init__(cls)

	return Plugin

pCodeButton = plugin_factory(CodeButton)
#pREButton = plugin_factory(REButton)
pTextUpdate = plugin_factory(TextUpdate)
pMplWidget = plugin_factory(MplWidget)
pScan1DButton = plugin_factory(Scan1DButton)
pEmbedFrame = plugin_factory(EmbedFrame)
pLineInput = plugin_factory(LineInput)
pRECustomPlan = plugin_factory(RECustomPlan)
pCodeContainter = plugin_factory(CodeContainer, is_container=True)
pDataBrowser = plugin_factory(DataBrowser)
pOphydProperties = plugin_factory(OphydProperties)
pOpenWindowButton = plugin_factory(OpenWindowButton)
#pOpenWindowButton2 = plugin_factory(OpenWindowButton2)
pArrayImage = plugin_factory(ArrayImage)
pBooleanLED = plugin_factory(BooleanLED)
