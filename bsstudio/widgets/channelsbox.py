from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from functools import partial
from bsstudio.functions import widgetValue, plotHeader, plotLPList
import numpy as np
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



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



class FieldListWidget(QWidget):
	def filter_fields(self, field_list):
		header = self.header
		field_list2 = []
		table = header.table()
		for i in range(len(field_list)):
			logger.info("Iteration "+str(i))
			#data = list(header.data(field_list[i]))
			try:
				data = table[field_list[i]]
			except KeyError:
				continue

			if not hasattr(data,"__len__") or len(data)<2:
				continue

			#if True in [str==type(d) for d in data]:
			#	continue
			#g = header.data(field_list[i])
			#try:
			#	next(g)
			#	next(g)
			#except StopIteration:
			#	continue
			field_list2.append(field_list[i])
			print(field_list2)
		return field_list2

	def populateFieldsFromList(self, field_list):
		header = self.header
		#field_list = list(header.fields())
		#field_list = self.filter_fields(field_list)
		# Commenting out because filter_fields is too slow
		self.tableWidget.setRowCount(len(field_list))
		for i in range(len(field_list)):
			view = QPushButton(self)
			obj_str = field_list[i]
			view.setText("View"+obj_str)
			def view_func(obj_str):
				import matplotlib.pyplot as plt
				#plotLPList([field_list[i]], header)
				plotLPList([obj_str], header)
				plt.show()
			#view.clicked.connect(partial(plotLPList,[field_list[i]], header))
			view.clicked.connect(partial(view_func, obj_str))
			alias = QLineEdit(self)
			labelItem = QTableWidgetItem(field_list[i])
			#label.setText(field_list[i])
			checkbox = QCheckBox(self)
			self.tableWidget.setCellWidget(i,self.view_col_num,view)
			self.tableWidget.setCellWidget(i,self.alias_col_num, alias)
			#self.tableWidget.setCellWidget(i,label)
			self.tableWidget.setItem(i,self.label_col_num,labelItem)
			self.tableWidget.setCellWidget(i,self.checkbox_col_num,checkbox)

	def populateFields(self, stream_name=None):
		if stream_name == None:
			field_list = list(self.header.fields())
		else:
			field_list = list(self.header.fields(stream_name))
		self.populateFieldsFromList(field_list)

	#def populateFieldsFiltered(self):
	#	field_list = list(self.header.fields())
	#	field_list = self.filter_fields(field_list)
	#	self.populateFieldsFromList(field_list)
		
	def __init__(self, parent, header, dataBrowser):
		#self.parent = parent
		self.header = header
		self.dataBrowser = dataBrowser
		QWidget.__init__(self,parent)
		self.setParent(parent)
		self.vl = QVBoxLayout()
		self.tableWidget = QTableWidget()
		self.checkbox_col_num = 0
		self.label_col_num = 1
		self.alias_col_num = 2
		self.view_col_num = 3
		self.tableWidget.setColumnCount(4)
		self.tableWidget.setSortingEnabled(True)

		self.populateFields()
		self.vl.addWidget(self.tableWidget)
		self.setLayout(self.vl)
		

	def saveAliases(self):
		N = self.tableWidget.rowCount()
		for i in range(N):
			alias = self.tableWidget.cellWidget(i,self.alias_col_num).text()
			if alias == "":
				continue
			field = self.tableWidget.item(i,self.label_col_num).text()
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
		return [self.tableWidget.item(i,1).text() for i in range(N) if self.tableWidget.cellWidget(i,0).isChecked()]
	

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
			field = self.fl.tableWidget.item(i,self.fl.label_col_num).text()
			checkBox = self.fl.tableWidget.cellWidget(i,self.fl.checkbox_col_num)
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
			field = self.fl.tableWidget.item(i,self.fl.label_col_num).text()
			alias_cell = self.fl.tableWidget.cellWidget(i,self.fl.alias_col_num)
			if (uid, field) in alias_fields_reverse.keys():
				#try:
				#	dataBrowser.alias_fields_reverse[uid]
				#except KeyError:
				#	dataBrowser.alias_fields_reverse[uid] = {}
				alias = dataBrowser.alias_fields_reverse[uid, field]
				alias_cell.setText(alias)


		
		


	def saveAliases(self):
		self.fl.saveAliases()

	def cb_selected(self):
		stream = self.stream_cb.currentText()
		if stream == "all":
			stream = None
		self.fl.populateFields(stream)
			
		
	def __init__(self, parent):
		ScrollMessageBox.__init__(self, parent)
		self.setParent(parent)
		self.uid = self.parent().currentUid()
		header = parent.dbObj[self.uid]
		self.fl = FieldListWidget(self.scroll, header, self.parent())
		self.scroll.setWidget(self.fl)
		button = QPushButton(self)
		button.setText("Apply")
		self.vl.addWidget(button)
		self.stream_cb = QComboBox(self)
		cb_choices = ["all"] + list(header.stream_names)
		self.stream_cb.addItems(cb_choices)
		self.vl.insertWidget(0, self.stream_cb)
		self.loadCheckedFields()
		self.loadAliases()
		button.pressed.connect(self.saveCheckedFields)
		button.pressed.connect(self.saveAliases)
		self.stream_cb.currentTextChanged.connect(self.cb_selected)


