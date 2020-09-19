import os
import numpy as np

"""The script to get file information"""
def Plotinfo(filename, fixed_axis,axis_value=None,):
    result={}
     # Check fixed_axis has a valid value
    if fixed_axis not in ["x", "y", "z", "X", "Y", "Z"]:
        print("Error: Fixed axis must be x, y or z.")
        exit(0)
    _x,_y,_z,_amplitude = np.loadtxt(os.path.dirname(__file__)+'/'+filename, delimiter=",").T

    if fixed_axis in ["x", "X"]:
        result['xmin']=_z.min()
        result['xmax']=_z.max()
        result['ymin']=_y.min()
        result['ymax']=_y.max()
        result['zmin']=_x.min()
        result['zmax']=_x.max()
        result['fixedmax']=_x.max()
        result['fixedmin']=_x.min()
        result['fixedaxis']='x'
    elif fixed_axis in ["y", "Y"]:
        result['xmin']=_x.min()
        result['xmax']=_x.max()
        result['ymin']=_z.min()
        result['ymax']=_z.max()
        result['zmin']=_y.min()
        result['zmax']=_y.max()
        result['fixedmax']=_y.max()
        result['fixedmin']=_y.min()
        result['fixedaxis']='y'
    else:
        result['xmin']=_x.min()
        result['xmax']=_x.max()
        result['ymin']=_y.min()
        result['ymax']=_y.max()
        result['zmin']=_z.min()
        result['zmax']=_z.max()
        result['fixedmax']=_z.max()
        result['fixedmin']=_z.min()
        result['fixedaxis']='z'

    result['step']=round((result['zmax']-result['zmin'])/10,2)
    result['filename']= str(filename)
    result['axis']= str(fixed_axis)
    result['value']= str(axis_value)
    return result

