# encoding: utf-8

from uiutil.window.root import RootWindow
from uiutil.window.child import ChildWindow
from ..frame.dns_config_launcher import DNSConfigLauncherFrame


class _DNSConfigLauncherWindow(object):

    def __init__(self,
                 *args,
                 **kwargs):
        super(_DNSConfigLauncherWindow, self).__init__(*args,
                                                       **kwargs)

    def _setup(self):
        self.title(u'DNS Config')
        self.dynamic_frame = DNSConfigLauncherFrame(parent=self._main_frame)


class DNSConfigLauncherRootWindow(_DNSConfigLauncherWindow, RootWindow):

    def __init__(self,
                 *args,
                 **kwargs):
        super(DNSConfigLauncherRootWindow, self).__init__(*args,
                                                          **kwargs)


class DNSConfigLauncherChildWindow(_DNSConfigLauncherWindow, ChildWindow):

    def __init__(self,
                 *args,
                 **kwargs):
        super(DNSConfigLauncherChildWindow, self).__init__(*args,
                                                           **kwargs)
