# encoding: utf-8

import logging_helper
from uiutil.tk_names import Radiobutton
from .base_widget import BaseWidget
from ..mixin import ObservableMixIn
from ..helper.arguments import pop_kwarg

logging = logging_helper.setup_logging()


class RadioButton(BaseWidget,
                  ObservableMixIn):

    WIDGET = Radiobutton
    VAR_TYPE = u'string_var'
    VAR_PARAM = u'variable'
    VAR_IS_OPTIONAL = False
    PASS_VALUE_TO_WIDGET = True
    TEXT = u'text'
    VALUE = u'value'

    def __init__(self,
                 # value,
                 # text,
                 *args,
                 **kwargs):

        logging.warning(u"RadioButton is in-development. Don't use in production code")

        # TODO: May need to move this to BaseWidget (Button currently broken if only value supplied)
        link = kwargs.get(u'link')
        text = pop_kwarg(kwargs, self.TEXT)
        value = pop_kwarg(kwargs, self.VALUE)

        # Value for this radio button.
        # If no value is provided, use the value
        # of the provided label
        self._value = (text
                       if value is None and link is None
                       else value)

        kwargs[self.TEXT] = text
        kwargs[self.VALUE] = self._value

        super(RadioButton, self).__init__(*args,
                                          **kwargs)
        pass

    def make_associations(self,
                          kwargs):
        if self.associate:
            kwargs[u'command'] = self._state_change

    def _state_change(self,
                      _=None):
        if self.associate._link:
            self.associate._link.value = self.value

        if self._command:
            self.do_command()

        self.associate.notify_observers()

    @property
    def selected(self):
        return self.value


