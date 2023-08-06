# encoding: utf-8

from uiutil.tk_names import Tk

from ._base import BaseWindow
from ..mixin.menubar import MenuBarMixIn


class RootWindow(BaseWindow,
                 MenuBarMixIn,
                 Tk):

    def __init__(self,
                 *args,
                 **kwargs):

        Tk.__init__(self)
        super(RootWindow, self).__init__(*args, **kwargs)
        self.make_active_application()

        self.mainloop()


class Standalone(RootWindow):

    def __init__(self,
                 frame,
                 title=None,
                 **kwargs):
        self.frame = frame
        self._title = title
        self.kwargs = kwargs
        super(Standalone, self).__init__(**kwargs)

    def _setup(self):
        self.title(self._title
                   if self._title is not None
                   else u"Standalone {frame}".format(frame=self.frame.__name__))
        self.frame = self.frame(**self.kwargs)


def standalone(frame,
               title=None,
               **kwargs):
    Standalone(frame=frame,
               title=title,
               **kwargs)
