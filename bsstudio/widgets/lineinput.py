from .CodeObject import CodeObject
from .REButton import makeProperty
from PyQt5.QtWidgets import QLineEdit

class LineInput(QLineEdit, CodeObject):
	def __init__(self, parent=None):
		#super().__init__(parent)
		QLineEdit.__init__(self,parent)
		CodeObject.__init__(self,parent,copyNameSpace=False)
		self._destination = ""
		self.returnPressed.connect(self.run_code)

	def default_code(self):
		return """
			ui = self.ui
			exec(self.destination+" = "+self.text())
			"""[1:]
		
	destination = makeProperty("destination")
