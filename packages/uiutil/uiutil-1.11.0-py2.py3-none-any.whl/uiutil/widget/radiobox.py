# -*- coding: utf-8 -*-

from collections import OrderedDict

from uiutil.helper.introspection import calling_base_frame
from uiutil.tk_names import EW, NORMAL, DISABLED
from ..frame.label import BaseLabelFrame
from ..helper.arguments import pop_kwarg, pop_mandatory_kwarg, raise_on_positional_args, get_grid_kwargs
from ..mixin import VarMixIn, ObservableMixIn, WidgetMixIn


class RadioBox(VarMixIn,
               WidgetMixIn,
               ObservableMixIn):
    # TODO: Add max_rows/max_columns, same behaviour as SwitchBox

    Radiobutton = u"TRadiobutton"  # TODO: Figure out how to add to radiobutton. Need a new widget?

    def __init__(self,
                 # title,
                 # frame=None,
                 # options=None,
                 # command=None,
                 # option_parameters=None,
                 # link=None,
                 # width=None,
                 # sort=True,
                 # take_focus=None,
                 # max_columns=None,
                 # max_rows=None,
                 *args,
                 **kwargs):
        """
        There's small leap to make with labels versus objects.
        Objects can be anything hashable, which the option is associated with
        and the labels are the strings displayed. If just labels are supplied,
        the labels are used as the associated objects (This is likely to be the
        most common usage).

        Getting the state of a switch uses the associated object as a key,
        not the label (unless they're the same)

        :param title: Text for the label frame
        :param options: A list of option labels or, if the option objects
                        and labels are different, a dictionary:

                                  {"label": <switch object>,
                                   ...
                                   "label": <switch object>}

        :param link: A Persist object (or subclass). A dictionary is stored that 
                     uses the labels as keys. This is because they're strings,
                     which are easier to store than objects

        :param switch_parameters: Parameters for the individual switches, e.g.:

                                  {<switch object>: {"tooltip", "Switch for the thing"},
                                    ...
                                   <switch object>: {"tooltip", "Switch for another thing"}}
        :param width: 
        :param args: invalid. positional args are poison in BaseWidget!
        :param kwargs:
        """

        self.initialising = True

        raise_on_positional_args(self, args)
        frame = pop_kwarg(kwargs, u'frame', calling_base_frame())
        title = pop_mandatory_kwarg(kwargs, u'title')
        options = pop_mandatory_kwarg(kwargs, u'options')
        option_parameters = pop_kwarg(kwargs, u'option_parameters', {})
        self.command = pop_kwarg(kwargs, u'command')
        self.link = pop_kwarg(kwargs, u'link')
        width = pop_kwarg(kwargs, u'width')
        sort = pop_kwarg(kwargs, u'sort', True)
        take_focus = pop_kwarg(kwargs, u'take_focus')
        max_rows = pop_kwarg(kwargs, u'max_rows')
        max_columns = pop_kwarg(kwargs, u'max_columns')

        grid_kwargs = get_grid_kwargs(frame=frame,
                                      **kwargs)

        # All other kwargs are discarded.

        super(RadioBox, self).__init__(*args, **kwargs)

        # Setup a containing frame
        self.containing_frame = BaseLabelFrame(frame)

        self.containing_frame._set_title(title=title)

        # Set up object to label mapping...

        if not isinstance(options, dict):
            # Only label labels, so make a dictionary
            # using those labels as the objects
            temp = OrderedDict()

            for option in options:
                # key=label: value=label (labels and objects are the same)
                temp[option] = option

            options = temp

        if sort:
            options = OrderedDict(sorted(options.items(),
                                         key=lambda t: t[0]))

        self.options = {}

        self._var = self.string_var(link=self.link,
                                    value=None if self.link else options.keys()[0])
        if width:
            minimum_width_for_labels = max([len(option) for option in options]) + 1
            if width < minimum_width_for_labels:
                width = minimum_width_for_labels

        if max_columns and max_rows:
            max_rows = len(options)

        if max_columns is None and max_rows is None:
            max_rows = len(options) - 1
            max_columns = 0
        elif max_rows is None:
            max_columns = len(options) - 1
            max_rows = 0
        else:
            max_rows -= 1
            max_columns = len(options) - 1

        for label, option_object in iter(options.items()):

            option_params = option_parameters.get(option_object, {})

            if take_focus is not None and u'takefocus' not in option_params:
                option_params.update({u'takefocus': take_focus})

            self.options[option_object] = self.containing_frame.radiobutton(
                                               text=label,
                                               variable=self._var,
                                               value=option_object,
                                               state=NORMAL,
                                               command=self._state_change,
                                               width=width,
                                               sticky=EW,
                                               **option_params)

            if self.containing_frame.row.current == max_rows:
                self.containing_frame.column.next()
                self.containing_frame.row.start()
            elif self.containing_frame.column.current == max_columns:
                self.containing_frame.row.next()
                self.containing_frame.column.start()
            else:
                self.containing_frame.row.next()

        self.containing_frame.grid(**grid_kwargs)

    def _state_change(self,
                      _=None):
        if self.link:
            self.link.value = self.value

        if self.command:
            self.command()

        self.notify_observers()

    @property
    def selected(self):
        return self.value

    @property
    def value(self):
        return self._var.get()

    @value.setter
    def value(self,
              value):
        self._var.set(value)

    def enable(self,
               option=None):
        if option is None:
            for option in self.options.values():
                option.config(state=NORMAL)
        else:
            option.config(state=NORMAL)

    def disable(self,
                option=None):
        if option is None:
            for option in self.options.values():
                option.config(state=DISABLED)
        else:
            option.config(state=DISABLED)
