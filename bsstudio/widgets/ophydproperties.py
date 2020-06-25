from .CodeObject import CodeObject
from .REButton import makeProperty
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.Qt import Qt
from .embedframe import CodeContainer
from .TextUpdate import TextUpdate
from .lineinput import LineInput
from ..functions import widgetValueString

class OphydProperties(CodeContainer):
	ophydObject = makeProperty("ophydObject")
	
	def __init__(self, parent):
		super().__init__(parent)
		self._ophydObject = ""
		
	def createFields(self, obj, obj_name):
		print("create fields")
		layout = QVBoxLayout()
		hlayout = QHBoxLayout()
		hlayout.setAlignment(Qt.AlignLeft)
		title = QLabel("<b>"+obj.name+"</b>")
		title.setFixedHeight(25)
		title.setFixedWidth(100)
	
		hlayout.addWidget(title)
		layout.addLayout(hlayout)
		for name in obj.component_names:
			sig = getattr(obj,name)
			hlayout = QHBoxLayout()
			hlayout.setAlignment(Qt.AlignLeft)
			w = QLabel(name)
			#w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
			w.setFixedHeight(25)
			w.setFixedWidth(200)
			hlayout.addWidget(w)
			w = TextUpdate(self, sig=obj_name+"."+name+".value")
			#w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
			w.setFixedHeight(25)
			w.setFixedWidth(200)
			hlayout.addWidget(w)
			try:
				if sig.write_access:
					w = LineInput(self, sig=obj.name+"."+name+".value")
					w.setFixedWidth(100)
					hlayout.addWidget(w)
			except:
				None
			layout.addLayout(hlayout)
		self.setLayout(layout)
			
	def resume_widget(self):
		self._paused = False
		self.runCode()
		self.resume_children()

	def default_code(self):
		return """
			from bsstudio.functions import widgetValueString
			ui = self.ui
			obj_name = widgetValueString(self, self.ophydObject) 
			ophydObject = eval(obj_name)
			self.createFields(ophydObject, obj_name)
			"""[1:]
