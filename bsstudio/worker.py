from PyQt5 import QtCore

class WorkerSignals(QtCore.QObject):
	trigger = QtCore.pyqtSignal(object, list)


class Worker(QtCore.QRunnable):
	signals = WorkerSignals()
	def __init__(self, fn, *args, **kwargs):
		super(Worker, self).__init__()
		self.fn = fn
		self.args = args
		self.kwargs = kwargs

	@QtCore.pyqtSlot()
	def run(self):
		self.fn(*self.args, **self.kwargs)
		#self.finished.emit()


