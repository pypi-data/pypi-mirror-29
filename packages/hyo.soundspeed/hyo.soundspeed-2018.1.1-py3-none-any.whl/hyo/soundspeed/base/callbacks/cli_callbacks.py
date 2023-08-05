from datetime import datetime, timedelta
import os
import logging

logger = logging.getLogger(__name__)

from hyo.soundspeed.base.callbacks.abstract_callbacks import AbstractCallbacks


class CliCallbacks(AbstractCallbacks):
    """CLI-based callbacks"""

    def __init__(self, sis_listener=None):
        super(CliCallbacks, self).__init__(sis_listener=sis_listener)

    def ask_number(self, title="", msg="Enter number", default=0.0,
                   min_value=-2147483647.0, max_value=2147483647.0, decimals=7):
        val = None
        while val is None:
            raw = input(msg)
            # print(raw)
            if raw == "":
                break
            try:
                testval = float(raw)
            except ValueError as e:
                logger.info("invalid input: %s\n" % e)
                continue

            if (testval > max_value) or (testval < min_value):
                logger.info("invalid value, use range [%f/%f]: %s" % (min_value, max_value, raw))
                continue
            else:
                val = testval
        return val

    def ask_text(self, title="", msg="Enter text"):
        val = input(msg)
        return val

    def ask_text_with_flag(self, title="", msg="Enter text", flag_label=""):
        """Ask user for text with a flag optional"""
        val = input(msg)
        val2 = input("%s? Y for Yes, otherwise No" % flag_label)
        flag = val2.lower() == "y"
        return val, flag

    def ask_date(self):
        """Ask user for date"""
        now = datetime.utcnow()
        date_msg = "Enter date as DD/MM/YYYY [default: %s]:" % now.strftime("%d/%m/%Y")
        time_msg = "Enter time as HH:MM:SS [default: %s]:" % now.strftime("%H:%M:%S")
        dt = None

        # date
        while True:
            raw = input(date_msg)
            # print(raw)
            if raw == "":
                dt = datetime(year=now.year, month=now.month, day=now.day)
                break

            try:
                dt = datetime.strptime(raw, "%d/%m/%Y")
                break

            except ValueError as e:
                logger.info("invalid input: %s\n" % e)
                continue

        # time
        while True:
            raw = input(time_msg)
            # print(raw)
            if raw == "":
                dt += timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
                break

            try:
                in_time = datetime.strptime(raw, "%H:%M:%S")
                dt += timedelta(hours=in_time.hour, minutes=in_time.minute,
                                seconds=in_time.second)
                break

            except ValueError as e:
                logger.info("invalid input: %s\n" % e)
                continue

        return dt

    def ask_location(self, default_lat=43.13555, default_lon=-70.9395):
        """Ask user for location"""

        try:
            _ = float(default_lat)
            _ = float(default_lon)

        except Exception:
            default_lat = 43.13555
            default_lon = -70.9395

        lat_msg = "Enter latitude as DD.DDD [default: %s]:" % default_lat
        lon_msg = "Enter longitude as DD.DDD [default: %s]:" % default_lon

        # lat
        lat = None
        while True:
            raw = input(lat_msg)
            # print(raw)
            if raw == "":
                break
            try:
                lat = float(raw)
                if (lat > 90) or (lat < -90):
                    logger.info("invalid latitude range [90/-90]: %s" % lat)
                    continue
                break
            except ValueError as e:
                logger.info("invalid input: %s\n" % e)
                continue

        # lon
        lon = None
        while True:
            raw = input(lon_msg)
            # print(raw)
            if raw == "":
                break
            try:
                lon = float(raw)
                if (lon > 180) or (lon < -180):
                    logger.info("invalid longitude range [180/-180]: %s" % lon)
                    continue
                break
            except ValueError as e:
                logger.info("invalid input: %s\n" % e)
                continue

        return lat, lon

    def ask_filename(self, saving=True, key_name=None, default_path=".",
                     title="Choose a path/filename", default_file="",
                     file_filter="All Files|*.*", multi_file=False):
        raw = " "
        if not saving:
            filemsg = "Enter existing filename:"
        else:
            filemsg = "Enter filename:"
        while raw == " " or (os.path.exists(raw) and raw != ""):
            raw = input(filemsg)
        return os.path.normpath(raw)

    def ask_directory(self, key_name=None, default_path=".",
                      title="Browse for folder", message=""):
        return os.path.normpath("c:/test/")

    def ask_location_from_sis(self):
        """Ask user whether retrieving location from SIS"""
        bool_msg = "Geographic location required for pressure/depth conversion and atlas lookup.\n" \
                   "Use geographic position from SIS?\'y' for yes, other inputs to enter position manually."

        raw = input(bool_msg)
        # print(raw)
        if (raw == "Y") or (raw == "y"):
            return True
        return False

    def ask_tss(self):
        """Ask user for transducer sound speed"""
        tss = 1500.0
        tss_msg = "Enter transducer sound speed in m/sec [default: %s]:" % tss

        # lat
        while True:
            raw = input(tss_msg)
            # print(raw)
            if raw == "":
                break
            try:
                tss = float(raw)
                if (tss > 2000) or (tss < 1000):
                    logger.info("invalid sound speed value: %s" % tss)
                    continue
                break
            except ValueError as e:
                logger.info("invalid input: %s\n" % e)
                continue

        return tss

    def ask_draft(self):
        """Ask user for draft"""
        draft = 8.0
        draft_msg = "Enter transducer draft in m [default: %s]:" % draft

        # lat
        while True:
            raw = input(draft_msg)
            # print(raw)
            if raw == "":
                break
            try:
                draft = float(raw)
                if (draft > 1000) or (draft < -1000):
                    logger.info("invalid draft value: %s" % draft)
                    continue
                break
            except ValueError as e:
                logger.info("invalid input: %s\n" % e)
                continue

        return draft

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
