import os
import logging

from PySide import QtGui, QtCore

logger = logging.getLogger(__name__)

from hyo.soundspeed.profile.dicts import Dicts
from hyo.soundspeedmanager.widgets.widget import AbstractWidget
from hyo.soundspeedmanager.dialogs.plot_profiles_dialog import PlotProfilesDialog
from hyo.soundspeedmanager.dialogs.project_new_dialog import ProjectNewDialog
from hyo.soundspeedmanager.dialogs.project_rename_dialog import ProjectRenameDialog
from hyo.soundspeedmanager.dialogs.project_switch_dialog import ProjectSwitchDialog
from hyo.soundspeedmanager.dialogs.import_data_dialog import ImportDataDialog
from hyo.soundspeedmanager.dialogs.export_single_profile_dialog import ExportSingleProfileDialog
from hyo.soundspeedmanager.dialogs.export_multi_profile_dialog import ExportMultiProfileDialog
from hyo.soundspeedmanager.dialogs.import_multi_profile_dialog import ImportMultiProfileDialog
from hyo.soundspeedmanager.dialogs.plot_multi_profile_dialog import PlotMultiProfileDialog
from hyo.soundspeedmanager.dialogs.export_profile_metadata_dialog import ExportProfileMetadataDialog
from hyo.soundspeedmanager.dialogs.text_editor_dialog import TextEditorDialog
from hyo.soundspeedmanager.dialogs.metadata_dialog import MetadataDialog
from hyo.soundspeedmanager.dialogs.common_metadata_dialog import CommonMetadataDialog


class Database(AbstractWidget):
    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))  # to be overloaded
    media = os.path.join(here, os.pardir, 'media')

    def __init__(self, main_win, lib):
        AbstractWidget.__init__(self, main_win=main_win, lib=lib)

        lbl_width = 60

        # create the overall layout
        self.main_layout = QtGui.QVBoxLayout()
        self.frame.setLayout(self.main_layout)

        # - active setup
        hbox = QtGui.QHBoxLayout()
        self.main_layout.addLayout(hbox)
        hbox.addStretch()
        self.active_label = QtGui.QLabel()
        hbox.addWidget(self.active_label)
        hbox.addStretch()

        # - list of setups
        hbox = QtGui.QHBoxLayout()
        self.main_layout.addLayout(hbox)

        # -- label
        vbox = QtGui.QVBoxLayout()
        hbox.addLayout(vbox)
        vbox.addStretch()
        label = QtGui.QLabel("Profiles:")
        label.setFixedWidth(lbl_width)
        vbox.addWidget(label)
        vbox.addStretch()

        # -- list
        self.ssp_list = QtGui.QTableWidget()
        self.ssp_list.setSortingEnabled(True)
        self.ssp_list.setFocus()
        self.ssp_list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ssp_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ssp_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.ssp_list.customContextMenuRequested.connect(self.make_context_menu)
        # noinspection PyUnresolvedReferences
        self.ssp_list.itemDoubleClicked.connect(self.load_profile)
        hbox.addWidget(self.ssp_list)

        # - RIGHT COLUMN
        right_vbox = QtGui.QVBoxLayout()
        hbox.addLayout(right_vbox)

        # -- project box
        self.project_box = QtGui.QGroupBox("Project")
        right_vbox.addWidget(self.project_box)
        # --- manage button box
        project_vbox = QtGui.QVBoxLayout()
        self.project_box.setLayout(project_vbox)
        self.manage_btn_box = QtGui.QDialogButtonBox(QtCore.Qt.Vertical)
        project_vbox.addWidget(self.manage_btn_box)

        # ---- new project
        self.btn_new_project = QtGui.QPushButton("New project")
        # noinspection PyUnresolvedReferences
        self.btn_new_project.clicked.connect(self.new_project)
        self.btn_new_project.setToolTip("Create a new project")
        self.manage_btn_box.addButton(self.btn_new_project, QtGui.QDialogButtonBox.ActionRole)
        self.new_project_act = QtGui.QAction('New Project DB', self)
        self.new_project_act.setShortcut('Ctrl+N')
        # noinspection PyUnresolvedReferences
        self.new_project_act.triggered.connect(self.new_project)
        self.main_win.database_menu.addAction(self.new_project_act)

        # ---- rename project
        self.btn_rename_project = QtGui.QPushButton("Rename project")
        # noinspection PyUnresolvedReferences
        self.btn_rename_project.clicked.connect(self.rename_project)
        self.btn_rename_project.setToolTip("Rename the current project")
        self.manage_btn_box.addButton(self.btn_rename_project, QtGui.QDialogButtonBox.ActionRole)
        self.rename_project_act = QtGui.QAction('Rename Current Project DB', self)
        self.rename_project_act.setShortcut('Ctrl+R')
        # noinspection PyUnresolvedReferences
        self.rename_project_act.triggered.connect(self.rename_project)
        self.main_win.database_menu.addAction(self.rename_project_act)

        # ---- load project
        self.btn_load_project = QtGui.QPushButton("Switch project")
        # noinspection PyUnresolvedReferences
        self.btn_load_project.clicked.connect(self.switch_project)
        self.btn_load_project.setToolTip("Switch to another existing project")
        self.manage_btn_box.addButton(self.btn_load_project, QtGui.QDialogButtonBox.ActionRole)
        self.load_project_act = QtGui.QAction('Switch Project DB', self)
        self.load_project_act.setShortcut('Ctrl+L')
        # noinspection PyUnresolvedReferences
        self.load_project_act.triggered.connect(self.switch_project)
        self.main_win.database_menu.addAction(self.load_project_act)

        # ---- import data
        self.btn_import_data = QtGui.QPushButton("Import data")
        # noinspection PyUnresolvedReferences
        self.btn_import_data.clicked.connect(self.import_data)
        self.btn_import_data.setToolTip("Import data from another project")
        self.manage_btn_box.addButton(self.btn_import_data, QtGui.QDialogButtonBox.ActionRole)
        self.import_data_act = QtGui.QAction('Import Data from Project DB', self)
        self.import_data_act.setShortcut('Ctrl+I')
        # noinspection PyUnresolvedReferences
        self.import_data_act.triggered.connect(self.import_data)
        self.main_win.database_menu.addAction(self.import_data_act)

        # ---- project folder
        self.btn_project_folder = QtGui.QPushButton("Open folder")
        # noinspection PyUnresolvedReferences
        self.btn_project_folder.clicked.connect(self.project_folder)
        self.btn_project_folder.setToolTip("Open projects folder")
        self.manage_btn_box.addButton(self.btn_project_folder, QtGui.QDialogButtonBox.ActionRole)
        self.project_folder_act = QtGui.QAction('Open Projects DB Folder', self)
        self.project_folder_act.setShortcut('Ctrl+P')
        # noinspection PyUnresolvedReferences
        self.project_folder_act.triggered.connect(self.project_folder)
        self.main_win.database_menu.addAction(self.project_folder_act)

        right_vbox.addStretch()
        right_vbox.addStretch()

        # -- profiles box
        self.profiles_box = QtGui.QGroupBox("Profiles")
        right_vbox.addWidget(self.profiles_box)

        # --- manage button box
        profiles_vbox = QtGui.QVBoxLayout()
        self.profiles_box.setLayout(profiles_vbox)
        self.product_btn_box = QtGui.QDialogButtonBox(QtCore.Qt.Vertical)
        profiles_vbox.addWidget(self.product_btn_box)

        # ---- import profiles
        btn = QtGui.QPushButton("Import profiles")
        # noinspection PyUnresolvedReferences
        btn.clicked.connect(self.import_profiles)
        btn.setToolTip("Import multiple profiles")
        self.product_btn_box.addButton(btn, QtGui.QDialogButtonBox.ActionRole)
        self.import_profiles_act = QtGui.QAction('Import Multiple Profiles', self)
        self.import_profiles_act.setShortcut('Ctrl+M')
        # noinspection PyUnresolvedReferences
        self.import_profiles_act.triggered.connect(self.import_profiles)
        self.main_win.database_menu.addSeparator()
        self.main_win.database_menu.addAction(self.import_profiles_act)

        # ---- export profiles
        btn = QtGui.QPushButton("Export profiles")
        # noinspection PyUnresolvedReferences
        btn.clicked.connect(self.export_profile_switch)
        btn.setToolTip("Export profile data")
        self.product_btn_box.addButton(btn, QtGui.QDialogButtonBox.ActionRole)
        self.export_profiles_act = QtGui.QAction('Export Multiple Profiles', self)
        self.export_profiles_act.setShortcut('Ctrl+X')
        # noinspection PyUnresolvedReferences
        self.export_profiles_act.triggered.connect(self.export_profile_switch)
        self.main_win.database_menu.addAction(self.export_profiles_act)

        # ---- plot profiles
        btn = QtGui.QPushButton("Make plots")
        # noinspection PyUnresolvedReferences
        btn.clicked.connect(self.plot_profiles)
        btn.setToolTip("Create plots with all the profiles")
        self.product_btn_box.addButton(btn, QtGui.QDialogButtonBox.ActionRole)
        self.plot_profiles_act = QtGui.QAction('Make Plots from Data', self)
        self.plot_profiles_act.setShortcut('Ctrl+P')
        # noinspection PyUnresolvedReferences
        self.plot_profiles_act.triggered.connect(self.plot_profiles)
        self.main_win.database_menu.addAction(self.plot_profiles_act)

        # ---- export metadata
        btn = QtGui.QPushButton("Export info")
        # noinspection PyUnresolvedReferences
        btn.clicked.connect(self.export_profile_metadata)
        btn.setToolTip("Export profile locations and metadata")
        self.product_btn_box.addButton(btn, QtGui.QDialogButtonBox.ActionRole)
        self.export_profile_metadata_act = QtGui.QAction('Export Data Info', self)
        self.export_profile_metadata_act.setShortcut('Ctrl+D')
        # noinspection PyUnresolvedReferences
        self.export_profile_metadata_act.triggered.connect(self.export_profile_metadata)
        self.main_win.database_menu.addAction(self.export_profile_metadata_act)

        # ---- output folder
        btn = QtGui.QPushButton("Output folder")
        # noinspection PyUnresolvedReferences
        btn.clicked.connect(self.output_folder)
        btn.setToolTip("Open the output folder")
        self.product_btn_box.addButton(btn, QtGui.QDialogButtonBox.ActionRole)
        self.output_folder_act = QtGui.QAction('Open Output Folder', self)
        self.output_folder_act.setShortcut('Ctrl+O')
        # noinspection PyUnresolvedReferences
        self.output_folder_act.triggered.connect(self.output_folder)
        self.main_win.database_menu.addAction(self.output_folder_act)

        # self.main_layout.addStretch()

        self.update_table()

    def make_context_menu(self, pos):
        """Make a context menu to deal with profile specific actions"""

        # check if any selection
        rows = self.ssp_list.selectionModel().selectedRows()
        if len(rows) == 0:
            logger.debug('Not profile selected')
            return

        menu = QtGui.QMenu(parent=self)
        qa_menu = QtGui.QMenu('Check quality', self)
        qa_menu.setIcon(QtGui.QIcon(os.path.join(self.media, 'qa.png')))

        # single selection
        if len(rows) == 1:

            stats_act = QtGui.QAction(QtGui.QIcon(os.path.join(self.media, 'stats.png')),
                                      "Profile stats", self, toolTip="Get some statistical info about the profile",
                                      triggered=self.stats_profile)
            menu.addAction(stats_act)

            metadata_act = QtGui.QAction(QtGui.QIcon(os.path.join(self.media, 'metadata_profile.png')),
                                         "Metadata info", self, toolTip="View/edit the profile metadata",
                                         triggered=self.metadata_profile)
            menu.addAction(metadata_act)

            menu.addMenu(qa_menu)
            dqa_compare_ref_act = QtGui.QAction("DQA (with reference)", self,
                                                toolTip="Assess data quality by comparison with the reference cast",
                                                triggered=self.dqa_full_profile)
            qa_menu.addAction(dqa_compare_ref_act)
            dqa_at_surface_act = QtGui.QAction("DQA (at surface)", self, toolTip="DQA with surface sound speed",
                                               triggered=self.dqa_at_surface)
            qa_menu.addAction(dqa_at_surface_act)

            menu.addSeparator()

            load_act = QtGui.QAction(QtGui.QIcon(os.path.join(self.media, 'load_profile.png')),
                                     "Load profile", self, toolTip="Load a profile", triggered=self.load_profile)
            menu.addAction(load_act)

            export_act = QtGui.QAction(QtGui.QIcon(os.path.join(self.media, 'export_profile.png')),
                                       "Export profile", self, toolTip="Export a single profile",
                                       triggered=self.export_single_profile)
            menu.addAction(export_act)

            delete_act = QtGui.QAction(QtGui.QIcon(os.path.join(self.media, 'delete.png')),
                                       "Delete profile", self, toolTip="Delete selected profile",
                                       triggered=self.delete_profile)
            menu.addAction(delete_act)

            def handle_menu_hovered(action):
                # noinspection PyArgumentList
                QtGui.QToolTip.showText(QtGui.QCursor.pos(), action.toolTip(), menu, menu.actionGeometry(action))

            # noinspection PyUnresolvedReferences
            menu.hovered.connect(handle_menu_hovered)

        else:  # multiple selection

            metadata_act = QtGui.QAction(QtGui.QIcon(os.path.join(self.media, 'metadata_profile.png')), "Edit Metadata",
                                         self, toolTip="Edit common metadata fields for multiple profiles",
                                         triggered=self.metadata_profile)
            menu.addAction(metadata_act)

            menu.addMenu(qa_menu)
            if len(rows) == 2:
                dqa_compare_two_act = QtGui.QAction("DQA (among selections)", self,
                                                    toolTip="Assess data quality by comparison between two casts",
                                                    triggered=self.dqa_full_profile)
                qa_menu.addAction(dqa_compare_two_act)

            dqa_at_surface_act = QtGui.QAction("DQA (at surface)", self, toolTip="DQA with surface sound speed",
                                               triggered=self.dqa_at_surface)
            qa_menu.addAction(dqa_at_surface_act)

            plot_act = QtGui.QAction(QtGui.QIcon(os.path.join(self.media, 'plot_comparison.png')),
                                     "Comparison plot", self, toolTip="Plot profiles for comparison",
                                     triggered=self.plot_comparison)
            menu.addAction(plot_act)

            menu.addSeparator()

            export_act = QtGui.QAction(QtGui.QIcon(os.path.join(self.media, 'export_profile.png')),
                                       "Export profiles", self, toolTip="Export multiple profiles",
                                       triggered=self.export_multi_profile)
            menu.addAction(export_act)

            delete_act = QtGui.QAction(QtGui.QIcon(os.path.join(self.media, 'delete.png')),
                                       "Delete profiles", self, toolTip="Delete selected profiles",
                                       triggered=self.delete_profile)
            menu.addAction(delete_act)

            def handle_menu_hovered(action):
                # noinspection PyArgumentList
                QtGui.QToolTip.showText(QtGui.QCursor.pos(), action.toolTip(), menu, menu.actionGeometry(action))

            # noinspection PyUnresolvedReferences
            menu.hovered.connect(handle_menu_hovered)

        menu.exec_(self.ssp_list.mapToGlobal(pos))

    def load_profile(self):
        logger.debug("user want to load a profile")

        # check if any selection
        rows = self.ssp_list.selectionModel().selectedRows()
        if len(rows) != 1:
            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "Database", "You need to select a single profile before loading it!")
            return

        if (self.ssp_list.item(rows[0].row(), 3).text() == "Future") or \
                (self.ssp_list.item(rows[0].row(), 4).text() == "Future"):
            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "Database",
                                          "You cannot load the selected profile from the database!\n\n"
                                          "If you need to access it, update to a newer version of Sound Speed Manager.")
            return

        # the primary key is the first column (= 0)
        pk = int(self.ssp_list.item(rows[0].row(), 0).text())
        success = self.lib.load_profile(pk)
        if not success:
            # noinspection PyCallByClass
            QtGui.QMessageBox.warning(self, "Database", "Unable to load profile!", QtGui.QMessageBox.Ok)
            return

        if self.lib.has_ssp():
            self.main_win.data_imported()
            self.main_win.switch_to_editor_tab()

    def stats_profile(self):
        logger.debug("user wants some stats on a single profile")

        # first, we clear the current data (if any)
        self.lib.clear_data()
        self.main_win.data_cleared()

        # check if any selection
        rows = self.ssp_list.selectionModel().selectedRows()
        if len(rows) != 1:
            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "Database", "Select a single profile before exporting it!")
            return

        # the primary key is the first column (= 0)
        pk = int(self.ssp_list.item(rows[0].row(), 0).text())
        success = self.lib.load_profile(pk, skip_atlas=True)
        if not success:
            # noinspection PyCallByClass
            QtGui.QMessageBox.warning(self, "Database", "Unable to load profile!", QtGui.QMessageBox.Ok)
            return

        msg = self.lib.profile_stats()
        if msg is not None:
            basename = "%s_%03d_stats" % (self.lib.current_project, pk)
            dlg = TextEditorDialog(title="Profile Statistical Info", basename=basename, body=msg,
                                   main_win=self, lib=self.lib, parent=self)
            dlg.exec_()

        # finally, we clear the just loaded data
        self.lib.clear_data()
        self.main_win.data_cleared()

    def metadata_profile(self):
        logger.debug("user wants view the profile metadata")

        # first, we clear the current data (if any)
        self.lib.clear_data()
        self.main_win.data_cleared()

        # check if any selection
        rows = self.ssp_list.selectionModel().selectedRows()
        if len(rows) == 1:  # single selection

            # the primary key is the first column (= 0)
            pk = int(self.ssp_list.item(rows[0].row(), 0).text())
            success = self.lib.load_profile(pk, skip_atlas=True)
            if not success:
                # noinspection PyCallByClass
                QtGui.QMessageBox.warning(self, "Database", "Unable to load profile!", QtGui.QMessageBox.Ok)
                return

            dlg = MetadataDialog(lib=self.lib, main_win=self.main_win, parent=self)
            dlg.exec_()

        else:  # multiple selection

            logger.debug("User wants to edit the metadata of multiple profiles")

            pks = [int(self.ssp_list.item(row.row(), 0).text()) for row in rows]
            logger.debug("pks: %s" % (pks, ))

            dlg = CommonMetadataDialog(lib=self.lib, main_win=self.main_win, pks=pks, parent=self)
            dlg.exec_()

        # finally, we clear the just loaded data
        self.lib.clear_data()
        self.main_win.data_cleared()

    def export_single_profile(self):
        logger.debug("user want to export a single profile")

        # first, we clear the current data (if any)
        self.lib.clear_data()
        self.main_win.data_cleared()

        # check if any selection
        rows = self.ssp_list.selectionModel().selectedRows()
        if len(rows) != 1:
            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "Database", "Select a single profile before exporting it!")
            return

        # the primary key is the first column (= 0)
        pk = int(self.ssp_list.item(rows[0].row(), 0).text())
        success = self.lib.load_profile(pk)
        if not success:
            # noinspection PyCallByClass
            QtGui.QMessageBox.warning(self, "Database", "Unable to load profile!", QtGui.QMessageBox.Ok)
            return

        dlg = ExportSingleProfileDialog(lib=self.lib, main_win=self.main_win, parent=self)
        dlg.exec_()

        # finally, we clear the just loaded data
        self.lib.clear_data()
        self.main_win.data_cleared()

    def plot_comparison(self):
        logger.debug("user want to plot multiple profiles for comparison")

        self.lib.clear_data()
        self.main_win.data_cleared()

        # check if any selection
        rows = self.ssp_list.selectionModel().selectedRows()
        if len(rows) < 2:
            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "Database", "Select multiple profiles before plotting them!")
            return

        pks = list()
        for row in rows:
            pks.append(int(self.ssp_list.item(row.row(), 0).text()))

        dlg = PlotMultiProfileDialog(main_win=self.main_win, lib=self.lib, pks=pks, parent=self)
        dlg.exec_()
        dlg.raise_window()

    def export_multi_profile(self):
        logger.debug("user want to export multiple profiles")

        self.lib.clear_data()
        self.main_win.data_cleared()

        # check if any selection
        rows = self.ssp_list.selectionModel().selectedRows()
        if len(rows) < 2:
            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "Database", "Select multiple profiles before exporting them!")
            return

        pks = list()
        for row in rows:
            pks.append(int(self.ssp_list.item(row.row(), 0).text()))

        dlg = ExportMultiProfileDialog(main_win=self.main_win, lib=self.lib, pks=pks, parent=self)
        dlg.exec_()

    def delete_profile(self):
        logger.debug("user want to delete a profile")

        # check if any selection
        rows = self.ssp_list.selectionModel().selectedRows()
        if len(rows) == 0:
            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "Database", "You need to select a profile before deleting it!")
            return

        # ask if the user want to delete it
        if len(rows) == 1:
            pk = int(self.ssp_list.item(rows[0].row(), 0).text())
            msg = "Do you really want to delete profile #%02d?" % pk
        else:
            msg = "Do you really want to delete %d profiles?" % len(rows)
        # noinspection PyCallByClass
        ret = QtGui.QMessageBox.warning(self, "Database", msg, QtGui.QMessageBox.Ok | QtGui.QMessageBox.No)
        if ret == QtGui.QMessageBox.No:
            return

        # actually perform the removal
        for row in rows:
            pk = int(self.ssp_list.item(row.row(), 0).text())
            success = self.lib.delete_db_profile(pk)
            if not success:
                # noinspection PyCallByClass
                QtGui.QMessageBox.critical(self, "Database", "Unable to remove the #%02d profile!" % pk)

        self.main_win.data_removed()

    def dqa_at_surface(self):
        logger.debug("user want to do DQA at surface")

        for row in self.ssp_list.selectionModel().selectedRows():

            pk = int(self.ssp_list.item(row.row(), 0).text())

            msg = self.lib.dqa_at_surface(pk)
            if msg is not None:
                basename = "%s_%03d_dqa_surface" % (self.lib.current_project, pk)
                dlg = TextEditorDialog(title="Surface DQA", basename=basename, body=msg,
                                       main_win=self, lib=self.lib, parent=self)
                dlg.exec_()

    def dqa_full_profile(self):
        logger.debug("user want to do a profile DQA")

        rows = self.ssp_list.selectionModel().selectedRows()
        if len(rows) == 1:

            pk = int(self.ssp_list.item(rows[0].row(), 0).text())
            if self.lib.ref is None:
                # noinspection PyCallByClass
                QtGui.QMessageBox.information(self, "DQA compare with reference cast",
                                              "You should set reference cast first!")
                return
            else:
                try:
                    msg = self.lib.dqa_full_profile(pk)
                except RuntimeError as e:
                    # noinspection PyCallByClass
                    QtGui.QMessageBox.critical(self, "DQA error",
                                               "%s" % e)
                    return

        elif len(rows) == 2:

            pk = int(self.ssp_list.item(rows[0].row(), 0).text())
            pk_ref = int(self.ssp_list.item(rows[1].row(), 0).text())
            try:
                msg = self.lib.dqa_full_profile(pk, pk_ref)

            except RuntimeError as e:
                # noinspection PyCallByClass
                QtGui.QMessageBox.critical(self, "DQA error",
                                           "%s" % e)
                return

        else:

            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "DQA comparison",
                                          "You need to select 1 or 2 profiles to do DQA comparison!")
            return

        if msg is not None:
            basename = "%s_dqa" % self.lib.current_project
            dlg = TextEditorDialog(title="Profile DQA", basename=basename, body=msg, init_size=QtCore.QSize(800, 800),
                                   main_win=self, lib=self.lib, parent=self)
            dlg.exec_()

    def new_project(self):
        logger.debug("user want to create a new project")

        self.main_win.switch_to_database_tab()

        dlg = ProjectNewDialog(lib=self.lib, main_win=self.main_win, parent=self)
        success = dlg.exec_()

        if success:
            self.update_table()

    def rename_project(self):
        logger.debug("user want to rename a project")

        self.main_win.switch_to_database_tab()

        dlg = ProjectRenameDialog(lib=self.lib, main_win=self.main_win, parent=self)
        success = dlg.exec_()

        if success:
            self.update_table()

    def switch_project(self):
        logger.debug("user want to switch to another project")

        self.main_win.switch_to_database_tab()

        dlg = ProjectSwitchDialog(lib=self.lib, main_win=self.main_win, parent=self)
        dlg.exec_()

        self.update_table()

    def import_data(self):
        logger.debug("user want to import data from another project")

        self.main_win.switch_to_database_tab()

        dlg = ImportDataDialog(lib=self.lib, main_win=self.main_win, parent=self)
        dlg.exec_()

        self.update_table()

    def project_folder(self):
        logger.debug("user want to open the project folder")

        self.main_win.switch_to_database_tab()
        self.lib.open_projects_folder()

    def output_folder(self):
        logger.debug("user want to open the output folder")

        self.main_win.switch_to_database_tab()
        self.lib.open_outputs_folder()

    def import_profiles(self):
        logger.debug("user want to import multiple profiles")

        self.main_win.switch_to_database_tab()

        # noinspection PyCallByClass
        QtGui.QMessageBox.warning(self, "Warning about multi-profile import",
                                  "The multi-profile dialog allows you to directly\n"
                                  "import profiles into the database, BUT skipping\n"
                                  "all the processing steps and the visual inspection!\n"
                                  "\n"
                                  "For your convenience, all the imported profiles are\n"
                                  "highlighted in red until loaded for visual inspection\n"
                                  "and saved back into the database.")

        dlg = ImportMultiProfileDialog(main_win=self.main_win, lib=self.lib, parent=self)
        dlg.exec_()

        self.update_table()

    def export_profile_switch(self):
        logger.debug("user want to export profile data")

        self.main_win.switch_to_database_tab()

        # check if any selection
        rows = self.ssp_list.selectionModel().selectedRows()

        nr_rows = len(rows)
        if nr_rows == 0:

            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "Profile Export", "You need to select at least 1 profile!")

        elif nr_rows == 1:

            self.export_single_profile()

        else:

            self.export_multi_profile()

    def export_profile_metadata(self):
        logger.debug("user want to export profile metadata")

        self.main_win.switch_to_database_tab()
        dlg = ExportProfileMetadataDialog(lib=self.lib, main_win=self.main_win, parent=self)
        dlg.exec_()

    def plot_profiles(self):
        logger.debug("user want to plot profiles")

        self.main_win.switch_to_database_tab()

        dlg = PlotProfilesDialog(lib=self.lib, main_win=self.main_win, parent=self)
        success = dlg.exec_()

        if success and not dlg.only_saved:
            self.lib.raise_plot_window()

    def update_table(self):
        # set the top label
        self.active_label.setText("<b>Current project: %s</b>" % self.lib.current_project)

        lst = self.lib.db_list_profiles()

        # prepare the table
        self.ssp_list.clear()
        self.ssp_list.setColumnCount(19)
        self.ssp_list.setHorizontalHeaderLabels(['id', 'time', 'location',
                                                 'sensor', 'probe', 'original path',
                                                 'institution',
                                                 'survey', 'vessel', 'sn',
                                                 'processing time', 'processing info', 'comments',
                                                 'pressure uom', 'depth uom', 'speed uom',
                                                 'temperature uom', 'conductivity uom', 'salinity uom',
                                                 ])

        # populate the table
        self.ssp_list.setRowCount(len(lst))

        for i, ssp in enumerate(lst):

            processed = True
            tokens = ssp[11].split(";")
            if Dicts.proc_user_infos['PLOTTED'] not in tokens:
                processed = False

            for j, field in enumerate(ssp):

                if j == 3:
                    label = '%s' % Dicts.first_match(Dicts.sensor_types, int(field))
                    # logger.debug('%s' % Dicts.first_match(Dicts.sensor_types, int(field)))

                elif j == 4:
                    label = '%s' % Dicts.first_match(Dicts.probe_types, int(field))
                    # logger.debug('%s' % Dicts.first_match(Dicts.probe_types, int(field)))

                else:
                    label = field

                item = QtGui.QTableWidgetItem("%s" % label)

                if (j == 3) and (int(field) == Dicts.sensor_types['Future']):
                    item.setForeground(QtGui.QColor(200, 100, 100))

                elif (j == 4) and (int(field) == Dicts.sensor_types['Future']):
                    item.setForeground(QtGui.QColor(200, 100, 100))

                if not processed:
                    item.setBackground(QtGui.QColor(200, 100, 100, 50))

                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                self.ssp_list.setItem(i, j, item)

        self.ssp_list.resizeColumnsToContents()

    def data_stored(self):
        self.update_table()

    def data_removed(self):
        self.update_table()

    def server_started(self):
        self.setDisabled(True)

    def server_stopped(self):
        self.setEnabled(True)
