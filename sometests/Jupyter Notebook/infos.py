import matplotlib.pyplot as plt
import numpy as np 
import matplotlib.patches as mpatches
import math
import sympy as sp
import progressbar
import os
from sympy import symbols
from sympy.solvers import solve
from scipy.io import FortranFile
from sympy import ImageSet, S 
from sympy import *
from mpl_toolkits.mplot3d import Axes3D
from sympy.solvers.solveset import nonlinsolve
from IPython.display import display
import inputs as i

global lx,ly,lz,nx,ny,nz,dx,dy,dz

lx,ly,lz=i.lx,i.ly,i.lz
nx,ny,nz=i.nx,i.ny,i.nz
dx,dy,dz=i.dx,i.dy,i.dz
name = i.name

global u,v

u,v= sp.symbols('u,v')

global visu_nx,visu_ny,visu_nz,visu_dx,visu_dy,visu_dz

visu_nx,visu_ny,visu_nz=4,4,4
visu_dx,visu_dy,visu_dz=lx/(visu_nx-1), ly/(visu_ny-1), lz/(visu_nz-1)

global u_plot,v_plot
u_plot=np.arange(0,1+0.05,0.05)
v_plot=np.arange(0,1+0.05,0.05)

global eq_storage,format_storage,count,number_points_u,number_points_v,u_matrix,v_matrix,point_matrix_x,point_matrix_y,point_matrix_z,point_matrix_x_no_deflection,point_matrix_y_no_deflection,point_matrix_z_no_deflection,berst_matrix,point_storage,nx_raf,dx_raf,ny_raf,dy_raf,nz_raf,dz_raf,nraf

eq_storage={}
format_storage = {}
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
