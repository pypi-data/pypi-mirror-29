# encoding: utf-8

import logging_helper
from ..tk_names import EW, NORMAL
from ..window.child import ChildWindow
from .frame import BaseFrame
from .label import BaseLabelFrame

logging = logging_helper.setup_logging()


class LauncherMixIn(object):

    def __init__(self,
                 window_class=ChildWindow,
                 *args,
                 **kwargs):
        super(LauncherMixIn, self).__init__(*args,
                                            **kwargs)

        self.subwindow_class = window_class
        self.groups = {}
        self.sub_windows = {}

    def add_launcher(self,
                     name,
                     button_text=None,
                     button_state=NORMAL,
                     # window_class=None,
                     *args,
                     **kwargs):

        self.button(text=button_text if button_text is not None else name,
                    state=button_state,
                    width=20,
                    command=lambda: self._launch_window(name=name,
                                                        *args,
                                                        **kwargs),
                    sticky=EW)

        self.row.next()

    def add_show_hide(self,
                      name,
                      button_text=None,
                      button_state=NORMAL,
                      init=True,
                      # hidden=False,
                      # window_class=None,
                      *args,
                      **kwargs):

        """ Adds a window launcher that will keep window state when closed.

        :param name:            Window Name
        :param button_text:     Test displayed on the launcher button if difrerent from name
        :param button_state:    Startup state of the button NORMAL / DISABLED
        :param init:            If True pre initialise the window.  (Hidden can be True / False)
                                If False window is initialised on first click.  (Hidden should be False)
        :param args:            
        :param kwargs:
        :return:
        """

        if init:
            self._show_hide_window(name=name,
                                   *args,
                                   **kwargs)

        self.button(text=button_text if button_text is not None else name,
                    state=button_state,
                    width=20,
                    command=lambda: self._show_hide_window(name=name,
                                                           *args,
                                                           **kwargs),
                    sticky=EW)

        self.row.next()

    def _create_window(self,
                       name,
                       window_class=None,
                       *args,
                       **kwargs):

        if window_class is None:
            window_class = self.subwindow_class

        # Add parent to window kwargs
        window_kwargs = kwargs.get(u'window_kwargs', {})
        window_kwargs[u'parent'] = self
        kwargs[u'window_kwargs'] = window_kwargs

        # Create window
        if name not in self.sub_windows:
            # Window not registered yet so lets open it
            self.sub_windows[name] = window_class(title=name,
                                                  *args,
                                                  **kwargs)

        else:
            # You should not get here!  But just in case...  Log a warning.
            logging.warning(u'Not creating window, there is already a definition for {w}'.format(w=name))

    def _launch_window(self,
                       name,
                       # window_class=None,
                       *args,
                       **kwargs):

        # Activate window
        if name not in self.sub_windows:
            # Window not registered yet so lets open it
            self._create_window(name=name,
                                *args,
                                **kwargs)

        elif not self.sub_windows[name].exists():
            # Window is registered but no longer open, so:
            # Clean it up
            self.sub_windows[name].close()
            self.sub_windows[name].destroy()
            del self.sub_windows[name]

            # Re-open it
            self._create_window(name=name,
                                *args,
                                **kwargs)

        elif self.sub_windows[name].state() == u'withdrawn':
            self.sub_windows[name].show()

        else:
            # Window is open so bring to front
            self.sub_windows[name].make_active_window()

    def _show_hide_window(self,
                          name,
                          hidden=False,
                          window_class=None,
                          *args,
                          **kwargs):

        if name not in self.sub_windows:
            # Add ensure os_closable is in window kwargs
            window_kwargs = kwargs.get(u'window_kwargs', {})
            window_kwargs[u'os_closable'] = False
            kwargs[u'window_kwargs'] = window_kwargs

            # Create window
            self._create_window(name=name,
                                window_class=window_class,
                                *args,
                                **kwargs)

            # Hide window if default is hidden
            if hidden:
                self.sub_windows[name].hide()

        else:
            if self.sub_windows[name].state() == u'withdrawn':
                self.sub_windows[name].show()

            else:
                self.sub_windows[name].hide()


class LauncherGroupFrame(LauncherMixIn,
                         BaseLabelFrame):

    def __init__(self,
                 *args,
                 **kwargs):
        super(LauncherGroupFrame, self).__init__(*args,
                                                 **kwargs)


class LauncherFrame(LauncherMixIn,
                    BaseFrame):

    def __init__(self,
                 *args,
                 **kwargs):
        super(LauncherFrame, self).__init__(*args,
                                            **kwargs)

    def add_launcher_group(self,
                           name,
                           *args,
                           **kwargs):

        self.groups[name] = LauncherGroupFrame(parent=self,
                                               title=name,
                                               *args,
                                               **kwargs)
        self.groups[name].grid(row=self.row.current,
                               column=self.column.current,
                               sticky=EW)

        self.row.next()

        return self.groups[name]

    def nice_groups(self,
                    *args,
                    **kwargs):
        for group_name, group in iter(self.groups.items()):
            group.nice_grid(*args, **kwargs)
