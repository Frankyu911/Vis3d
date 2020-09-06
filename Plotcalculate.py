#!/usr/local/bin/python3.7

import numpy as np

def Plotcalculate(filename, x, y, z):
    # Read from the file. Expected format: `X,Y,Z,Amplitude`
    _x, _y, _z, _amplitude = np.loadtxt(filename, delimiter=",").T

    # Take the other values for the given fixed axis value
    x_axis = []
    y_axis = []
    z_axis = []
    ap = []

    # Update our internal representation of the data
    for i in range(len(_amplitude)):
        x_axis += [_x[i]]
        y_axis += [_y[i]]
        z_axis += [_z[i]]
        ap += [_amplitude[i]]

    i = 0;
    while i < len(_amplitude):
        if x_axis[i] == x:
            if y_axis[i] == y:
                if z_axis[i] == z:
                    return ap[i]
                else:
                    i += 1
                    continue
            else:
                i +=1
                continue
        else:
            i +=1
            continue



