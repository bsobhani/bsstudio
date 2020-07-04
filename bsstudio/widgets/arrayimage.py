from .TextUpdate import TextUpdateBase
from .mplwidget import MplWidget
from .REButton import makeProperty
class ArrayImage(TextUpdateBase, MplWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self._updatePeriod = "1500"

	def default_code(self):
		return """
		from bsstudio.functions import widgetValue
		import numpy as np
		self.canvas.ax.clear()
		array = None
		if self.source != "":
			array = eval(self.source)
		array = widgetValue(array)
		#self.canvas.ax.plot([0,1,0])
		self.canvas.ax.imshow(array)
		self.canvas.draw()
		self.timer.setInterval(eval(self.updatePeriod))
		"""[1:]

	updatePeriod = makeProperty("updatePeriod")
