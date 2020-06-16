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
from PyQt5.QtDesigner import QPyDesignerTaskMenuExtension 

class GeoLocationMenuEntry(QPyDesignerTaskMenuExtension):

  def __init__(self, widget, parent):

      QPyDesignerTaskMenuExtension.__init__(self, parent)

      self.widget = widget
      self.editStateAction = QAction(
          self.tr("Update Location..."), self)
      self.connect(self.editStateAction,
          SIGNAL("triggered()"), self.updateLocation)

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

      if iid != "com.trolltech.Qt.Designer.TaskMenu":
          return None

      if isinstance(obj, CodeButton):
          print("wrhwrt")
          return GeoLocationMenuEntry(obj, parent)

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
			#return ""
			#return "QQ_Widgets.geolocationwidget"
			#return None
			#return "QQ_Widgets"
			return self.cls.__module__

		def whatsThis(self):
			return "this"

		def createWidget(self, parent):
			w = self.cls(parent)
			#w.initialize()
			w.pause_widget()
			"""
			#w.id = 5
			#w.setProperty("id", 50)
			#self.core.setPropertyEditor(QDesignerPropertyEditorInterface() )
			@pyqtSlot(result=QVariant)
			def print_test():
				print("asdf1234")
				return QVariant(5)
			if self.core.propertyEditor():
				#print(dir(self.core))
				#print(dir(self.core.propertyEditor()))
				#self.core.propertyEditor().setObject(self.core.propertyEditor().object())
				#self.core.propertyEditor().setObject(QWidget(parent))
				self.core.propertyEditor().setPropertyValue("id", QVariant(66), True)
				w._id=66
				print(w._id)
				#self.core.propertyEditor().setProperty("iasdf1d", 66)
				print(self.domXml())
				print(self.core.propertyEditor().object())
				print(self.core.propertyEditor().currentPropertyName())
				#self.core.propertyEditor().setPropertyValue("id", 66, 1)
			#w.style().unpolish(w)
			#w.style().polish(w)
			#w.update()
			"""
			return w

		def init_core(self):
			global core_initialized
			if core_initialized:
				return
			core = self.core
			children = core.formWindowManager().children()
			#print(dir(core.formWindowManager()))
			a = QAction("zzz",core.formWindowManager())
			for c in children:
				if hasattr(c, "iconText"):
					def hi():
						print("aaaaa")
						#print(c.actionGroup().parent())
						#a.setActionGroup(c.actionGroup())
						print(core.actionEditor())
						return "Hello"
					#c.setToolTip("asdfb")
					#c.triggered.connect(hi)

			a.setToolTip("nnnnn")
			a.setIconText("abcd")
			a.setText("zzz")
			print(dir(core.formWindowManager()))
			print(core.formWindowManager().activeFormWindow())
			print(core.actionEditor())
			print(dir(core))
			#print(dir(a))
			#print(a.menuRole())
			#print(a.isVisible())
			def preview():
				import os
				print("preview")
				fileName = core.formWindowManager().activeFormWindow().fileName()
				cmd = 'ipython --profile=collection --matplotlib=qt5 -c "import bsstudio\nbsstudio.load(\\"'+fileName+'\\")"'
				#os.spawnl(os.P_NOWAIT, cmd)
				#print(dir(core.formWindowManager().activeFormWindow()))
				os.system(cmd + " &")

				p = core.findChildren(QWidget)
				print(p)
				#core.actionEditor().addAction(a)
				#print(core.actionEditor().actions())
				#print(dir(core.formWindowManager().actionGroup()))
	
				
			p = core.formWindowManager().findChild(QAction, "__qt_default_preview_action")
			p.triggered.disconnect()
			p.triggered.connect(preview)
			
			#print(core.formWindowManager().children())
			core_initialized = True

		def initialize(self, core):
			if self.initialized:
				return
			#get_ipython()
			self.core = core
			self.init_core()

			self.manager = core.extensionManager()
			if self.manager:
				factory = GeoLocationTaskMenuFactory(parent=self.manager)
				#factory = QExtensionFactory(parent=self.manager)
				#print(self.manager.registerExtensions, factory)
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
pScan1DButton = plugin_factory(Scan1DButton)
pEmbedFrame = plugin_factory(EmbedFrame)
pLineInput = plugin_factory(LineInput)
pRECustomPlan = plugin_factory(RECustomPlan)
pCodeContainter = plugin_factory(CodeContainer, is_container=True)
pDataBrowser = plugin_factory(DataBrowser)
