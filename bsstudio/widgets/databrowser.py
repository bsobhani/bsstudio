import numpy as np
from .Base import BaseWidget
from . import CodeContainer
from .REButton import makeProperty
from PyQt5.QtCore import QDateTime
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtWidgets import QSizePolicy
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
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FieldListWidget(QWidget):
	def filter_fields(self, field_list):
		header = self.header
		field_list2 = []
		for i in range(len(field_list)):
			data = list(header.data(field_list[i]))

			if not hasattr(data,"__len__") or len(data)<2:
				continue

			if True in [str==type(d) for d in data]:
				continue
			field_list2.append(field_list[i])
		return field_list2
		
	def __init__(self, parent, header, dataBrowser):
		#self.parent = parent
		self.header = header
		self.dataBrowser = dataBrowser
		QWidget.__init__(self,parent)
		self.setParent(parent)
		print("parents:",parent,self.parent())
		field_list = list(header.fields())
		#field_list = header.fields()
		self.vl = QVBoxLayout()
		self.tableWidget = QTableWidget()
		self.tableWidget.setColumnCount(3)
		#field_list = self.filter_fields(field_list)
		#Disabling filter fields because it is too slow
		self.tableWidget.setRowCount(len(field_list))
		for i in range(len(field_list)):
			alias = QLineEdit(self)
			label = QLabel(self)
			label.setText(field_list[i])
			checkbox = QCheckBox(self)
			self.tableWidget.setCellWidget(i,2,alias)
			self.tableWidget.setCellWidget(i,1,label)
			self.tableWidget.setCellWidget(i,0,checkbox)
		self.vl.addWidget(self.tableWidget)
		self.setLayout(self.vl)

	def saveAliases(self):
		N = self.tableWidget.rowCount()
		for i in range(N):
			alias = self.tableWidget.cellWidget(i,2).text()
			if alias == "":
				continue
			field = self.tableWidget.cellWidget(i,1).text()
			#print(self.parent(), self.parent().parent())
			dataBrowser = self.dataBrowser
			dbObj = dataBrowser.dbObj
			aliases = dataBrowser.aliases
			alias_fields_reverse = dataBrowser.alias_fields_reverse
			#uid = self.parent().uid
			uid = dataBrowser.currentUid()
			aliases[alias] = np.array(list(dbObj[uid].data(field)))
			#try:
			#	alias_fields_reverse[uid]
			#except KeyError:
			#	alias_fields_reverse[uid] = {}
			existing_field_keys = [key for key, val in alias_fields_reverse.items() if val == alias]
			for key in existing_field_keys:
				alias_fields_reverse[key] = ""
				
			alias_fields_reverse[uid, field] = alias
			

	#def getSavedAliases(self):
	#	dataBrowser = self.dataBrowser
	#	return dataBrowser.aliases[dataBrowser.currentUid()]
			
		

	def checkedFields(self):
		N = self.tableWidget.rowCount()
		return [self.tableWidget.cellWidget(i,1).text() for i in range(N) if self.tableWidget.cellWidget(i,0).isChecked()]
		
		

class ScrollMessageBox(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.scroll = QScrollArea()
		self.scroll.setWidgetResizable(True)
		self.vl = QVBoxLayout()
		self.vl.addWidget(self.scroll)
		self.setLayout(self.vl)
		self.content = QLabel(self)
		self.content.setWordWrap(True)
		self.scroll.setWidget(self.content)
		self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class ChannelsBox(ScrollMessageBox):
	def saveCheckedFields(self):
		self.parent().checked_fields[self.uid] = self.fl.checkedFields()

	def savedFields(self):
		if self.uid not in self.parent().checked_fields:
			return []
		return self.parent().checked_fields[self.uid]
		
	def loadCheckedFields(self):
		fields = self.savedFields()
		N = self.fl.tableWidget.rowCount()
		for i in range(N):
			field = self.fl.tableWidget.cellWidget(i,1).text()
			checkBox = self.fl.tableWidget.cellWidget(i,0)
			if field in fields:
				checkBox.setChecked(True)

	def loadAliases(self):
		#aliases = self.fl.getSavedAliases()
		dataBrowser = self.parent()
		alias_fields_reverse = dataBrowser.alias_fields_reverse
		N = self.fl.tableWidget.rowCount()
		uid = dataBrowser.currentUid()
		#if uid not in alias_fields_reverse.keys():
		#	return
		for i in range(N):
			field = self.fl.tableWidget.cellWidget(i,1).text()
			alias_cell = self.fl.tableWidget.cellWidget(i,2)
			if (uid, field) in alias_fields_reverse.keys():
				#try:
				#	dataBrowser.alias_fields_reverse[uid]
				#except KeyError:
				#	dataBrowser.alias_fields_reverse[uid] = {}
				alias = dataBrowser.alias_fields_reverse[uid, field]
				alias_cell.setText(alias)


		
		


	def saveAliases(self):
		self.fl.saveAliases()
		
	def __init__(self, parent):
		ScrollMessageBox.__init__(self, parent)
		self.setParent(parent)
		self.uid = self.parent().currentUid()
		self.fl = FieldListWidget(self.scroll, parent.dbObj[self.uid], self.parent())
		self.scroll.setWidget(self.fl)
		button = QPushButton(self)
		button.setText("Apply")
		self.vl.addWidget(button)
		self.loadCheckedFields()
		self.loadAliases()
		button.pressed.connect(self.saveCheckedFields)
		button.pressed.connect(self.saveAliases)

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
		#self.loadScansButton.clicked.connect(self.__updateTable)
		self.loadScansButton.clicked.connect(self.worker.start)
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

	def showMenu(self,event):
		menu = QMenu()
		action1 = QAction("Info", self)
		channels = QAction("Channels", self)
		view_plot = QAction("View Plot", self)
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
		if action.text() == "View Plot":
			from bluesky.callbacks import LivePlot
			header = self.dbObj[self.currentUid()]
			fields = self.selectedFields()
			#lp = LivePlot(fields)
			#lp.start(header.start)
			#for e in header.events():
			#	lp.event(e)
			plotLPList(fields, header)


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
			logger.info("len results: "+str(len(results)) +", i:"+str(i))
			#self.listWidget.addItem(r.start['uid'])
			for j in range(len(cols)):
				#item = QTableWidgetItem(r.start['uid'])
				logger.info(str(i)+" "+ str(j) + " "+str(cols[j]))
				try:
					field = r.start[cols[j]]
				except KeyError:
					field = None
				#print(str(i)+" "+ str(j) + " "+str(cols[j]))
				#print(r.start[cols[j]])
				#item = QTableWidgetItem(str(r.start[cols[j]]))
				item = DataTableWidgetItem(str(field))
				self.listWidget.setItem(i,j,item)

		if self.tableColumns!="":
			#for colName in eval(self.tableColumns):
			#	self.listWidget.hideColumn(self.findHorizontalHeaderIndex(colName))
			tableColumns = eval(self.tableColumns)
			for i in range(self.listWidget.columnCount()):
				if self.listWidget.horizontalHeaderItem(i).text() not in tableColumns:
					logger.info("hiding column "+self.listWidget.horizontalHeaderItem(i).text())
					self.listWidget.hideColumn(i)
				else:
					self.listWidget.showColumn(i)
					

	def findHorizontalHeaderIndex(self, key):
		logger.info("horizonal header count: "+str(self.listWidget.columnCount()))
		for i in range(self.listWidget.columnCount()):
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
