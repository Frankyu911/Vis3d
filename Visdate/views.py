import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from mpld3 import plugins, fig_to_html, save_html, fig_to_dict
import json
import numpy as np
from scipy.interpolate import griddata

#for numpy array is not json serializable error  继承解码器
from Plot import Plot


def index(request):


    result=Plot('A-8x16.csv','y',0.11)

    return render(request, 'index.html', {'graph1': result,})


def change(request):

    result=Plot('A-8x16.csv','y',0.1)

    return HttpResponse(content=result, content_type=json,status= None)

def upload(request):
    if request.method == "POST":
        filename = request.FILES['file'].name

        result=Plot(filename,'y',0.1)
    return render(request, 'index.html', {'graph1': result,})



