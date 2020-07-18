# Imports
from PyQt5 import QtWidgets, QtCore
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5 import StatusbarQt
from matplotlib.backend_bases import StatusbarBase
import matplotlib
from .Base import BaseWidget

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

#def on_mouse_move(event):
#	print('Event received:',event.x,event.y)
# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
	def __init__(self):
		self.fig = Figure()
		self.ax = self.fig.add_subplot(111)

		Canvas.__init__(self, self.fig)
		Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		Canvas.updateGeometry(self)
		#self.mpl_connect('motion_notify_event',on_mouse_move)
		#self.ax.plot([0, 1], [1, 1])

	def wipe(self):
		self.fig.clf()
		self.ax = self.fig.add_subplot(111)
		

# Matplotlib widget
class MplWidget(QtWidgets.QWidget, BaseWidget):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
		self.canvas = MplCanvas()				   # Create canvas object

		self.toolbar = NavigationToolbar(self.canvas, self)
		#self.statusbar = StatusbarBase(self.canvas.manager.toolmanager)
		#self.statusbar = StatusbarQt(self, None)

		self.vbl = QtWidgets.QVBoxLayout()		   # Set box for plotting
		self.vbl.addWidget(self.toolbar)
		self.vbl.addWidget(self.canvas)
		#self.vbl.addWidget(self.statusbar)
		#self.vbl.addWidget(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.canvas, self))
		self.setLayout(self.vbl)
		def format_coord(x, y):
			return "x={:0.2f},y={:0.2f}".format(x,y)
		self.canvas.ax.format_coord = format_coord
		#self.canvas.ax.figure.tight_layout()
		#self.canvas.window().statusbar().setVisible(True)

	def sizeHint(self):
		return QtCore.QSize(400, 300) 
