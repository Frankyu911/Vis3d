import os

import numpy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from mpld3 import plugins, fig_to_html, save_html, fig_to_dict
import json
import numpy as np
from scipy.interpolate import griddata

# for numpy array is not json serializable error  继承解码器
from Plot import Plot
from Plotinfo import Plotinfo
from Plotcalculate import Plotcalculate

def index(request):
    context_dict = {}

    return render(request, 'index.html', context=context_dict)


def accurateMode(request):
    context_dict = {}
    context_dict['show'] = 'no'
    return render(request, 'accurateMode.html', context=context_dict)


def accurateUpload(request):
    context_dict = {}
    if request.method == "POST":
        try:
            filename = request.FILES['file'].name
            axis = request.POST.get("axis")
            values = request.POST.get("values")
            info = Plotinfo(filename, axis)
            if info["fixedmin"] <= float(values) <= info["fixedmax"]:
                context_dict['show'] = 'yes'
                nu = float(values)
                result = Plot(filename, axis, nu)
                info = Plotinfo(filename, axis)
                context_dict['info'] = info
                context_dict['graph1'] = result
                return render(request, 'accurateMode.html', context=context_dict)
            else:
                context_dict['errorinfo'] = "The Value is out of range. The value range of the axis you choose is " + \
                                            str(info["fixedmin"]) + " to " + str(info["fixedmax"])  + \
                                            " (" + info["fixedaxis"] + ")" + '.'

                return render(request, 'accurateMode.html', context=context_dict)
        except:
            context_dict['errorinfo'] = "You selected the wrong file or entered the wrong axis or missing an input"
            return render(request, 'accurateMode.html', context=context_dict)

        else:
            return render(request, 'accurateMode.html', context=context_dict)


def compareMode(request):
    context_dict = {}
    return render(request, 'compareMode.html', context=context_dict)

def compareUpload(request):
    context_dict = {}
    if request.method == "POST":
        try:
            filename = request.FILES['file'].name
            axis = request.POST.get("axis")
            values = request.POST.get("values")
            filename_second = request.FILES['files'].name
            axis_second = request.POST.get("axiss")
            values_second = request.POST.get("valuess")
            info = Plotinfo(filename, axis)
            info_second = Plotinfo(filename, axis)
            if info["fixedmin"] <= float(values) <= info["fixedmax"] and info_second["fixedmin"] <= float(values) <= info_second["fixedmax"] :
                context_dict['show'] = 'yes'
                nu = float(values)
                nu_second = float(values_second)
                result = Plot(filename, axis, nu)
                result_second = Plot(filename_second, axis_second, nu_second)

                context_dict['info'] = info
                context_dict['info_second'] = info_second
                context_dict['graph1'] = result
                context_dict['graph2'] = result_second
                return render(request, 'compareMode.html', context=context_dict)
            else:
                context_dict['errorinfo'] = "The Value is out of range. The value range of the axis you choose is " + \
                                            str(info["fixedmin"]) + " to " + str(info["fixedmax"])  + \
                                            " (" + info["fixedaxis"] + ")" + '.'

                return render(request, 'compareMode.html', context=context_dict)
        except:
            context_dict['errorinfo'] = "You selected the wrong file or entered the wrong axis or missing an input"
            return render(request, 'compareMode.html', context=context_dict)

        else:
            return render(request, 'compareMode.html', context=context_dict)

def calculateMode(request):
    context_dict = {}
    return render(request, 'calculateMode.html', context=context_dict)

def calculateUpload(request):
    context_dict = {}
    if request.method == "POST":
        filename = request.FILES['file'].name
        x = request.POST.get("x_values")
        y = request.POST.get("y_values")
        z = request.POST.get("z_values")
        result = Plotcalculate(filename,float(x),float(y),float(z))
        print(x,y,z)
        context_dict ['show'] = 'yes'
        context_dict ['x'] = x
        context_dict ['y'] = y
        context_dict ['z'] = z
        context_dict ['result'] = str(result)
        return render(request, 'calculateMode.html', context=context_dict)

def easyMode(request):
    context_dict = {}

    return render(request, 'easyMode.html', context=context_dict)

def easyUpload(request):
    context_dict = {}
    if request.method == "POST":
        filename = request.FILES['file'].name
        axis = request.POST.get("axis")
        info = Plotinfo(filename, axis)
        zmin = info['zmin']
        zmax = info['zmax']
        context_dict['info'] = info
        y = numpy.linspace(zmin,zmax,10,endpoint=True).tolist()
        jslist = []
        for index in range(0, 9):
            context_dict['graph' + str(index)] = Plot(filename, axis, round(y[index], 2))
            jslist.append(round(y[index], 2))
        context_dict['jsl'] = jslist
    return render(request, 'easyMode.html', context=context_dict)

def home(request):
    context_dict = {}
    result = Plot('A-8x16.csv', 'y', 0.15)
    result2 = Plot('A-8x16.csv', 'y', 0.10)
    info = Plotinfo('A-8x16.csv', 'z')
    context_dict['info'] = info
    zmin = info['zmin']
    zmax = info['zmax']
    step = info['step']

    x = numpy.arange(zmin, zmax, step).tolist()
    jslist = []
    # 0到5 6个
    for index in range(0, 6):
        # print(round(nu,2))
        context_dict['graph' + str(index)] = Plot('A-8x16.csv', 'z', round(x[index], 2))
        jslist.append(round(x[index], 2))
    context_dict['jsl'] = jslist
    return render(request, 'indextwpo.html', context=context_dict)


def change(request):
    result = Plot('A-8x16.csv', 'y', 0.1)

    return HttpResponse(content=result, content_type=json, status=None)


def upload(request):
    context_dict = {}
    result = Plot('A-8x16.csv', 'y', 0.15)
    result2 = Plot('A-8x16.csv', 'y', 0.10)
    info = Plotinfo('A-8x16.csv', 'z')
    context_dict['info'] = info
    zmin = info['zmin']
    zmax = info['zmax']
    step = info['step']

    x = numpy.arange(zmin, zmax, step).tolist()
    jslist = []
    # 0到5 6个
    for index in range(0, 6):
        # print(round(nu,2))
        context_dict['graph' + str(index)] = Plot('A-8x16.csv', 'z', round(x[index], 2))
        jslist.append(round(x[index], 2))
    context_dict['jsl'] = jslist
    context_dict = {}
    if request.method == "POST":
        filename = request.FILES['file'].name
        axis = request.POST.get("axis")
        values = request.POST.get("values")
        nu = float(values)
        result = Plot(filename, axis, nu)
        context_dict['graph1'] = result
    return render(request, 'indextwpo.html', context=context_dict)


def save(request):
    context_dict = {}
    Plot('A-8x16.csv', 'y', 0.1, show=False, save=True)
    context_dict['text'] = 'save success'

    return JsonResponse(context_dict, safe=False)
#
# def ajax_add(request):
#     i1 = int(request.GET.get("i1"))
#     i2 = int(request.GET.get("i2"))
#     ret = i1 + i2
#     return JsonResponse(ret, safe=False)

# $("#b1").on("click", function () {
#             $.ajax({
#             url:"/ajax_add/",
#             type:"GET",
#             data:{"i1":$("#i1").val(),"i2":$("#i2").val()},
#             success:function (data) {
#                 $("#i3").val(data);}
#             });
#         });
