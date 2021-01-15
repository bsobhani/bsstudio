from .CodeObject import CodeObject
from .REButton import makeProperty
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5 import QtCore
from PyQt5.Qt import Qt
from .embedframe import CodeContainer
from .TextUpdate import TextUpdate
from .lineinput import LineInput
from ..functions import widgetValueString
import logging
import time
		
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class OphydProperties(CodeContainer):
	ophydObject = makeProperty("ophydObject")
	
	def __init__(self, parent):
		super().__init__(parent)
		self._ophydObject = ""
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

	def makeRow(self, obj, name, obj_name):
		logger.debug("here1")
		sig = getattr(obj,name)
		hlayout = QHBoxLayout()
		hlayout.setAlignment(Qt.AlignLeft)
		w = QLabel(name)
		logger.debug("here2")
		#w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		w.setFixedHeight(25)
		w.setFixedWidth(200)
		hlayout.addWidget(w)
		#w = TextUpdate(self, sig=obj_name+"."+name+".value")
		if hasattr(sig, "get"):
			logger.info("hasattr value:"+obj.name)
			#w = TextUpdate(self, sig=obj_name+"."+name+".get(timeout=.5)")
			w = TextUpdate(self, sig=obj_name+"."+name+".get()")
		else:
			logger.info("does not hasattr value:"+obj.name)
			w = TextUpdate(self, sig="str('unknown')")
		#w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		logger.debug("here3")
		w.setFixedHeight(25)
		w.setFixedWidth(200)
		hlayout.addWidget(w)
		logger.debug("here")
		if not hasattr(sig, "write_access") or sig.write_access:
			#w = LineInput(self, sig=obj_name+"."+name+".value")
			w = LineInput(self, sig=obj_name+"."+name+".put(eval(self.text())) #")
			w.setFixedWidth(100)
			hlayout.addWidget(w)
		return hlayout

		
	def createFields(self, obj, obj_name):
		layout = QVBoxLayout()
		hlayout = QHBoxLayout()
		hlayout.setAlignment(Qt.AlignLeft)
		title = QLabel("<b>"+obj.name+"</b>")
		title.setFixedHeight(25)
		title.setFixedWidth(100)
	
		hlayout.addWidget(title)
		layout.addLayout(hlayout)
		for name in obj.component_names:
			try:
				hlayout = self.makeRow(obj, name, obj_name)
				layout.addLayout(hlayout)
			except:
				logger.warn("error making row for " + obj_name + " and " + name)
		self.setLayout(layout)
			
	def resumeWidget(self):
		self._paused = False
		self.runCode()
		self.resumeChildren()

	def default_code(self):
		return """
			from bsstudio.functions import widgetValueString
			ui = self.ui
			obj_name = widgetValueString(self, self.ophydObject) 
			ophydObject = eval(obj_name)
			self.createFields(ophydObject, obj_name)
			"""[1:]
