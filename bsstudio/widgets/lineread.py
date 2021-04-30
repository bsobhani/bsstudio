from .CodeObject import CodeObject
from .TextUpdate import TextUpdateBase
from .REButton import makeProperty
from PyQt5.QtWidgets import QLineEdit
import textwrap

class LineRead(QLineEdit, TextUpdateBase):
	def __init__(self, parent=None,*, sig=""):
		#super().__init__(parent)
		QLineEdit.__init__(self,parent)
		TextUpdateBase.__init__(self,parent)
		self._copyNameSpace = False
		#CodeObject.__init__(self,parent,copyNameSpace=False)
	###	self._destination = ""
	###	self.destination = sig
		textUpdateCode = textwrap.dedent(TextUpdateBase.default_code(self))
		self._textUpdateCode = bytes(textUpdateCode, "utf-8")
		self.returnPressed.connect(self.runCode)

	def timeout(self):
		if not self.hasFocus():
			self.runInNameSpace(self.textUpdateCode)

	def default_code(self):
		return """
			from bsstudio.functions import widgetValue
			ui = self.ui
			#destination = widgetValue(eval(self.destination))
			#val = widgetValue(eval(self.text()))
			if self.hasFocus() and self.destination!="":
				exec(self.destination+" = "+self.text())
			"""[1:]
		
	textUpdateCode = makeProperty("textUpdateCode", "QByteArray")
	### destination = makeProperty("destination")