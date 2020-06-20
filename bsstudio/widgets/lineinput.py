from .CodeObject import CodeObject
from .REButton import makeProperty
from PyQt5.QtWidgets import QLineEdit

class LineInput(QLineEdit, CodeObject):
	def __init__(self, parent=None,*, sig=""):
		#super().__init__(parent)
		QLineEdit.__init__(self,parent)
		CodeObject.__init__(self,parent,copyNameSpace=False)
		self._destination = ""
		self.destination = sig
		self.returnPressed.connect(self.run_code)

	def default_code(self):
		return """
			from bsstudio.functions import widgetValue
			ui = self.ui
			#destination = widgetValue(eval(self.destination))
			#val = widgetValue(eval(self.text()))
			exec(self.destination+" = "+self.text())
			"""[1:]
		
	destination = makeProperty("destination")
