from bluesky_widgets.examples.qt_search import QtSearchListWithButton, SearchListWithButton
from bluesky_widgets.qt._searches import QtSearches
from bluesky_widgets.qt.figures import QtFigures
from bluesky_widgets.models.plot_specs import FigureSpecList
from bluesky_widgets.models.run_tree import RunTree
from bluesky_widgets.qt.run_tree import QtTreeView
from bluesky_widgets.models.search import Search
from .widgets.REButton import makeProperty
from .functions import evalInNs
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtProperty
from bluesky_widgets.examples.utils.generate_msgpack_data import get_catalog

from .widgets import BaseWidget
class ExampleAppConversion(QtSearchListWithButton, BaseWidget):
	def __init__(self, parent):
		BaseWidget.__init__(self, parent)
		self.searches = SearchListWithButton()
		#QtSearchListWithButton.__init__(self, self.searches)
		QtSearchListWithButton.__init__(self, self.searches, parent=parent)
		#QWidget.__init__(self, parent)

class QtSearchesConversion(QtSearches, BaseWidget):
	def __init__(self, parent):
		BaseWidget.__init__(self, parent)
		self._db = ""
		self.searches = SearchListWithButton()
		QtSearches.__init__(self, self.searches, parent=parent)

	def setDbObj(self):
		from bluesky_widgets.examples.utils.add_search_mixin import columns
		db = evalInNs(self, self.db)
		self.searches.append(Search(db, columns=columns))
	def resumeWidget(self):
		self.setDbObj()
	db = makeProperty("db")

class QtFiguresConversion(QtFigures, BaseWidget):
	def __init__(self, parent):
		BaseWidget.__init__(self, parent)
		#self.searches = SearchListWithButton()
		#QtSearchListWithButton.__init__(self, self.searches)
		QtFigures.__init__(self, FigureSpecList(), parent=parent)
		#QWidget.__init__(self, parent)

class QtTreeViewConversion(QtTreeView, BaseWidget):
	def __init__(self, parent):
		BaseWidget.__init__(self, parent)
		self._runHeader=""
		self.model = RunTree()
		QtTreeView.__init__(self, self.model, parent=parent)

	def setHeaderObj(self):
		h = evalInNs(self, self.runHeader)
		if hasattr(h, "metadata"):
			self.model.run = h
		else:
			self.model.run = get_catalog()[-1]
			self.model.run.metadata = h
	def resumeWidget(self):
		self.setHeaderObj()
		
	runHeader = makeProperty("runHeader")
