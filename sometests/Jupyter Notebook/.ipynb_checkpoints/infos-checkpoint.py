import matplotlib.pyplot as plt
import numpy as np 
import matplotlib.patches as mpatches
import math
import sympy as sp
import progressbar
import os

from mayavi import mlab
from sympy import symbols
from sympy.solvers import solve
from scipy.io import FortranFile
from sympy import ImageSet, S 
from sympy import *
from mpl_toolkits.mplot3d import Axes3D
from sympy.solvers.solveset import nonlinsolve
from IPython.display import display
import inputs as i

global lx,ly,lz,nx,ny,nz,dx,dy,dz,xp,yp,zp

lx,ly,lz=i.domain_info['x'][0],i.domain_info['y'][0],i.domain_info['z'][0]
nx,ny,nz=i.domain_info['x'][1],i.domain_info['y'][1],i.domain_info['z'][1]
xp,yp,zp=i.domain_info['x'][2],i.domain_info['y'][2],i.domain_info['z'][2]
dx,dy,dz=i.domain_info['x'][3],i.domain_info['y'][3],i.domain_info['z'][3]
name = i.name

global u,v,t

u,v,t= sp.symbols('u,v,t')

global u_plot,v_plot,t_plot
u_plot=np.arange(0,1+0.05,0.05)
v_plot=np.arange(0,1+0.05,0.05)
t_plot=np.arange(0,1+0.05,0.05)


global eq_storage,solid_storage,count,number_points_u,number_points_v,u_matrix,v_matrix,point_matrix_x,point_matrix_y,point_matrix_z,point_matrix_x_no_deflection,point_matrix_y_no_deflection,point_matrix_z_no_deflection,berst_matrix,point_storage,nx_raf,dx_raf,ny_raf,dy_raf,nz_raf,dz_raf,nraf

eq_storage={}
solid_storage={}
count,number_points_u,number_points_v=0,0,0
u_matrix,v_matrix=[],[]
point_matrix_x,point_matrix_y,point_matrix_z=np.empty((3,3)),np.empty((3,3)),np.empty((3,3))
point_matrix_x_no_deflection, point_matrix_y_no_deflection, point_matrix_z_no_deflection= point_matrix_x.copy(),point_matrix_y.copy(),point_matrix_z.copy()
berst_matrix = np.empty((3,3), dtype=float)
point_storage={}

nraf=1
nx_raf = nx*nraf
dx_raf = lx/(nx_raf-1)
ny_raf = ny*nraf
dy_raf = ly/(ny_raf-1)
nz_raf = nz*nraf
dz_raf = lz/(nz_raf-1)

epsi_3d = np.zeros((nx,ny,nz),dtype=np.float32)
epsi_3d_x_raf = np.zeros((nx_raf,ny,nz),dtype=np.float32)
epsi_3d_y_raf = np.zeros((nx,ny_raf,nz),dtype=np.float32)
epsi_3d_z_raf = np.zeros((nx,ny,nz_raf),dtype=np.float32)

global list_storage
list_storage={}
