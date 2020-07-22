from django.http import  HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from mpld3 import plugins, fig_to_html, save_html, fig_to_dict
import json
import numpy as np
from scipy.interpolate import griddata

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        #检查Object类型
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

fig = plt.figure()
plt.scatter([1, 10], [5, 9])
f = open('jsondata.json', 'w')
data = json.dumps(fig_to_dict(fig), cls=NumpyEncoder)
f.write(data)
f.close()
