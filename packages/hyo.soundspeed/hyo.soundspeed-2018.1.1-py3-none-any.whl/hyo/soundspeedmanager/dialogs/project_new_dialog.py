from PySide import QtGui
from PySide import QtCore

import logging
logger = logging.getLogger(__name__)

from hyo.soundspeedmanager.dialogs.dialog import AbstractDialog


class ProjectNewDialog(AbstractDialog):

    def __init__(self, main_win, lib, parent=None):
        AbstractDialog.__init__(self, main_win=main_win, lib=lib, parent=parent)

        self.fmt_outputs = list()

        self.setWindowTitle("New project")
        self.setMinimumWidth(160)

        # outline ui
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        # -- label
        hbox  = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(hbox)
        hbox.addStretch()
        label = QtGui.QLabel("Project name:")
        hbox.addWidget(label)
        hbox.addStretch()
        # -- value
        self.new_project = QtGui.QLineEdit()
        rex = QtCore.QRegExp('[a-zA-Z0-9_.-]+')
        validator = QtGui.QRegExpValidator(rex)
        self.new_project.setValidator(validator)
        self.mainLayout.addWidget(self.new_project)
        # -- space
        self.mainLayout.addSpacing(6)
        # -- button
        btn = QtGui.QPushButton("Create")
        self.mainLayout.addWidget(btn)
        # noinspection PyUnresolvedReferences
        btn.clicked.connect(self.on_create)

    def on_create(self):
        logger.debug("creating project")

        txt = self.new_project.text()

        if len(txt) == 0:
            msg = "Set the project name!"
            QtGui.QMessageBox.warning(self, "Creation warning", msg, QtGui.QMessageBox.Ok)
            return

        if txt in self.lib.list_projects():
            msg = "The project '%s' already exists. Load it!" % txt
            QtGui.QMessageBox.warning(self, "Creation warning", msg, QtGui.QMessageBox.Ok)
            return

        self.lib.current_project = txt
        self.lib.save_settings_to_db()
        self.lib.reload_settings_from_db()
        self.accept()
