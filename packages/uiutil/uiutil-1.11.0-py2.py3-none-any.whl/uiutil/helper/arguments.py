# encoding: utf-8

import attr
from .introspection import calling_base_frame


ROW = u'row'
COLUMN = u'column'

GRID_KWARGS = (ROW,
               COLUMN,
               u'columnspan',
               u'rowspan',
               u'sticky',
               u'padx',
               u'pady')

START = u'start'
CURRENT = u'current'
NEXT = u'next'


@attr.s(frozen=True)
class _Position(object):
    FIRST = attr.ib(default=START)
    START = attr.ib(default=START)
    CURRENT = attr.ib(default=CURRENT)
    NEXT = attr.ib(default=NEXT)


Position = _Position()


def pop_mandatory_kwarg(kwargs,
                        key):
    try:
        return kwargs.pop(key)
    except KeyError:
        raise ValueError(u'Missing mandatory parameter "{key}"'.format(key=key))


def pop_kwarg(kwargs,
              key,
              default=None):
    try:
        return kwargs.pop(key)
    except KeyError:
        return default


def raise_on_positional_args(caller, args):
    if args:
        raise ValueError(u'positional arguments are not accepted by {c}'.format(c=caller.__class__))


def kwargs_only(f):
    def new_f(**kwargs):
        return f(**kwargs)
    return new_f


def get_grid_kwargs(frame=None,
                    **kwargs):

    grid_kwargs = {key: value
                   for key, value in iter(kwargs.items())
                   if key in GRID_KWARGS}
    if not frame:
        frame = calling_base_frame()

    try:
        default_row = frame.row.current
    except AttributeError:
        default_row = 0

    try:
        default_column = frame.column.current
    except AttributeError:
        default_column = 0

    # Don't need to set row or column in the original call
    # if it's just the current value
    grid_kwargs[ROW] = grid_kwargs.get(ROW, default_row)

    if grid_kwargs[ROW] == Position.START:
        grid_kwargs[ROW] = frame.row.start()

    elif grid_kwargs[ROW] == Position.NEXT:
        grid_kwargs[ROW] = frame.row.next()

    elif grid_kwargs[ROW] == Position.CURRENT:
        # Don't need to set CURRENT, as it's used by default,
        # but added for those why prefer to use it in their
        # calls.
        grid_kwargs[ROW] = frame.row.current

    grid_kwargs[COLUMN] = grid_kwargs.get(COLUMN, default_column)

    if grid_kwargs[COLUMN] == Position.START:
        grid_kwargs[COLUMN] = frame.column.start()

    elif grid_kwargs[COLUMN] == Position.NEXT:
        grid_kwargs[COLUMN] = frame.column.next()

    elif grid_kwargs[COLUMN] == Position.CURRENT:
        # Don't need to set CURRENT, as it's used by default,
        # but added for those why prefer to use it in their
        # calls.
        grid_kwargs[COLUMN] = frame.column.current

    return grid_kwargs


def get_non_grid_kwargs(**kwargs):
    return {k: v for k, v in iter(kwargs.items()) if k not in GRID_KWARGS}


def grid_and_non_grid_kwargs(frame=None,
                             **kwargs):
    return (get_grid_kwargs(frame=frame,
                            **kwargs),
            get_non_grid_kwargs(**kwargs))


def get_widget_kwargs(**kwargs):
        return {key: value
                for key, value in iter(kwargs.items())
                if key not in GRID_KWARGS}
