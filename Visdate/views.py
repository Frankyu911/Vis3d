import os

import numpy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from mpld3 import plugins, fig_to_html, save_html, fig_to_dict
import json
import numpy as np
from scipy.interpolate import griddata

#for numpy array is not json serializable error  继承解码器
from Plot import Plot
from Plotinfo import Plotinfo


def index(request):

    context_dict = {}
    result=Plot('A-8x16.csv','y',0.15)
    result2=Plot('A-8x16.csv','y',0.10)
    info = Plotinfo('A-8x16.csv','z')
    context_dict['info']=info
    zmin= info['zmin']
    zmax= info['zmax']
    step= info['step']


    x = numpy.arange(zmin, zmax, step).tolist()
    jslist=[]
    #0到5 6个
    for index in range(0,6):
             # print(round(nu,2))
        context_dict['graph'+str(index)]=Plot('A-8x16.csv','z',round(x[index],2))
        jslist.append(round(x[index],2))
    context_dict['jsl']=jslist
    return render(request, 'index.html', context=context_dict)


def change(request):

    result=Plot('A-8x16.csv','y',0.1)

    return HttpResponse(content=result, content_type=json,status= None)

def upload(request):
    context_dict = {}
    if request.method == "POST":
        filename = request.FILES['file'].name
        axis=request.POST.get("axis")
        values=request.POST.get("values")
        nu=float(values)
        result=Plot(filename,axis,nu)
        context_dict['graph1'] = result
    return render(request, 'index.html', context=context_dict)


def save(request):
    context_dict = {}
    Plot('A-8x16.csv','y',0.1,show=False,save=True)
    context_dict['text']='save success'

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
