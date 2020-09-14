import cola
import cola.app
import cola.main
from functools import partial
from cola.qtutils import add_action
from cola.i18n import N_
from cola.widgets.browse import worktree_browser
from cola.widgets.toolbar import ToolBar
from cola.widgets.commitmsg import CommitMessageEditor
from cola.widgets.status import StatusWidget
from cola.widgets.branch import BranchesWidget
from PyQt5.QtWidgets import QApplication, QMenu
from PyQt5.QtCore import QCoreApplication

import cola.models.prefs
cola.models.prefs.Defaults.editor="designer"

#cola.app.initialize()
#args = cola.main.parse_args(["cola"])
#context = cola.app.application_init(args)

actions = []

def make_menu(menu):
	for a in actions:
		action = menu.addAction(a)
		#mainThread = QCoreApplication.instance().thread()
		#action.moveToThread(mainThread)

context = None
def cmd_browse(args):
	from cola.widgets.browse import worktree_browser

	#context = cola.app.application_init(args)
	global context
	context = new_context(args)
	#view = worktree_browser(context, show=False, update=False, settings=args.settings)
	view = worktree_browser(context, show=False, update=False)
	#return cola.app.application_run(context, view)
	cola.app.initialize_view(context, view)
	cola.app.default_start(context, view)
	def open_repo(context):
		cola.guicmds.open_repo(context)
		
	view.open_repo_action = add_action(
		view, N_('Open...'), partial(cola.guicmds.open_repo, context))
	#	view, N_('Open...'), partial(open_repo, context))
	view.open_repo_action.triggered.connect(view.tree.action_refresh.trigger)
	actions.append(view.open_repo_action)
	#view.tree.update_actions()
	view.tree.action_refresh.trigger()
	#view.tree.model().refresh()
	view.refresh()
	#view.open_repo_action.trigger()
	#context.app.start()
	return view

def run():
	#app = QApplication.instance()
	args = cola.main.parse_args(["cola"])

	return cmd_browse(args)

def make_commit():
	args = cola.main.parse_args(["cola"])
	#context = new_context(args)
	global context
	#context = cola.app.application_init(args)
	commit_editor = CommitMessageEditor(context, None)
	cola.app.initialize_view(context, commit_editor)
	cola.app.default_start(context, commit_editor)
	#commit_editor.show()
	#context.app.start()
	return commit_editor

def new_context(args):
	"""Create top-level ApplicationContext objects"""
	context = cola.app.ApplicationContext(args)
	#context.settings = args.settings or cola.settings.Settings.read()
	#context.settings = cola.settings.Settings.read()
	#context.settings = Settings(verify=cola.git.is_work_tree)
	context.settings = cola.settings.Settings()
	context.settings.load()
	context.git = cola.app.git.create()
	context.cfg = cola.app.gitcfg.create(context)
	context.fsmonitor = cola.app.fsmonitor.create(context)
	context.selection = cola.app.selection.create()
	context.model = cola.app.main.create(context)
	#cola.guicmds.install()
	#cola.icons.install(args.icon_themes)
	cola.icons.install(cola.app.get_icon_themes(context))
	#toolbar = ToolBar.create(context, "asdf")
	#toolbar.show()
	#context.app = cola.app.new_application(context, args)
	#context.timer = cola.app.Timer()

	return context

def make_branches():
	args = cola.main.parse_args(["cola"])
	#context = cola.app.application_init(args)
	#cola.app.process_args(args)
	#context = cola.app.new_context(args)
	context = new_context(args)
	#context = cola.app.ApplicationContext(args)
	#context.git = cola.git.create()
	#context.model = cola.models.main.create(context)
	commit_editor = BranchesWidget(context, None)
	cola.app.initialize_view(context, commit_editor)
	#cola.app.default_start(context, commit_editor)
	#commit_editor.show()
	#context.app.start()
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
	branches_editor = make_branches()
	#status_editor = make_status()
	#print(context.model)
	view = run()
	#view.show()
	app1.exec_()
	print("here")
