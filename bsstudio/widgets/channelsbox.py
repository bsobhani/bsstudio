from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from functools import partial
from bsstudio.functions import widgetValue, plotHeader, plotLPList

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
		for i in range(len(field_list)):
			#data = list(header.data(field_list[i]))

			#if not hasattr(data,"__len__") or len(data)<2:
			#	continue

			#if True in [str==type(d) for d in data]:
			#	continue
			g = header.data(field_list[i])
			try:
				next(g)
				next(g)
			except StopIteration:
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
		self.tableWidget.setColumnCount(4)
		self.tableWidget.setSortingEnabled(True)
		#field_list = self.filter_fields(field_list)
		# Commenting out because filter_fields is too slow
		self.tableWidget.setRowCount(len(field_list))
		for i in range(len(field_list)):
			view = QPushButton(self)
			view.setText("View")
			view.clicked.connect(partial(plotLPList,[field_list[i]], header))
			alias = QLineEdit(self)
			labelItem = QTableWidgetItem(field_list[i])
			#label.setText(field_list[i])
			checkbox = QCheckBox(self)
			self.tableWidget.setCellWidget(i,3,view)
			self.tableWidget.setCellWidget(i,2,alias)
			#self.tableWidget.setCellWidget(i,1,label)
			self.tableWidget.setItem(i,1,labelItem)
			self.tableWidget.setCellWidget(i,0,checkbox)
		self.vl.addWidget(self.tableWidget)
		self.setLayout(self.vl)

	def saveAliases(self):
		N = self.tableWidget.rowCount()
		for i in range(N):
			alias = self.tableWidget.cellWidget(i,2).text()
			if alias == "":
				continue
			field = self.tableWidget.item(i,1).text()
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
			field = self.fl.tableWidget.item(i,1).text()
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
			field = self.fl.tableWidget.item(i,1).text()
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


