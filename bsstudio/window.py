from PyQt5 import uic, QtWidgets, QtCore, QtGui
import sys
#from .widgets.REButton import Worker
from .worker import Worker
import typing
from .widgets import BaseWidget
#from .widgets import all_bss_widgets
import threading
import logging

def getMainWindow() -> typing.Union[QtWidgets.QMainWindow, None]:
	# Global function to find the (open) QMainWindow in application
	app = QtWidgets.QApplication.instance()
	for widget in app.topLevelWidgets():
		#if issubclass(widget.__class__, QtWidgets.QMainWindow):
		#if widget.__class__.__name__ == 'MainWindow':
		if isinstance(widget, MainWindow):
			return widget
	return None

def isMainWindow(w):
	return isinstance(w, MainWindow)

#def ui():
#	return getMainWindow()

def getWidgetById(id):
	for w in all_bss_widgets:
		if w.id == id:
			return w
	return None

mainWindow = None

def create_main_window(f):
	#f = "/home/bsobhani/bsw/bss_test9.ui"
	#class MainWindow(QtWidgets.QMainWindow):
	global MainWindow
	class MainWindow(*uic.loadUiType(f)):
		def __init__(self, parent=None):
			self.isLoaded = False
			super().__init__(parent)
			self.uiFilePath = f

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
			self.isLoaded = True

		def mousePressEvent(self, event):
			focused_widget = QtWidgets.QApplication.focusWidget()
			if issubclass(focused_widget.__class__, QtWidgets.QLineEdit):
				focused_widget.clearFocus()
			QtWidgets.QWidget.mousePressEvent(self, event)	

		def closeEvent(self, evt):
			print("close event")
			#for child in self.children():
			for child in self.findChildren(QtWidgets.QWidget):
				try:
					child.close()
				except:
					None
			self.deleteLater()

	global mainWindow
	mainWindow = MainWindow()

		

def load(f, noexec=False, verbose=False):
	import os
	log_dir = os.environ.get("BSSTUDIO_LOG_FILE_NAME")
	if log_dir is None:
		log_dir = "log"
	if verbose:
		logging.basicConfig(level=logging.WARN, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", datefmt='%Y-%m-%d %H:%M:%S')
	else:
		logging.basicConfig(filename=log_dir, filemode='a', level=logging.WARN, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", datefmt='%Y-%m-%d %H:%M:%S')
	app = QtWidgets.QApplication.instance() # checks if QApplication already exists 
	if not app: # create QApplication if it doesnt exist 
		app = QtWidgets.QApplication(sys.argv)
	#app = QtWidgets.QApplication([])


	#mainWindow = MainWindow(f)
	global mainWindow
	create_main_window(f)
	mainWindow.show()
	widgets = app.allWidgets()
	for w in widgets:
		if issubclass(w.__class__, BaseWidget):
			w.resume_widget()
	#app.exec_()
	if not noexec:
		app.exec_()
	return app
