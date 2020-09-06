import numpy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from Plot import Plot
from Plotinfo import Plotinfo
from Plotcalculate import Plotcalculate

def index(request):
    context_dict = {}

    return render(request, 'index.html', context=context_dict)

def about(request):
    context_dict = {}
    return render(request, 'about.html', context=context_dict)

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
            info = Plotinfo(filename, axis, axis_value=values)
            if info["fixedmin"] <= float(values) <= info["fixedmax"]:
                context_dict['show'] = 'yes'
                nu = float(values)
                result = Plot(filename, axis, nu)
                context_dict['info'] = info
                context_dict['graph1'] = result
                return render(request, 'accurateMode.html', context=context_dict)
            else:
                context_dict['errorinfo'] = "The Value is out of range. The value range of the axis you choose is " + \
                                            str(info["fixedmin"]) + " to " + str(info["fixedmax"])  + \
                                            " (" + info["fixedaxis"] + ")" + '.'

                return render(request, 'accurateMode.html', context=context_dict)
        except:
            context_dict['errorinfo'] = "You selected the wrong file or entered the wrong axis or missed an input"
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
            info = Plotinfo(filename, axis,values)
            info_second = Plotinfo(filename_second, axis_second,values_second)
            context_dict['show'] = 'yes'
            nu = float(values)
            nu_second = float(values_second)
            result = Plot(filename, axis, nu,figsize=(4.5,3.8))
            result_second = Plot(filename_second, axis_second, nu_second,figsize=(4.5,3.8))
            context_dict['info'] = info
            context_dict['info_second'] = info_second
            context_dict['graph1'] = result
            context_dict['graph2'] = result_second
            return render(request, 'compareMode.html', context=context_dict)

        except:
            context_dict['errorinfo'] = "You selected the wrong file or entered the wrong axis or missing an input"
            return render(request, 'compareMode.html', context=context_dict)



def calculateMode(request):
    context_dict = {}
    return render(request, 'calculateMode.html', context=context_dict)

def calculateUpload(request):
    context_dict = {}
    try:
        if request.method == "POST":
            filename = request.FILES['file'].name
            x = request.POST.get("x_values")
            y = request.POST.get("y_values")
            z = request.POST.get("z_values")
            result = Plotcalculate(filename,float(x),float(y),float(z))

            context_dict ['filename'] = str(filename)
            context_dict ['show'] = 'yes'
            context_dict ['x'] = x
            context_dict ['y'] = y
            context_dict ['z'] = z
            if result == None:
                context_dict ['result'] = "No result"
            else:
                context_dict ['result'] = str(result)
            return render(request, 'calculateMode.html', context=context_dict)
    except:
            context_dict['errorinfo'] = "You selected the wrong file or entered the wrong axis or missing an input"
            return render(request, 'calculateMode.html', context=context_dict)
def easyMode(request):
    context_dict = {}
    context_dict['show'] = 'no'
    return render(request, 'easyMode.html', context=context_dict)

def easyUpload(request):
    context_dict = {}
    if request.method == "POST":
        try:
            filename = request.FILES['file'].name
            axis = request.POST.get("axis")
            info = Plotinfo(filename, axis)
            zmin = info['zmin']
            zmax = info['zmax']
            context_dict['info'] = info
            context_dict['filename'] = str(request.POST)
            y = numpy.linspace(zmin,zmax,10,endpoint=True).tolist()
            jslist = []
            context_dict['show'] = 'yes'
            for index in range(0, 10):
                context_dict['graph' + str(index)] = Plot(filename, axis, round(y[index], 2))
                jslist.append(round(y[index], 2))
                print(index)
            context_dict['jsl'] = jslist
            return render(request, 'easyMode.html', context=context_dict)
        except:
            context_dict['errorinfo'] = "Please upload the correct file and choose a valid axis"
            return render(request, 'easyMode.html', context=context_dict)


def save(request):
    try:
        context_dict = {}
        filename=request.GET.get("filename")
        value=request.GET.get("value")
        axis=request.GET.get("axis")
        info=Plotinfo(filename,axis,value)
        color=request.GET.get("color")
        if color=="":
            color="magma"
        amax=request.GET.get("amax")
        if amax=="":
            amax=2500
        amin=request.GET.get("amin")
        if amin=="":
            amin=0
        level=request.GET.get("level")
        if level == "":
            level=30
        xmax=request.GET.get("xmax")
        if xmax == "":
            xmax=info['xmax']
        xmin=request.GET.get("xmin")
        if xmin == "":
            xmin=info['xmin']
        ymax=request.GET.get("ymax")
        if ymax == "":
            ymax=info['ymax']
        ymin=request.GET.get("ymin")
        if ymin == "":
            ymin=info['ymin']
        result = Plot(filename, axis, float(value),levels=int(level),color=color,amp_max=int(amax),
                      amp_min=int(amin),xmax=float(xmax),xmin=float(xmin),ymax=float(ymax),ymin=float(ymin),save=True)
        context_dict['text'] = 'Save success （To local folder）'
        return JsonResponse(context_dict, safe=False)
    except:
        context_dict = {}
        context_dict['text'] = 'Save failed, please enter the correct information!'
        return JsonResponse(context_dict, safe=False)



def update(request):
    try:
        filename=request.GET.get("filename")
        value=request.GET.get("value")
        axis=request.GET.get("axis")
        info=Plotinfo(filename,axis,value)
        color=request.GET.get("color")
        if color=="":
            color="magma"
        amax=request.GET.get("amax")
        if amax=="":
            amax=2500
        amin=request.GET.get("amin")
        if amin=="":
            amin=0
        level=request.GET.get("level")
        if level == "":
            level=30
        xmax=request.GET.get("xmax")
        if xmax == "":
            xmax=info['xmax']
        xmin=request.GET.get("xmin")
        if xmin == "":
            xmin=info['xmin']
        ymax=request.GET.get("ymax")
        if ymax == "":
            ymax=info['ymax']
        ymin=request.GET.get("ymin")
        if ymin == "":
            ymin=info['ymin']
        result = Plot(filename, axis, float(value),levels=int(level),color=color,amp_max=int(amax),
                      amp_min=int(amin),xmax=float(xmax),xmin=float(xmin),ymax=float(ymax),ymin=float(ymin))
        return HttpResponse(content=result, content_type=json,status= None)
    except:
        context_dict = {}
        context_dict['error'] = 'yes'
        context_dict['text'] = 'Update failed, please enter the correct information!'
        return JsonResponse(context_dict, safe=False)

