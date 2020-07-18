from .Base import BaseWidget
from . import CodeContainer
from .REButton import makeProperty
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QListWidget, QTableWidget, QTableWidgetItem, QFrame, QVBoxLayout, QLabel, QPushButton
from bsstudio.functions import widgetValue, plotHeader
from collections.abc import Iterable
import time


class DataBrowser(CodeContainer):
	def __init__(self, parent):
		super().__init__(parent)
		self._db = ""
		self.dbObj = None
		self._dbKwargs = "{}"
		self._plots = "[]"
		self._plotArgsList = "[[]]"
		self._plotKwargsList = "[{}]"
		layout = QVBoxLayout()
		#self.listWidget = QListWidget()
		self.listWidget = QTableWidget()
		now = QDateTime.currentDateTime()
		self.startDateTime = QDateTimeEdit(now.addMonths(-6))
		self.endDateTime = QDateTimeEdit(now)
		self.loadScansButton = QPushButton("Load Scans")
		layout.addWidget(self.startDateTime)
		layout.addWidget(self.endDateTime)
		layout.addWidget(self.loadScansButton)
		layout.addWidget(self.listWidget)
		self.setLayout(layout)

		self.loadScansButton.clicked.connect(self.__updateTable)
		self.listWidget.itemSelectionChanged.connect(self.__replot)

	def __updateTable(self):
		self.runCode()
		self._updateTable()


	def __replot(self):
		self.runCode()
		self._replot()

	def updateTable(self, db, dbKwargs):
		#self.listWidget.clear()
		since = self.startDateTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
		until = self.endDateTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
		results = list(db(since=since, until=until, **dbKwargs))
		self.listWidget.setRowCount(len(results))
		self.listWidget.setSortingEnabled(True)
		self.listWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		col_set=set([])
		for r in results:
			cols = [k for k,v in r.start.items() if not isinstance(v,Iterable) or type(v)==str]
			col_set.update(cols)	
		cols = list(col_set)
		self.listWidget.setColumnCount(len(cols))
		self.listWidget.setHorizontalHeaderLabels(cols)
		for i in range(len(results)):
			r = results[i]
			#self.listWidget.addItem(r.start['uid'])
			for j in range(len(cols)):
				#item = QTableWidgetItem(r.start['uid'])
				print(cols[j])
				print(r.start[cols[j]])
				item = QTableWidgetItem(str(r.start[cols[j]]))
				self.listWidget.setItem(i,j,item)

	def findHorizontalHeaderIndex(self, key):
		for i in range(self.listWidget.columnCount()):
			if self.listWidget.horizontalHeaderItem(i).text()==key:
				return i
		return None

	"""
	def currentUid(self):
		row = self.listWidget.currentRow()
		uid_col = self.findHorizontalHeaderIndex("uid")
		item = self.listWidget.item(row,uid_col)
		if item is None:
			return None
		return item.text()
	"""
	def currentUid(self):
		uids = self.currentUids()
		if len(uids)==0:
			return None
		return uids[0]

	def currentUids(self):
		rows = self.listWidget.selectedItems()
		uid_col = self.findHorizontalHeaderIndex("uid")
		uids = [item.text() for item in rows if item.column()==uid_col]
		return uids
		

	def startData(self,key):
		return self.dbObj[self.currentUid()].start[key]
		

	"""
	def replot(self, plots, db):
		from copy import copy
		#item = self.listWidget.currentItem()
		uid = self.currentUid()
		if uid is None:
			return
		if plots is None:
			return
		for p in plots:
			if not hasattr(p, "ax"):
				p._LivePlot__setup()
				
		
		for p in plots:
			plotHeader(p, db[uid])
			p.ax.figure.tight_layout()
	"""

	def replotUid(self, plots, db, uid):
		if uid is None:
			return
		if plots is None:
			return
		for p in plots:
			if not hasattr(p, "ax"):
				p._LivePlot__setup()
		
		for p in plots:
			plotHeader(p, db[uid])
			p.ax.figure.tight_layout()
		

	def replot(self, plots, db):
		for uid in self.currentUids():
			self.replotUid(plots, db, uid)

	def default_code(self):
		return """
			ui = self.ui
			from functools import partial
			from bsstudio.functions import widgetValue
			from bsstudio.functions import makeLivePlots 
			db = widgetValue(eval(self.db))
			self.dbObj = db
			#self.startDateTime.dateTimeChanged.connect(partial(self.updateTable, db))
			#self.endDateTime.dateTimeChanged.connect(partial(self.updateTable, db))
			plots = eval(self.plots)
			for plot in plots:
				plot.canvas.ax.clear()
			try:
				plotArgsList = widgetValue(eval(self.plotArgsList))
			except TypeError:
				print(self.plotArgsList)
				print("databrowser plotargslist exception")
				plotArgsList = None
			plotKwargsList = eval(self.plotKwargsList)
			dbKwargs = widgetValue(eval(self.dbKwargs))
			livePlots = makeLivePlots(plots, plotArgsList, plotKwargsList)
			#self.replot(plots, db)
			#self.updateTable(db, dbKwargs)
			#self.listWidget.currentTextChanged.connect(partial(self.replot, plots, db))
			self._replot = partial(self.replot, livePlots, db)
			self._updateTable = partial(self.updateTable, db, dbKwargs)
			#for plot in plots:
			#	plot.canvas.update()
			#	plot.update()
			#	plot.canvas.draw()
			
			
			"""[1:]

	db = makeProperty("db")
	dbKwargs = makeProperty("dbKwargs")
	plots = makeProperty("plots")
	plotArgsList = makeProperty("plotArgsList")
	plotKwargsList = makeProperty("plotKwargsList")
