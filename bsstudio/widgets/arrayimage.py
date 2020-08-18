from .TextUpdate import TextUpdateBase
from .mplwidget import MplWidget
from .REButton import makeProperty
from PyQt5 import QtCore
import pyqtgraph as pg
import time

import logging

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARN)

from ..worker import Worker, WorkerSignals
class ArrayImage(TextUpdateBase, pg.GraphicsLayoutWidget):
	def __init__(self, parent):
		#super().__init__(parent)
		pg.GraphicsLayoutWidget.__init__(self, parent)
		TextUpdateBase.__init__(self, parent)
		self._updatePeriod = "10000"
		self.updatePeriod_ = eval(self._updatePeriod)
		#self.threadpool.setMaxThreadCount(1)
		self.threadType = "qthread"
		#self.ui.histogram.hide()
		#self.ui.roiBtn.hide()
		#self.ui.menuBtn.hide()
		self.imv = pg.ImageItem()
		self.view = self.addViewBox()
		#self.view.setBorder(None)
		#self.centralWidget.setBorder((0,0,0))
		self.centralWidget.layout.setSpacing(0)
		self.centralWidget.setContentsMargins(0,0,0,0)
		self.centralWidget.layout.setContentsMargins(0,0,0,0)
		self.view.setContentsMargins(0,0,0,0)
		print(self.centralWidget)
		self.view.addItem(self.imv)
		#pg.GraphicsView.setCentralItem(self, self.imv)
	
	def setUpdatePeriod(self, p):
		self.updatePeriod_ = p

	def default_code(self):
		return """
		import logging
		logger = logging.getLogger(__name__)
		import time
		t0 = time.time()
		from PyQt5 import QtCore
		from bsstudio.functions import widgetValue
		from bsstudio.worker import Worker, WorkerSignals
		import numpy as np
		#self.canvas.ax.clear()
		array = None
		logger.info("time before eval source: "+str(time.time()-t0))
		if self.source != "":
			array = eval(self.source)
		logger.info("time before widgetValue: "+str(time.time()-t0))
		array = widgetValue(array)
		t2 = time.time()
		logger.info("time before imshow: "+str(t2-t0))
		#self.canvas.ax.imshow(array)
		self.imv.setImage(array)
		self.view.autoRange(padding=0)
		t3 = time.time()
		logger.info("time after imshow: "+str(t3-t0))
		#self.canvas.draw()
		logger.info("time after draw: "+str(time.time()-t0))
		self.setUpdatePeriod(eval(self.updatePeriod))
		t1 = time.time()
		logger.info("time at end of runCode: "+str(t1-t0))
		"""[1:]

	def closeEvent(self, evt):
		self.pause_widget()
		self.worker.cancel()
		pg.GraphicsLayoutWidget.closeEvent(self,evt)
		TextUpdateBase.closeEvent(self,evt)

	def resume_widget(self):
		TextUpdateBase.resume_widget(self)


class ArrayImage2(TextUpdateBase, MplWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self._updatePeriod = "10000"
		self.updatePeriod_ = eval(self._updatePeriod)
		#self.threadpool.setMaxThreadCount(1)
		self.threadType = "qthread"
	
	def setUpdatePeriod(self, p):
		self.updatePeriod_ = p

	def default_code(self):
		return """
		import logging
		logger = logging.getLogger(__name__)
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

