"""
Contains the main Window definition for Mu's UI.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import logging
import os.path
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import (QToolBar, QAction, QDesktopWidget, QWidget,
                             QVBoxLayout, QTabWidget, QFileDialog, QMessageBox,
                             QLabel, QMainWindow, QStatusBar, QDockWidget,
                             QShortcut)
from PyQt5.QtGui import QKeySequence, QStandardItemModel, QStandardItem
from mu import __version__
from mu.interface.dialogs import LogDisplay, ModeSelector
from mu.interface.themes import (DayTheme, NightTheme, ContrastTheme,
                                 DEFAULT_FONT_SIZE, DAY_STYLE, NIGHT_STYLE,
                                 CONTRAST_STYLE)
from mu.interface.panes import (DebugInspector, PythonProcessPane,
                                JupyterREPLPane, MicroPythonREPLPane,
                                FileSystemPane)
from mu.interface.editor import EditorPane
from mu.resources import load_icon, load_pixmap


logger = logging.getLogger(__name__)


class ButtonBar(QToolBar):
    """
    Represents the bar of buttons across the top of the editor and defines
    their behaviour.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setMovable(False)
        self.setIconSize(QSize(64, 64))
        self.setToolButtonStyle(3)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setObjectName("StandardToolBar")
        self.reset()

    def reset(self):
        """
        Resets the button states.
        """
        self.slots = {}
        self.clear()

    def change_mode(self, mode):
        self.reset()
        self.addAction(name="new", display_name=_("New"),
                       tool_text=_("Create a new Python script."))
        self.addAction(name="load", display_name=_("Load"),
                       tool_text=_("Load a Python script."))
        self.addAction(name="save", display_name=_("Save"),
                       tool_text=_("Save the current Python script."))
        self.addSeparator()

        for action in mode.actions():
            self.addAction(name=action['name'],
                           display_name=action['display_name'],
                           tool_text=action['description'])

        self.addSeparator()
        self.addAction(name="zoom-in", display_name=_('Zoom-in'),
                       tool_text=_("Zoom in (to make the text bigger)."))
        self.addAction(name="zoom-out", display_name=_('Zoom-out'),
                       tool_text=_("Zoom out (to make the text smaller)."))
        self.addAction(name="theme", display_name=_('Theme'),
                       tool_text=_("Toggle theme between day, night or "
                                   "high contrast."))
        self.addSeparator()
        self.addAction(name="check", display_name=_('Check'),
                       tool_text=_("Check your code for mistakes."))
        self.addAction(name="help", display_name=_('Help'),
                       tool_text=_("Show help about Mu in a browser."))
        self.addAction(name="quit", display_name=_('Quit'),
                       tool_text=_("Quit Mu."))

    def set_responsive_mode(self, width, height):
        """
        Compact button bar for when window is very small.
        """
        font_size = DEFAULT_FONT_SIZE
        if width < 940 and height > 600:
            self.setIconSize(QSize(48, 48))
        elif height < 600 and width < 940:
            font_size = 10
            self.setIconSize(QSize(32, 32))
        else:
            self.setIconSize(QSize(64, 64))
        stylesheet = "QWidget{font-size: " + str(font_size) + "px;}"
        self.setStyleSheet(stylesheet)

    def addAction(self, name, display_name, tool_text):
        """
        Creates an action associated with an icon and name and adds it to the
        widget's slots.
        """
        action = QAction(load_icon(name), display_name, self,
                         toolTip=tool_text)
        super().addAction(action)
        self.slots[name] = action

    def connect(self, name, handler, shortcut=None):
        """
        Connects a named slot to a handler function and optional hot-key
        shortcuts.
        """
        self.slots[name].pyqtConfigure(triggered=handler)
        if shortcut:
            self.slots[name].setShortcut(QKeySequence(shortcut))


class FileTabs(QTabWidget):
    """
    Extend the base class so we can override the removeTab behaviour.
    """

    def __init__(self):
        super(FileTabs, self).__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)
        self.currentChanged.connect(self.change_tab)

    def removeTab(self, tab_id):
        """
        Ask the user before closing the file.
        """
        window = self.nativeParentWidget()
        modified = window.current_tab.isModified()
        if modified:
            msg = ('There is un-saved work, closing the tab will cause you '
                   'to lose it.')
            if window.show_confirmation(msg) == QMessageBox.Cancel:
                return
        super(FileTabs, self).removeTab(tab_id)

    def change_tab(self, tab_id):
        """
        Update the application title to reflect the name of the file in the
        currently selected tab.
        """
        current_tab = self.widget(tab_id)
        window = self.nativeParentWidget()
        if current_tab:
            window.update_title(current_tab.label)
        else:
            window.update_title(None)


class Window(QMainWindow):
    """
    Defines the look and characteristics of the application's main window.
    """

    title = _("Mu {}").format(__version__)
    icon = "icon"
    timer = None
    usb_checker = None

    _zoom_in = pyqtSignal(int)
    _zoom_out = pyqtSignal(int)

    def zoom_in(self):
        """
        Handles zooming in.
        """
        self._zoom_in.emit(2)

    def zoom_out(self):
        """
        Handles zooming out.
        """
        self._zoom_out.emit(2)

    def connect_zoom(self, widget):
        """
        Connects a referenced widget to the zoom related signals.
        """
        self._zoom_in.connect(widget.zoomIn)
        self._zoom_out.connect(widget.zoomOut)

    @property
    def current_tab(self):
        """
        Returns the currently focussed tab.
        """
        return self.tabs.currentWidget()

    def set_read_only(self, is_readonly):
        """
        Set all tabs read-only.
        """
        self.read_only_tabs = is_readonly
        for tab in self.widgets:
            tab.setReadOnly(is_readonly)

    def get_load_path(self, folder):
        """
        Displays a dialog for selecting a file to load. Returns the selected
        path. Defaults to start in the referenced folder.
        """
        path, _ = QFileDialog.getOpenFileName(self.widget, 'Open file', folder,
                                              '*.py *.PY *.hex')
        logger.debug('Getting load path: {}'.format(path))
        return path

    def get_save_path(self, folder):
        """
        Displays a dialog for selecting a file to save. Returns the selected
        path. Defaults to start in the referenced folder.
        """
        path, _ = QFileDialog.getSaveFileName(self.widget, 'Save file', folder)
        logger.debug('Getting save path: {}'.format(path))
        return path

    def get_microbit_path(self, folder):
        """
        Displays a dialog for locating the location of the BBC micro:bit in the
        host computer's filesystem. Returns the selected path. Defaults to
        start in the referenced folder.
        """
        path = QFileDialog.getExistingDirectory(self.widget,
                                                'Locate BBC micro:bit', folder,
                                                QFileDialog.ShowDirsOnly)
        logger.debug('Getting micro:bit path: {}'.format(path))
        return path

    def add_tab(self, path, text, api):
        """
        Adds a tab with the referenced path and text to the editor.
        """
        new_tab = EditorPane(path, text)
        new_tab.connect_margin(self.breakpoint_toggle)
        new_tab_index = self.tabs.addTab(new_tab, new_tab.label)
        new_tab.set_api(api)

        @new_tab.modificationChanged.connect
        def on_modified():
            modified_tab_index = self.tabs.currentIndex()
            self.tabs.setTabText(modified_tab_index, new_tab.label)
            self.update_title(new_tab.label)

        self.tabs.setCurrentIndex(new_tab_index)
        self.connect_zoom(new_tab)
        self.set_theme(self.theme)
        new_tab.setFocus()
        if self.read_only_tabs:
            new_tab.setReadOnly(self.read_only_tabs)

    def focus_tab(self, tab):
        index = self.tabs.indexOf(tab)
        self.tabs.setCurrentIndex(index)
        tab.setFocus()

    @property
    def tab_count(self):
        """
        Returns the number of active tabs.
        """
        return self.tabs.count()

    @property
    def widgets(self):
        """
        Returns a list of references to the widgets representing tabs in the
        editor.
        """
        return [self.tabs.widget(i) for i in range(self.tab_count)]

    @property
    def modified(self):
        """
        Returns a boolean indication if there are any modified tabs in the
        editor.
        """
        for widget in self.widgets:
            if widget.isModified():
                return True
        return False

    def add_filesystem(self, home, file_manager):
        """
        Adds the file system pane to the application.
        """
        self.fs_pane = FileSystemPane(home)
        self.fs = QDockWidget(_('Filesystem on micro:bit'))
        self.fs.setWidget(self.fs_pane)
        self.fs.setFeatures(QDockWidget.DockWidgetMovable)
        self.fs.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.fs)
        self.fs_pane.setFocus()
        file_manager.on_list_files.connect(self.fs_pane.on_ls)
        self.fs_pane.list_files.connect(file_manager.ls)
        self.fs_pane.microbit_fs.put.connect(file_manager.put)
        self.fs_pane.microbit_fs.delete.connect(file_manager.delete)
        self.fs_pane.microbit_fs.list_files.connect(file_manager.ls)
        self.fs_pane.local_fs.get.connect(file_manager.get)
        self.fs_pane.local_fs.list_files.connect(file_manager.ls)
        file_manager.on_put_file.connect(self.fs_pane.microbit_fs.on_put)
        file_manager.on_delete_file.connect(self.fs_pane.microbit_fs.on_delete)
        file_manager.on_get_file.connect(self.fs_pane.local_fs.on_get)
        file_manager.on_list_fail.connect(self.fs_pane.on_ls_fail)
        file_manager.on_put_fail.connect(self.fs_pane.on_put_fail)
        file_manager.on_delete_fail.connect(self.fs_pane.on_delete_fail)
        file_manager.on_get_fail.connect(self.fs_pane.on_get_fail)
        self.connect_zoom(self.fs_pane)
        return self.fs_pane

    def add_micropython_repl(self, repl, name):
        """
        Adds a MicroPython based REPL pane to the application.
        """
        repl_pane = MicroPythonREPLPane(port=repl.port, theme=self.theme)
        self.add_repl(repl_pane, name)

    def add_jupyter_repl(self, kernel_manager, kernel_client):
        """
        Adds a Jupyter based REPL pane to the application.
        """
        kernel_manager.kernel.gui = 'qt4'
        kernel_client.start_channels()
        ipython_widget = JupyterREPLPane(theme=self.theme)
        ipython_widget.kernel_manager = kernel_manager
        ipython_widget.kernel_client = kernel_client
        self.add_repl(ipython_widget, _('Python3 (Jupyter)'))

    def add_repl(self, repl_pane, name):
        """
        Adds the referenced REPL pane to the application.
        """
        self.repl_pane = repl_pane
        self.repl = QDockWidget(_('{} REPL').format(name))
        self.repl.setWidget(repl_pane)
        self.repl.setFeatures(QDockWidget.DockWidgetMovable)
        self.repl.setAllowedAreas(Qt.BottomDockWidgetArea |
                                  Qt.LeftDockWidgetArea |
                                  Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.repl)
        self.connect_zoom(self.repl_pane)
        self.repl_pane.set_theme(self.theme)
        self.repl_pane.setFocus()

    def add_python3_runner(self, script_name, working_directory,
                           interactive=False, debugger=False,
                           command_args=None):
        """
        Display console output for the referenced Python script.

        The script will be run within the workspace_path directory.

        If interactive is True (default is False) the Python process will
        run in interactive mode (dropping the user into the REPL when the
        script completes).

        If debugger is True (default is False) the script will be run within
        a debug runner session. The debugger overrides the interactive flag
        (you cannot run the debugger in interactive mode).

        If there is a list of command_args (the default is None) then these
        will be passed as further arguments into the command run in the
        new process.
        """
        self.process_runner = PythonProcessPane(self)
        self.runner = QDockWidget(_("Running: {}").format(
                                  os.path.basename(script_name)))
        self.runner.setWidget(self.process_runner)
        self.runner.setFeatures(QDockWidget.DockWidgetMovable)
        self.runner.setAllowedAreas(Qt.BottomDockWidgetArea |
                                    Qt.LeftDockWidgetArea |
                                    Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.runner)
        self.process_runner.start_process(script_name, working_directory,
                                          interactive, debugger, command_args)
        self.process_runner.setFocus()
        self.connect_zoom(self.process_runner)
        return self.process_runner

    def add_debug_inspector(self):
        """
        Display a debug inspector to view the call stack.
        """
        self.debug_inspector = DebugInspector()
        self.debug_model = QStandardItemModel()
        self.debug_inspector.setModel(self.debug_model)
        self.debug_inspector.setUniformRowHeights(True)
        self.inspector = QDockWidget(_('Debug Inspector'))
        self.inspector.setWidget(self.debug_inspector)
        self.inspector.setFeatures(QDockWidget.DockWidgetMovable)
        self.inspector.setAllowedAreas(Qt.BottomDockWidgetArea |
                                       Qt.LeftDockWidgetArea |
                                       Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.inspector)
        self.connect_zoom(self.debug_inspector)

    def update_debug_inspector(self, locals_dict):
        """
        Given the contents of a dict representation of the locals in the
        current stack frame, update the debug inspector with the new values.
        """
        excluded_names = ['__builtins__', '__debug_code__',
                          '__debug_script__', ]
        names = sorted([x for x in locals_dict if x not in excluded_names])
        self.debug_model.clear()
        self.debug_model.setHorizontalHeaderLabels([_('Name'), _('Value'), ])
        for name in names:
            try:
                # DANGER!
                val = eval(locals_dict[name])
            except Exception:
                val = None
            if isinstance(val, list):
                # Show a list consisting of rows of position/value
                list_item = QStandardItem(name)
                for i, i_val in enumerate(val):
                    list_item.appendRow([
                        QStandardItem(str(i)),
                        QStandardItem(repr(i_val))
                    ])
                self.debug_model.appendRow([
                    list_item,
                    QStandardItem(_('(A list of {} items.)').format(len(val)))
                ])
            elif isinstance(val, dict):
                # Show a dict consisting of rows of key/value pairs.
                dict_item = QStandardItem(name)
                for k, k_val in val.items():
                    dict_item.appendRow([
                        QStandardItem(repr(k)),
                        QStandardItem(repr(k_val))
                    ])
                self.debug_model.appendRow([
                    dict_item,
                    QStandardItem(_('(A dict of {} items.)').format(len(val)))
                ])
            else:
                self.debug_model.appendRow([
                    QStandardItem(name),
                    QStandardItem(locals_dict[name]),
                ])

    def remove_filesystem(self):
        """
        Removes the file system pane from the application.
        """
        if hasattr(self, 'fs') and self.fs:
            self.fs_pane = None
            self.fs.setParent(None)
            self.fs.deleteLater()
            self.fs = None

    def remove_repl(self):
        """
        Removes the REPL pane from the application.
        """
        if hasattr(self, 'repl') and self.repl:
            self.repl_pane = None
            self.repl.setParent(None)
            self.repl.deleteLater()
            self.repl = None

    def remove_python_runner(self):
        """
        Removes the runner pane from the application.
        """
        if hasattr(self, 'runner') and self.runner:
            self.process_runner = None
            self.runner.setParent(None)
            self.runner.deleteLater()
            self.runner = None

    def remove_debug_inspector(self):
        """
        Removes the debug inspector pane from the application.
        """
        if hasattr(self, 'inspector') and self.inspector:
            self.debug_inspector = None
            self.debug_model = None
            self.inspector.setParent(None)
            self.inspector.deleteLater()
            self.inspector = None

    def set_theme(self, theme):
        """
        Sets the theme for the REPL and editor tabs.
        """
        self.theme = theme
        if theme == 'contrast':
            self.setStyleSheet(CONTRAST_STYLE)
            new_theme = ContrastTheme
            new_icon = 'theme_day'
        elif theme == 'night':
            new_theme = NightTheme
            new_icon = 'theme_contrast'
            self.setStyleSheet(NIGHT_STYLE)
        else:
            self.setStyleSheet(DAY_STYLE)
            new_theme = DayTheme
            new_icon = 'theme'
        for widget in self.widgets:
            widget.set_theme(new_theme)
        self.button_bar.slots['theme'].setIcon(load_icon(new_icon))
        if hasattr(self, 'repl') and self.repl:
            self.repl_pane.set_theme(theme)

    def show_logs(self, log, theme):
        """
        Display the referenced content of the log.
        """
        log_box = LogDisplay()
        log_box.setup(log, theme)
        log_box.exec()

    def show_message(self, message, information=None, icon=None):
        """
        Displays a modal message to the user.

        If information is passed in this will be set as the additional
        informative text in the modal dialog.

        Since this mechanism will be used mainly for warning users that
        something is awry the default icon is set to "Warning". It's possible
        to override the icon to one of the following settings: NoIcon,
        Question, Information, Warning or Critical.
        """
        message_box = QMessageBox(self)
        message_box.setText(message)
        message_box.setWindowTitle('Mu')
        if information:
            message_box.setInformativeText(information)
        if icon and hasattr(message_box, icon):
            message_box.setIcon(getattr(message_box, icon))
        else:
            message_box.setIcon(message_box.Warning)
        logger.debug(message)
        logger.debug(information)
        message_box.exec()

    def show_confirmation(self, message, information=None, icon=None):
        """
        Displays a modal message to the user to which they need to confirm or
        cancel.

        If information is passed in this will be set as the additional
        informative text in the modal dialog.

        Since this mechanism will be used mainly for warning users that
        something is awry the default icon is set to "Warning". It's possible
        to override the icon to one of the following settings: NoIcon,
        Question, Information, Warning or Critical.
        """
        message_box = QMessageBox()
        message_box.setText(message)
        message_box.setWindowTitle(_('Mu'))
        if information:
            message_box.setInformativeText(information)
        if icon and hasattr(message_box, icon):
            message_box.setIcon(getattr(message_box, icon))
        else:
            message_box.setIcon(message_box.Warning)
        message_box.setStandardButtons(message_box.Cancel | message_box.Ok)
        message_box.setDefaultButton(message_box.Cancel)
        logger.debug(message)
        logger.debug(information)
        return message_box.exec()

    def update_title(self, filename=None):
        """
        Updates the title bar of the application. If a filename (representing
        the name of the file currently the focus of the editor) is supplied,
        append it to the end of the title.
        """
        title = self.title
        if filename:
            title += ' - ' + filename
        self.setWindowTitle(title)

    def autosize_window(self):
        """
        Makes the editor 80% of the width*height of the screen and centres it.
        """
        screen = QDesktopWidget().screenGeometry()
        w = int(screen.width() * 0.8)
        h = int(screen.height() * 0.8)
        self.resize(w, h)
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def reset_annotations(self):
        """
        Resets the state of annotations on the current tab.
        """
        self.current_tab.reset_annotations()

    def annotate_code(self, feedback, annotation_type):
        """
        Given a list of annotations about the code in the current tab, add
        the annotations to the editor window so the user can make appropriate
        changes.
        """
        self.current_tab.annotate_code(feedback, annotation_type)

    def show_annotations(self):
        """
        Show the annotations added to the current tab.
        """
        self.current_tab.show_annotations()

    def setup(self, breakpoint_toggle, theme):
        """
        Sets up the window.

        Defines the various attributes of the window and defines how the user
        interface is laid out.
        """
        self.theme = theme
        self.breakpoint_toggle = breakpoint_toggle
        # Give the window a default icon, title and minimum size.
        self.setWindowIcon(load_icon(self.icon))
        self.update_title()
        self.read_only_tabs = False
        self.setMinimumSize(800, 400)

        self.widget = QWidget()

        widget_layout = QVBoxLayout()
        self.widget.setLayout(widget_layout)
        self.button_bar = ButtonBar(self.widget)
        self.tabs = FileTabs()
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)
        self.status_bar = StatusBar(parent=self)
        self.setStatusBar(self.status_bar)
        self.addToolBar(self.button_bar)
        self.show()
        self.autosize_window()

    def resizeEvent(self, resizeEvent):
        """
        Respond to window getting too small for the button bar to fit well.
        """
        size = resizeEvent.size()
        self.button_bar.set_responsive_mode(size.width(), size.height())

    def select_mode(self, modes, current_mode, theme):
        """
        Display the mode selector dialog and return the result.
        """
        mode_select = ModeSelector()
        mode_select.setup(modes, current_mode, theme)
        mode_select.exec()
        try:
            return mode_select.get_mode()
        except Exception as ex:
            return None

    def change_mode(self, mode):
        """
        Given a an object representing a mode, recreates the button bar with
        the expected functionality.
        """
        self.button_bar.change_mode(mode)
        # Update the autocomplete / tooltip APIs for each tab to the new mode.
        api = mode.api()
        for widget in self.widgets:
            widget.set_api(api)

    def set_usb_checker(self, duration, callback):
        """
        Sets up a timer that polls for USB changes via the "callback" every
        "duration" seconds.
        """
        self.usb_checker = QTimer()
        self.usb_checker.timeout.connect(callback)
        self.usb_checker.start(duration * 1000)

    def set_timer(self, duration, callback):
        """
        Set a repeating timer to call "callback" every "duration" seconds.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(callback)
        self.timer.start(duration * 1000)  # Measured in milliseconds.

    def stop_timer(self):
        """
        Stop the repeating timer.
        """
        if self.timer:
            self.timer.stop()
            self.timer = None

    def connect_tab_rename(self, handler, shortcut):
        """
        Connect the double-click event on a tab and the keyboard shortcut to
        the referenced handler (causing the Save As dialog).
        """
        self.tabs.shortcut = QShortcut(QKeySequence(shortcut), self)
        self.tabs.shortcut.activated.connect(handler)
        self.tabs.tabBarDoubleClicked.connect(handler)


class StatusBar(QStatusBar):
    """
    Defines the look and behaviour of the status bar along the bottom of the
    UI.
    """
    def __init__(self, parent=None, mode='python'):
        super().__init__(parent)
        self.mode = mode
        # Mode selector.
        self.mode_label = QLabel()
        self.mode_label.setToolTip(_("Select edit mode."))
        self.addPermanentWidget(self.mode_label)
        self.set_mode(mode)
        # Logs viewer
        self.logs_label = QLabel()
        self.logs_label.setPixmap(load_pixmap('logs').scaledToHeight(24))
        self.logs_label.setToolTip(_('View logs.'))
        self.addPermanentWidget(self.logs_label)

    def connect_logs(self, handler, shortcut):
        """
        Connect the mouse press event and keyboard shortcut for the log widget
        to the referenced handler function.
        """
        self.logs_label.shortcut = QShortcut(QKeySequence(shortcut),
                                             self.parent())
        self.logs_label.shortcut.activated.connect(handler)
        self.logs_label.mousePressEvent = handler

    def connect_mode(self, handler, shortcut):
        """
        Connect the mouse press event and keyboard shortcut for the mode widget
        to the referenced handler function.
        """
        self.mode_label.shortcut = QShortcut(QKeySequence(shortcut),
                                             self.parent())
        self.mode_label.shortcut.activated.connect(handler)
        self.mode_label.mousePressEvent = handler

    def set_message(self, message, pause=5000):
        """
        Displays a message in the status bar for a certain period of time.
        """
        self.showMessage(message, pause)

    def set_mode(self, mode):
        """
        Updates the mode label to the new mode.
        """
        self.mode_label.setText(mode.capitalize())
