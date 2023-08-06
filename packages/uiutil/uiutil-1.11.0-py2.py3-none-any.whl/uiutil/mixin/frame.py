# encoding: utf-8

from uiutil.helper.introspection import calling_base_frame
from ..helper.arguments import grid_and_non_grid_kwargs
from .all import AllMixIn


class FrameMixIn(AllMixIn):

    FRAME = None  # Redefine in subclass

    def _common_init(self,
                     parent=None,
                     *args,
                     **kwargs):

        self.parent= parent if parent else calling_base_frame(exclude=self)

        # Keep a list of frames added
        self._frames = []

        grid_kwargs, kwargs = grid_and_non_grid_kwargs(frame=self.parent,
                                                       **kwargs)

        # Unfortunately everything Tkinter is written in Old-Style classes so it blows up if you use super!
        self.FRAME.__init__(self, master=self.parent, **kwargs)

        kwargs.update(grid_kwargs)

        AllMixIn.__init__(self, *args, **kwargs)

    def exists(self):
        return self.winfo_exists() != 0

    def close(self):
        self.cancel_poll()
        self.close_pool()

        for frame in self._frames:
            frame.close()

    def register_frame(self,
                       frame_object):
        self._frames.append(frame_object)

    def add_frame(self,
                  frame,
                  **kwargs):
        frame_object = frame(**kwargs)
        self.regsiter_frame(frame_object)
        return frame_object
