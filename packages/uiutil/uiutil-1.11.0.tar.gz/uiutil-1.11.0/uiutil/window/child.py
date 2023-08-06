# encoding: utf-8

from uiutil.tk_names import Toplevel

from ._base import BaseWindow


class ChildWindow(BaseWindow,
                  Toplevel):

    def __init__(self,
                 *args,
                 **kwargs):

        Toplevel.__init__(self)
        super(ChildWindow, self).__init__(*args, **kwargs)
        self.make_active_window()
