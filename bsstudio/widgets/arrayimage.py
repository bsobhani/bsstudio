from .TextUpdate import TextUpdateBase
from .mplwidget import MplWidget
from .REButton import makeProperty
from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout
import pyqtgraph as pg
import matplotlib.cm
import time
from functools import partial

import logging

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARN)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class ArrayImage(TextUpdateBase, pg.GraphicsLayoutWidget):
	def __init__(self, parent):
		pg.GraphicsLayoutWidget.__init__(self, parent)
		TextUpdateBase.__init__(self, parent)
		self._updatePeriod = "10000"
		self._enableHistogram = False
		self.updatePeriod_ = eval(self._updatePeriod)
		self.threadMode = "qtimer"
		self._useThreading = False
		self.imv = pg.ImageItem()
		self.view = self.addPlot()
		self.centralWidget.layout.setSpacing(0)
		self.centralWidget.setContentsMargins(0,0,0,0)
		self.centralWidget.layout.setContentsMargins(0,0,0,0)
		self.view.setContentsMargins(0,0,0,0)
		self.view.addItem(self.imv)
		self.lineh = self.view.addLine(y=.5)
		self.lineh.setMovable(True)
		self.linev = self.view.addLine(x=.5)
		self.linev.setMovable(True)
		self.linesToggle()
		self.hist = pg.HistogramLUTItem(image=self.imv,fillHistogram=True)
		self.setLayout(QVBoxLayout())
		self.addItem(self.hist)
		histogramAction = self.view.getViewBox().menu.addAction("Histogram")
		linesAction = self.view.getViewBox().menu.addAction("Lines")
		histogramAction.triggered.connect(self.histogramToggle)
		linesAction.triggered.connect(self.linesToggle)
		self.hist.hide()

		vb = self.view.getViewBox()

		submenu_cmaps = vb.menu.addMenu('cmaps');
		col_inferno = submenu_cmaps.addAction('inferno')
		col_viridis = submenu_cmaps.addAction('viridis')
		col_cividis = submenu_cmaps.addAction('cividis')
		col_magma = submenu_cmaps.addAction('magma')
		col_gray = submenu_cmaps.addAction('gray')

		def set_cmap(c):
			import bsstudio.widgets.ut as ut
			pos, rgba_colors = zip(*ut.cmapToColormap(c))
			# Set the colormap
			pgColormap = pg.ColorMap(pos, rgba_colors)
			self.imv.setLookupTable(pgColormap.getLookupTable())
			self.hist.gradient.setColorMap(pgColormap)
		col_gray.triggered.connect(partial(set_cmap, matplotlib.cm.gray))
		col_viridis.triggered.connect(partial(set_cmap, matplotlib.cm.viridis))
		col_magma.triggered.connect(partial(set_cmap, matplotlib.cm.magma))
		col_cividis.triggered.connect(partial(set_cmap, matplotlib.cm.cividis))
		col_inferno.triggered.connect(partial(set_cmap, matplotlib.cm.inferno))

		vb.setMouseMode(vb.RectMode)



		
	def toggleWidgetVisibility(self, w):
		if w.isVisible():
			w.hide()
		else:
			w.show()

	def histogramToggle(self):
		self.toggleWidgetVisibility(self.hist)

	def linesToggle(self):
		self.toggleWidgetVisibility(self.lineh)
		self.toggleWidgetVisibility(self.linev)
	
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
			import numpy as np
			import pyqtgraph as pg
			pg.setConfigOption('background', 'w')
			pg.setConfigOption('foreground', 'k')
			pg.setConfigOptions(antialias=False)
			array = None
			logger.debug("time before eval source: "+str(time.time()-t0))
			if self.source != "":
				try:
					array = eval(self.source)
				except:
					array = None
			logger.debug("time before widgetValue: "+str(time.time()-t0))
			array = widgetValue(array)
			t2 = time.time()
			logger.debug("time before imshow: "+str(t2-t0))
			if not hasattr(self,"ran_once"):
				self.imv.setImage(array,autoRange=True, autoLevels=True, autoDownSample=False)
				self.hist.setHistogramRange(self.imv.levels[0],self.imv.levels[1],padding=0)
			else:
				self.imv.setImage(array,autoRange=False, autoLevels=False, autoDownSample=False)
			t3 = time.time()
			logger.debug("time after imshow: "+str(t3-t0))
			logger.debug("time after draw: "+str(time.time()-t0))
			self.setUpdatePeriod(eval(self.updatePeriod))
			t1 = time.time()
			logger.debug("time at end of runCode: "+str(t1-t0))
			self.ran_once = True
			"""[1:]


	def closeEvent(self, evt):
		#self.closing.emit()
		self.pauseWidget()
		self.worker.cancel()
		pg.GraphicsLayoutWidget.closeEvent(self,evt)
		TextUpdateBase.closeEvent(self,evt)

	def resumeWidget(self):
		TextUpdateBase.resumeWidget(self)


