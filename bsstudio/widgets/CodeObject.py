from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
from PyQt5.QtCore import pyqtSignal
import inspect
from itertools import dropwhile
import textwrap
from .Base import BaseWidget
import sys
from IPython import get_ipython
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, QMutex, QObject
from ..worker import Worker, WorkerSignals
from functools import partial
import logging
import time
import threading

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARN)

class CodeThread(QThread):
	mutex = QMutex()
	destroyAllThreads = pyqtSignal()
	def safe_terminate(self):
		if not self.isRunning():
			return
		while self.waitingForLock:
			time.sleep(.1)
		self.terminate()
		self.wait()
		CodeThread.mutex.unlock()

	def run(self):
		self.waitingForLock = True
		#CodeThread.destroyAllThreads.connect(self.quit)
		CodeThread.mutex.lock()
		self.waitingForLock = False
		self.parent().runCode_()
		CodeThread.mutex.unlock()



class CodeObject(BaseWidget):

	def __init__(self, parent=None, copyNameSpace=True):
		#self.parent = parent
		super().__init__(parent)
		code = textwrap.dedent(self.default_code())
		self._code = bytes(code, "utf-8")
		self._paused = True
		self._useThreading = False
		self._copyNameSpace = copyNameSpace
		self.ns_extras = {}

	def addToNameSpace(self, key, val):
		self.ns_extras[key] = val

	@Property("QByteArray", designable=True)
	def code(self):
		return self._code

	@code.setter
	def code(self, val):
		self._code = val

		
	def default_code(self):
		return ""

	def pause_widget(self):
		logger.info("pausing widget")
		self._paused = True

	def resume_widget(self):
		logger.info("unpausing widget")
		self._paused = False
		#self.setup_namespace()

		
	def setup_namespace(self):
		t0 = time.time()
		ip = get_ipython()
		if self._copyNameSpace:
			ns = ip.user_ns.copy()
		else:
			ns = ip.user_ns
			
		ns['self'] = self
		ns.update(self.ns_extras)
		self.ns = ns
		logger.info("setup_namespace duration for "+self.objectName()+": "+str(time.time()-t0))

	def runInNameSpace(self, codeString):
		if self._paused:
			logger.info("widget paused")
			return
		self.setup_namespace()
		logger.info("runInNameSpace for "+self.objectName())
		
		try:
			t0 = time.time()
			exec(codeString, self.ns)
			logger.info("exec duration for "+self.objectName()+": "+str(time.time()-t0))
		except BaseException as e:
			additional_info = " Check code in "+self.objectName()+" widget"
			raise type(e)(str(e) + additional_info).with_traceback(sys.exc_info()[2])
		del self.ns


	def runPaused(self):
		pass

	def runCode_(self):
		self.runInNameSpace(self._code)

	def runCode(self):
		#CodeThread.destroyAllThreads.emit()
		if self._paused:
			self.runPaused()
			return
		if not self._useThreading:
			self.runCode_()
		else:
			code_thread = CodeThread(self)
			self.closing.connect(code_thread.safe_terminate)
			code_thread.start()
			

	def closeEvent(self, evt):
		self.closing.emit()
		super().closeEvent(evt)
