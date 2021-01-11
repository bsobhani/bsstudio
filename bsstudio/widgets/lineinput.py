from .CodeObject import CodeObject
from .TextUpdate import TextUpdateBase
from .REButton import makeProperty
from PyQt5.QtWidgets import QLineEdit
import textwrap
import logging

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARN)

class LineInput(QLineEdit, TextUpdateBase):
	def __init__(self, parent=None,*, sig=""):
		QLineEdit.__init__(self,parent)
		TextUpdateBase.__init__(self,parent)
		self._copyNameSpace = False
		self._destination = ""
		self.destination = sig
		textUpdateCode = textwrap.dedent(TextUpdateBase.default_code(self))
		self._textUpdateCode = bytes(textUpdateCode, "utf-8")
		self.returnPressed.connect(self.runCode)
		self.updateTextSignal.connect(self.setText)

	def timeout(self):
		if not self.hasFocus() and self.source!="":
			logger.info(self.objectName()+":timeout")
			logger.info(self.objectName()+":code:"+str(self.textUpdateCode))
			self.runInNameSpace(self.textUpdateCode)

	def default_code(self):
		return """
			from bsstudio.functions import widgetValue
			ui = self.ui
			val = widgetValue(eval(self.text()))

			if self.hasFocus() and self.destination!="":
				exec(self.destination+" = "+self.text())
			"""[1:]
		
	textUpdateCode = makeProperty("textUpdateCode", "QByteArray")
	destination = makeProperty("destination")
