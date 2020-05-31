from PyQt5 import uic, QtWidgets, QtCore
import sys
from bsstudio.widgets.REButton import Worker

f = "/home/bsobhani/bsw/bss_test8.ui"
#class MainWindow(QtWidgets.QMainWindow):
class MainWindow(*uic.loadUiType(f)):
	def __init__(self, f, parent=None):
		super().__init__(parent)

		self.setupUi(self)
		#self.ui = uic.loadUi(f)
		#self.worker = Worker(self.ui.show)
		self.worker = Worker(self.show)

		def call_func(func, params):
			func(*params)

		self.threadpool = QtCore.QThreadPool(self)
		self.threadpool.start(self.worker)
		#self.ui.show()
		self.worker.signals.trigger.connect(call_func)

		

def load(f):
	app = QtWidgets.QApplication.instance() # checks if QApplication already exists 
	if not app: # create QApplication if it doesnt exist 
		app = QtWidgets.QApplication(sys.argv)
	#app = QtWidgets.QApplication([])


	mainWindow = MainWindow(f)
	mainWindow.show()
	#app.exec_()
	app.exit(app.exec_())
