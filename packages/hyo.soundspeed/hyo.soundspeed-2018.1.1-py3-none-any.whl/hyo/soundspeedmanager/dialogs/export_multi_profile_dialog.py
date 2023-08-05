from PySide import QtGui
from PySide import QtCore

import os
import logging
logger = logging.getLogger(__name__)

from hyo.soundspeedmanager.dialogs.dialog import AbstractDialog
from hyo.soundspeed.base.helper import explore_folder
from hyo.soundspeed.profile.dicts import Dicts


class ExportMultiProfileDialog(AbstractDialog):

    def __init__(self, main_win, lib, pks, parent=None):
        AbstractDialog.__init__(self, main_win=main_win, lib=lib, parent=parent)

        # check the passed primary keys
        if type(pks) is not list:
            raise RuntimeError("The dialog takes a list of primary keys, not %s" % type(pks))
        if len(pks) < 2:
            raise RuntimeError("The dialog takes a list of at least 2 primary keys, not %s" % len(pks))
        self._pks = pks

        # the list of selected writers passed to the library
        self.selected_writers = list()

        self.setWindowTitle("Export multiple profiles")
        self.setMinimumWidth(160)

        settings = QtCore.QSettings()

        # outline ui
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        # label
        hbox = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(hbox)
        hbox.addStretch()
        label = QtGui.QLabel("Select output formats:")
        hbox.addWidget(label)
        hbox.addStretch()
        # buttons
        hbox = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(hbox)
        hbox.addStretch()
        # - fmt layout
        self.fmtLayout = QtGui.QHBoxLayout()
        hbox.addLayout(self.fmtLayout)
        # -- left
        self.leftButtonBox = QtGui.QDialogButtonBox(QtCore.Qt.Vertical)
        self.leftButtonBox.setFixedWidth(100)
        self.fmtLayout.addWidget(self.leftButtonBox)
        # -- right
        self.rightButtonBox = QtGui.QDialogButtonBox(QtCore.Qt.Vertical)
        self.rightButtonBox.setFixedWidth(100)
        self.fmtLayout.addWidget(self.rightButtonBox)
        hbox.addStretch()
        # add buttons (retrieving name, description and extension from the library)
        for idx, name in enumerate(self.lib.name_writers):

            if len(self.lib.ext_writers[idx]) == 0:
                continue

            btn = QtGui.QPushButton("%s" % self.lib.desc_writers[idx])
            btn.setCheckable(True)
            btn.setToolTip("Select %s format [*.%s]" % (self.lib.desc_writers[idx],
                                                        ", *.".join(self.lib.ext_writers[idx])))

            btn_settings = settings.value("export_single_%s" % name)
            if btn_settings is None:
                settings.setValue("export_single_%s" % name, False)
            if settings.value("export_single_%s" % name) == 'true':
                btn.setChecked(True)
                self.selected_writers.append(name)

            if (idx % 2) == 0:
                self.leftButtonBox.addButton(btn, QtGui.QDialogButtonBox.ActionRole)
            else:
                self.rightButtonBox.addButton(btn, QtGui.QDialogButtonBox.ActionRole)

        # noinspection PyUnresolvedReferences
        self.leftButtonBox.clicked.connect(self.on_select_writer_btn)
        # noinspection PyUnresolvedReferences
        self.rightButtonBox.clicked.connect(self.on_select_writer_btn)

        self.mainLayout.addSpacing(16)

        # option for selecting the output folder
        select_output_folder = settings.value("select_output_folder")
        if select_output_folder is None:
            settings.setValue("select_output_folder", False)
        hbox = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(hbox)
        hbox.addStretch()
        self.selectFolder = QtGui.QCheckBox('Select output folder', self)
        self.selectFolder.setChecked(settings.value("select_output_folder") == 'true')
        hbox.addWidget(self.selectFolder)
        hbox.addStretch()

        # option for opening the output folder
        export_open_folder = settings.value("export_open_folder")
        if export_open_folder is None:
            settings.setValue("export_open_folder", True)
        hbox = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(hbox)
        hbox.addStretch()
        self.openFolder = QtGui.QCheckBox('Open output folder', self)
        self.openFolder.setChecked(settings.value("export_open_folder") == 'true')
        hbox.addWidget(self.openFolder)
        hbox.addStretch()

        # export
        hbox = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(hbox)
        hbox.addStretch()
        btn = QtGui.QPushButton("Export profiles")
        btn.setMinimumHeight(32)
        hbox.addWidget(btn)
        # noinspection PyUnresolvedReferences
        btn.clicked.connect(self.on_export_profile_btn)
        hbox.addStretch()

    def on_select_writer_btn(self, btn):
        """Update the list of writers to pass to the library"""
        logger.debug("%s -> %s" % (btn.text(), btn.isChecked()))
        idx = self.lib.desc_writers.index(btn.text())
        name = self.lib.name_writers[idx]

        settings = QtCore.QSettings()

        if btn.isChecked():
            self.selected_writers.append(name)
            settings.setValue("export_single_%s" % name, True)

        else:
            settings.setValue("export_single_%s" % name, False)
            if name in self.selected_writers:
                self.selected_writers.remove(name)

    def on_export_profile_btn(self):
        logger.debug("export profiles clicked")

        if len(self.selected_writers) == 0:
            msg = "Select output formats before data export!"
            QtGui.QMessageBox.warning(self, "Export warning", msg, QtGui.QMessageBox.Ok)
            return

        settings = QtCore.QSettings()

        select_output_folder = self.selectFolder.isChecked()
        settings.setValue("select_output_folder", select_output_folder)
        if select_output_folder:

            # ask user for output folder path
            # noinspection PyCallByClass
            output_folder = QtGui.QFileDialog.getExistingDirectory(self, "Select output folder",
                                                                   settings.value("export_folder"))
            if not output_folder:
                return
        else:
            output_folder = self.lib.outputs_folder
        settings.setValue("export_folder", output_folder)
        logger.debug('output folder: %s' % output_folder)

        # CARIS-specific check for file concatenation
        for writer in self.selected_writers:

            if writer == 'caris':
                caris_path = os.path.join(output_folder, "CARIS", self.lib.current_project + ".svp")
                if os.path.exists(caris_path):
                    msg = "An existing CARIS file is present in the output folder.\n\n" \
                          "Do you want to remove it to avoid possible profile duplications?"
                    ret = QtGui.QMessageBox.question(self, "CARIS export", msg,
                                                     QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                    if ret == QtGui.QMessageBox.Yes:
                        os.remove(caris_path)
                break

        # special case for Fugro ISS format
        force_writer_instrument_for_next_casts = None
        custom_writer_instrument = None

        # actually do the export
        current_project = None
        for pk in self._pks:

            success = self.lib.load_profile(pk, skip_atlas=True)
            if not success:

                # noinspection PyCallByClass
                QtGui.QMessageBox.warning(self, "Database", "Unable to load profile #%02d!" % pk, QtGui.QMessageBox.Ok)
                continue

            # special case: synthetic profile and NCEI
            skip_export = False
            for writer in self.selected_writers:

                if writer != 'ncei':
                    continue

                if self.lib.ssp.l[0].meta.sensor_type == Dicts.sensor_types['Synthetic']:

                    msg = "Attempt to export a synthetic profile in NCEI format!"
                    QtGui.QMessageBox.warning(self, "Export warning", msg, QtGui.QMessageBox.Ok)
                    skip_export = True
                    continue

                if self.lib.current_project == 'default':

                    msg = "The 'default' project cannot be used for NCEI export.\n\n" \
                          "Rename the project in the Database tab!"
                    if self.lib.setup.noaa_tools:
                        msg += "\n\nRecommend in project_survey format, e.g. OPR-P999-RA-17_H12345"
                    QtGui.QMessageBox.warning(self, "Export warning", msg, QtGui.QMessageBox.Ok)
                    skip_export = True
                    continue

                if self.lib.setup.noaa_tools and self.lib.not_noaa_project(self.lib.current_project):
                    if self.lib.not_noaa_project(current_project):
                        current_project = self.lib.cb.ask_formatted_text(default=self.lib.noaa_project)
                        if self.lib.not_noaa_project(current_project):
                            msg = "The project name cannot be used for NCEI export.\n\n" \
                                  "Rename the project in the Database tab!\n\n" \
                                  "Recommend \"project_survey\" format, e.g. OPR-P999-RA-17_H12345"
                            QtGui.QMessageBox.warning(self, "Export warning", msg, QtGui.QMessageBox.Ok)
                            skip_export = True
                            continue

                if not self.lib.ssp.cur.meta.survey or \
                        not self.lib.ssp.cur.meta.vessel or \
                        not self.lib.ssp.cur.meta.institution:

                    msg = "Survey, vessel, and institution metadata are mandatory for NCEI export.\n\n" \
                          "To fix the issue:\n" \
                          "- Load the profile (if not already loaded)\n" \
                          "- Set the missing values using the Metadata button on the Editor tool bar\n"
                    # noinspection PyCallByClass
                    QtGui.QMessageBox.warning(self, "Export warning", msg, QtGui.QMessageBox.Ok)
                    skip_export = True
                    continue

                # special case for Fugro ISS format with NCEI format
                if self.lib.ssp.cur.meta.probe_type == Dicts.probe_types['ISS']:
                    logger.info("special case: NCEI and ISS format")

                    if force_writer_instrument_for_next_casts is None:

                        msg = "Enter the instrument type and model \n(if you don't know, leave it blank):"
                        instrument, flag = self.lib.cb.ask_text_with_flag("ISS for NCEI", msg,
                                                                          flag_label="Apply to all the next profiles")
                        logger.debug("user input for ISS: %s, %r" % (instrument, flag))
                        # if empty, we just use the sensor type
                        if instrument is None or instrument == "":
                            instrument = self.lib.ssp.cur.meta.sensor
                        if flag:  # to skip the user dialog for next casts
                            force_writer_instrument_for_next_casts = instrument
                        else:
                            force_writer_instrument_for_next_casts = None
                        custom_writer_instrument = instrument

                    else:  # user asked to apply to all the next profiles
                        custom_writer_instrument = force_writer_instrument_for_next_casts

            if skip_export:
                continue

            self.progress.start(text="Exporting profile #%02d" % pk)
            try:
                self.progress.update(value=60)
                self.lib.export_data(data_path=output_folder, data_formats=self.selected_writers,
                                     custom_writer_instrument=custom_writer_instrument)

            except RuntimeError as e:
                self.progress.end()
                msg = "Issue in exporting the data for profile #%02d.\nReason: %s" % (pk, e)
                # noinspection PyCallByClass
                QtGui.QMessageBox.critical(self, "Export error", msg, QtGui.QMessageBox.Ok)
                continue
            self.progress.end()

        # opening the output folder
        export_open_folder = self.openFolder.isChecked()
        settings.setValue("export_open_folder", export_open_folder)
        if export_open_folder:

            explore_folder(output_folder)  # open the output folder

        else:

            msg = "Profile successfully exported!"
            # noinspection PyCallByClass
            QtGui.QMessageBox.information(self, "Export profile", msg, QtGui.QMessageBox.Ok)

        self.accept()
