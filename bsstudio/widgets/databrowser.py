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

		self.startDateTime.dateTimeChanged.connect(self.runCode)
		self.endDateTime.dateTimeChanged.connect(self.runCode)
		self.listWidget.currentTextChanged.connect(self.runCode)

	def updateTable(self, db):
		self.listWidget.clear()
		since = self.startDateTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
		until = self.endDateTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
		results = db(since=since, until=until)
		for r in results:
			self.listWidget.addItem(r.start['uid'])

	def replot(self, plots, db):
		for p in plots:
			if not hasattr(p, "ax"):
				p._LivePlot__setup()
			p.ax.clear()
		item = self.listWidget.currentItem()
		if item is None:
			return
		uid = item.text()
		for p in plots:
			plotHeader(p, db[uid])


	def default_code(self):
		return """
			ui = self.ui
			from functools import partial
			from bsstudio.functions import widgetValue
			from bsstudio.functions import makeLivePlots 
			db = widgetValue(eval(self.db))
			self.updateTable(db)
			#self.startDateTime.dateTimeChanged.connect(partial(self.updateTable, db))
			#self.endDateTime.dateTimeChanged.connect(partial(self.updateTable, db))
			plots = eval(self.plots)
			try:
				plotArgsList = eval(self.plotArgsList)
			except:
				print("databrowser plotargslist exception")
				plotArgsList = [[]]
			plotKwargsList = eval(self.plotKwargsList)
			plots = makeLivePlots(plots, plotArgsList, plotKwargsList)
			self.replot(plots, db)
			#self.listWidget.currentTextChanged.connect(partial(self.replot, plots, db))
			
			
			"""[1:]

	db = makeProperty("db")
	plots = makeProperty("plots")
	plotArgsList = makeProperty("plotArgsList")
	plotKwargsList = makeProperty("plotKwargsList")
