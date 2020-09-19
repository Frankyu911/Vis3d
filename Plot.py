import os
import matplotlib.pyplot as plt
from mpld3 import plugins, fig_to_dict
import json
import numpy as np
from scipy.interpolate import griddata


# This is a custom JSONEncoder which should be implemented for serializing the Numpy array
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        # check the type of object
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


"""
The most important visualisation script, which processes files and returns JSON file.
"""

def Plot(filename, fixed_axis, axis_value, levels=30, amp_min=0, amp_max=2500, color="magma",
         save=False, file_prefix="", show=True, xmin=None, xmax=None, ymin=None, ymax=None, figsize=(6.4, 4.8)):
    # Check fixed_axis has a valid value
    if fixed_axis not in ["x", "y", "z", "X", "Y", "Z"]:
        print("Error: Fixed axis must be x, y or z.")
        exit(0)
    _x, _y, _z, _amplitude = np.loadtxt(os.path.dirname(__file__) + '/' + filename, delimiter=",").T
    # Count the number of measurements we have for the given fixed_axis value
    if fixed_axis in ["x", "X"]:
        n = np.count_nonzero(_x == axis_value)
    elif fixed_axis in ["y", "Y"]:
        n = np.count_nonzero(_y == axis_value)
    else:
        n = np.count_nonzero(_z == axis_value)

    # Check if we have any measurements
    if n <= 0:
        exit(0)

    # Take the other values for the given fixed axis value
    x_axis = []
    y_axis = []
    amplitude = []

    # Update our internal representation of the data
    for i in range(len(_amplitude)):
        if fixed_axis in ["x", "X"]:
            if _x[i] == axis_value:
                x_axis += [_z[i]]
                y_axis += [_y[i]]
                amplitude += [_amplitude[i]]

        elif fixed_axis in ["y", "Y"]:
            if _y[i] == axis_value:
                x_axis += [_x[i]]
                y_axis += [_z[i]]
                amplitude += [_amplitude[i]]

        else:
            if _z[i] == axis_value:
                x_axis += [_x[i]]
                y_axis += [_y[i]]
                amplitude += [_amplitude[i]]

    # Convert from Python arrays to Numpy arrays
    x = np.array(x_axis)
    y = np.array(y_axis)
    amplitude = np.array(amplitude)

    # Create a linear space for interpolating between x and z axes values
    xi = np.linspace(x.min() if xmin == None else xmin, x.max() if xmax == None else xmax, 1000)
    yi = np.linspace(y.min() if ymin == None else ymin, y.max() if ymax == None else ymax, 1000)

    # Interpolate the x and z axes to fill in the gaps between measurements
    amplitudei = griddata((x, y), amplitude, (xi[None, :], yi[:, None]), method='cubic')

    # Plot the interpolated data as a contour map
    if fixed_axis in ["x", "X"]:
        xlab = "z (m)"
        ylab = "y (m)"
    elif fixed_axis in ["y", "Y"]:
        xlab = "x (m)"
        ylab = "z (m)"
    else:
        xlab = "x (m)"
        ylab = "y (m)"

    title = filename.split("/")[-1] + "-" + fixed_axis + "=" + str(axis_value) + "m"
    # Create new plot figure
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)

    # Select colour
    if color == "magma":
        colormap = plt.cm.magma
    if color == "inferno":
        colormap = plt.cm.inferno
    if color == "plasma":
        colormap = plt.cm.plasma
    if color == "viridis":
        colormap = plt.cm.viridis

    #  Create a contour plot
    cs = ax.contourf(xi, yi, amplitudei, levels=levels, cmap=colormap, vmin=amp_min, vmax=amp_max)

    ax.invert_xaxis()
    ax.axis('scaled')
    ax.set_facecolor((0.0, 0.0, 0.0))
    ax.set_title(title, pad=20)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)

    #  Connect to MousePosition Plugins
    plugins.connect(fig, plugins.MousePosition(fontsize=12))

    #  Create colour bar scale for the colour map
    cbar = fig.colorbar(cs)
    cbar.ax.set_ylabel("Amplitude (Pa)")

    if save:
        # Save to local computer
        plt.savefig(file_prefix + title + ".png", bbox_inches='tight',
                    dpi=300, quality=100)
    if show:
        # Return JSON for visualisation
        g1 = json.dumps(fig_to_dict(fig), cls=NumpyEncoder)
        return g1
