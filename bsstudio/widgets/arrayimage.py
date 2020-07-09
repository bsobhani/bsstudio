from .TextUpdate import TextUpdateBase
from .mplwidget import MplWidget
from .REButton import makeProperty
from PyQt5 import QtCore
import time

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from ..worker import Worker, WorkerSignals
def print_hi():
	print("hi")
class ArrayImage(TextUpdateBase, MplWidget):
	def print_hi(self):
		print("hi self")
	def __init__(self, parent):
		super().__init__(parent)
		self._updatePeriod = "500"
		self.updatePeriod_ = 500
		#self.busy = False
		#self.threadpool = QtCore.QThreadPool(self)
		self.threadpool.setMaxThreadCount(1)
	
	def setUpdatePeriod(self, p):
		self.updatePeriod_ = p

	def default_code(self):
		return """
		from PyQt5 import QtCore
		from bsstudio.functions import widgetValue
		from bsstudio.worker import Worker, WorkerSignals
		import numpy as np
		self.canvas.ax.clear()
		array = None
		if self.source != "":
			array = eval(self.source)
		#self.array = widgetValue(array)
		array = widgetValue(array)
		self.canvas.ax.imshow(array)
		self.canvas.draw()
		self.setUpdatePeriod(eval(self.updatePeriod))
		"""[1:]

	#def timeout(self):
	#	self.runCode2()
	#	self.timer.setInterval(self.updatePeriod_)

	#def timeout(self):
	#	#if self.worker is not None or self.worker.
	#	if self.threadpool.waitForDone(10):
	#		TextUpdateBase.timeout(self)
	#		self.timer.setInterval(self.updatePeriod_)
	#	else:
	#		logger.info("Thread still running for ArrayImage")
		
	def timeout(self):
		TextUpdateBase.timeout(self)
		self.timer.setInterval(self.updatePeriod_)

	def print_asdf(self):
		print("asdf")
		time.sleep(10)

	#def runCode2(self):
	#	if not self.busy:
	#		self.busy = True
	#		worker = Worker(self.runCode)
	#		self.threadpool.start(worker)
	#		self.busy = False


	def resume_widget(self):
		TextUpdateBase.resume_widget(self)

	#def runCode(self):
	#	#self.worker.signals.trigger.emit(self.print_hi,[])
	#	self.worker.signals.trigger.emit(self.runCode2,[])

	updatePeriod = makeProperty("updatePeriod")
