from datetime import datetime
import os
import random
import logging

logger = logging.getLogger(__name__)

from hyo.soundspeed.base.callbacks.abstract_callbacks import AbstractCallbacks


class TestCallbacks(AbstractCallbacks):
    """Used only for testing since the methods do not require user interaction"""

    def __init__(self, sis_listener=None):
        super(TestCallbacks, self).__init__(sis_listener=sis_listener)

    def ask_number(self, title="", msg="Enter number", default=0.0,
                   min_value=-2147483647.0, max_value=2147483647.0, decimals=7):
        return random.random() * 100.0

    def ask_text(self, title="", msg="Enter text"):
        return "Hello world"

    def ask_text_with_flag(self, title="", msg="Enter text", flag_label=""):
        return "Hello world", True

    def ask_date(self):
        return datetime.utcnow()

    def ask_location(self, default_lat=43.13555, default_lon=-70.9395):
        try:
            _ = float(default_lat)
            _ = float(default_lon)

        except Exception:
            default_lat = 43.13555
            default_lon = -70.9395

        return default_lat + random.random(), default_lon + random.random()

    def ask_filename(self, saving=True, key_name=None, default_path=".",
                     title="Choose a path/filename", default_file="",
                     file_filter="All Files|*.*", multi_file=False):
        return os.path.normpath(__file__)

    def ask_directory(self, key_name=None, default_path=".",
                      title="Browse for folder", message=""):
        return os.path.normpath(os.path.dirname(__file__))

    def ask_location_from_sis(self):
        return True

    def ask_tss(self):
        return 1500.0

    def ask_draft(self):
        return 8.0

    def msg_tx_no_verification(self, name, protocol):
        """Profile transmitted but not verification available"""
        pass

    def msg_tx_sis_wait(self, name):
        """Profile transmitted, SIS is waiting for confirmation"""
        pass

    def msg_tx_sis_confirmed(self, name):
        """Profile transmitted, SIS confirmed"""
        pass

    def msg_tx_sis_not_confirmed(self, name, ip):
        """Profile transmitted, SIS not confirmed"""
        pass
