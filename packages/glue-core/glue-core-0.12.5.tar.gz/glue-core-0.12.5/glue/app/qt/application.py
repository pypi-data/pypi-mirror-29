# pylint: disable=W0223

from __future__ import absolute_import, division, print_function

import os
import sys
import warnings
import webbrowser

from qtpy import QtCore, QtWidgets, QtGui, compat
from qtpy.QtCore import Qt

from glue.core.application_base import Application
from glue.core.message import ApplicationClosedMessage
from glue.core import command, Data
from glue.core.coordinates import WCSCoordinates
from glue import env
from glue.main import load_plugins
from glue.icons.qt import get_icon
from glue.utils.qt import get_qapp
from glue.app.qt.actions import action
from glue.dialogs.data_wizard.qt import data_wizard
from glue.dialogs.link_editor.qt import LinkEditor
from glue.app.qt.edit_subset_mode_toolbar import EditSubsetModeToolBar
from glue.app.qt.mdi_area import GlueMdiArea
from glue.app.qt.layer_tree_widget import PlotAction, LayerTreeWidget
from glue.app.qt.preferences import PreferencesDialog
from glue.viewers.common.qt.data_viewer import DataViewer
from glue.viewers.scatter.qt import ScatterViewer
from glue.viewers.image.qt import ImageViewer
from glue.utils import nonpartial, defer_draw
from glue.utils.qt import (pick_class, GlueTabBar, qurl_to_path,
                           set_cursor_cm, messagebox_on_error, load_ui)

from glue.app.qt.feedback import submit_bug_report, submit_feedback
from glue.app.qt.plugin_manager import QtPluginManager
from glue.app.qt.versions import QVersionsDialog
from glue.app.qt.terminal import glue_terminal, IPythonTerminalError
from glue.config import qt_fixed_layout_tab, qt_client, startup_action

__all__ = ['GlueApplication']
DOCS_URL = 'http://www.glueviz.org'


def _fix_ipython_pylab():

    try:
        from IPython import get_ipython
    except ImportError:
        return

    shell = get_ipython()

    if shell is None:
        return

    from IPython.core.error import UsageError

    # UnknownBackend exists only in IPython 5.0 and above, so if it doesn't
    # exist we just set UnknownBackend to be a fake exception class
    try:
        from IPython.terminal.pt_inputhooks import UnknownBackend
    except ImportError:
        class UnknownBackend(Exception):
            pass

    try:
        shell.enable_pylab('inline', import_all=True)
    except ValueError:
        # if the shell is a normal terminal shell, we get here
        pass
    except UnknownBackend:
        # if the shell is a normal terminal shell, we can also get here
        pass
    except UsageError:
        pass

    # Make sure we disable interactive mode (where figures get redrawn for
    # every single Matplotlib command)
    import matplotlib
    matplotlib.interactive(False)


class GlueLogger(QtWidgets.QWidget):

    """
    A window to display error messages
    """

    def __init__(self, button_console, parent=None):

        super(GlueLogger, self).__init__(parent)

        self.button_console = button_console
        self.button_stylesheet = button_console.styleSheet()

        self.button_console.clicked.connect(self._show)

        self._text = QtWidgets.QTextEdit()
        self._text.setTextInteractionFlags(Qt.TextSelectableByMouse)

        clear = QtWidgets.QPushButton("Clear")
        clear.clicked.connect(nonpartial(self._clear))

        report = QtWidgets.QPushButton("Send Bug Report")
        report.clicked.connect(nonpartial(self._send_report))

        if isinstance(sys.stderr, GlueLogger):
            if isinstance(sys.stderr._stderr_original, GlueLogger):
                raise Exception('Too many nested GlueLoggers')
            self._stderr_original = sys.stderr._stderr_original
        else:
            self._stderr_original = sys.stderr

        sys.stderr = self

        l = QtWidgets.QVBoxLayout()
        h = QtWidgets.QHBoxLayout()
        l.setContentsMargins(2, 2, 2, 2)
        l.setSpacing(2)
        h.setContentsMargins(0, 0, 0, 0)

        l.addWidget(self._text)
        h.insertStretch(0)
        h.addWidget(report)
        h.addWidget(clear)
        l.addLayout(h)

        self.setLayout(l)

    def _set_console_button(self, attention):
        if attention:
            self.button_console.setStyleSheet('color: red; text-decoration: underline;')
        else:
            self.button_console.setStyleSheet(self.button_stylesheet)

    def write(self, message):
        """
        Interface for sys.excepthook
        """
        self._stderr_original.write(message)
        self._text.moveCursor(QtGui.QTextCursor.End)
        self._text.insertPlainText(message)
        self._set_console_button(attention=True)

    def flush(self):
        """
        Interface for sys.excepthook
        """
        pass

    def _send_report(self):
        """
        Send the contents of the log as a bug report
        """
        text = self._text.document().toPlainText()
        submit_bug_report(text)

    def _clear(self):
        """
        Erase the log
        """
        self._text.setText('')
        self._set_console_button(attention=False)
        self.close()

    def _show(self):
        """
        Show the log
        """
        self.show()
        self.raise_()

    def keyPressEvent(self, event):
        """
        Hide window on escape key
        """
        if event.key() == Qt.Key_Escape:
            self.hide()

    def closeEvent(self, event):
        if sys.stderr is self:
            sys.stderr = self._stderr_original


class GlueApplication(Application, QtWidgets.QMainWindow):

    """ The main GUI application for the Qt frontend"""

    def __init__(self, data_collection=None, session=None):

        # At this point we need to check if a Qt application already exists -
        # this happens for example if using the %gui qt/qt5 mode in Jupyter. We
        # should keep a reference to the original icon so that we can restore it
        # later
        self._original_app = QtWidgets.QApplication.instance()
        if self._original_app is not None:
            self._original_icon = self._original_app.windowIcon()

        # Now we can get the application instance, which involves setting it
        # up if it doesn't already exist.
        self.app = get_qapp()

        QtWidgets.QMainWindow.__init__(self)
        Application.__init__(self, data_collection=data_collection,
                             session=session)

        icon = get_icon('app_icon')
        self.app.setWindowIcon(icon)

        # Even though we loaded the plugins in start_glue, we re-load them here
        # in case glue was started directly by initializing this class.
        load_plugins()

        self.setWindowTitle("Glue")
        self.setWindowIcon(icon)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._actions = {}
        self._terminal = None
        self._setup_ui()
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)

        # The following is a counter that never goes down, even if tabs are
        # deleted (this is by design, to avoid having two tabs called the
        # same if a tab is removed then a new one added again)
        self._total_tab_count = 0

        lwidget = self._layer_widget
        a = PlotAction(lwidget, self)
        lwidget.ui.layerTree.addAction(a)
        lwidget.bind_selection_to_edit_subset()

        self._tweak_geometry()
        self._create_actions()
        self._create_menu()
        self._connect()
        self.new_tab()
        self._update_plot_dashboard(None)

    def run_startup_action(self, name):
        if name in startup_action.members:
            startup_action.members[name](self.session, self.data_collection)
        else:
            raise Exception("Unknown startup action: {0}".format(name))

    def _setup_ui(self):
        self._ui = load_ui('application.ui', None,
                           directory=os.path.dirname(__file__))
        self.setCentralWidget(self._ui)
        self._ui.tabWidget.setTabBar(GlueTabBar())

        lw = LayerTreeWidget()
        lw.set_checkable(False)
        self._vb = QtWidgets.QVBoxLayout()
        self._vb.setContentsMargins(0, 0, 0, 0)
        self._vb.addWidget(lw)
        self._ui.data_layers.setLayout(self._vb)
        self._layer_widget = lw

        # Data toolbar

        self._data_toolbar = QtWidgets.QToolBar()

        self._data_toolbar.setIconSize(QtCore.QSize(16, 16))

        self._button_open_data = QtWidgets.QToolButton()
        self._button_open_data.setText("Open Data")
        self._button_open_data.setIcon(get_icon('glue_open'))
        self._button_open_data.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self._button_open_data.clicked.connect(nonpartial(self._choose_load_data))

        self._data_toolbar.addWidget(self._button_open_data)

        self._button_link_data = QtWidgets.QToolButton()
        self._button_link_data.setText("Link Data")
        self._button_link_data.setIcon(get_icon('glue_link'))
        self._button_link_data.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self._button_link_data.clicked.connect(self._set_up_links)

        self._data_toolbar.addWidget(self._button_link_data)

        self._button_ipython = QtWidgets.QToolButton()
        self._button_ipython.setCheckable(True)
        self._button_ipython.setText("IPython Terminal")
        self._button_ipython.setIcon(get_icon('IPythonConsole'))
        self._button_ipython.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self._button_ipython.clicked.connect(self._toggle_terminal)

        self._data_toolbar.addWidget(self._button_ipython)

        self._button_open_data = QtWidgets.QToolButton()
        self._button_open_data.setText("Open Session")
        self._button_open_data.setIcon(get_icon('glue_open'))
        self._button_open_data.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self._button_open_data.clicked.connect(nonpartial(self._restore_session))

        self._data_toolbar.addWidget(self._button_open_data)

        self._button_open_data = QtWidgets.QToolButton()
        self._button_open_data.setText("Save Session")
        self._button_open_data.setIcon(get_icon('glue_filesave'))
        self._button_open_data.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self._button_open_data.clicked.connect(nonpartial(self._choose_save_session))

        self._data_toolbar.addWidget(self._button_open_data)

        spacer = QtWidgets.QWidget()
        spacer.setMinimumSize(20, 10)
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                             QtWidgets.QSizePolicy.Preferred)

        self._data_toolbar.addWidget(spacer)

        self.addToolBar(self._data_toolbar)

        # Selection mode toolbar

        tbar = EditSubsetModeToolBar()
        self._mode_toolbar = tbar

        self.addToolBar(self._mode_toolbar)

        # Error console toolbar

        self._console_toolbar = QtWidgets.QToolBar()

        self._console_toolbar.setIconSize(QtCore.QSize(16, 16))

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Preferred)

        self._console_toolbar.addWidget(spacer)

        self._button_preferences = QtWidgets.QToolButton()
        self._button_preferences.setText("Preferences")
        self._button_preferences.setIcon(get_icon('glue_settings'))
        self._button_preferences.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self._button_preferences.clicked.connect(nonpartial(self._edit_settings))

        self._console_toolbar.addWidget(self._button_preferences)

        self._button_console = QtWidgets.QToolButton()
        self._button_console.setText("View Error Console")
        self._button_console.setToolButtonStyle(Qt.ToolButtonTextOnly)

        self._console_toolbar.addWidget(self._button_console)

        self.addToolBar(self._console_toolbar)

        self._log = GlueLogger(button_console=self._button_console)
        self._log.window().setWindowTitle("Console Log")
        self._log.resize(550, 550)
        self._log.hide()

    def _set_up_links(self, event):
        LinkEditor.update_links(self.data_collection)

    def _tweak_geometry(self):
        """Maximize window by default."""
        self._ui.main_splitter.setStretchFactor(0, 0.1)
        self._ui.main_splitter.setStretchFactor(1, 0.9)
        self._ui.data_plot_splitter.setStretchFactor(0, 0.25)
        self._ui.data_plot_splitter.setStretchFactor(1, 0.5)
        self._ui.data_plot_splitter.setStretchFactor(2, 0.25)

    @property
    def tab_widget(self):
        return self._ui.tabWidget

    @property
    def tab_bar(self):
        return self._ui.tabWidget.tabBar()

    @property
    def tab_count(self):
        """
        The number of open tabs
        """
        return self._ui.tabWidget.count()

    @property
    def current_tab(self):
        return self._ui.tabWidget.currentWidget()

    def get_tab_index(self, widget):
        for idx in range(self.tab_count):
            if self.tab(idx) == widget:
                return idx
        raise Exception("Tab not found")

    def tab(self, index=None):
        if index is None:
            return self.current_tab
        return self._ui.tabWidget.widget(index)

    def new_tab(self):
        """Spawn a new tab page"""
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)
        widget = GlueMdiArea(self)
        widget.setLayout(layout)
        tab = self.tab_widget
        self._total_tab_count += 1
        tab.addTab(widget, str("Tab %i" % self._total_tab_count))
        tab.setCurrentWidget(widget)
        widget.subWindowActivated.connect(self._update_plot_dashboard)

    def close_tab(self, index, warn=True):
        """ Close a tab window and all associated data viewers """

        # do not delete the last tab
        if self.tab_widget.count() == 1:
            return

        if warn and not os.environ.get('GLUE_TESTING'):
            buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            dialog = QtWidgets.QMessageBox.warning(
                self, "Confirm Close",
                "Are you sure you want to close this tab? "
                "This will close all data viewers in the tab.",
                buttons=buttons, defaultButton=QtWidgets.QMessageBox.Cancel)
            if not dialog == QtWidgets.QMessageBox.Ok:
                return

        w = self.tab_widget.widget(index)

        for window in w.subWindowList():
            widget = window.widget()
            if isinstance(widget, DataViewer):
                widget.close(warn=False)

        w.close()

        self.tab_widget.removeTab(index)

    def add_widget(self, new_widget, label=None, tab=None,
                   hold_position=False):
        """
        Add a widget to one of the tabs.

        Returns the window that this widget is wrapped in.

        :param new_widget: new QtWidgets.QWidget to add

        :param label: label for the new window. Optional
        :type label: str

        :param tab: Tab to add to. Optional (default: current tab)
        :type tab: int

        :param hold_position: If True, then override Qt's default
                              placement and retain the original position
                              of new_widget
        :type hold_position: bool
        """

        # Find first tab that supports addSubWindow
        if tab is None:
            if hasattr(self.current_tab, 'addSubWindow'):
                pass
            else:
                for tab in range(self.tab_count):
                    page = self.tab(tab)
                    if hasattr(page, 'addSubWindow'):
                        break
                else:
                    self.new_tab()
                    tab = self.tab_count - 1

        page = self.tab(tab)
        pos = getattr(new_widget, 'position', None)
        sub = new_widget.mdi_wrap()

        sub.closed.connect(self._clear_dashboard)

        if label:
            sub.setWindowTitle(label)
        page.addSubWindow(sub)
        page.setActiveSubWindow(sub)
        if hold_position and pos is not None:
            new_widget.move(pos[0], pos[1])

        self.tab_widget.setCurrentWidget(page)

        return sub

    def _edit_settings(self):
        self._editor = PreferencesDialog(self, parent=self)
        self._editor.show()

    def gather_current_tab(self):
        """Arrange windows in current tab via tiling"""
        self.current_tab.tileSubWindows()

    def _get_plot_dashboards(self, sub_window):

        widget = sub_window.widget()

        if not isinstance(widget, DataViewer):
            return QtWidgets.QWidget(), QtWidgets.QWidget(), ""

        layer_view = widget.layer_view()
        options_widget = widget.options_widget()

        return layer_view, options_widget, str(widget)

    def _clear_dashboard(self):

        for widget, title in [(self._ui.plot_layers, "Plot Layers"),
                              (self._ui.plot_options, "Plot Options")]:
            layout = widget.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout()
                layout.setContentsMargins(4, 4, 4, 4)
                widget.setLayout(layout)
            while layout.count():
                layout.takeAt(0).widget().hide()

        self._ui.plot_options_label.setText("Plot Options")
        self._ui.plot_layers_label.setText("Plot Layers")

    def _update_plot_dashboard(self, sub_window):
        self._clear_dashboard()

        if sub_window is None:
            return

        layer_view, options_widget, title = self._get_plot_dashboards(
            sub_window)

        layout = self._ui.plot_layers.layout()
        layout.addWidget(layer_view)

        layout = self._ui.plot_options.layout()
        layout.addWidget(options_widget)

        layer_view.show()
        options_widget.show()

        if title:
            self._ui.plot_options_label.setText("Plot Options - %s" % title)
            self._ui.plot_layers_label.setText("Plot Layers - %s" % title)
        else:
            self._ui.plot_options_label.setText("Plot Options")
            self._ui.plot_layers_label.setText("Plot Layers")

        self._update_focus_decoration()

    def _update_focus_decoration(self):
        mdi_area = self.current_tab
        active = mdi_area.activeSubWindow()

        for win in mdi_area.subWindowList():
            widget = win.widget()
            if isinstance(widget, DataViewer):
                widget.set_focus(win is active)

    def _connect(self):
        self.setAcceptDrops(True)
        self._layer_widget.setup(self._data)

        self.tab_widget.tabCloseRequested.connect(self.close_tab)

    def _create_menu(self):
        mbar = self.menuBar()
        menu = QtWidgets.QMenu(mbar)
        menu.setTitle("&File")

        menu.addAction(self._actions['data_new'])
        if 'data_importers' in self._actions:
            submenu = menu.addMenu("I&mport data")
            for a in self._actions['data_importers']:
                submenu.addAction(a)
        # menu.addAction(self._actions['data_save'])  # XXX add this
        menu.addAction(self._actions['session_reset'])
        menu.addAction(self._actions['session_restore'])
        menu.addAction(self._actions['session_save'])
        if 'session_export' in self._actions:
            submenu = menu.addMenu("E&xport")
            for a in self._actions['session_export']:
                submenu.addAction(a)
        menu.addSeparator()
        menu.addAction("Edit &Preferences", self._edit_settings)
        # Here we use close instead of self.app.quit because if we are launching
        # glue from an environment with a Qt event loop already existing, we
        # don't want to quit this. Using close here is safer, though it does
        # mean that any dialog we launch from glue has to be either modal (to
        # prevent quitting) or correctly define its parent so that it gets
        # closed too.
        menu.addAction("&Quit", self.close)
        mbar.addMenu(menu)

        menu = QtWidgets.QMenu(mbar)
        menu.setTitle("&Edit ")
        menu.addAction(self._actions['undo'])
        menu.addAction(self._actions['redo'])
        mbar.addMenu(menu)

        menu = QtWidgets.QMenu(mbar)
        menu.setTitle("&View ")

        a = QtWidgets.QAction("&Console Log", menu)
        a.triggered.connect(self._log._show)
        menu.addAction(a)
        mbar.addMenu(menu)

        menu = QtWidgets.QMenu(mbar)
        menu.setTitle("&Canvas")
        menu.addAction(self._actions['tab_new'])
        menu.addAction(self._actions['viewer_new'])
        menu.addAction(self._actions['fixed_layout_tab_new'])
        menu.addSeparator()
        menu.addAction(self._actions['gather'])
        menu.addAction(self._actions['tab_rename'])
        mbar.addMenu(menu)

        menu = QtWidgets.QMenu(mbar)
        menu.setTitle("Data &Manager")
        menu.addActions(self._layer_widget.actions())

        mbar.addMenu(menu)

        menu = QtWidgets.QMenu(mbar)
        menu.setTitle("&Plugins")
        menu.addAction(self._actions['plugin_manager'])
        menu.addSeparator()

        if 'plugins' in self._actions:
            for plugin in self._actions['plugins']:
                menu.addAction(plugin)

        mbar.addMenu(menu)

        # trigger inclusion of Mac Native "Help" tool
        menu = mbar.addMenu("&Help")

        a = QtWidgets.QAction("&Online Documentation", menu)
        a.triggered.connect(nonpartial(webbrowser.open, DOCS_URL))
        menu.addAction(a)

        a = QtWidgets.QAction("Send &Feedback", menu)
        a.triggered.connect(nonpartial(submit_feedback))
        menu.addAction(a)

        menu.addSeparator()
        menu.addAction("Version information", self._show_glue_info)

    def _show_glue_info(self):
        window = QVersionsDialog(parent=self)
        window.show()
        window.exec_()

    def _choose_load_data(self, data_importer=None):
        if data_importer is None:
            self.add_datasets(self.data_collection, data_wizard())
        else:
            data = data_importer()
            if not isinstance(data, list):
                raise TypeError("Data loader should return list of "
                                "Data objects")
            for item in data:
                if not isinstance(item, Data):
                    raise TypeError("Data loader should return list of "
                                    "Data objects")
            self.add_datasets(self.data_collection, data)

    def _create_actions(self):
        """ Create and connect actions, store in _actions dict """
        self._actions = {}

        a = action("&New Data Viewer", self,
                   tip="Open a new visualization window in the current tab",
                   shortcut=QtGui.QKeySequence.New)
        a.triggered.connect(nonpartial(self.choose_new_data_viewer))
        self._actions['viewer_new'] = a

        if len(qt_client.members) == 0:
            a.setEnabled(False)

        a = action("New Fixed Layout Tab", self,
                   tip="Create a new tab with a fixed layout")
        a.triggered.connect(nonpartial(self.choose_new_fixed_layout_tab))
        self._actions['fixed_layout_tab_new'] = a

        if len(qt_fixed_layout_tab.members) == 0:
            a.setEnabled(False)

        a = action('New &Tab', self,
                   shortcut=QtGui.QKeySequence.AddTab,
                   tip='Add a new tab')
        a.triggered.connect(nonpartial(self.new_tab))
        self._actions['tab_new'] = a

        a = action('&Rename Tab', self,
                   shortcut="Ctrl+R",
                   tip='Set a new label for the current tab')
        a.triggered.connect(nonpartial(self.tab_bar.choose_rename_tab))
        self._actions['tab_rename'] = a

        a = action('&Gather Windows', self,
                   tip='Gather plot windows side-by-side',
                   shortcut='Ctrl+G')
        a.triggered.connect(nonpartial(self.gather_current_tab))
        self._actions['gather'] = a

        a = action('&Save Session', self,
                   tip='Save the current session')
        a.triggered.connect(nonpartial(self._choose_save_session))
        self._actions['session_save'] = a

        # Add file loader as first item in File menu for convenience. We then
        # also add it again below in the Import menu for consistency.
        a = action("&Open Data Set", self, tip="Open a new data set",
                   shortcut=QtGui.QKeySequence.Open)
        a.triggered.connect(nonpartial(self._choose_load_data,
                                       data_wizard))
        self._actions['data_new'] = a

        # We now populate the "Import data" menu
        from glue.config import importer

        acts = []

        # Add default file loader (later we can add this to the registry)
        a = action("Import from file", self, tip="Import from file")
        a.triggered.connect(nonpartial(self._choose_load_data,
                                       data_wizard))
        acts.append(a)

        for i in importer:
            label, data_importer = i
            a = action(label, self, tip=label)
            a.triggered.connect(nonpartial(self._choose_load_data,
                                           data_importer))
            acts.append(a)

        self._actions['data_importers'] = acts

        from glue.config import exporters
        if len(exporters) > 0:
            acts = []
            for e in exporters:
                label, saver, checker, mode = e
                a = action(label, self,
                           tip='Export the current session to %s format' %
                           label)
                a.triggered.connect(nonpartial(self._choose_export_session,
                                               saver, checker, mode))
                acts.append(a)

            self._actions['session_export'] = acts

        a = action('Open S&ession', self,
                   tip='Restore a saved session')
        a.triggered.connect(nonpartial(self._restore_session))
        self._actions['session_restore'] = a

        a = action('Reset S&ession', self,
                   tip='Reset session to clean state')
        a.triggered.connect(nonpartial(self._reset_session))
        self._actions['session_reset'] = a

        a = action("Undo", self,
                   tip='Undo last action',
                   shortcut=QtGui.QKeySequence.Undo)
        a.triggered.connect(nonpartial(self.undo))
        a.setEnabled(False)
        self._actions['undo'] = a

        a = action("Redo", self,
                   tip='Redo last action',
                   shortcut=QtGui.QKeySequence.Redo)
        a.triggered.connect(nonpartial(self.redo))
        a.setEnabled(False)
        self._actions['redo'] = a

        # Create actions for menubar plugins
        from glue.config import menubar_plugin
        acts = []
        for label, function in menubar_plugin:
            a = action(label, self, tip=label)
            a.triggered.connect(nonpartial(function,
                                           self.session,
                                           self.data_collection))
            acts.append(a)
        self._actions['plugins'] = acts

        a = action('&Plugin Manager', self,
                   tip='Open plugin manager')
        a.triggered.connect(nonpartial(self.plugin_manager))
        self._actions['plugin_manager'] = a

    def choose_new_fixed_layout_tab(self):
        """
        Creates a new tab with a fixed layout
        """

        tab_cls = pick_class(list(qt_fixed_layout_tab.members), title='Fixed layout tab',
                             label="Choose a new fixed layout tab",
                             sort=True)

        return self.add_fixed_layout_tab(tab_cls)

    def add_fixed_layout_tab(self, tab_cls):

        tab = tab_cls(session=self.session)

        self._total_tab_count += 1

        name = 'Tab {0}'.format(self._total_tab_count)
        if hasattr(tab, 'LABEL'):
            name += ': ' + tab.LABEL
        self.tab_widget.addTab(tab, name)
        self.tab_widget.setCurrentWidget(tab)
        tab.subWindowActivated.connect(self._update_plot_dashboard)

        return tab

    def choose_new_data_viewer(self, data=None):
        """ Create a new visualization window in the current tab
        """

        if data and data.ndim == 1 and ScatterViewer in qt_client.members:
            default = ScatterViewer
        elif data and data.ndim > 1 and ImageViewer in qt_client.members:
            default = ImageViewer
        else:
            default = None

        client = pick_class(list(qt_client.members), title='Data Viewer',
                            label="Choose a new data viewer",
                            default=default, sort=True)

        if client is None:
            return

        cmd = command.NewDataViewer(viewer=client, data=data)
        return self.do(cmd)

    new_data_viewer = defer_draw(Application.new_data_viewer)

    def _choose_save_session(self):
        """ Save the data collection and hub to file.

        Can be restored via restore_session
        """

        # include file filter twice, so it shows up in Dialog
        outfile, file_filter = compat.getsavefilename(
            parent=self, filters=("Glue Session (*.glu);; "
                                  "Glue Session including data (*.glu)"))

        # This indicates that the user cancelled
        if not outfile:
            return

        # Add extension if not specified
        if '.' not in outfile:
            outfile += '.glu'

        with set_cursor_cm(Qt.WaitCursor):
            self.save_session(
                outfile, include_data="including data" in file_filter)

    @messagebox_on_error("Failed to export session")
    def _choose_export_session(self, saver, checker, outmode):
        checker(self)
        if outmode is None:
            return saver(self)
        elif outmode in ['file', 'directory']:
            outfile, file_filter = compat.getsavefilename(parent=self)
            if not outfile:
                return
            return saver(self, outfile)
        else:
            assert outmode == 'label'
            label, ok = QtWidgets.QInputDialog.getText(self, 'Choose a label:',
                                                       'Choose a label:')
            if not ok:
                return
            return saver(self, label)

    @messagebox_on_error("Failed to restore session")
    def _restore_session(self, show=True):
        """ Load a previously-saved state, and restart the session """
        fltr = "Glue sessions (*.glu)"
        file_name, file_filter = compat.getopenfilename(
            parent=self, filters=fltr)
        if not file_name:
            return

        ga = self.restore_session_and_close(file_name)
        return ga

    @property
    def is_empty(self):
        """
        Returns `True` if there are no viewers and no data.
        """
        return (len([viewer for tab in self.viewers for viewer in tab]) == 0 and
                len(self.data_collection) == 0)

    def _reset_session(self, show=True, warn=True):
        """
        Reset session to clean state.
        """

        if not os.environ.get('GLUE_TESTING') and warn and not self.is_empty:
            buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            dialog = QtWidgets.QMessageBox.warning(
                self, "Confirm Close",
                "Are you sure you want to reset the session? "
                "This will close all datasets, subsets, and data viewers",
                buttons=buttons, defaultButton=QtWidgets.QMessageBox.Cancel)
            if not dialog == QtWidgets.QMessageBox.Ok:
                return

        # Make sure the closeEvent gets executed to close the GlueLogger
        self._log.close()
        self.app.processEvents()

        ga = GlueApplication()
        ga.start(block=False)

        # We need to close this after we open the next application otherwise
        # Qt will quit since there are no actively open windows.
        self.close()

        return ga

    @staticmethod
    def restore_session(path, show=True):
        """
        Reload a previously-saved session

        Parameters
        ----------
        path : str
            Path to the file to load
        show : bool, optional
            If True (the default), immediately show the widget

        Returns
        -------
        app : :class:`glue.app.qt.application.GlueApplication`
            The loaded application
        """
        ga = Application.restore_session(path)
        if show:
            ga.start(block=False)
        return ga

    def has_terminal(self, create_if_not=True):
        """
        Returns True if the IPython terminal is present.
        """
        if self._terminal is None and create_if_not:
            self._create_terminal()
        return self._terminal is not None

    def _create_terminal(self):

        if self._terminal is not None:  # already set up
            return

        try:
            widget = glue_terminal(data_collection=self._data,
                                   dc=self._data,
                                   hub=self._hub,
                                   session=self.session,
                                   application=self,
                                   **vars(env))
        except IPythonTerminalError:
            self._button_ipython.setEnabled(False)
        else:
            self._terminal = self.add_widget(widget)
            self._terminal.closed.connect(self._on_terminal_close)
            self._hide_terminal()

    def _toggle_terminal(self):
        if self._terminal is None:
            self._create_terminal()
        if self._terminal.isVisible():
            self._hide_terminal()
            if self._terminal.isVisible():
                warnings.warn("An unexpected error occurred while "
                              "trying to hide the terminal")
        else:
            self._show_terminal()
            if not self._terminal.isVisible():
                warnings.warn("An unexpected error occurred while "
                              "trying to show the terminal")

    def _on_terminal_close(self):
        if self._button_ipython.isChecked():
            self._button_ipython.blockSignals(True)
            self._button_ipython.setChecked(False)
            self._button_ipython.blockSignals(False)

    def _hide_terminal(self):
        self._terminal.hide()

    def _show_terminal(self):
        self._terminal.show()
        self._terminal.widget().show()

    def start(self, size=None, position=None, block=True, maximized=True):
        """
        Show the GUI and start the application.

        Parameters
        ----------
        size : (int, int) Optional
            The default width/height of the application.
            If not provided, uses the full screen
        position : (int, int) Optional
            The default position of the application
        """
        if maximized:
            self.showMaximized()
        else:
            self.show()
        if size is not None:
            self.resize(*size)
        if position is not None:
            self.move(*position)

        self.raise_()  # bring window to front

        # at some point during all this, the MPL backend
        # switches. This call restores things, so
        # figures are still inlined in the notebook.
        # XXX find out a better place for this
        _fix_ipython_pylab()

        if block:
            return self.app.exec_()

    exec_ = start

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    @messagebox_on_error("Failed to load files")
    def dropEvent(self, event):

        urls = event.mimeData().urls()

        paths = [qurl_to_path(url) for url in urls]

        if any(path.endswith('.glu') for path in paths):
            if len(paths) != 1:
                raise Exception("When dragging and dropping files onto glue, "
                                "only a single .glu session file can be "
                                "dropped at a time, or multiple datasets, but "
                                "not a mix of both.")
            else:
                self.restore_session_and_close(paths[0])
        else:
            self.load_data(paths)

        event.accept()

    @messagebox_on_error("Failed to restore session")
    def restore_session_and_close(self, path, warn=True):

        if warn and not self.is_empty:
            buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            dialog = QtWidgets.QMessageBox.warning(
                self, "Confirm Close",
                "Loading a session file will close the existing session. Are you "
                "sure you want to continue?",
                buttons=buttons, defaultButton=QtWidgets.QMessageBox.Cancel)
            if not dialog == QtWidgets.QMessageBox.Ok:
                return

        with set_cursor_cm(Qt.WaitCursor):
            app = self.restore_session(path)
            app.setGeometry(self.geometry())
            self.close()

    def closeEvent(self, event):
        """Emit a message to hub before closing."""
        for tab in self.viewers:
            for viewer in tab:
                viewer.close(warn=False)
        self._log.close()
        self._hub.broadcast(ApplicationClosedMessage(None))
        event.accept()
        if self._original_app is not None:
            self._original_app.setWindowIcon(self._original_icon)

    def report_error(self, message, detail):
        """
        Display an error in a modal

        :param message: A short description of the error
        :type message: str
        :param detail: A longer description
        :type detail: str
        """
        qmb = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Error", message)
        qmb.setDetailedText(detail)
        qmb.resize(400, qmb.size().height())
        qmb.exec_()

    def plugin_manager(self):
        from glue.main import _installed_plugins
        pm = QtPluginManager(installed=_installed_plugins)
        pm.ui.exec_()

    def _update_undo_redo_enabled(self):
        undo, redo = self._cmds.can_undo_redo()
        self._actions['undo'].setEnabled(undo)
        self._actions['redo'].setEnabled(redo)
        self._actions['undo'].setText('Undo ' + self._cmds.undo_label)
        self._actions['redo'].setText('Redo ' + self._cmds.redo_label)

    @property
    def viewers(self):
        """
        A list of lists of open Data Viewers.

        Each inner list contains the viewers open on a particular tab.
        """
        result = []
        for t in range(self.tab_count):
            tab = self.tab(t)
            item = []
            for subwindow in tab.subWindowList():
                widget = subwindow.widget()
                if isinstance(widget, DataViewer):
                    item.append(widget)
            result.append(tuple(item))
        return tuple(result)

    @property
    def tab_names(self):
        """
        The name of each tab

        A list of strings
        """
        return [self.tab_bar.tabText(i) for i in range(self.tab_count)]

    @tab_names.setter
    def tab_names(self, values):
        for index, value in enumerate(values):
            self.tab_bar.setTabText(index, value)

    @staticmethod
    def _choose_merge(data, others):

        w = load_ui('merge.ui', None, directory=os.path.dirname(__file__))
        w.button_yes.clicked.connect(w.accept)
        w.button_no.clicked.connect(w.reject)
        w.show()
        w.raise_()

        # Add the main dataset to the list. Some of the 'others' may also be
        # new ones, so it doesn't really make sense to distinguish between
        # the two here. The main point is that some datasets, including at
        # least one new one, have a common shape.
        others.append(data)
        others.sort(key=lambda x: x.label)
        for i, d in enumerate(others):
            if isinstance(d.coords, WCSCoordinates):
                if i == 0:
                    break
                else:
                    others[0], others[i] = others[i], others[0]
                    break

        label = others[0].label
        w.merged_label.setText(label)

        entries = [QtWidgets.QListWidgetItem(other.label) for other in others]
        for e in entries:
            e.setCheckState(Qt.Checked)

        for d, item in zip(others, entries):
            w.choices.addItem(item)

        if not w.exec_():
            return None, None

        result = [layer for layer, entry in zip(others, entries)
                  if entry.checkState() == Qt.Checked]

        if result:
            return result, str(w.merged_label.text())

        return None, None

    def __gluestate__(self, context):
        state = super(GlueApplication, self).__gluestate__(context)
        state['tab_names'] = self.tab_names
        return state

    @classmethod
    def __setgluestate__(cls, rec, context):
        self = super(GlueApplication, cls).__setgluestate__(rec, context)
        if 'tab_names' in rec:
            self.tab_names = rec['tab_names']
        return self
