from .Base import BaseWidget
from . import CodeContainer
from .REButton import makeProperty
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtWidgets import QListWidget, QFrame, QVBoxLayout, QLabel
from bsstudio.functions import widgetValue, plotHeader

class DataBrowser(CodeContainer):
	def __init__(self, parent):
		super().__init__(parent)
		self._db = ""
		self._dbKwargs = "{}"
		self._plots = "[]"
		self._plotArgsList = "[[]]"
		self._plotKwargsList = "[{}]"
		layout = QVBoxLayout()
		self.listWidget = QListWidget()
		now = QDateTime.currentDateTime()
		self.startDateTime = QDateTimeEdit(now.addMonths(-6))
		self.endDateTime = QDateTimeEdit(now)
		layout.addWidget(self.startDateTime)
		layout.addWidget(self.endDateTime)
		layout.addWidget(self.listWidget)
		self.setLayout(layout)

		#self.startDateTime.dateTimeChanged.connect(self.runCode)
		#self.endDateTime.dateTimeChanged.connect(self.runCode)
		#self.listWidget.currentTextChanged.connect(self.runCode)
		self.startDateTime.dateTimeChanged.connect(self.__updateTable)
		self.endDateTime.dateTimeChanged.connect(self.__updateTable)
		self.listWidget.currentTextChanged.connect(self.__replot)

	def __updateTable(self):
		self.runCode()
		self._updateTable()


	def __replot(self):
		self.runCode()
		self._replot()

	def updateTable(self, db, dbKwargs):
		self.listWidget.clear()
		since = self.startDateTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
		until = self.endDateTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
		results = db(since=since, until=until, **dbKwargs)
		for r in results:
			self.listWidget.addItem(r.start['uid'])

	def replot(self, plots, db):
		item = self.listWidget.currentItem()
		print("item",item)
		if item is None:
			return
		for p in plots:
			if not hasattr(p, "ax"):
				p._LivePlot__setup()
			p.ax.clear()
		
		uid = item.text()
		print("uid",uid)
		for p in plots:
			plotHeader(p, db[uid])


	def default_code(self):
		return """
			ui = self.ui
			from functools import partial
			from bsstudio.functions import widgetValue
			from bsstudio.functions import makeLivePlots 
			db = widgetValue(eval(self.db))
			#self.startDateTime.dateTimeChanged.connect(partial(self.updateTable, db))
			#self.endDateTime.dateTimeChanged.connect(partial(self.updateTable, db))
			plots = eval(self.plots)
			try:
				plotArgsList = eval(self.plotArgsList)
			except:
				print("databrowser plotargslist exception")
				plotArgsList = [[]]
			plotKwargsList = eval(self.plotKwargsList)
			dbKwargs = eval(self.dbKwargs)
			plots = makeLivePlots(plots, plotArgsList, plotKwargsList)
			#self.replot(plots, db)
			#self.updateTable(db, dbKwargs)
			#self.listWidget.currentTextChanged.connect(partial(self.replot, plots, db))
			self._replot = partial(self.replot, plots, db)
			self._updateTable = partial(self.updateTable, db, dbKwargs)
			
			
			"""[1:]

	db = makeProperty("db")
	dbKwargs = makeProperty("dbKwargs")
	plots = makeProperty("plots")
	plotArgsList = makeProperty("plotArgsList")
	plotKwargsList = makeProperty("plotKwargsList")
