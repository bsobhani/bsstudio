from .TextUpdate import TextUpdateBase
from .mplwidget import MplWidget
from .REButton import makeProperty
from PyQt5 import QtCore
import time

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from ..worker import Worker, WorkerSignals
class ArrayImage(TextUpdateBase, MplWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self._updatePeriod = "1500"
		self.updatePeriod_ = eval(self._updatePeriod)
		self.threadpool.setMaxThreadCount(1)
	
	def setUpdatePeriod(self, p):
		self.updatePeriod_ = p

	def default_code(self):
		return """
		import logging
		logger = logging.getLogger(__name__)
		logger.setLevel(logging.DEBUG)
		import time
		t0 = time.time()
		from PyQt5 import QtCore
		from bsstudio.functions import widgetValue
		from bsstudio.worker import Worker, WorkerSignals
		import numpy as np
		self.canvas.ax.clear()
		array = None
		logger.info("time before eval source: "+str(time.time()-t0))
		if self.source != "":
			array = eval(self.source)
		logger.info("time before widgetValue: "+str(time.time()-t0))
		array = widgetValue(array)
		t2 = time.time()
		logger.info("time before imshow: "+str(t2-t0))
		self.canvas.ax.imshow(array)
		t3 = time.time()
		logger.info("time after imshow: "+str(t3-t0))
		self.canvas.draw()
		logger.info("time after draw: "+str(time.time()-t0))
		self.setUpdatePeriod(eval(self.updatePeriod))
		t1 = time.time()
		logger.info("time at end of runCode: "+str(t1-t0))
		"""[1:]


	def resume_widget(self):
		TextUpdateBase.resume_widget(self)

	updatePeriod = makeProperty("updatePeriod")
