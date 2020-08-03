import cola
import cola.app
import cola.main
from cola.widgets.browse import worktree_browser
from cola.widgets.commitmsg import CommitMessageEditor
from cola.widgets.status import StatusWidget
from PyQt5.QtWidgets import QApplication

#cola.app.initialize()
#args = cola.main.parse_args(["cola"])
#context = cola.app.application_init(args)

def cmd_browse(args):
	from cola.widgets.browse import worktree_browser  # pylint: disable=all

	context = cola.app.application_init(args)
	view = worktree_browser(context, show=False, update=False, settings=args.settings)
	#return cola.app.application_run(context, view)
	cola.app.initialize_view(context, view)
	cola.app.default_start(context, view)
	context.app.start()
	return view

def run():
	#app = QApplication.instance()
	args = cola.main.parse_args(["cola"])

	#view = worktree_browser(context,show=False)
	#view.show()
	#return view
	
	#return cola.main.cmd_browse(args)
	return cmd_browse(args)

def make_commit():
	args = cola.main.parse_args(["cola"])
	context = cola.app.application_init(args)
	commit_editor = CommitMessageEditor(context, None)
	cola.app.initialize_view(context, commit_editor)
	cola.app.default_start(context, commit_editor)
	#commit_editor.show()
	return commit_editor

def make_status():
	class TB:
		def add_corner_widget(self, val):
			pass
	titlebar = TB()
	status_editor = StatusWidget(context, titlebar, None)
	status_editor.show()
	return status_editor
	
	

if __name__=="__main__":
	app1 = QApplication([])
	#commit_editor = make_commit()
	#status_editor = make_status()
	#print(context.model)
	view = run()
	#view.show()
	app1.exec_()
	print("here")
