import os

import mpld3
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from mpld3 import plugins, fig_to_html, save_html, fig_to_dict
import json
import numpy as np
from mpld3.plugins import PointHTMLTooltip
from scipy.interpolate import griddata

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        #检查Object类型
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def Plot(filename, fixed_axis, axis_value, levels=30, amp_min=0, amp_max=2500,
         save=False, file_prefix="", show=True, xmin=None, xmax=None, ymin=None, ymax=None):
     # Check fixed_axis has a valid value
    if fixed_axis not in ["x", "y", "z", "X", "Y", "Z"]:
        print("Error: Fixed axis must be x, y or z.")
        exit(0)
    _x,_y,_z,_amplitude = np.loadtxt(os.path.dirname(__file__)+'/'+filename, delimiter=",").T
    # Count the number of measurements we have for the given fixed_axis value 返回元组,n 为选择的 行数
    if fixed_axis in ["x", "X"]:
        n = np.count_nonzero(_x == axis_value)
    elif fixed_axis in ["y", "Y"]:
        n = np.count_nonzero(_y == axis_value)
    else:
        n = np.count_nonzero(_z == axis_value)

    # Check if we have any measurements
    if n <= 0:
        print("Error: The " + fixed_axis + " axis has no measurements at " + str(axis_value) + "m.")
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

    # Create a linear space for interpolating between x and z axes values 等差数列
    xi = np.linspace(x.min() if xmin == None else xmin, x.max() if xmax == None else xmax, 1000)
    yi = np.linspace(y.min() if ymin == None else ymin, y.max() if ymax == None else ymax, 1000)


    # Interpolate the x and z axes to fill in the gaps between measurements
    amplitudei = griddata((x, y), amplitude, (xi[None,:], yi[:,None]), method='cubic')

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
    # Create new plot figure  fig是大图 ，ax是小图数组

    fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(4.8,3.6))


    # # Create a contour plot   填充图像， cmap 显示图级，vmin到vmax颜色浮动，cm全称表示colormap，颜色库
    cs = ax.contourf(xi, yi, amplitudei, levels=levels,cmap=plt.cm.magma, vmin=amp_min, vmax=amp_max)

    #反转x轴
    ax.invert_xaxis()
    # 设置坐标平均
    ax.axis('scaled')
    ax.set_facecolor((0.0, 0.0, 0.0))
    ax.set_title(title, pad=20)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)


    #
    plugins.connect(fig, plugins.MousePosition(fontsize=12))





    # # Create colour bar scale for the colour map
    cbar = fig.colorbar(cs)
    cbar.ax.set_ylabel("Amplitude (Pa)")



    if save:
        plt.savefig(file_prefix+title+".png", bbox_inches='tight',
                    dpi=300, quality=100)

    #save_html(fig, 'fig.html')
    #json.dumps 用于将 Python 对象编码成 JSON 字符串
    #要使用自定义的' ' JSONEncoder ' '子类(例如，一个覆盖' ' .default() ' '方法来序列化其他类型的子类
    # )，用' ' cls ' ' kwarg指定它;否则使用' ' JSONEncoder ' .json
    # f = open('jsondata.json', 'w')
    # f.write(g1)
    # f.close()
    if show:
        g1 = json.dumps(fig_to_dict(fig), cls=NumpyEncoder)
        return g1

