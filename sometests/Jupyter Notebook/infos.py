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
nome = i.nome

global u,v

u,v= sp.symbols('u,v')

global nxvisualizacao,ny_visualizacao,nz_visualizacao,dx_visualizacao,dy_visualizacao,dz_visualizacao

nx_visualizacao,ny_visualizacao,nz_visualizacao=4,4,4
dx_visualizacao,dy_visualizacao,dz_visualizacao=lx/(nx_visualizacao-1), ly/(ny_visualizacao-1), lz/(nz_visualizacao-1)

global u_plot,v_plot
u_plot=np.arange(0,1+0.05,0.05)
v_plot=np.arange(0,1+0.05,0.05)

global armz_eq,armz_nomenclt_epsi,contador,npsu,npsv,mu,mv,mpx,mpy,mpz,mpx_sem_desvio,mpy_sem_desvio,mpz_sem_desvio,mm,armz_pt,nx_raf,dx_raf,ny_raf,dy_raf,nz_raf,dz_raf,nraf

armz_eq={}
armz_nomenclt_epsi = {}
contador,npsu,npsv=0,0,0
mu,mv=[],[]
mpx,mpy,mpz=np.empty((3,3)),np.empty((3,3)),np.empty((3,3))
mpx_sem_desvio, mpy_sem_desvio, mpz_sem_desvio= mpx.copy(),mpy.copy(),mpz.copy()
mm = np.empty((3,3), dtype=float)
armz_pt={}

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
