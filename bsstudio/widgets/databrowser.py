import numpy as np
from .Base import BaseWidget
from . import CodeContainer
from .REButton import makeProperty
from .channelsbox import ChannelsBox
from .channelsbox import ScrollMessageBox
from PyQt5.QtCore import QDateTime
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtWidgets import QListWidget, QTableWidget, QTableWidgetItem, QFrame, QVBoxLayout, QLabel, QPushButton
from bsstudio.functions import widgetValue, plotHeader, plotLPList
from collections.abc import Iterable
from functools import partial
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DBFetchResultsThread(QThread):
	def run():
		pass	
		

	
		


class DataTableWidgetItem(QTableWidgetItem):
	def __lt__(self, other):
		try:
			return float(self.text()) < float(other.text())
		except:
			return self.text() < other.text() 	

class DataBrowser(CodeContainer):
	def __init__(self, parent):
		super().__init__(parent)
		self._db = ""
		#self._tableColumns = '["time"]'
		self._tableColumns = ''
		self.dbObj = None
		self._dbKwargs = "{}"
		self._plots = "[]"
		self._plotArgsList = "[[]]"
		self._plotKwargsList = "[{}]"
		self.aliases = {}
		self.alias_fields_reverse = {}
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

		self.worker.setFunc(self.__updateTable)
		self.loadScansButton.clicked.connect(self.__updateTable)
		#self.loadScansButton.clicked.connect(self.worker.start)
		self.listWidget.itemSelectionChanged.connect(self.__replot)

		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.showMenu)
		self.checked_fields = {}

	def selectedFields(self, uid=None):
		if self.currentUid() not in self.checked_fields.keys():
			return []
		if uid == None:
			uid = self.currentUid()
		return self.checked_fields[uid]

	def plotSelectedUids(self):
		from bluesky.callbacks import LivePlot
		for uid in self.currentUids():
			header = self.dbObj[uid]
			fields = self.selectedFields(uid)
			#lp = LivePlot(fields)
			#lp.start(header.start)
			#for e in header.events():
			#	lp.event(e)
			plotLPList(fields, header)


	def showMenu(self,event):
		menu = QMenu()
		action1 = QAction("Info", self)
		channels = QAction("Channels", self)
		view_plot = QAction("Plot checked items", self)
		clear_action = menu.addAction(action1)
		channels_action = menu.addAction(channels)
		view_plot_action = menu.addAction(view_plot)
		action = menu.exec_(self.mapToGlobal(event))
		if action.text() == "Info":
			messageBox = ScrollMessageBox(self)
			messageBox.content.setText(str(self.dbObj[self.currentUid()].start))
			messageBox.show()
		if action.text() == "Channels":
			self.channelsBox = ChannelsBox(self)
			self.channelsBox.show()
		if action.text() == "Plot checked items":
			self.plotSelectedUids()
			

	def __updateTable(self):
		self.runCode()
		self._updateTable()
		#self.updateTable(self.dbObj, {})


	def __replot(self):
		self.runCode()
		#self._replot()

	def updateTable(self, db, dbKwargs):
		#self.listWidget.clear()
		since = self.startDateTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
		until = self.endDateTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
		logger.info("Reading results started")
		#results = list(db(since=since, until=until, **dbKwargs))
		results = []
		original_text = self.loadScansButton.text()
		self.loadScansButton.clicked.disconnect()
		self.loadScansButton.clicked.connect(self.worker.cancel)
		for i,r in enumerate(db(since=since, until=until, **dbKwargs)):
			results.append(r)
			N = 4
			k = (i//10)%N
			self.loadScansButton.setText("Loading"+"."*(k)+" "*(N-k))
			if self.worker.cancelled:
				break
		self.worker.resume()
		self.loadScansButton.clicked.disconnect()
		self.loadScansButton.clicked.connect(self.worker.start)
		self.loadScansButton.setText(original_text)
		logger.info("Reading results stopped")
		self.listWidget.setRowCount(len(results))
		self.listWidget.setSortingEnabled(True)
		#self.listWidget.clear()
		#self.listWidget.clearContents()
		self.listWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		col_set=set([])
		for r in results:
			cols = [k for k,v in r.start.items() if not isinstance(v,Iterable) or type(v)==str]
			col_set.update(cols)	
		cols = list(col_set)

 

		self.listWidget.setColumnCount(len(cols))
		self.listWidget.setHorizontalHeaderLabels(cols)
		time.sleep(2) # Needed to make filtering columns work properly - unclear why

		for i in range(len(results)):
			r = results[i]
			#logger.info("len results: "+str(len(results)) +", i:"+str(i))
			#self.listWidget.addItem(r.start['uid'])
			for j in range(len(cols)):
				#item = QTableWidgetItem(r.start['uid'])
				#logger.info(str(i)+" "+ str(j) + " "+str(cols[j]))
				try:
					field = r.start[cols[j]]
				except KeyError:
					#logger.info("Could not find field " + cols[j])
					field = None
				#print(str(i)+" "+ str(j) + " "+str(cols[j]))
				#print(r.start[cols[j]])
				#item = QTableWidgetItem(str(r.start[cols[j]]))
				item = DataTableWidgetItem(str(field))
				self.listWidget.setItem(i,j,item)
				#time.sleep(.1)


		#self.listWidget.setColumnCount(1)

		if self.tableColumns!="":
			#for colName in eval(self.tableColumns):
			#	self.listWidget.hideColumn(self.findHorizontalHeaderIndex(colName))
			tableColumns = eval(self.tableColumns)
			for i in range(self.listWidget.columnCount()):
				#colHeader = self.listWidget.horizontalHeaderItem(i)
				#if colHeader.text() not in tableColumns:
				if self.listWidget.horizontalHeaderItem(i).text() not in tableColumns:
					#logger.info("hiding column "+colHeader.text())
					print(self.listWidget.isColumnHidden(i))
					self.listWidget.hideColumn(i)
					self.listWidget.update()
					#assert self.listWidget.isColumnHidden(i) == True
				else:
					self.listWidget.showColumn(i)




		for i in range(self.listWidget.columnCount()):
			print(self.listWidget.isColumnHidden(i))


					

	def findHorizontalHeaderIndex(self, key):
		logger.info("horizonal header count: "+str(self.listWidget.columnCount()))
		for i in range(self.listWidget.columnCount()):
			#colHeader = self.listwidget.horizontalheaderitem(i)
			#if colHeader.text()==key:
			if self.listWidget.horizontalHeaderItem(i).text()==key:
				logger.info(key + " found")
				return i
		return None


	def currentUid(self):
		uids = self.currentUids()
		if len(uids)==0:
			return None
		#return uids[0]
		uid_col = self.findHorizontalHeaderIndex("uid")
		uid_row = self.listWidget.currentRow()
		return self.listWidget.item(uid_row, uid_col).text()

	def currentUids(self):
		#rows = self.listWidget.selectedItems()
		uid_col = self.findHorizontalHeaderIndex("uid")
		#uids = [item.text() for item in rows if item.column()==uid_col]
		rows = [item.row() for item in self.listWidget.selectedItems()]
		rows = list(set(rows))
		uids = [self.listWidget.item(row, uid_col).text() for row in rows]
		return uids
		

	def startData(self,key):
		if self.currentUid() is None:
			return []
		return self.dbObj[self.currentUid()].start[key]
		

	def replotUid(self, plots, db, uid):
		logger.info("replot uid: "+uid)
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
		#self.replotUid(plots, db, self.currentUid())

	def default_code(self):
		return """
				ui = self.ui
				from functools import partial
				from bsstudio.functions import widgetValue
				from bsstudio.functions import makeLivePlots 
				db = widgetValue(eval(self.db))
				self.dbObj = db
				self.uid = None
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
				for uid in self.currentUids():
					self.uid = uid
					plots = eval(self.plots)
					plotArgsList = widgetValue(eval(self.plotArgsList))
					livePlots = makeLivePlots(plots, plotArgsList, plotKwargsList)
					self.replotUid(livePlots, db, uid)
				#self._replot = partial(self.replot, livePlots, db)
				self._updateTable = partial(self.updateTable, db, dbKwargs)
				#for plot in plots:
				#	plot.canvas.update()
				#	plot.update()
				#	plot.canvas.draw()
				
				
			"""[1:]

	db = makeProperty("db")
	dbKwargs = makeProperty("dbKwargs")
	plots = makeProperty("plots")
	tableColumns = makeProperty("tableColumns")
	plotArgsList = makeProperty("plotArgsList")
	plotKwargsList = makeProperty("plotKwargsList")
