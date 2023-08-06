import numpy as np
from matplotlib.animation import TimedAnimation

from ntype import is_real_number, is_integer_valued_real
from plot import plot_2D
from indicator import Progress_Bar


from matplotlib.animation import FFMpegWriter
default_writer = FFMpegWriter(fps=20, bitrate=500, extra_args=['-vcodec','libx264'])


def estimate_global_norm_range(N_t, func, num_of_sample=10, func_args={},
                               percen_lower=1, percen_upper=99, show_progress=True):
    """Return estimated global range for 2D (pcolormesh-like) plot.

    ## Returns:
    - vmin
    - vmax
    """

    ## Check input arguments
    for arg in [N_t, num_of_sample]:
        assert is_integer_valued_real(arg)
    assert num_of_sample <= N_t
    for arg in [percen_lower, percen_upper]:
        assert is_real_number(arg)
        assert (0 <= arg) and (arg <= 100)
    assert percen_lower <= percen_upper

    assert callable(func)
    assert type(func_args) is dict

    assert type(show_progress) is bool

    sample_indices = np.random.randint(0, N_t-1, num_of_sample)

    if show_progress:
        progress_bar = Progress_Bar(num_of_sample)
    uppers = []
    lowers = []

    for idx, sample_index in enumerate(sample_indices):
        frame_data = func(sample_index, **func_args)
        lowers.append(np.percentile(frame_data, percen_lower))
        uppers.append(np.percentile(frame_data, percen_upper))
        if show_progress:
            progress_bar.print(idx)

    vmin = np.percentile(lowers, percen_lower)
    vmax = np.percentile(uppers, percen_upper)

    return vmin, vmax


def process_frames_argument(frames):
    """
    Check and process 'frames' argument
    into a proper iterable for an animation object

    ## Arguments
    # frames
    : a seed for an integer-type iterable that is used as a sequence of frame indices
    - if integer or integer-valued float (e.g. 1.0):
        The 'frames' is interpreted as the number of total frames
        and the sequence frame indices becomes [ 0, 1, 2, ..., 'frames' - 1 ]
        which is equivalent to range('frames').
    - if array-like:
        All elements in 'frames' should be integer or integer-valued float.
        Then, the 'frames' itself is used as a sequence of frame indices.
    """

    result = None
    if np.iterable(frames):
        try: frames_arr = np.array(frames)
        except: raise TypeError("'frames' should be convertable to numpy.array")
        for idx in range(len(frames_ndarr)):
            frame_idx = frames_arr[idx]
            assert is_real_number(frame_idx)
            assert int(frame_idx) == frame_idx
            frames_arr[idx] = int(frame_idx)
        #self.frames = frames_arr
        result = frames_arr
    elif is_real_number(frames):
        assert int(frames) == frames
        frames = int(frames)
        #self.frames = range(frames)
        result = range(frames)

    return result


class Animate_2D(TimedAnimation):
    def __init__(self, X_mesh, Y_mesh, func, frames, func_args={}, **plot_kwargs):

        assert type(func_args) is dict
        self.func_args = func_args

        assert callable(func)
        self.func = func

        self.frames = process_frames_argument(frames)
        self.num_of_frames = len(self.frames)

        self.fig, self.ax, self.pcm = plot_2D(X_mesh, Y_mesh, C=None, **plot_kwargs)

        super().__init__(self.fig, blit=True)

    def _init_draw(self):
        self.progress_bar = Progress_Bar(self.num_of_frames)

    def _draw_frame(self, idx):
        C = self.func(idx, **self.func_args)
        self.pcm.set_array(C.ravel(order='C'))
        self.progress_bar.print(idx)

    def new_frame_seq(self):
        return self.frames

    def save(self, *args, **kwargs):
        """Save animation into a movie file.

        [NOTE] If 'writer' is not specified, default writer defined in this module
        will be used to generate the movie file.

        [TODO] Implement docstring inheritance.
        """
        writer = None
        if 'writer' in kwargs.keys():
            writer = kwargs.pop('writer')
        else: writer = default_writer
        super().save(*args, **kwargs, writer=writer)
