import logging


class SisParseFilter(logging.Filter):
    def filter(self, record):

        if (record.name == 'hyo.soundspeed.listener.sis.sis') and \
                (record.funcName == "parse") and \
                (record.levelname == "INFO"):

            return False

        return True


logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # change to WARNING to reduce verbosity, DEBUG for high verbosity
ch_formatter = logging.Formatter('%(levelname)-9s %(name)s.%(funcName)s:%(lineno)d > %(message)s')
ch.setFormatter(ch_formatter)
ch.addFilter(SisParseFilter())
logger.addHandler(ch)


from hyo.soundspeedmanager import gui

gui.gui()
