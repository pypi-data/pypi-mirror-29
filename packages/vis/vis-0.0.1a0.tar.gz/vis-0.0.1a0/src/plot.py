import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams, axes
from matplotlib.figure import Figure
from matplotlib.colors import Normalize, LogNorm, SymLogNorm, is_color_like
from matplotlib.animation import TimedAnimation

from sys import stdout

from ntype import is_real_number


def augment_polar_mesh_for_colormesh(r_values, theta_values):
    """
    Returns polar mesh for matplotlib.pyplot.pcolormesh() in polar coordinates.

    polar coordinates of data points -> polar mesh for colormesh
    polar coordinates is assumed to be equidistanced in a sense that
    the r_values and theta_values are assumed to be equally-spaced.
    """

    N_r = len(r_values)
    N_theta = len(theta_values)

    delta_r = (r_values[-1] - r_values[0]) / (N_r - 1)
    delta_theta = (theta_values[-1] - theta_values[0]) / (N_theta - 1)

    mesh_r_values = (np.arange(N_r + 1) - 0.5) * delta_r
    mesh_r_values[0] = 0
    mesh_theta_values = (np.arange(N_theta + 1) - 0.5) * delta_theta

    mesh_R, mesh_Theta = np.meshgrid(mesh_r_values, mesh_theta_values, indexing='ij')

    return mesh_R, mesh_Theta


def construct_polar_mesh_for_colormesh(r_values, theta_values):
    """
    Returns polar mesh for matplotlib.pyplot.pcolormesh() in Cartesian coordinates

    polar coordinates of data points -> polar mesh for colormesh
    polar coordinates is assumed to be equidistanced in a sense that
    the r_values and theta_values are assumed to be equally-spaced.
    """

    mesh_R, mesh_Theta = augment_polar_mesh_for_colormesh(r_values, theta_values)

    mesh_X = mesh_R * np.cos(mesh_Theta)
    mesh_Y = mesh_R * np.sin(mesh_Theta)

    return mesh_X, mesh_Y


def set_global_fontsize_from_fig(fig, scale=1.5):
    """
    Set matplotlib.rcParams['font.size'] value so that
    all texts on a plot would look nice in terms of fontsize.

    [NOTE] The formula for the font size is:

    fontsize = sqrt(fig_area) * 'scale'

    where fig_area = fig_height * fig_width (in inch)
    """

    fig_size_inch = fig.get_size_inches()
    fig_size_len_geom_mean = (fig_size_inch[0] * fig_size_inch[1]) ** 0.5
    rcParams['font.size'] = fig_size_len_geom_mean * scale
    return rcParams['font.size']


def is_axes(obj):
    return axes._base._AxesBase in type(obj).mro()

def is_figure(obj):
    return Figure in type(obj).mro()

def is_norm(obj):
    return Normalize in type(obj).mro()


def process_fig_and_ax_argument(fig, ax, default_figsize=None):
    """Process 'fig' and 'ax' arguments.

    'fig' is of type: 'matplotlib.figure.Figure' (or its child object)
    'ax' is of type: 'matplotlib.axes._base._AxesBase' (or its child object)

    'fig' and 'ax' should be simultaneously None or of respective proper type.
    """
    if default_figsize is not None:
        assert type(default_figsize) in [tuple, list]
        assert len(default_figsize) == 2

    if (fig is None) and (ax is None):
        fig, ax = plt.subplots(figsize=default_figsize)
    else:
        assert (is_figure(fig)) and (is_axes(ax))
    return fig, ax


def check_limit_argument(arg):

    if arg is not None:
        try: arg = list(arg)
        except:
            raise TypeError("argument(=%s) should be convertable to list" % str(arg))

        assert len(arg) == 2


def get_ylim(data):
    mid_lower_percentile = 1
    mid_upper_percentile = 99

    p_000 = data.min()
    p_001 = np.percentile(data,mid_lower_percentile)
    p_099 = np.percentile(data,mid_upper_percentile)
    p_100 = data.max()

    ## Set width of each percentile spacing
    ## .. the larger the width, the range of data that corresponds
    ## .. to that percentile spacing is wide
    ## e.g. if the data values are uniformly distributed, say, from 0 to 1000,
    ## .. the p_000 = 0, p_001 = 10, p_099 = 990, p_100 = 1000
    ## .. thus from_000_to_001 = p_001 - p_000 = 10 - 0 = 10 and so on.
    from_000_to_001 = p_001 - p_000
    from_001_to_099 = p_099 - p_001
    from_099_to_100 = p_100 - p_099

    ## Define default values of data's minimum and maximum value
    # For data with singular point where the data value(s) diverge(s),
    # .. the data value range shouldn't be from minimum to maximum
    # .. since minimum and/or maximum would be so large or so small
    # .. so that most of the other, non-singular points would be invisible
    # In order to determine whether the input data's plotting ragne should be
    # .. adjusted for the singular or near-singular (so large values for only few point(s)),
    # .. the width of data values from minimum to some small fraction of percentile
    # .. or from maximum to some slightly small percentile
    # .. and majority of values range are compared.
    # .. (e.g. compare from_000_to_001 and 'from_001_to_099'.
    # .. If 'from_000_to_001' is too large than 'from_001_to_099'
    # .. then, it is likely that the there's a (near) singular value(s)
    # .. that diverges in negative direction)
    # e.g. For data whose values are uniformly distributed from 0 to 1000,
    # .. 'from_000_to_001' = 10 - 0 = 10, 'from_001_to_099' = 990 - 10 = 980
    # .. thus, ratio = 'from_001_to_099' / 'from_000_to_001' = 98
    # .. however, for data whose 'ratio' is much smaller than 98
    # .. is likely to have (near) singular point whose value(s) diverge(s) toward negative direction
    ratioMinimum = 1e-2 * (mid_upper_percentile - mid_lower_percentile)

    assert from_001_to_099 != 0
    if (from_000_to_001 / from_001_to_099 > 1.0 / ratioMinimum): y_min = p_001
    else: y_min = p_000 - 0.1 * from_001_to_099
    if (from_099_to_100 / from_001_to_099 > 1.0 / ratioMinimum): y_max = p_099
    else: y_max = p_100 + 0.1 * from_001_to_099

    return y_min, y_max




def plot_1D(x, y, *input_plot_args, fig=None, ax=None, xlabel='', ylabel='', xlim=None, ylim=None, title='',
            figsize=None, mathtext_fontset='stix', font_size_scale=2.0, ax_color=None, **input_plot_kwargs):

    ## Process input arguments
    #
    # Process 'x', 'y'
    try: x = np.array(x)
    except: raise Exception("'x' should be plottable object")
    try: y = np.array(y)
    except: raise Exception("'y' should be plottable object")

    for arg in [x, y]:
        assert type(arg) is np.ndarray
        assert arg.ndim == 1
    #if hasattr(x, 'shape') and hasattr(y, 'shape'):
    assert x.shape == y.shape
    #
    # Process 'ax' and 'fig'
    fig, ax = process_fig_and_ax_argument(fig, ax, default_figsize=figsize)
    #
    # Process limit-like objects
    for arg in [xlim, ylim]: check_limit_argument(arg)
    #
    # Process labels
    for arg in [xlabel, ylabel]: assert type(arg) is str
    #
    assert type(mathtext_fontset) is str
    #
    if ax_color is not None: assert is_color_like(ax_color)

    ## Set appropriate fontsize system (e.g. 'medium', 'large', 'x-large' etc.)
    set_global_fontsize_from_fig(fig, font_size_scale)
    rcParams['mathtext.fontset'] = mathtext_fontset

    ## Determine ylim
    if ylim is None:
        try: ylim = get_ylim(y)
        except: ylim = (None, None)

    ## Determine xlim
    if xlim is None:
        if x.size != 0:
            xlim = (x.min(), x.max())
        else:
            xlim = (None, None)

    if ax_color is None: ax_color = (0,0,0,1)
    ax_plot_kwargs = {}
    if 'color' not in input_plot_kwargs.keys():
        ax_plot_kwargs['color'] = ax_color

    # values in 'ax_plot_kwargs' will be overided by 'input_plot_kwargs' if there's any collision
    plot_kwargs = {**ax_plot_kwargs, **input_plot_kwargs}

    line, = ax.plot(x, y, *input_plot_args, **plot_kwargs)

    ax.set_ylim(*ylim)
    ax.tick_params(axis='y', labelsize='x-large', colors=ax_color)
    ax.set_ylabel(ylabel, fontsize='xx-large', color=ax_color)

    ax.set_xlim(*xlim)
    ax.tick_params(axis='x', labelsize='x-large')
    ax.set_xlabel(xlabel, fontsize='xx-large')

    return fig, ax, line




def plot_2D(X_mesh, Y_mesh, C=None, fig=None, ax=None, x_label='', y_label='', color_label='',
            xlim=None, ylim=None, vmin=None, vmax=None, log_scale=False, linthresh=None, linscale=None,
            title='', pcolormesh_kwargs={}, figsize=None):

    ## Check input arguments and assign into member variables if needed.
    for arg in [X_mesh, Y_mesh]:
        assert type(arg) is np.ndarray
        assert arg.ndim == 2
    assert X_mesh.shape == Y_mesh.shape
    mesh_shape = X_mesh.shape  # Equivalent to Y_mesh.shape if X_mesh.shape == Y_mesh.shape

    expected_C_shape = tuple(np.array(mesh_shape) - 1)
    if C is None:
        C = np.zeros(expected_C_shape)
    else:
        assert type(C) is np.ndarray
        assert C.shape == expected_C_shape

    # Process 'ax' and 'fig'
    fig, ax = process_fig_and_ax_argument(fig, ax, default_figsize=figsize)
    # if (fig is None) and (ax is None):
    #     fig, ax = plt.subplots(figsize=(8,6))
    # else:
    #     assert (is_figure(fig)) and (is_axes(ax))

    assert type(log_scale) is bool

    # Process limit-like objects
    for arg in [xlim, ylim]: check_limit_argument(arg)
    # for arg in [xlim, ylim]:
    #     if arg is not None:
    #         try: arg = list(arg)
    #         except:
    #             raise TypeError("'xlim', 'ylim' should be convertable to list")
    #         assert len(arg) == 2

    for arg in [vmin, vmax]:
        if arg is not None: assert is_real_number(arg)

    C_min, C_max = C.min(), C.max()
    vmin_given, vmax_given = vmin, vmax
    if vmin is None: vmin = C_min
    #else: assert vmin >= C_min
    if vmax is None: vmax = C_max
    #else: assert vmax <= C_max

    assert vmin <= vmax

    assert type(pcolormesh_kwargs) is dict


    ## Initial Settings for appearence
    set_global_fontsize_from_fig(fig, scale=1.5)
    rcParams['mathtext.fontset'] = 'stix'


    ## Set a normalization function
    norm = None
    if 'norm' in pcolormesh_kwargs.keys():
        norm_given = pcolormesh_kwargs.pop('norm')
        assert is_norm(norm_given)
        norm = norm_given
        if norm.vmin is None: norm.vmin = vmin
        else:
            if vmin_given is not None:
                if vmin_given != norm.vmin:
                    raise Exception("given norm's vmin and given vmin are different.")
        if norm.vmax is None: norm.vmax = vmax
        else:
            if vmax_given is not None:
                if vmax_given != norm.vmax:
                    raise Exception("given norm's vmax and given vmax are different.")
    elif log_scale:
        if vmin > 0:
            norm = LogNorm(vmin=vmin, vmax=vmax)
        else:
            # Set 'linscale' argument
            if linscale is None: linscale = 1.0
            else:
                assert is_real_number(linscale)
                assert linscale > 0
            # Set 'linthresh' argument
            min_radius = min(map(abs, [vmin, vmax]))
            if linthresh is not None:
                assert is_real_number(linthresh)
                assert (linthresh > 0) and (linthresh < min_radius)
            else:
                linthresh = 0.1 * linscale * min_radius

            #print('vmin, vmax: ',vmin, vmax)
            #print('linthresh, linscale: ', linthresh, linscale)

            # Instantiate 'SymLogNorm'
            norm = SymLogNorm(linthresh=linthresh, linscale=linscale, vmin=vmin, vmax=vmax)
    else: norm = Normalize(vmin=vmin, vmax=vmax)

    pcm = ax.pcolormesh(X_mesh, Y_mesh, C, norm=norm, **pcolormesh_kwargs)

    cb = fig.colorbar(pcm, ax=ax)

    ax.tick_params(axis='both', labelsize='large')
    cb.ax.tick_params(axis='y', labelsize='large')

    ax.axis('square')

    if xlim is None: xlim = (X_mesh.min(), X_mesh.max())
    ax.set_xlim(*xlim)
    if ylim is None: ylim = (Y_mesh.min(), Y_mesh.max())
    ax.set_ylim(*ylim)

    ax.set_title(title, fontsize='xx-large')
    ax.set_xlabel(x_label, fontsize='xx-large')
    ax.set_ylabel(y_label, fontsize='xx-large')
    cb.set_label(color_label, fontsize='xx-large', rotation=270, va='bottom')

    return fig, ax, pcm
