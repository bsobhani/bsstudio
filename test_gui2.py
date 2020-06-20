from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
import bsstudio

def print_hi():
	print("hi")
	#cmd = 'import bsstudio\nbsstudio.load("/home/bsobhani/bsw/bss_test54.ui")'
	#ip = get_ipython()
	#exec(cmd, ip.user_ns)
	import test_gui

app = QApplication.instance() # checks if QApplication already exists 
if not app: # create QApplication if it doesnt exist 
	app = QApplication(sys.argv)
#if __name__=="__main__":
#	app = QApplication([])

widget = QWidget()
layout = QVBoxLayout()
label = QLabel("test")
layout.addWidget(label)
button = QPushButton("test")
button.clicked.connect(print_hi)
layout.addWidget(button)
widget.setLayout(layout)
widget.show()
if __name__=="__main__":
	app.exec_()
#app.exit(app.exec_())
