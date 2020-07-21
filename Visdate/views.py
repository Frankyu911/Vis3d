import sys

import matplotlib
from django.shortcuts import render
import PlotAmplitudes
import sys
import numpy as np
# matplotlib.use('agg')
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import mpld3


def index(request):
    context_dict = {}
    fig, ax = plt.subplots()
    ax.scatter([1, 10], [5, 9])

    html_fig = mpld3.fig_to_html(fig,template_type='general')
    plt.close(fig)
    return render(request, 'index.html', context={'div_figure' : html_fig})
