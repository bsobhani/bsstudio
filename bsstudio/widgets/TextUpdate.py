from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
from PyQt5.QtCore import QThread
from ophyd.sim import det
import inspect
from itertools import dropwhile
import textwrap
from .CodeObject import CodeObject
from ophyd.ophydobj import OphydObject
import logging
from ..worker import Worker
import time
import threading
import sip

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

main_thread = threading.current_thread()

def isOphyd(obj):
	return issubclass(obj, OphydObject)

class WorkerThread(QThread):
	def setFunc(self, func):
		self.func = func
	def run(self):
		self.func()	

class TextUpdateBase(CodeObject):
	def __init__(self, parent=None,*,sig=""):
		self.parent = parent
		#super().__init__(parent)
		#QLabel.__init__(self, parent)
		CodeObject.__init__(self, parent)
		self.updatePeriod_ = 1500
		self._source = ""
		self.source = sig
		self._useThreading = False
		self.threadpool.setMaxThreadCount(1)
		#self.worker = Worker(self.start_thread)
		self.worker = WorkerThread(self)
		self.worker.setFunc(self.start_thread)
		self.start_time = time.time()

	def timeout(self):
		self.runCode()

	def start_thread(self):
		t0 = time.time()
		while not sip.isdeleted(self):
			if time.time()-t0>self.updatePeriod_/1000 and main_thread.isAlive():
				self.timeout()
				logger.info("runCode duration: "+str(time.time()-t0))
				logger.info("update period: "+str(self.updatePeriod_))
				#time.sleep(self.updatePeriod_/1000)

	def updateText(self, val):
		if val == None:
			self.setText("unknown")
			logger.info("setting text to unknown")
		else:
			self.setText(val)
	

	def default_code(self):
		return """
			from bsstudio.functions import widgetValue, fieldValue
			ui = self.ui
			v = widgetValue(fieldValue(self, "source"))
			if v is not None:
				v = str(v)
			self.updateText(v)
			"""[1:]

	@Property(str, designable=True)
	def source(self):
		return self._source

	@source.setter
	def source(self, val):
		self._source = val

	def pause_widget(self):
		self._paused = True

	def resume_widget(self):
		CodeObject.resume_widget(self)
		#self.threadpool.clear()
		#self.threadpool.start(self.worker)
		self.worker.start()




class TextUpdate(QLabel, TextUpdateBase):
	def __init__(self, parent=None,*,sig=""):
		self.parent = parent
		#super().__init__(parent)
		QLabel.__init__(self, parent)
		TextUpdateBase.__init__(self, parent, sig=sig)

	def atq(self):
		print("about to quit")

