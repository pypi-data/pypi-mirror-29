# encoding: utf-8

from PIL import Image, ImageTk
from logging_helper import setup_logging

from uiutil.helper.introspection import locate_calling_stack_frame_from_base_frame
from uiutil.tk_names import NORMAL, DISABLED, TclError
from ..helper.arguments import pop_kwarg, raise_on_positional_args
from ..mixin import WidgetMixIn, VarMixIn

logging = setup_logging()

READONLY = u'readonly'


class BaseWidget(WidgetMixIn,
                 VarMixIn):

    # Define WIDGET when subclassing.
    # It should be a ttk widget, e.g ttk.Button
    #
    # Define VAR_TYPE when subclassing.
    # It should be a VarMixIn type, e.g self.string_var
    #
    # Define VAR_PARAM when subclassing.
    # It should be the parameter name into WIDGET that takes the variable, e.g. textvariable

    STYLE = None
    VAR_IS_OPTIONAL = True
    DEFAULT_VALUE = None
    PASS_VALUE_TO_WIDGET = False

    def __init__(self,
                 # frame=None,
                 # value=None,
                 # command,
                 # trace=None,
                 # link=None,
                 # bind=None,
                 # allow_invalid_values=True,
                 # image=None,
                 # enabled_state=NORMAL,
                 # style=None,
                 # associate=None,
                 *args,
                 **kwargs):
        """
        No positional args are allowed.
        
        When subclassing, if validation is required, just add a staticmethod
        called validate that returns a Boolean and optionally a method called
        permit_invalid_value
        
        e.g.
        @staticmethod
        def validate(value):
            try:
                return 0 <= value <= 1000
            except:
                pass
            return False
            
        @staticmethod
        def permit_invalid_value(value):
            return len([c for c in value if c not in u'0123456789:ABCDEFabcdef']) == 0
        
        :param frame: Add the widget to this frame.
                      If not supplied, the nearest BaseFrame or BaseLabelFrame
                      in the stack will be used.
        :param value: The initial value of the variable associated with the
                      widget.  If this is not supplied, then no variable is
                      created. Use the underlying widget's parameter to set
                      a static value (e.g. text for a Label)
        :param command: a function to trigger when the widget is clicked
        :param trace: function to trigger when the variable is modified
        :param link: a persistent object that the variable will link to
        :param bind: bindings for the widget. This can be a list of bindings or a single binding.
                     Each binding must be a tuple. ("event", function)
        :param allow_invalid_values
        :param image
        :param enabled_state: default is NORMAL, can be set to other values such as 'readonly',
                              which is useful in some cases.
        :param args: NO POSITIONAL ARGS ARE ALLOWED
        :param kwargs: Parameters to pass to add_widget_and_position
        """

        try:
            self.WIDGET
        except AttributeError:
            raise NotImplementedError(u'WIDGET must be defined')

        try:
            self.VAR_TYPE
        except AttributeError:
            raise NotImplementedError(u'VAR_TYPE must be defined')

        try:
            self.VAR_PARAM
        except AttributeError:
            raise NotImplementedError(u'VAR_PARAM must be defined')

        raise_on_positional_args(self, args)

        frame = pop_kwarg(kwargs, u'frame')

        bindings = pop_kwarg(kwargs, u'bind')
        self.associate = pop_kwarg(kwargs, u'associate', self)
        self.enabled_state = pop_kwarg(kwargs, u'enabled_state', NORMAL)
        self.allow_invalid_values = pop_kwarg(kwargs, u'allow_invalid_values', True)
        self._style = pop_kwarg(kwargs, u'style', self.STYLE)

        super(BaseWidget, self).__init__(parent=frame, **kwargs)

        self.containing_frame, self._calling_stack_frame = locate_calling_stack_frame_from_base_frame(frame)

        if not self.has_association:
            self.create_variable(kwargs=kwargs)

        self.create_widget(kwargs)
        self.copy_methods_of_underlying_widgets()
        if self._style:
            self.widget.configure(style=self.style)
        self.add_bindings(bindings)
        self.register_validation()

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self,
              style):
        self._style = style

    @property
    def has_association(self):
        return self.associate is not self

    def make_associations(self,
                          kwargs):
        return None

    def create_variable(self,
                        kwargs):

        if self.VAR_TYPE is None and self.VAR_PARAM is None:
            return

        trace = pop_kwarg(kwargs, u'trace')
        self._link = pop_kwarg(kwargs, u'link')

        if self.PASS_VALUE_TO_WIDGET:
            value = kwargs.get(u'value')
        else:
            value = pop_kwarg(kwargs, u'value', self.DEFAULT_VALUE)

        if not self.VAR_IS_OPTIONAL or value is not None:
            # Declare the var
            var_type = getattr(self, self.VAR_TYPE)
            self._var = var_type(trace=trace,
                                 link=self._link,
                                 value=value)

            kwargs[self.VAR_PARAM] = self._var

    def create_widget(self,
                      kwargs):

        self._command = kwargs.get(u'command')

        self.make_associations(kwargs)

        image = pop_kwarg(kwargs, u'image')
        size = pop_kwarg(kwargs, u'size')
        if image:
            if isinstance(image, basestring):
                image = Image.open(image)
            if size:
                try:
                    image = image.resize(size)
                except Exception as e:
                    e
            image = ImageTk.PhotoImage(image)
            self.image = image
            kwargs[u'image'] = self.image

        if kwargs.get(u'tooltip') is not None:
            self.widget, self.tooltip = self.containing_frame.add_widget_and_position(
                                            widget=self.WIDGET,
                                            frame=self.containing_frame,
                                            **kwargs)
        else:
            self.widget = self.containing_frame.add_widget_and_position(
                              widget=self.WIDGET,
                              **kwargs)

    @property
    def has_tooltip(self):
        try:
            return bool(self.tooltip)
        except AttributeError:
            return False

    def set_cursor(self,
                   state=u""):
        try:
            self.config(cursor=state)
        except TclError:
            # Associated widget has probably been destroyed
            pass

    def do_command(self,
                   *args,
                   **kwargs):
        # Auto close tooltips on action

        if self.has_tooltip:
            self.tooltip.close()

        self.set_cursor(u"wait")
        try:
            self._command(*args, **kwargs)
        except Exception as e:
            self.set_cursor()
            logging.exception(e)
            raise e
        self.set_cursor()

    def copy_methods_of_underlying_widgets(self):
        # TODO: Could we do this with __getattr__ instead?
        widget_unbound_method_names = [method
                                       for method in dir(self.WIDGET)
                                       if not method.startswith(u'_') and method not in dir(self)]

        for method in widget_unbound_method_names:
             setattr(self, method, getattr(self.widget, method))

    def add_bindings(self,
                     bindings):
        if bindings:
            if not isinstance(bindings, list):
                bindings = [bindings]
            try:
                for binding in bindings:
                    if not isinstance(binding, tuple):
                        raise ValueError(u"Each binding in the list must be a tuple."
                                         u" e.g. (u'<Return>', self._bound_function)")
                    self.bind(*binding)

            except AttributeError as e:
                raise RuntimeError(u'Underlying widget does not have a bind method')

    def register_validation(self):
        try:
            self.valid
            self.widget[u'validate'] = u"key",
            self.widget[u'validatecommand'] = (self.widget.register(self.do_validation), u"%P")
        except AttributeError:
            pass  # no validation

    def do_validation(self,
                      new_value):
        # Allow a blank, otherwise it prevents deletion to the start of the field
        if new_value.strip() == u"":
            return True

        new_value_is_valid = self.valid(new_value)
        result = True if self.permit_invalid_value(new_value) else new_value_is_valid

        if result:
            self.config(foreground=u'black' if new_value_is_valid else u'red')

        return result

    def permit_invalid_value(self,
                             value):
        return self.allow_invalid_values

    @property
    def calling_stack_frame(self):
        if self._calling_stack_frame:
            return (u"Created by {func} at line {line} in {source}"
                    .format(source=self._calling_stack_frame[1],
                            func=self._calling_stack_frame[3],
                            line=self._calling_stack_frame[2]))
        return u""

    @property
    def value(self):
        try:
            return self.associate._var.get()
        except AttributeError:
            raise RuntimeError(u'No variable was declared for the {widget} widget. {calling_stack_frame}'
                               .format(widget=self.__class__.__name__,
                                       calling_stack_frame=self.calling_stack_frame))

    @value.setter
    def value(self,
              value):
        try:
            self.associate._var.set(value)
        except AttributeError:
            raise RuntimeError(u'No variable was declared for the {widget} widget. {calling_stack_frame}'
                               .format(widget=self.__class__.__name__,
                                       calling_stack_frame=self.calling_stack_frame))

    def enable(self):
        self.widget.config(state=self.enabled_state)

    def disable(self):
        self.widget.config(state=DISABLED)

    @property
    def config(self):
        return self.widget.config
