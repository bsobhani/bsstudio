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
logger.setLevel(logging.INFO)

class CodeThread(QThread):
	mutex = QMutex()
	#terminating = False

	def safe_terminate(self):
		self.terminating = True
		while self.waitingForLock:
			logger.info("waiting for lock" + str(self))
			CodeThread.mutex.unlock()
			time.sleep(.1)
		logger.info("before terminate")
		if self.wait(1):
			return
		self.terminate()
		logger.info("after terminate")
		self.wait()
		CodeThread.mutex.unlock()

	def run(self):
		logger.info("starting thread" + str(self))
		self.waitingForLock = True
		CodeThread.mutex.lock()
		self.waitingForLock = False
		if self.terminating:
			logger.info("thread exiting due to terminate")
			CodeThread.mutex.unlock()
			return
		self.parent().runCode_()
		CodeThread.mutex.unlock()
	def __init__(self, parent):
		#super().__init__(parent)
		QThread.__init__(self, parent)
		self.waitingForLock = False
		self.terminating = False
		



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

	def pauseWidget(self):
		logger.info("pausing widget")
		self._paused = True

	def resumeWidget(self):
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

	def terminate_thread(self):
		while self.code_thread.waitingForLock:
			time.sleep(.1)
		self.code_thread.terminate()
		self.code_thread.wait()

	def runCode(self):
		#CodeThread.destroyAllThreads.emit()
		if self._paused:
			self.runPaused()
			return
		if not self._useThreading:
			self.runCode_()
		else:
			self.code_thread = CodeThread(self)
			self.closing.connect(self.code_thread.safe_terminate)
			#self.closing.connect(self.terminate_thread)
			self.code_thread.start()
			

	def closeEvent(self, evt):
		#self.terminate_thread()
		#self.code_thread.wait()
		super().closeEvent(evt)
