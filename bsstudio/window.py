from PyQt5 import uic, QtWidgets, QtCore, QtGui
import sys
#from .widgets.REButton import Worker
from .worker import Worker
import typing
from .widgets import BaseWidget
#from .widgets import all_bss_widgets
import threading
import logging
import sip
import sys



from .functions import deleteWidgetAndChildren

def setup_verbose_logging():
	#fileh = logging.FileHandler('/tmp/logfile', 'a')
	fileh = logging.StreamHandler(sys.stdout)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fileh.setFormatter(formatter)

	log = logging.getLogger()  # root logger
	for hdlr in log.handlers[:]:  # remove all old handlers
		log.removeHandler(hdlr)
	log.addHandler(fileh)      # set the new handler

def setup_file_logging(f="log"):
	fileh = logging.FileHandler(f, 'a')
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fileh.setFormatter(formatter)

	log = logging.getLogger()  # root logger
	for hdlr in log.handlers[:]:  # remove all old handlers
		log.removeHandler(hdlr)
	log.addHandler(fileh)      # set the new handler




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
	global MainWindow
	return isinstance(w, MainWindow)

mainWindow = None
main_app = None

def create_main_window(f):
	global MainWindow
	class MainWindow(*uic.loadUiType(f)):
		def __init__(self, parent=None):
			self.isLoaded = False
			super().__init__(parent)
			self.uiFilePath = f

			self.setupUi(self)
			self.isLoaded = True

		def mousePressEvent(self, event):
			focused_widget = QtWidgets.QApplication.focusWidget()
			if issubclass(focused_widget.__class__, QtWidgets.QLineEdit):
				focused_widget.clearFocus()
			QtWidgets.QWidget.mousePressEvent(self, event)	

		def closeEvent(self, evt):
			for child in self.findChildren(QtWidgets.QWidget):
				try:
					child.close()
					if isinstance(child, BaseWidget):
						#child.setParent(None)
						child.deleteLater()
				except:
					None
			self.deleteLater()
			#main_app.exit()


	global mainWindow
	mainWindow = MainWindow()
	mainWindow.show()

		

def load(f, noexec=False, verbose=False):
	import os
	log_dir = os.environ.get("BSSTUDIO_LOG_FILE_NAME")
	if log_dir is None:
		log_dir = "log"
	logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", datefmt='%Y-%m-%d %H:%M:%S')
	"""
	logging.basicConfig(filename=log_dir, filemode='a', level=logging.WARN, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", datefmt='%Y-%m-%d %H:%M:%S')
	if verbose:
		print("enabling verbose")
		#logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", datefmt='%Y-%m-%d %H:%M:%S')
	else:
		logging.basicConfig(filename=log_dir, filemode='a', level=logging.WARN, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", datefmt='%Y-%m-%d %H:%M:%S')
	"""
	if not verbose:
		setup_file_logging()
	else:
		setup_verbose_logging()
	app = QtWidgets.QApplication.instance() # checks if QApplication already exists 
	if not app: # create QApplication if it doesnt exist 
		app = QtWidgets.QApplication(sys.argv)
	global main_app
	main_app = app


	global mainWindow
	create_main_window(f)
	mainWindow.show()
	widgets = app.allWidgets()
	for w in widgets:
		if issubclass(w.__class__, BaseWidget):
			w.resume_widget()
	#app.exec_()
	if not noexec:
		#sys.exit( app.exec_() )
		app.exec_()
	return app
