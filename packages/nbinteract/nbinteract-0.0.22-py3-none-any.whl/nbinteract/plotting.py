"""
Plot functions for nbinteract.

To test code without having to restart kernel, use:

```
import bqplot as bq
import nbinteract as nbi
import toolz.curried as tz
from importlib import reload

reload(nbi.plotting)

```
"""
import numpy as np
import bqplot as bq
import collections
import ipywidgets as widgets
import itertools
import functools
import logging
import toolz.curried as tz

from . import util

__all__ = ['hist', 'bar', 'scatter_drag', 'scatter', 'line']

PLACEHOLDER_ZEROS = np.zeros(10)
PLACEHOLDER_RANGE = np.arange(10)

DARK_BLUE = '#475A77'
GOLDENROD = '#FEC62C'

##############################################################################
# Helpers for plot options
##############################################################################

# Default plot options, copied from bqplot's default values
default_options = {
    'title': '',
    'aspect_ratio': 6.0,
    'xlabel': '',
    'ylabel': '',
    'xlim': (None, None),
    'ylim': (None, None),
    'animation_duration': 0,
    'bins': 10,
    'normalized': True,
}

options_docstring = '''options (dict): Options for the plot. Available options:

            {desc}
'''.rstrip()

option_doc = {
    'title':
        'Title of the plot',
    'aspect_ratio':
        'Aspect ratio of plot figure (float)',
    'animation_duration':
        'Duration of transition on change of data, in milliseconds.',
    'xlabel':
        'Label of the x-axis',
    'ylabel':
        'Label of the y-axis',
    'xlim':
        'Tuple containing (lower, upper) for x-axis',
    'ylim':
        'Tuple containing (lower, upper) for y-axis',
    'bins':
        'Non-negative int for the number of bins (default 10)',
    'normalized': (
        'Normalize histogram area to 1 if True. If False, plot '
        'unmodified counts. (default True)'
    ),
}


def _update_option_docstring(func, allowed, indent='    ' * 3):
    """
    Updates docstring of func, filling in appearance of {options} with a
    description of the options.

    >>> def f(): '''{options}'''
    >>> f = _update_option_docstring(f, ['title', 'xlim'])
    >>> print(f.__doc__)
    options (dict): Options for the plot. Available options:
    <BLANKLINE>
                title: Title of the plot
                xlim: Tuple containing (lower, upper) for x-axis
    <BLANKLINE>
    """
    if not (func.__doc__ and '{options}' in func.__doc__):
        return func

    descriptions = [option + ': ' + option_doc[option] for option in allowed]
    full_desc = ('\n' + indent).join(descriptions)
    func.__doc__ = func.__doc__.format(
        options=options_docstring.format(desc=full_desc)
    )
    return func


def use_options(allowed, defaults=default_options):
    """
    Decorator that logs warnings when unpermitted options are passed into its
    wrapped function. Fills in missing options with their default values if not
    present.

    Requires that wrapped function has an keyword-only argument named
    `options`. If wrapped function has {options} in its docstring, fills in
    with the docs for allowed options.

    Args:
        allowed (list str): list of option keys allowed. If the wrapped
            function is called with an option not in allowed, log a warning.
            All values in allowed must also be present in `defaults`.

    Kwargs:
        defaults (dict): Dict of default option values.

    Returns:
        Wrapped function with options validation.

    >>> @use_options(['title'])
    ... def test(*, options={}): return options['title']

    >>> test(options={'title': 'Hello'})
    'Hello'

    >>> test(options={'not_allowed': 123}) # Also logs error message
    ''
    """

    def update_docstring(f):
        _update_option_docstring(f, allowed)

        @functools.wraps(f)
        def check_options(*args, **kwargs):
            options = kwargs.get('options', {})
            not_allowed = [
                option for option in options if option not in allowed
            ]
            if not_allowed:
                logging.warning(
                    'The following options are not supported by '
                    'this function and will likely result in '
                    'undefined behavior: {}.'.format(not_allowed)
                )
            options_with_defaults = {**defaults, **options}
            kwargs_with_defaults = {**kwargs, 'options': options_with_defaults}

            return f(*args, **kwargs_with_defaults)

        return check_options

    return update_docstring


##############################################################################
# Plotting functions
##############################################################################


@use_options([
    'title', 'aspect_ratio', 'animation_duration', 'xlabel', 'ylabel', 'xlim',
    'ylim', 'bins', 'normalized'
])
def hist(hist_function, *, options={}, **interact_params):
    """
    Generates an interactive histogram that allows users to change the
    parameters of the input hist_function.

    Args:
        hist_function (Array | (*args -> Array int | Array float)):
            Function that takes in parameters to interact with and returns an
            array of numbers. These numbers will be plotted in the resulting
            histogram.

    Kwargs:
        {options}

        interact_params (dict): Keyword arguments in the same format as
            `ipywidgets.interact`. One argument is required for each argument
            of `hist_function`.

    Returns:
        VBox with two children: the interactive controls and the figure.

    >>> def gen_random(n_points):
    ...     return np.random.normal(size=n_points)
    >>> hist(gen_random, n_points=(0, 1000, 10))
    VBox(...)
    """
    params = {
        'marks': [{
            'sample': _array_or_placeholder(hist_function),
            'bins': tz.get('bins'),
            'normalized': tz.get('normalized'),
            'scales': (
                lambda opts: {'sample': opts['x_sc'], 'count': opts['y_sc']}
            ),
        }],
    }

    [hist], fig = _create_plot(marks=[bq.Hist], options=options, params=params)

    def wrapped(**interact_params):
        hist.sample = util.maybe_call(hist_function, interact_params)

    controls = widgets.interactive(wrapped, **interact_params)

    return widgets.VBox([controls, fig])


@use_options([
    'title', 'aspect_ratio', 'animation_duration', 'xlabel', 'ylabel', 'ylim'
])
def bar(x_fn, y_fn, *, options={}, **interact_params):
    """
    Generates an interactive bar chart that allows users to change the
    parameters of the inputs x_fn and y_fn.

    Args:
        x_fn (Array | (*args -> Array str | Array int | Array float)):
            If array, uses array values for categories of bar chart.

            If function, must take parameters to interact with and return an
            array of strings or numbers. These will become the categories on
            the x-axis of the bar chart.

        y_fn (Array | (Array, *args -> Array int | Array float)):
            If array, uses array values for heights of bars.

            If function, must take in the output of x_fn as its first parameter
            and optionally other parameters to interact with. Must return an
            array of numbers. These will become the heights of the bars on the
            y-axis.

    Kwargs:
        {options}

        interact_params (dict): Keyword arguments in the same format as
            `ipywidgets.interact`. One argument is required for each argument
            of both `x_fn` and `y_fn`. If `x_fn` and `y_fn` have conflicting
            parameter names, prefix the corresponding kwargs with `x__` and
            `y__`.

    Returns:
        VBox with two children: the interactive controls and the figure.

    >>> bar(['a', 'b', 'c'], [4, 7, 10])
    VBox(...)

    >>> def categories(n): return np.arange(n)
    >>> def heights(xs, offset):
    ...     return xs + offset
    >>> bar(categories, heights, n=(0, 10), offset=(1, 10))
    VBox(...)

    >>> def multiply(xs, n):
    ...     return xs * n
    >>> bar(categories, multiply, x__n=(0, 10), y__n=(1, 10))
    VBox(...)
    """
    params = {
        'marks': [{
            'x': _array_or_placeholder(x_fn, PLACEHOLDER_RANGE),
            'y': _array_or_placeholder(y_fn)
        }]
    }

    [bar], fig = _create_plot(
        x_sc=bq.OrdinalScale, marks=[bq.Bars], options=options, params=params
    )

    def wrapped(**interact_params):
        x_data = util.maybe_call(x_fn, interact_params, prefix='x')
        bar.x = x_data

        y_bound = util.maybe_curry(y_fn, x_data)
        bar.y = util.maybe_call(y_bound, interact_params, prefix='y')

    controls = widgets.interactive(wrapped, **interact_params)

    return widgets.VBox([controls, fig])


@use_options([
    'title', 'aspect_ratio', 'animation_duration', 'xlabel', 'ylabel', 'xlim',
    'ylim'
])
def scatter_drag(
    x_points: 'Array', y_points: 'Array', *, show_eqn=True, options={}
):
    """
    Generates an interactive scatter plot with the best fit line plotted over
    the points. The points can be dragged by the user and the line will
    automatically update.

    Args:
        x_points (Array Number): x-values of points to plot

        y_points (Array Number): y-values of points to plot

    Kwargs:
        show_eqn (bool): If True (default), displays the best fit line's
            equation above the scatterplot.

        {options}

    Returns:
        VBox with two children: the equation widget and the figure.

    >>> xs = np.arange(10)
    >>> ys = np.arange(10) + np.random.rand(10)
    >>> scatter_drag(xs, ys)
    VBox(...)
    """
    params = {
        'marks': [{
            'x': x_points,
            'y': y_points,
            'enable_move': True,
        }, {
            'colors': [GOLDENROD],
        }]
    }

    [scat, lin], fig = _create_plot(
        marks=[bq.Scatter, bq.Lines], options=options, params=params
    )

    equation = widgets.Label()

    # create line fit to data and display equation
    def update_line(change=None):
        x_sc = scat.scales['x']
        lin.x = [
            x_sc.min if x_sc.min is not None else np.min(scat.x),
            x_sc.max if x_sc.max is not None else np.max(scat.x),
        ]
        poly = np.polyfit(scat.x, scat.y, deg=1)
        lin.y = np.polyval(poly, lin.x)
        if show_eqn:
            equation.value = 'y = {:.2f}x + {:.2f}'.format(poly[0], poly[1])

    update_line()

    scat.observe(update_line, names=['x', 'y'])

    return widgets.VBox([equation, fig])


@use_options([
    'title', 'aspect_ratio', 'animation_duration', 'xlabel', 'ylabel', 'xlim',
    'ylim'
])
def scatter(x_fn, y_fn, *, options={}, **interact_params):
    """
    Generates an interactive scatter chart that allows users to change the
    parameters of the inputs x_fn and y_fn.

    Args:
        x_fn (Array | (*args -> Array str | Array int | Array float)):
            If array, uses array values for x-coordinates.

            If function, must take parameters to interact with and return an
            array of strings or numbers. These will become the x-coordinates
            of the scatter plot.

        y_fn (Array | (Array, *args -> Array int | Array float)):
            If array, uses array values for y-coordinates.

            If function, must take in the output of x_fn as its first parameter
            and optionally other parameters to interact with. Must return an
            array of numbers. These will become the y-coordinates of the
            scatter plot.

    Kwargs:
        {options}

        interact_params (dict): Keyword arguments in the same format as
            `ipywidgets.interact`. One argument is required for each argument
            of both `x_fn` and `y_fn`. If `x_fn` and `y_fn` have conflicting
            parameter names, prefix the corresponding kwargs with `x__` and
            `y__`.

    Returns:
        VBox with two children: the interactive controls and the figure.

    >>> def x_values(n): return np.random.choice(100, n)
    >>> def y_values(xs): return np.random.choice(100, len(xs))
    >>> scatter(x_values, y_values, n=(0,200))
    VBox(...)
    """
    params = {
        'marks': [{
            'x': _array_or_placeholder(x_fn),
            'y': _array_or_placeholder(y_fn),
        }]
    }

    [scat], fig = _create_plot(
        marks=[bq.Scatter], options=options, params=params
    )

    def wrapped(**interact_params):
        x_data = util.maybe_call(x_fn, interact_params, prefix='x')
        scat.x = x_data

        y_bound = util.maybe_curry(y_fn, x_data)
        scat.y = util.maybe_call(y_bound, interact_params, prefix='y')

    controls = widgets.interactive(wrapped, **interact_params)

    return widgets.VBox([controls, fig])


@use_options([
    'title', 'aspect_ratio', 'animation_duration', 'xlabel', 'ylabel', 'xlim',
    'ylim'
])
def line(x_fn, y_fn, *, options={}, **interact_params):
    """
    Generates an interactive line chart that allows users to change the
    parameters of the inputs x_fn and y_fn.

    Args:
        x_fn (Array | (*args -> Array str | Array int | Array float)):
            If array, uses array values for x-coordinates.

            If function, must take parameters to interact with and return an
            array of strings or numbers. These will become the x-coordinates
            of the line plot.

        y_fn (Array | (Array, *args -> Array int | Array float)):
            If array, uses array values for y-coordinates.

            If function, must take in the output of x_fn as its first parameter
            and optionally other parameters to interact with. Must return an
            array of numbers. These will become the y-coordinates of the line
            plot.

    Kwargs:
        {options}

        interact_params (dict): Keyword arguments in the same format as
            `ipywidgets.interact`. One argument is required for each argument
            of both `x_fn` and `y_fn`. If `x_fn` and `y_fn` have conflicting
            parameter names, prefix the corresponding kwargs with `x__` and
            `y__`.

    Returns:
        VBox with two children: the interactive controls and the figure.

    >>> line([1, 2, 3], [4, 7, 10])
    VBox(...)

    >>> def x_values(max): return np.arange(0, max)
    >>> def y_values(xs, sd):
    ...     return xs + np.random.normal(len(xs), scale=sd)
    >>> line(x_values, y_values, max=(10, 50), sd=(1, 10))
    VBox(...)
    """
    [line], fig = _create_plot(marks=[bq.Lines], options=options)

    def wrapped(**interact_params):
        x_data = util.maybe_call(x_fn, interact_params, prefix='x')
        line.x = x_data

        y_bound = util.maybe_curry(y_fn, x_data)
        line.y = util.maybe_call(y_bound, interact_params, prefix='y')

    controls = widgets.interactive(wrapped, **interact_params)

    return widgets.VBox([controls, fig])


##############################################################################
# Private helper functions
##############################################################################

_default_params = {
    'x_sc': {
        'min': tz.compose(tz.first, tz.get('xlim')),
        'max': tz.compose(tz.second, tz.get('xlim')),
    },
    'y_sc': {
        'min': tz.compose(tz.first, tz.get('ylim')),
        'max': tz.compose(tz.second, tz.get('ylim')),
    },
    'x_ax': {
        'label': tz.get('xlabel'),
        'scale': tz.get('x_sc'),
    },
    'y_ax': {
        'label': tz.get('ylabel'),
        'scale': tz.get('y_sc'),
        'orientation': 'vertical',
    },
    'marks': {
        'scales': lambda opts: {'x': opts['x_sc'], 'y': opts['y_sc']},
        'colors': [DARK_BLUE],
        'stroke': DARK_BLUE,
    },
    'fig': {
        'marks': tz.get('marks'),
        'axes': lambda opts: [opts['x_ax'], opts['y_ax']],
        'title': tz.get('title'),
        'max_aspect_ratio': tz.get('aspect_ratio'),
        'animation_duration': tz.get('animation_duration'),
    },
}


def _merge_with_defaults(params):
    """
    Performs a 2-level deep merge of params with _default_params with corrent
    merging of params for each mark.

    This is a bit complicated since params['marks'] is a list and we need to
    make sure each mark gets the default params.
    """
    marks_params = [
        {**default, **param}
        for default, param
        in zip(itertools.repeat(_default_params['marks']), params['marks'])
    ] if 'marks' in params else [_default_params['marks']]

    merged_without_marks = tz.merge_with(
        tz.merge, tz.dissoc(_default_params, 'marks'),
        tz.dissoc(params, 'marks')
    )

    return {**merged_without_marks, **{'marks': marks_params}}


def _create_plot(
    *,
    x_sc=bq.LinearScale,
    y_sc=bq.LinearScale,
    x_ax=bq.Axis,
    y_ax=bq.Axis,
    marks=[bq.Mark],
    fig=bq.Figure,
    options={},
    params={}
):
    """
    Initializes all components of a bqplot figure and returns resulting
    (marks, figure) tuple. Each plot component is passed in as a class.

    The plot options should be passed into options.

    Any additional parameters required by the plot components are passed into
    params as a dict of { plot_component: { trait: value, ... } }

    For example, to change the grid lines of the x-axis:
    params={ 'x_ax': {'grid_lines' : 'solid'} }

    And to give two marks different colors:
    params={
        'marks': [
            {'colors': [DARK_BLUE]},
            {'colors': [GOLDENROD]},
        ]
    }

    If the param value is a function, it will be called with the options dict
    augmented with all previously created plot elements. This permits
    dependencies on plot elements:
    params={ 'x_ax': {'scale': lambda opts: opts['x_sc'] } }
    """

    def maybe_call(maybe_fn, opts):
        if callable(maybe_fn):
            return maybe_fn(opts)
        return maybe_fn

    def call_params(component, opts):
        return {
            trait: maybe_call(val, opts)
            for trait, val in component.items()
        }

    params = _merge_with_defaults(params)

    x_sc = x_sc(**call_params(params['x_sc'], options))
    y_sc = y_sc(**call_params(params['y_sc'], options))
    options = {**options, **{'x_sc': x_sc, 'y_sc': y_sc}}

    x_ax = x_ax(**call_params(params['x_ax'], options))
    y_ax = y_ax(**call_params(params['y_ax'], options))
    options = {**options, **{'x_ax': x_ax, 'y_ax': y_ax}}

    marks = [
        mark_cls(**call_params(mark_params, options))
        for mark_cls, mark_params in zip(marks, params['marks'])
    ]
    options = {**options, **{'marks': marks}}

    fig = fig(**call_params(params['fig'], options))

    return marks, fig


def _array_or_placeholder(
    maybe_iterable, placeholder=PLACEHOLDER_ZEROS
) -> np.array:
    """
    Return maybe_iterable's contents or a placeholder array.

    Used to give bqplot its required initial points to plot even if we're using
    a function to generate points.
    """
    if isinstance(maybe_iterable, collections.Iterable):
        return np.array([i for i in maybe_iterable])
    return placeholder
