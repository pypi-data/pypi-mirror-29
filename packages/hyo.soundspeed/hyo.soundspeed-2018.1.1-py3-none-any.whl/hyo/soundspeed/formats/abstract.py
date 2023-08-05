from abc import ABCMeta, abstractmethod, abstractproperty
import logging

logger = logging.getLogger(__name__)

from hyo.soundspeed.profile.profilelist import ProfileList


class AbstractFormat(metaclass=ABCMeta):
    """ Common abstract data format """

    def __init__(self):
        self.name = self.__class__.__name__.lower()
        self.desc = "Abstract Format"  # a human-readable description
        self.version = "0.1.0"
        self._ssp = None  # profile list
        self._ext = set()
        self._project = str()
        self.multicast_support = False

        self.s = None  # settings
        self.cb = None  # callbacks

    @property
    def ssp(self):
        return self._ssp

    @ssp.setter
    def ssp(self, value):
        self._ssp = value

    @property
    def ext(self):
        return self._ext

    @property
    def driver(self):
        return "%s.%s" % (self.name, self.version)

    def init_data(self):
        """Create a new empty profile list"""
        self._ssp = ProfileList()
