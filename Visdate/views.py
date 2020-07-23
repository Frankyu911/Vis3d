from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from mpld3 import plugins, fig_to_html, save_html, fig_to_dict
import json
import numpy as np
from scipy.interpolate import griddata

#for numpy array is not json serializable error  继承解码器
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        #检查Object类型
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def index(request):

    fixed_axis = "y"
    axis_value = 0.1
    levels=50
    amp_min=0
    amp_max=2500
    xmin=None
    xmax=None
    ymin=None
    ymax=None


    # Read from the file. Expected format: `X,Y,Z,Amplitude`
    _x,_y,_z,_amplitude = np.loadtxt('/Users/yefanyu/Desktop/ProjectWorkSpace/Vis3d/A-8x16.csv', delimiter=",").T

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

    # Create a linear space for interpolating between x and z axes values
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


    # Create new plot figure  fig是大图 ，ax是小图数组
    fig, ax = plt.subplots(nrows=1, ncols=1)


    # # Create a contour plot   填充图像， cmap 显示图级，vmin到vmax颜色浮动，cm全称表示colormap，颜色库
    cs = ax.contourf(xi, yi, amplitudei, levels=levels,cmap=plt.cm.magma, vmin=amp_min, vmax=amp_max)
    #反转x轴
    ax.invert_xaxis()
    # 设置坐标平均
    ax.axis('scaled')
    ax.set_facecolor((0.0, 0.0, 0.0))
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)

    # # Set maximum value as 30cm (0.3m)
    if fixed_axis in ["x", "X", "z", "z"]:
        ax.set_ylim(0, 0.3)


    # # Create colour bar scale for the colour map
    cbar = fig.colorbar(cs)
    cbar.ax.set_ylabel("Amplitude (Pa)")


    #save_html(fig, 'fig.html')
    #json.dumps 用于将 Python 对象编码成 JSON 字符串
    #要使用自定义的' ' JSONEncoder ' '子类(例如，一个覆盖' ' .default() ' '方法来序列化其他类型的子类
    # )，用' ' cls ' ' kwarg指定它;否则使用' ' JSONEncoder ' .json
    g1 = json.dumps(fig_to_dict(fig), cls=NumpyEncoder)
    f = open('jsondata.json', 'w')
    f.write(g1)
    f.close()


    return render(request, 'index.html', {'graph1': g1,})

def ajax_add(request):
    i1 = int(request.GET.get("i1"))
    i2 = int(request.GET.get("i2"))
    ret = i1 + i2
    return JsonResponse(ret, safe=False)

def change(request):
    fixed_axis = "y"
    axis_value = 0.05
    levels=10
    amp_min=0
    amp_max=2500
    xmin=None
    xmax=None
    ymin=None
    ymax=None


    # Read from the file. Expected format: `X,Y,Z,Amplitude`
    _x,_y,_z,_amplitude = np.loadtxt('/Users/yefanyu/Desktop/ProjectWorkSpace/Vis3d/A-8x16.csv', delimiter=",").T

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

    # Create a linear space for interpolating between x and z axes values
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


    # Create new plot figure  fig是大图 ，ax是小图数组
    fig, ax = plt.subplots(nrows=1, ncols=1)


    # # Create a contour plot   填充图像， cmap 显示图级，vmin到vmax颜色浮动，cm全称表示colormap，颜色库
    cs = ax.contourf(xi, yi, amplitudei, levels=levels,cmap=plt.cm.magma, vmin=amp_min, vmax=amp_max)
    #反转x轴
    ax.invert_xaxis()
    # 设置坐标平均
    ax.axis('scaled')
    ax.set_facecolor((0.0, 0.0, 0.0))
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)

    # # Set maximum value as 30cm (0.3m)
    if fixed_axis in ["x", "X", "z", "z"]:
        ax.set_ylim(0, 0.3)


    # # Create colour bar scale for the colour map
    cbar = fig.colorbar(cs)
    cbar.ax.set_ylabel("Amplitude (Pa)")


    #save_html(fig, 'fig.html')
    #json.dumps 用于将 Python 对象编码成 JSON 字符串
    #要使用自定义的' ' JSONEncoder ' '子类(例如，一个覆盖' ' .default() ' '方法来序列化其他类型的子类
    # )，用' ' cls ' ' kwarg指定它;否则使用' ' JSONEncoder ' .json
    g2 = json.dumps(fig_to_dict(fig), cls=NumpyEncoder)
    # f = open('jsondata.json', 'w')
    # f.write(g2)
    # f.close()

    return HttpResponse(content=g2, content_type=json,status= None)
