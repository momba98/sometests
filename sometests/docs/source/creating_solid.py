# -*- coding: utf-8 -*-
"""
O usuário recebe nessa página todas informações dos argumentos de todas as funções presentes no código:

"""
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
import infos as s
import inputs as i

point_storage=s.point_storage
number_points_u=s.number_points_u
number_points_v=s.number_points_v
u=s.u
v=s.v
t=s.t
u_plot=s.u_plot
v_plot=s.v_plot
t_plot=s.t_plot
u_matrix=s.u_matrix
v_matrix=s.v_matrix
point_matrix_x=s.point_matrix_x
point_matrix_y=s.point_matrix_y
point_matrix_z=s.point_matrix_z
lz=s.lz
lx=s.lx
ly=s.ly
eq_storage=s.eq_storage
visu_nz,visu_ny,visu_nx=s.visu_nz,s.visu_ny,s.visu_nx
visu_dz,visu_dy,visu_dx=s.visu_dz,s.visu_dy,s.visu_dx
count=s.count
nraf=s.nraf
nx_raf = s.nx_raf
dx_raf = s.dx_raf
ny_raf = s.ny_raf
dy_raf = s.dy_raf
nz_raf = s.nz_raf
dz_raf = s.dz_raf
epsi_3d_x_raf = s.epsi_3d_x_raf
epsi_3d_y_raf = s.epsi_3d_y_raf
epsi_3d_z_raf = s.epsi_3d_z_raf
name=s.name
dx=s.dx
dy=s.dy
dz=s.dz
ny=s.ny
nx=s.nx
nz=s.nz
epsi_3d=s.epsi_3d
format_storage=s.format_storage
list_storage=s.list_storage

def set_point_matrix(num_u_points,num_v_points):
    
    """
    
    Importante função em que o usuário determinará o número de pontos em cada direção :obj:`[u,v]`.
    
    Caso fique em dúvida da namenclatura de quais pontos serão necessários setar, execute uma célula (após executar a função em pauta) com :obj:`print(point_storage)`::
        
        #exemplo de como tirar a dúvida dos pontos que devem receber algum input
        set_point_matrix(3,3)
        print(point_storage)
    
    Basicamente, os pontos a serem determinados possuem 2 sub-índices: :obj:`i` e :obj:`j` → :obj:`Pij`.
    
    Os sub-índices começarão em :obj:`0` e irão até :obj:`i-1` and/or :obj:`j-1`.
    
    Args:
        num_u_points (:obj:`int`): Determine o número de pontos que a direção :obj:`u` terá.
        num_v_points (:obj:`int`): Determine o número de pontos que a direção :obj:`v` terá.
    
    Exemplo:
        Será explicitado quais pontos deverão ser setados de acordo com as entrys::
        
            set_point_matrix(3,2) #função é chamada
            
            point_storage['P00'] = [x,y,z] #declara-se as informações do ponto
            point_storage['P01'] = [x,y,z] #qualquer ponto de 3 coordenadas dentro do domínio
            point_storage['P10'] = [x,y,z]
            point_storage['P11'] = [x,y,z]
            point_storage['P20'] = [x,y,z]
            point_storage['P21'] = [x,y,z]
            
        Note que o primeiro subíndice, :obj:`i`, começa em :obj:`0` e termina em :obj:`2`, que é o correspondente a :obj:`num_u_points=3-num_v_points=1`.
        
        O dicionário :obj:`point_storage` faz parte da mecânica do código, não deve ser alterado. Auxilia na setagem e no armazenamento das informações.

    """
        
    point_storage={}
    
    global number_points_v, number_points_u, u_matrix, v_matrix, point_matrix_x, point_matrix_y, point_matrix_z
    
    number_points_u=num_u_points
    number_points_v=num_v_points
    
    for i in range(0,number_points_u,1):
        for j in range(0,number_points_v,1):
            point_storage[f'P{i}{j}'] = [0,0,0]            
    
    mut=np.array([u**0,u**1,u**2,u**3,u**4,u**5,u**6,u**7,u**8,u**9])
    mvt=np.array(([v**0],[v**1],[v**2],[v**3],[v**4],[v**5],[v**6],[v**7],[v**8],[v**9]))
    
    u_matrix=mut[:number_points_u]
    v_matrix=mvt[:number_points_v]
    point_matrix_x=np.empty((number_points_u,number_points_v))
    point_matrix_y=np.empty((number_points_u,number_points_v))
    point_matrix_z=np.empty((number_points_u,number_points_v))


def create_point_matrix(deflection=False):
    
    """
    Auxílio na hora de setar os pontos necessários para as equações da função :obj:`gen_bezier()`.
    
    Args: 
        deflection (:obj:`Bool`, optional): Sete como :obj:`True` caso queira que a superfície passe pelos pontos de controle 
            (pontos intermediários, os que normalmente dão a curvatura suave à superfície). Baseia-se num artifício
            matemático que *hackeia* a Bézier, forçando-a a fazer algo que normalmente não faria.
    Warning:
        :obj:`deflection=True` **não demonstrará efeito em todos os casos!**
        
        O parâmetro pode ficar setado como True sem danificar o código, porém só efetivamente desviará a superfície 
        caso :obj:`n_num_u_points=3` ao mesmo tempo que :obj:`n_num_v_points=2` ou vice-versa.
        
        **O porquê da restrição:** 
        
        Como pode-se imaginar, não há necessidade de desviar a superfície para passar em pontos intermediários caso existam apenas 2 
        pontos na direção :obj:`[u,v]` pois não há pontos intermediários. Também, caso a superfície tenha 3 pontos em cada direção 
        :obj:`[u,v]` ou mais, torna-se *matematicamente complicado* descrever o desvio.
            
    """
    for i in range(number_points_u):
        for j in range(number_points_v):
            point_matrix_x[i][j] = point_storage[f'P{i}{j}'][0]
            point_matrix_y[i][j] = point_storage[f'P{i}{j}'][1]
            point_matrix_z[i][j] = point_storage[f'P{i}{j}'][2]
        
    global point_matrix_x_no_deflection, point_matrix_y_no_deflection, point_matrix_z_no_deflection
    
    point_matrix_x_no_deflection, point_matrix_y_no_deflection, point_matrix_z_no_deflection= point_matrix_x.copy(), point_matrix_y.copy(), point_matrix_z.copy()
    
    if deflection==True:
        if number_points_u==3:
            if number_points_v==2:
                point_matrix_x[1][0] = point_matrix_x[1][0]*2 - (point_matrix_x[0][0]+point_matrix_x[2][0])/2
                point_matrix_x[1][1] = point_matrix_x[1][1]*2 - (point_matrix_x[0][1]+point_matrix_x[2][1])/2
                point_matrix_y[1][0] = point_matrix_y[1][0]*2 - (point_matrix_y[0][0]+point_matrix_y[2][0])/2
                point_matrix_y[1][1] = point_matrix_y[1][1]*2 - (point_matrix_y[0][1]+point_matrix_y[2][1])/2
                point_matrix_z[1][0] = point_matrix_z[1][0]*2 - (point_matrix_z[0][0]+point_matrix_z[2][0])/2
                point_matrix_z[1][1] = point_matrix_z[1][1]*2 - (point_matrix_z[0][1]+point_matrix_z[2][1])/2

        if number_points_u==2:
            if number_points_v==3:
                point_matrix_x[0][1] = point_matrix_x[0][1]*2 - (point_matrix_x[0][0]+point_matrix_x[0][2])/2
                point_matrix_x[1][1] = point_matrix_x[1][1]*2 - (point_matrix_x[1][0]+point_matrix_x[1][2])/2
                point_matrix_y[0][1] = point_matrix_y[0][1]*2 - (point_matrix_y[0][0]+point_matrix_y[0][2])/2
                point_matrix_y[1][1] = point_matrix_y[1][1]*2 - (point_matrix_y[1][0]+point_matrix_y[1][2])/2
                point_matrix_z[0][1] = point_matrix_z[0][1]*2 - (point_matrix_z[0][0]+point_matrix_z[0][2])/2
                point_matrix_z[1][1] = point_matrix_z[1][1]*2 - (point_matrix_z[1][0]+point_matrix_z[1][2])/2
                
def translate(direction,quantity):
    
    """
    Caso tenha se precipitado em relação à posição de sua superfície, translade seus pontos de forma eficiente 
    em qualquer direção. 

    Args:
        direction (:obj:`str`): Defina em qual direção a translação será feita. Deve assumir :obj:`'x', 'y', 'z'`.
        quantity (:obj:`int`): Assume quantas unidades de comprimento de domínio o usuário quer translate sua superfície.
        
    Warning: 
        Deverá ser obrigatoriamente chamada entre a função :obj:`create_point_matrix()` e a função :obj:`gen_bezier()`.
        
    Exemplo:
        Para "empurrar" 1.5 unidades para trás e "puxar" 0.5 unidades para o lado::
        
            set_point_matrix(2,2)

            point_storage['P00'] = [x,y,z] 
            point_storage['P01'] = [x,y,z] 
            point_storage['P10'] = [x,y,z]
            point_storage['P11'] = [x,y,z]

            create_point_matrix()

            translate('y',1.5)

            translate('x',-0.5)

            gen_bezier('0',capô)

    """
    
    if direction=='x':
        for i in range(number_points_u):
            for j in range(number_points_v):
                point_matrix_x_no_deflection[i][j] = point_matrix_x_no_deflection[i][j]+quantity
                point_matrix_x[i][j] = point_matrix_x[i][j]+quantity
    
    if direction=='y':
        for i in range(number_points_u):
            for j in range(number_points_v):
                point_matrix_y_no_deflection[i][j] = point_matrix_y_no_deflection[i][j]+quantity
                point_matrix_y[i][j] = point_matrix_y[i][j]+quantity
    
    if direction=='z':
        for i in range(number_points_u):
            for j in range(number_points_v):
                point_matrix_z_no_deflection[i][j] = point_matrix_z_no_deflection[i][j]+quantity
                point_matrix_z[i][j] = point_matrix_z[i][j]+quantity


        
def gen_bezier(identif, name, show_equation=False):
    
    """
    
    As equações de Bézier são governadas pelos parâmetros :obj:`u` e :obj:`v` e fornecem leis para curvas/superfícies. 
    
    São definidas por pontos arbitrados pelo usuário, tendo um mínimo de 2 em cada direção :obj:`[u,v]` e sem algum máximo pré-determinado.
    
    Os pontos iniciais e finais determinam onde a curva começa e termina, obviamente. *São os únicos pontos por onde a Bézier (naturalmente) passará com certeza*. 
    Os pontos intermediários estão encarregados de fornecer à Bézier uma curvatura suave, sem canto vivo/descontinuidade, 
    portanto a curva/superfície nunca *encosta* neles.
    
    Como o grau das equações é definido por :obj:`número de pontos definidos pelo usuário - 1`, recomenda-se usar no máximo 3 pontos em cada direção, 
    para que assim os cálculos se tornem baratos e viáveis. **Caso um objeto seja extremamente complexo, recomenda-se dividí-lo em várias superfícies de grau 2.**
    
    Args:
        identif (:obj:`str`): Crie a *identificação* da sua superfície com :obj:`'n'`, onde :obj:`n=0,1,2,3...` (começar em '0' e somar '1' a cada nova superfície).
        name (:obj:`str`): Crie um name para a superfície. Não há regras. 
        show_equations (:obj:`Bool`, optional): Sete como :obj:`True` caso queira visualizar as equações governantes da superfície em questão.
        
    Warning:
        :obj:`identif()` **necessita atenção especial**: o usuário voltará a chamar o parâmetro por diversas vezes ao decorrer do código.
        
    É importante frisar que, caso construída uma superfície muito complexa (com variações não lineares entre os pontos em mais de 2 direções :obj:`xyz`, uma
    superfície muito torcida), a convergência das equações não é garantida - por enquanto.
    
    .. image:: images/ex_supcomplexa.png
       :align: right
       :scale: 40%
                         
    A superfície ao lado possui seguintes equações::
    
        x(𝑢,𝑣) = 4𝑢²−2𝑢+𝑣²(3𝑢2−6𝑢+3)+𝑣(−6𝑢²+12𝑢−6)+3
        
        y(𝑢,𝑣) = 2𝑢²+𝑣²(2𝑢²+1)+𝑣(4−4𝑢²) 
        
        z(𝑢,𝑣) = −3𝑢²+4𝑢+𝑣²(−11𝑢²+14𝑢−7)+𝑣(18𝑢²−20𝑢+10)
        
    Evidentemente, são equações longas, não lineares e dependentes de mais de uma variável. O solver não se dá muito bem com isso. Sobre 
    convergência, consultar a função :obj:`intersection_preview()`.
    
    """
    
    for matrix_base,direction,matrix_no_deflection in [point_matrix_x,'x',point_matrix_x_no_deflection],[point_matrix_y,'y',point_matrix_y_no_deflection],[point_matrix_z,'z',point_matrix_z_no_deflection]:
    
        global berst_matrix
        
        berst_matrix = np.empty((number_points_u,number_points_u), dtype=float)

        berstein(number_points_u)

        final_matrix_partial=u_matrix.dot(berst_matrix[::-1,:]).dot(matrix_base)

        berst_matrix = np.empty((number_points_v,number_points_v), dtype=float)

        berstein(number_points_v)

        final_matrix=final_matrix_partial.dot(berst_matrix[::-1,:].T).dot(v_matrix)

        eq=lambdify([u,v],final_matrix[0])

        matrix_plot=np.empty((u_plot.size,v_plot.size))

        for up in u_plot:
            for vp in v_plot:
                matrix_plot[int(up*(u_plot.size-1))][int(vp*(v_plot.size-1))]=eq(up,vp)

        eq_storage[f'{direction}{identif}'] = [name,final_matrix,eq,matrix_plot,np.amin(matrix_plot),np.amax(matrix_plot),number_points_u,number_points_v,matrix_no_deflection.copy(),'bezier']
        
        if show_equation==True:
            print(f'{direction}(u,v) #{identif} surface parametric equation: '),display(final_matrix[0]),print('\n')
            
            
def berstein(n_p):
    
    """
    Matemática chave por trás das curvas/superfícies de Bézier, dentro da própria função :obj:`gen_bezier()`. 
    
    Args:
        n_p(:obj:`int`): Não há necessidade alguma de manipulação por parte do usuário.
    
    """
        
    for i in range(n_p): 
        Bint = sp.expand((math.factorial(n_p-1) / (math.factorial(i)*math.factorial(n_p-1-i)))*u**i*(1-u)**(n_p-1-i))
        coef = sp.Poly(Bint, u)
        aux = coef.coeffs()
        for c in range(i):
            aux.append(0)
        for j in range(n_p):
            berst_matrix[i][j]=aux[j] 
                    
                
            
def gen_toroid(identif, name, bases_plane, external_radius, profile_circle_radius, center_1, center_2, init_height, tor_raf_path=False):
    
    """
    not updated
    
    """
    
    global matrix_superior
    
    matrix_superior=np.array([[[0,profile_circle_radius],
                                 [0,profile_circle_radius+profile_circle_radius*0.552284749831],
                                 [profile_circle_radius-profile_circle_radius*0.552284749831,profile_circle_radius+profile_circle_radius],
                                 [profile_circle_radius,profile_circle_radius+profile_circle_radius]],

                                [[external_radius-profile_circle_radius,external_radius],
                                 [external_radius-profile_circle_radius+profile_circle_radius*0.552284749831,external_radius],
                                 [external_radius,external_radius-profile_circle_radius+profile_circle_radius*0.552284749831],
                                 [external_radius,external_radius-profile_circle_radius]]])


    global matrix_inferior
    
    matrix_inferior=np.array([[[0,profile_circle_radius],
                                 [0,profile_circle_radius+profile_circle_radius*0.552284749831],
                                 [profile_circle_radius-profile_circle_radius*0.552284749831,profile_circle_radius+profile_circle_radius],
                                 [profile_circle_radius,profile_circle_radius+profile_circle_radius]],

                                [[external_radius-profile_circle_radius,external_radius-profile_circle_radius*2],
                                 [external_radius-profile_circle_radius-profile_circle_radius*0.552284749831,external_radius-profile_circle_radius*2],
                                 [external_radius-profile_circle_radius*2,external_radius-profile_circle_radius-profile_circle_radius*0.552284749831],
                                 [external_radius-profile_circle_radius*2,external_radius-profile_circle_radius]]])
    
    if bases_plane=='xy':
        dirct='z'
    if bases_plane=='xz':
        dirct='y'
    if bases_plane=='zy':
        dirct='x'
        
    gen_revolve_profile(identif, name, dirct, center_1, center_2, init_height, alternative=True, rev_raf_path=tor_raf_path)
    

def gen_revolve_profile(identif, name, direction, center_1, center_2, init_height, deflection=False, alternative=False, rev_raf_path=False):
    
    """
    construir sempre no sentido positivos, sem idas e voltas, ou seja, cada 'axis' so pode ter 1 'radius'
    primeiro ponto sempre deve ser 0, e será setado como isso caso nao seja inputado certo
    inferior e superior must end at the same point
    
    Exemplo de matriz alternativa::
    
        c.matrix_superior=np.array([
                                    [
                                     [0,6],
                                     [0,10],
                                     [6,12],
                                    ],

                                    [
                                     [5,6],
                                     [6,6],
                                     [6,5],
                                    ],

                                              ],dtype=float)


        c.matrix_inferior=np.array([
                                    [
                                     [0],
                                     [0],
                                     [6],
                                     [12]
                                    ],

                                    [
                                     [5],
                                     [4],
                                     [4],
                                     [4.75]
                                    ],

                                              ],dtype=float)
    
    """
    
    fig = plt.figure(figsize=(12.5,12.5))
    
    if rev_raf_path==False:
        ax = fig.add_subplot(1, 1, 1)
        
    maxi=0
    
    for profile_type in ['superior','inferior']:
        
        if alternative==False:
            number_beziers=int(input(f'How many Béziers will governate {profile_type} revolve profile?' ))
            
        if alternative==True:
            if profile_type=='superior':
                number_beziers=matrix_superior.shape[2]
            if profile_type=='inferior':
                number_beziers=matrix_inferior.shape[2]

        for amount in range(0,number_beziers,1):
            
            if alternative==False:

                number_points=int(input(f'How many points [2-5] will governate Bézier #{amount+1}?' ))

                point_matrix_x_2d = np.empty((number_points,1), dtype=float)
                point_matrix_y_2d = np.empty((number_points,1), dtype=float)

                mtt=np.array([t**0,t**1,t**2,t**3,t**4])
                t_matrix=mtt[:number_points]

                for amount2 in range(0,number_points,1):
                    point_matrix_x_2d[amount2][0] = float(input(f'Set Point {amount2} Axis coordinate (Bezier #{amount+1}):'))
                    if point_matrix_x_2d[amount2][0]>maxi:
                        maxi=point_matrix_x_2d[amount2][0]
                    point_matrix_y_2d[amount2][0] = float(input(f'Set Point {amount2} Radius coordinate (Bezier #{amount+1}):'))
                    if point_matrix_y_2d[amount2][0]>maxi:
                        maxi=point_matrix_y_2d[amount2][0]
                if amount==0:
                    point_matrix_x_2d[0][0]=0
            
            if alternative==True:

                if profile_type=='superior':
                    number_points=matrix_superior.shape[1]
                    point_matrix_x_2d = matrix_superior[0][:,amount].reshape(-1, 1)
                    point_matrix_y_2d = matrix_superior[1][:,amount].reshape(-1, 1)
                    maxi=np.amax(matrix_superior)


                if profile_type=='inferior':
                    number_points=matrix_inferior.shape[1]
                    point_matrix_x_2d = matrix_inferior[0][:,amount].reshape(-1, 1)
                    point_matrix_y_2d = matrix_inferior[1][:,amount].reshape(-1, 1)
                
                mtt=np.array([t**0,t**1,t**2,t**3,t**4])
                t_matrix=mtt[:number_points]
                
                
            point_matrix_x_no_deflection_2d=point_matrix_x_2d.copy()
            point_matrix_y_no_deflection_2d=point_matrix_y_2d.copy()

            if deflection==True:
                if number_points==3:
                    point_matrix_x_2d[1][0] = point_matrix_x_2d[1][0]*2 - (point_matrix_x_2d[0][0]+point_matrix_x_2d[2][0])/2
                    point_matrix_y_2d[1][0] = point_matrix_y_2d[1][0]*2 - (point_matrix_y_2d[0][0]+point_matrix_y_2d[2][0])/2
                    
            global berst_matrix

            for matrix_base,direc,matrix_no_deflection in [point_matrix_x_2d,'x',point_matrix_x_no_deflection_2d],[point_matrix_y_2d,'y',point_matrix_y_no_deflection_2d]:

                berst_matrix = np.empty((number_points,number_points), dtype=float)

                berstein(number_points)

                final_matrix=t_matrix.dot(berst_matrix[::-1,:]).dot(matrix_base)

                eq=lambdify(t,final_matrix[0])
                
                eq_storage[f'{profile_type}{direc}{identif},Bezier{amount+1}'] = [eq,
                                                                                  final_matrix,
                                                                                  matrix_base.copy(),
                                                                                  matrix_no_deflection.copy(),
                                                                                  number_points,
                                                                                  direction,
                                                                                  number_beziers,
                                                                                  name,
                                                                                  type(eq(t_plot))
                                                                                 ]
                
                
                
        if rev_raf_path==True:
            loop_path=['normal','x','y','z']

        if rev_raf_path==False:
            loop_path=['normal']

        for raf in loop_path:
            
            dx_gen,dy_gen,dz_gen=dx,dy,dz
            nx_gen,ny_gen,nz_gen=nx,ny,nz

            if raf=='normal':
                if rev_raf_path==True:
                    ax = fig.add_subplot(2, 2, 1)
                    
            if raf=='x':
                dx_gen,nx_gen=dx_raf,nx_raf
                ax = fig.add_subplot(2, 2, 2)
                
            if raf=='y':
                dy_gen,ny_gen=dy_raf,ny_raf
                ax = fig.add_subplot(2, 2, 3)
                
            if raf=='z':
                dz_gen,nz_gen=dz_raf,nz_raf
                ax = fig.add_subplot(2, 2, 4)

            if direction=='x':
                n1,d1=nx_gen,dx_gen
            if direction=='y':
                n1,d1=ny_gen,dy_gen
            if direction=='z':
                n1,d1=nz_gen,dz_gen

            radius_list=[]
            old_radius=10203040

            for c1 in np.arange(0,n1,1):
                for amount4 in range(1,number_beziers+1,1):
                    sol = solveset(eq_storage[f'{profile_type}x{identif},Bezier{amount4}'][1][0] - c1*d1 , t, domain=S.Reals)                    
                    for i in range(0,len(sol.args),1):
                        if 0<=round(sol.args[i],2)<=1.0:
                            raio=round(eq_storage[f'{profile_type}y{identif},Bezier{amount4}'][0](sol.args[i]),5)

                            if eq_storage[f'{profile_type}y{identif},Bezier{amount4}'][8] != np.ndarray:
                                if amount4>1 and round(sol.args[i],2)!=0:
                                    radius_list.append(raio)
                                    old_radius=raio
                                else:
                                    radius_list.append(raio)
                                    old_radius=raio

                            elif eq_storage[f'{profile_type}y{identif},Bezier{amount4}'][8] == np.ndarray:
                                if raio!=old_radius:
                                    radius_list.append(raio)
                                    old_radius=raio

            list_storage[f'{profile_type}{identif}_{raf}'] = [radius_list.copy()]

            for count in range(1,number_beziers+1,1):

                if eq_storage[f'{profile_type}y{identif},Bezier{count}'][8] == np.ndarray:
                    try:
                        ax.plot(eq_storage[f'{profile_type}x{identif},Bezier{count}'][0](t_plot),eq_storage[f'{profile_type}y{identif},Bezier{count}'][0](t_plot), color='grey')
                        ax.scatter(eq_storage[f'{profile_type}x{identif},Bezier{count}'][3],eq_storage[f'{profile_type}y{identif},Bezier{count}'][3], color='black')
                    except:
                        pass

                elif eq_storage[f'{profile_type}y{identif},Bezier{count}'][8] != np.ndarray:
                    subs = np.full((eq_storage[f'{profile_type}x{identif},Bezier{count}'][0](t_plot).size,1),
                                    eq_storage[f'{profile_type}y{identif},Bezier{count}'][0](t_plot))
                    ax.plot(eq_storage[f'{profile_type}x{identif},Bezier{count}'][0](t_plot),subs, color='grey')
                    ax.scatter(eq_storage[f'{profile_type}x{identif},Bezier{count}'][3],eq_storage[f'{profile_type}y{identif},Bezier{count}'][3], color='black')
        
            ax.set_xlabel('Axis', fontsize=10),ax.set_ylabel('R', fontsize=10)
            ax.set_xlim(-0.5,maxi+0.5),ax.set_ylim(-0.5,maxi+0.5)
            ax.set_title(f'Revolve Profile (raf_{raf})',size=14)
            ax.plot([-0.5,maxi+0.5],[0,0], 'k--')
            ax.grid(True, alpha=0.3)

            for c1 in np.arange(0,n1,1):
                ax.plot([c1*d1,c1*d1],[0,max(lx,ly,lz)],'r--', alpha = 0.3, linewidth=0.8)
                try:
                    ax.plot([c1*d1,c1*d1],[list_storage[f'inferior{identif}_{raf}'][0][c1],list_storage[f'superior{identif}_{raf}'][0][c1]],'k', alpha = 0.5,)
                except:
                    pass
                

    #gen_revolve_cylinder    
        
    if eq_storage[f'superiorx{identif},Bezier1'][5] =='x':
        bases_plane='zy'
    if eq_storage[f'superiorx{identif},Bezier1'][5] =='y':
        bases_plane='xz'
    if eq_storage[f'superiorx{identif},Bezier1'][5] =='z':
        bases_plane='xy'
        
    check=eq_storage[f'superiorx{identif},Bezier1'][6] 
    final_height = init_height + eq_storage[f'superiorx{identif},Bezier{check}'][3][-1]

    superior_radius=0
    inferior_radius=100000
    
    for counter in range(1,check+1,1):        
        if np.amax(eq_storage[f'superiory{identif},Bezier{counter}'][3])>superior_radius:
            superior_radius=np.amax(eq_storage[f'superiory{identif},Bezier{counter}'][3])
            
    for counter in range(1,eq_storage[f'inferiorx{identif},Bezier1'][6]+1,1):        
        if np.amin(eq_storage[f'inferiory{identif},Bezier{counter}'][3])<inferior_radius:
            inferior_radius=np.amax(eq_storage[f'inferiory{identif},Bezier{counter}'][3])
            
    axis = np.linspace(init_height, final_height, 30)
    theta = np.linspace(0, 2*np.pi, 30)
    
    theta_grid, a3=np.meshgrid(theta, axis)
    
    a1 = superior_radius*np.cos(theta_grid) + center_1
    a2 = superior_radius*np.sin(theta_grid) + center_2
    
    if bases_plane=='zy':
        axis1,axis2,axis3=a3,a1,a2
    if bases_plane=='xz':
        axis1,axis2,axis3=a1,a2,a3
    if bases_plane=='xy':
        axis1,axis2,axis3=a1,a3,a2
        
    eq_storage[f'superiorrc{identif}'] = [eq_storage[f'superiorx{identif},Bezier1'][7],axis1.copy(),axis2.copy(),axis3.copy(),
                                          bases_plane,superior_radius,center_1,center_2,init_height,final_height,rev_raf_path]
    
    a1 = inferior_radius*np.cos(theta_grid) + center_1
    a2 = inferior_radius*np.sin(theta_grid) + center_2
    
    if bases_plane=='zy':
        axis1,axis2,axis3=a3,a1,a2
    if bases_plane=='xz':
        axis1,axis2,axis3=a1,a2,a3
    if bases_plane=='xy':
        axis1,axis2,axis3=a1,a3,a2
    
    
    eq_storage[f'inferiorrc{identif}'] = [eq_storage[f'inferiorx{identif},Bezier1'][7],axis1.copy(),axis2.copy(),axis3.copy(),
                                          bases_plane,inferior_radius,center_1,center_2,init_height,final_height,rev_raf_path]

def gen_sphere(identif,name,radius,cex,cey,cez):
    
    """
    not updated
    
    """
    
    pi = np.pi
    cos = np.cos
    sin = np.sin
    phi, theta = np.mgrid[0:pi:30j, 0:2*pi:30j]
    
    x = radius*sin(phi)*cos(theta) + cex
    y = radius*sin(phi)*sin(theta) + cey
    z = radius*cos(phi) + cez
        
    eq_storage[f's{identif}'] = [name,x.copy(),z.copy(),y.copy(),cex,cey,cez,radius]
    
    
def gen_cylinder(identif,name,bases_plane,radius,center_1,center_2,init_height,final_height):
    
    """
    not updated
    
    """
    
    axis = np.linspace(init_height, final_height, 30)
    theta = np.linspace(0, 2*np.pi, 30)
    
    theta_grid, a3=np.meshgrid(theta, axis)
    
    a1 = radius*np.cos(theta_grid) + center_1
    a2 = radius*np.sin(theta_grid) + center_2
    
    if bases_plane=='zy':
        axis1,axis2,axis3=a3,a1,a2
    if bases_plane=='xz':
        axis1,axis2,axis3=a1,a2,a3
    if bases_plane=='xy':
        axis1,axis2,axis3=a1,a3,a2
        
    eq_storage[f'c{identif}'] = [name,axis1.copy(),axis2.copy(),axis3.copy(),bases_plane,radius,center_1,center_2,init_height,final_height]
    
                
def surface_plot(engine,init_identif,final_identif, points=False, alpha=0.3):
    
    """
    Visualize all the work done. 
    
    Args:
        engine (:obj:`str`): Choose which engine will render your solid, :obj:`'matplotlib'` or :obj:`'mayavi'`.
        init_identif (:obj:`str`): Determine o início do intervalo de superfícies a serem plotadas através da identificação :obj:`identif`.
        final_identif (:obj:`str`): Determine o final do intervalo (endpoint não incluido) de superfícies a serem plotadas através da identificação :obj:`identif`
        points (:obj:`Bool`, optional): Caso queira visualizar os pontos que governam sua superfície, sete como :obj:`True`.
        alpha (:obj:`float`, optional): Controlador da opacidade da superfície em questão. Pode assumir qualquer valor entre :obj:`0` (transparente) e :obj:`1` (opaco).

    """
    init_identif=int(init_identif)
    final_identif=int(final_identif)
    
    global fig,ax
    
    if engine=='mayavi':
        fig = mlab.figure(engine=None, bgcolor=(1,1,0.9), fgcolor=(0,0,0),size=(1000, 500))
        fig.scene.parallel_projection = True
        mlab.clf()
        
        colormaps=['summer','Accent','pink','spectral','copper','autumn','Oranges','jet','winter','seismic','hsv','rainbow']
        choice=np.random.randint(0,12,1)[0]
        
        for plot in np.arange(init_identif,final_identif,1):
            for p,c in eq_storage.items():
                if p==f'x{plot}':
                    surf=mlab.mesh(eq_storage[f'x{plot}'][3], eq_storage[f'y{plot}'][3], eq_storage[f'z{plot}'][3],
                           colormap=colormaps[choice], opacity=alpha)
                    
                if p==f's{plot}':
                    surf=mlab.mesh(eq_storage[f's{plot}'][1], eq_storage[f's{plot}'][3], eq_storage[f's{plot}'][2],
                           colormap=colormaps[choice], opacity=alpha)

                if p==f'c{plot}':
                    surf=mlab.mesh(eq_storage[f'c{plot}'][1], eq_storage[f'c{plot}'][3], eq_storage[f'c{plot}'][2],
                           colormap=colormaps[choice], opacity=alpha)

                if p==f'superiorrc{plot}':
                    surf=mlab.mesh(eq_storage[f'superiorrc{plot}'][1], eq_storage[f'superiorrc{plot}'][3], eq_storage[f'superiorrc{plot}'][2],
                           colormap=colormaps[choice], opacity=alpha)
                    
                if p==f'inferiorrc{plot}':
                    surf=mlab.mesh(eq_storage[f'inferiorrc{plot}'][1], eq_storage[f'inferiorrc{plot}'][3], eq_storage[f'inferiorrc{plot}'][2],
                           colormap=colormaps[choice], opacity=alpha)
        
        
        mlab.plot3d([0, lx], [0, 0], [0, 0], color=(1,0,0), tube_radius=None, figure=fig, opacity=0.225)
        mlab.plot3d([0, lx], [ly, ly], [0, 0], color=(1,0,0), tube_radius=None, figure=fig, opacity=0.225)
        mlab.plot3d([0, lx], [0, 0], [lz, lz], color=(1,0,0), tube_radius=None, figure=fig, opacity=0.225)
        mlab.plot3d([0, lx], [ly, ly], [lz, lz], color=(1,0,0), tube_radius=None, figure=fig, opacity=0.225)

        mlab.plot3d([0, 0], [0, ly], [0, 0], color=(0,1,0), tube_radius=None, figure=fig, opacity=0.225)
        mlab.plot3d([lx, lx], [0, ly], [0, 0], color=(0,1,0), tube_radius=None, figure=fig, opacity=0.225)
        mlab.plot3d([0, 0], [0, ly], [lz, lz], color=(0,1,0), tube_radius=None, figure=fig, opacity=0.225)
        mlab.plot3d([lx, lx], [0, ly], [lz, lz], color=(0,1,0), tube_radius=None, figure=fig, opacity=0.225)

        mlab.plot3d([0, 0], [0, 0], [0, lz], color=(0,0,1), tube_radius=None, figure=fig, opacity=0.225)
        mlab.plot3d([0, 0], [ly, ly], [0, lz], color=(0,0,1), tube_radius=None, figure=fig, opacity=0.225)
        mlab.plot3d([lx, lx], [0, 0], [0, lz], color=(0,0,1), tube_radius=None, figure=fig, opacity=0.225)
        mlab.plot3d([lx, lx], [ly, ly], [0, lz], color=(0,0,1), tube_radius=None, figure=fig, opacity=0.225)    

        mlab.plot3d([0, lx], [0, ly], [0, lz], color=(1,0,0), tube_radius=None, figure=fig, opacity=0)
        ax=mlab.axes(xlabel='x', ylabel='y', zlabel='z',ranges=(0.0,lx,0.0,ly,0.0,lz), nb_labels=6)
        ax.property.color = (1,1,1) 
        ax.property.opacity = 0

        ax.axes.font_factor = 0.8
        ax.axes.label_format = '    %3.1f'
        mlab.orientation_axes()
        mlab.view(azimuth=-22.5, elevation=242.5)
        
    if engine=='matplotlib':
        
        fig = plt.figure(figsize=(11,9))
        ax = fig.add_subplot(1, 1, 1, projection='3d', proj_type='ortho')

        ax.set_xlabel('x'),ax.set_ylabel('z'),ax.set_zlabel('y'),ax.set_xlim(0,max([lx,ly,lz])),ax.set_ylim(0,max([lx,ly,lz])),ax.set_zlim(0,max([lx,ly,lz])),
        ax.view_init(25,-45),ax.set_title('Surface/Control Points',size=20)

        for y in [0,ly]: #domínio
            ax.plot([0,0],[0,lz],[y,y],   'k--',linewidth=0.5,alpha=0.7)
            ax.plot([0,lx],[0,0],[y,y],   'k--',linewidth=0.5,alpha=0.7)
            ax.plot([0,lx],[lz,lz],[y,y], 'k--',linewidth=0.5,alpha=0.7)
            ax.plot([lx,lx],[lz,0],[y,y], 'k--',linewidth=0.5,alpha=0.7)
            ax.plot([lx,lx],[0,0],[0,y],  'k--',linewidth=0.5,alpha=0.7)
            ax.plot([0,0],[0,0],[0,y],    'k--',linewidth=0.5,alpha=0.7)
            ax.plot([0,0],[lz,lz],[0,y],  'k--',linewidth=0.5,alpha=0.7)
            ax.plot([lx,lx],[lz,lz],[0,y],'k--',linewidth=0.5,alpha=0.7)

        for plot in np.arange(init_identif,final_identif,1):
            for p,c in eq_storage.items():
                if p==f'x{plot}':
                    surf = ax.plot_surface(eq_storage[f'x{plot}'][3],eq_storage[f'z{plot}'][3],eq_storage[f'y{plot}'][3],antialiased=True,shade=True,alpha=alpha,label=eq_storage[f'x{plot}'][0])
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)
                    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)
                    if points == True:
                        ax.scatter(eq_storage[f'x{plot}'][8],eq_storage[f'z{plot}'][8],eq_storage[f'y{plot}'][8],s=200)
                        for i in range(0,eq_storage[f'x{plot}'][6],1):
                            for j in range(0,eq_storage[f'x{plot}'][7],1):
                                ax.text(eq_storage[f'x{plot}'][8][i][j],eq_storage[f'z{plot}'][8][i][j],eq_storage[f'y{plot}'][8][i][j],f' P{i}{j}',size=12.5)

                if p==f's{plot}':
                    surf = ax.plot_surface(eq_storage[f's{plot}'][1], eq_storage[f's{plot}'][2], eq_storage[f's{plot}'][3], alpha=alpha, label=eq_storage[f's{plot}'][0])
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)
                    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)

                if p==f'c{plot}':
                    surf = ax.plot_surface(eq_storage[f'c{plot}'][1], eq_storage[f'c{plot}'][2], eq_storage[f'c{plot}'][3], alpha=alpha, label=eq_storage[f'c{plot}'][0])
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)
                    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)

                if p==f'superiorrc{plot}':
                    surf=ax.plot_surface(eq_storage[f'superiorrc{plot}'][1], eq_storage[f'superiorrc{plot}'][3], eq_storage[f'superiorrc{plot}'][2],
                           alpha=alpha, label=eq_storage[f'inferiorrc{plot}'][0])
                    
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)
                    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)
                
                if p==f'inferiorrc{plot}':
                    surf=ax.plot_surface(eq_storage[f'inferiorrc{plot}'][1], eq_storage[f'inferiorrc{plot}'][3], eq_storage[f'inferiorrc{plot}'][2],
                           alpha=alpha, label=eq_storage[f'inferiorrc{plot}'][0])
                    
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)
                    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)

        ax.invert_yaxis()

        plt.show()    


def intersection_preview(init_identif,final_identif):
    
    """
    Uma *mini simulação de Epsi*. Para poucos nós em cada direção será checado se os limites são coerentes ou não, 
    ou seja, **se as funções de Bézier convergiram para o determinado espaçamento de nós ou não**. Cada ponto no gráfico significa uma intersecção entre o vetor e a superfície.
    Se todos forem razoáveis, a superfície será bem entendida pelo solver.
    
    Args:
        init_identif (:obj:`str`): Determine o início do intervalo de superfícies a serem calculadas através da identificação :obj:`identif`.
        final_identif (:obj:`str`): Determine o final do intervalo (endpoint não incluido) de superfícies a serem calcuadas através da identificação :obj:`identif`.
        
    Warning:
        :obj:`intersection_preview()` é uma função destinada **apenas** à conferência de convergência de superfícies de Bézier. Outros objetos não cabem nessa função.
    
    """
    
    init_identif=int(init_identif)
    final_identif=int(final_identif)
    
    fig = plt.figure(figsize=(9,9))
    ax = fig.add_subplot(1, 1, 1, projection='3d', proj_type='ortho')
    
    ax.set_xlabel('x'),ax.set_ylabel('z'),ax.set_zlabel('y'),ax.set_xlim(0,max([lx,ly,lz])),ax.set_ylim(0,max([lx,ly,lz])),ax.set_zlim(0,max([lx,ly,lz])),
    ax.view_init(25,-45),(),ax.set_title('Surface/Intersections',size=20)
    
    for plot in np.arange(init_identif,final_identif,1):
        ax.plot_surface(eq_storage[f'x{plot}'][3],eq_storage[f'z{plot}'][3],eq_storage[f'y{plot}'][3],color='c',antialiased=True,shade=True, alpha=0.4) #cmap='Wistia'
        
        for n1,n2,d1,d2,e1,e2,cor in [visu_ny,visu_nz,visu_dy,visu_dz,f'y{plot}',f'z{plot}','magenta'],[visu_nx,visu_nz,visu_dx,visu_dz,f'x{plot}',f'z{plot}','blue'],[visu_nx,visu_ny,visu_dx,visu_dy,f'x{plot}',f'y{plot}','aqua']:
            nobj=0
            for c1 in range(0,n1,1):
                for c2 in range(0,n2,1):
                    try:
                        sol = nonlinsolve([eq_storage[e1][1][0]-c1*d1,eq_storage[e2][1][0]-c2*d2],[u,v])
                        for a in range(0,len(sol.args)):
                            if sol.args[a][0].is_real == True:
                                if 0<=sol.args[a][0]<=1:
                                    if sol.args[a][1].is_real == True:
                                        if 0<=sol.args[a][1]<=1:
                                            nobj+=1
                                            ax.scatter(eq_storage[f'x{plot}'][2](float(sol.args[a][0]),float(sol.args[a][1])),
                                                       eq_storage[f'z{plot}'][2](float(sol.args[a][0]),float(sol.args[a][1])),
                                                       eq_storage[f'y{plot}'][2](float(sol.args[a][0]),float(sol.args[a][1])),s=100,color=cor)
                    except: 
                        pass

            for cx in range(0,visu_nx,1):
                for cz in range(0,visu_nz,1):
                    ax.plot((cx*visu_dx,cx*visu_dx),(cz*visu_dz,cz*visu_dz),(0,ly),color='blue',linestyle='--', linewidth=1.2)

            for cx in range(0,visu_nx,1):
                for cy in range(0,visu_ny,1):
                    ax.plot((cx*visu_dx,cx*visu_dx),(0,lz),(cy*visu_dy,cy*visu_dy),color='aqua',linestyle='--', linewidth=1.2)

            for cz in range(0,visu_nz,1):
                for cy in range(0,visu_ny,1):
                    ax.plot((0,lx),(cz*visu_dz,cz*visu_dz),(cy*visu_dy,cy*visu_dy),color='magenta',linestyle='--', linewidth=1.2)

            if nobj>0:
                print(f'Surface #{plot}: {str(e1[0]+e2[0])} plane got {nobj} intersections','\n')
            else:
                print(f'Surface #{plot}: {str(e1[0]+e2[0])} plane got no intersections ','\n')

    ax.invert_yaxis()

    plt.show()

def gen_epsi_revolve(identif):
    
    """
    not updated
    
    """
    
    if eq_storage[f'superiorrc{identif}'][10]==True:
        loop_path=['normal','x','y','z']
    if eq_storage[f'superiorrc{identif}'][10]==False:
        loop_path=['normal']
    
    for raf in loop_path:
        
        print(raf)
        dx_gen,dy_gen,dz_gen=dx,dy,dz
        nx_gen,ny_gen,nz_gen=nx,ny,nz
        matrix_gen=epsi_3d

        try:
            if raf=='x':
                dx_gen,nx_gen=dx_raf,nx_raf
                matrix_gen=epsi_3d_x_raf
            if raf=='y':
                dy_gen,ny_gen=dy_raf,ny_raf
                matrix_gen=epsi_3d_y_raf
            if raf=='z':
                dz_gen,nz_gen=dz_raf,nz_raf
                matrix_gen=epsi_3d_z_raf
        except:
            pass

        x=np.linspace(0.,lx,nx_gen,dtype=np.float32)
        y=np.linspace(0.,ly,ny_gen,dtype=np.float32)
        z=np.linspace(0.,lz,nz_gen,dtype=np.float32)
                                                                            

        X = np.zeros_like(matrix_gen)
        Y = np.zeros_like(matrix_gen)
        Z = np.zeros_like(matrix_gen)

        for j in range(y.size):
            for k in range(z.size):
                X[:,j,k] = x
        for i in range(x.size):
            for k in range(z.size):
                Y[i,:,k] = y
        for i in range(x.size):
            for j in range(y.size):
                Z[i,j,:] = z


        if eq_storage[f'superiorrc{identif}'][4]=='xy':
            X, Y = np.meshgrid(x, y)
            epsi = np.zeros_like(X)
            bar = progressbar.ProgressBar(widgets=[f'#{identif} (revolve): ', progressbar.AnimatedMarker(), progressbar.Percentage(), progressbar.Bar(),'  ', 
                                                   progressbar.Timer()],max_value=((int(eq_storage[f'superiorrc{identif}'][9]/dz_gen)+1)-math.ceil(eq_storage[f'superiorrc{identif}'][8]/dz_gen))).start()

            for cz in range(math.ceil(eq_storage[f'superiorrc{identif}'][8]/dz_gen),int(eq_storage[f'superiorrc{identif}'][9]/dz_gen)+1,1):
                bar+=1
                epsi=matrix_gen[:,:,cz].T
                dis = np.sqrt((X-eq_storage[f'superiorrc{identif}'][6])**2.+(Y-eq_storage[f'superiorrc{identif}'][7])**2.)
                epsi[dis<=list_storage[f'superior{identif}_{raf}'][0][cz-math.ceil(eq_storage[f'superiorrc{identif}'][8]/dz_gen)]] = 1
                epsi[dis<list_storage[f'inferior{identif}_{raf}'][0][cz-math.ceil(eq_storage[f'inferiorrc{identif}'][8]/dz_gen)]] = 0
                matrix_gen[:,:,cz]=epsi.T.copy()

        if eq_storage[f'superiorrc{identif}'][4]=='zy':
            Z, Y = np.meshgrid(z, y)
            epsi = np.zeros_like(Z)
            bar = progressbar.ProgressBar(widgets=[f'#{identif} (revolve): ', progressbar.AnimatedMarker(), progressbar.Percentage(), progressbar.Bar(),'  ', 
                                                   progressbar.Timer()],max_value=(2*(int(eq_storage[f'superiorrc{identif}'][9]/dx_gen)+1)-math.ceil(eq_storage[f'superiorrc{identif}'][8]/dx_gen))).start()

            for cx in range(math.ceil(eq_storage[f'superiorrc{identif}'][8]/dx_gen),int(eq_storage[f'superiorrc{identif}'][9]/dx_gen)+1,1):
                bar+=1
                epsi=matrix_gen[cx,:,:]
                dis = np.sqrt((Z-eq_storage[f'superiorrc{identif}'][6])**2.+(Y-eq_storage[f'superiorrc{identif}'][7])**2.)
                epsi[dis<=list_storage[f'superior{identif}_{raf}'][0][cx-math.ceil(eq_storage[f'superiorrc{identif}'][8]/dx_gen)]] = 1
                epsi[dis<list_storage[f'inferior{identif}_{raf}'][0][cx-math.ceil(eq_storage[f'inferiorrc{identif}'][8]/dx_gen)]] = 0
                matrix_gen[cx,:,:]=epsi.copy()

        if eq_storage[f'superiorrc{identif}'][4]=='xz':
            X, Z = np.meshgrid(x, z)
            epsi = np.zeros_like(X)
            bar = progressbar.ProgressBar(widgets=[f'#{identif} (revolve): ', progressbar.AnimatedMarker(), progressbar.Percentage(), progressbar.Bar(),'  ', 
                                                   progressbar.Timer()],max_value=(2*(int(eq_storage[f'superiorrc{identif}'][9]/dy_gen)+1)-math.ceil(eq_storage[f'superiorrc{identif}'][8]/dy_gen))).start()

            for cy in range(math.ceil(eq_storage[f'superiorrc{identif}'][8]/dy_gen),int(eq_storage[f'superiorrc{identif}'][9]/dy_gen)+1,1):
                bar+=1
                epsi=matrix_gen[:,cy,:].T
                dis = np.sqrt((X-eq_storage[f'superiorrc{identif}'][6])**2.+(Z-eq_storage[f'superiorrc{identif}'][7])**2.)
                epsi[dis<=list_storage[f'superior{identif}_{raf}'][0][cy-math.ceil(eq_storage[f'superiorrc{identif}'][8]/dy_gen)]] = 1
                epsi[dis<list_storage[f'inferior{identif}_{raf}'][0][cy-math.ceil(eq_storage[f'inferiorrc{identif}'][8]/dy_gen)]] = 0
                matrix_gen[:,cy,:]=epsi.T.copy()

        bar.finish()

def gen_epsi_bezier(surface_type,plane,identif,bez_raf_path=False):
    
    """
    
    Nesta função, usamos as equações geradas pelos pontos fornecidos pelo usuário para setar os limites de onde é solid (na Epsi, :obj:`1`) e onde
    não é solid (na Epsi, :obj:`0`). Vamos setar o que é considerado entry e exit, ou ambos ao mesmo tempo, **para todas as superfícies criadas**. 
    Vamos, também, tornar mais barata o cálculo de nossa Epsi com simetrias. Vamos definir qual o melhor plane para calcular os limites.
    
    **Preste atenção. Se algo pode dar errado, é aqui.**
        
    Args:
        surface_type (:obj:`str`): Defina se a superfície em questão é considerada uma entry, uma exit ou ambos em relação ao solid.
        
                            +-------------------------+------------------------------------+
                            | surface_type            | Set :obj:`surface_type` as         | 
                            +=========================+====================================+
                            | entry                   | :obj:`'entry+exit and/or entry'`   |
                            +-------------------------+------------------------------------+
                            | exit                    | :obj:`'entry+exit and/or exit'`    |
                            +-------------------------+------------------------------------+
                            | entry/exit              |  whatever                          |
                            +-------------------------+------------------------------------+
                            | entry/exit + entry      | :obj:`'entry+exit and/or entry'`   |
                            +-------------------------+------------------------------------+
                            | entry/exit + exit       | :obj:`'entry+exit and/or exit'`    |  
                            +-------------------------+------------------------------------+

    Args: 
        plane (:obj:`str`): Escolha o melhor plane para resolver sua superfície. Caso o plane xy seja o melhor, setar :obj:`plane='xy'`. Pode assumir apenas :obj:`'xz','xy','zy'`.
        identif (:obj:`str`): Repita o argumento :obj:`identif` da superfície em questão.
            Caso utilize este termo, projete apenas metade das superfícies caso elas cruzem o axis de simetria. Caso contrário, o método não resulta em ganhos significativos.
        bez_raf_path (:obj:`Bool`, optional): No início do projeto (fase de ajustes de superfícies) o usuário não terá interesse em setar como True, uma vez que esse argumento 
            calcula todos os refinamentos da malha, o que pode tomar um tempo desnecessário.
    
    **Exemplo:**
        .. figure:: images/ex_entradasaidasaida.png
           :scale: 70%
           :align: center
           
        Podemos notar 2 supefícies na figura, uma verde (:obj:`identif='0'`) e outra roxa (:obj:`identif='1'`). 
        De acordo com esta situação, a invocação da função :obj:`gen_epsi()` pode se dar na seguinte forma::
            
            gen_epsi('entry+exit and/or entry','zy','0')
            gen_epsi('entry+exit and/or exit','zy','1')
           
        Podemos notar também um ponto que é o início de um vetor perpendicular ao plane 'zy'. Este vetor é a representação do que define o :obj:`surface_type` de cada superfície.
        Toda vez que o vetor encontrar alguma superfícies, será definido um limite para a criação da Epsi.
        Devemos imaginar que para cada combinação de coordenada 'z' e 'y' (espaçamento definido por dz e dy) um vetor desses é originado. Portanto: 
        
            1. O sólido verde é considerado *entry Pura* pois, no instante em que é interceptado pelos vetores, 
            **entra-se no sólido**. 
            
            2. O sólido roxo deve ser dividido em 2 partes e é considerado *entry/exit + exit*. A primeira parte é a superior, logo acima da superfície verde.
            Toda esta parte será interceptada pelos vetores duas vezes e **por isso é considerada entry/exit**. A segunda parte é a inferior, que 'compartilha'
            altura com a superfície verde. Esta parte será interceptada pelos vetores apenas uma vez e em todas elas o sólido já terá acabado, por isso é considerada
            também como **exit**.
        
    Warning:
        Caso construída uma superfície que possua segmentos com possíveis entrys/exits simultâneas (superfície roxa), certificar que a superfície seja construída 
        no sentido positivo: os pontos iniciais devem ser mais próximos da origem do que os pontos finais, independente do plane.
    
    Warning:
        Caso a superfície identificada com :obj:`identif` seja *entry*, a partir do momento em que a Epsi encontrar a superfície até o fim da 
        Epsi será setado como 1. Caso seja *exit*, 
        a partir do momento em que a Epsi encontrar a superfície até o fim da Epsi será setado como 0. 
        
        *É necessário perceber que a ordem com que essa 
        função é chamada tem muita importância:* caso o usuário chame primeiro as exits, o código vai entender que a partir do encontro da superfície 
        é necessário marcar como 0 algo que já está setado como 0 (a matriz Epsi é setada inicialmente apemas com 0, com dimensões nx, ny e nz). Seguindo a lógica, 
        o usuário agora então chamaria as entrys. A partir do encontro da superfície, tudo será setado com 1 até o fim da matriz e assim ficará definido. 
        Ou seja, o sólido *não foi representado corretamente.*
    
    Warning:
        **Explicando 'plane' mais uma vez:**
        
        Para cada combinação de coordenada (xy, xz ou zy), imagine um vetor saíndo de cada nó existente.
        Como por exemplo, falaremos do plane xy. De cada posição x e de cada posição y possível, sairá um vetor em direção à z.
        Toda vez que esse vetor cruzar uma superfície, será contabilizado um limite para a Epsi. O usuário já determinou que 
        tipo de limite será no argumento anterior.
        *Logo, é de extrema importância que o usuário escolha o plane certo para resolver o seu sólido.*
        Imagine outro exemplo, onde o usuário construiu um quadrado no plane xy (ou seja, paralelo ao plane xy), com alguma altura constante qualquer.
        Esse quadrado não possui dimensão alguma para qualquer plane a não ser o plane xy.
        Em outras palavras, o plane zy e o plane zx nunca cruzarão este quadrado, logo a Epsi não será construída corretamente pois não haverá limite algum para isso.
        E isso é perfeitamente demonstrado pela a função :obj:`intersection_preview()`. Inclusive, o retorno desta função explicita onde há interceptação dos vetores com a superfície, 
        tornando mais clara a escolha deste argumento.
    """   
    
    if bez_raf_path==True:
        loop_path=['normal','x','y','z']
    if bez_raf_path==False:
        loop_path=['normal']
        
    for raf in loop_path:
        
        dx_gen,dy_gen,dz_gen=dx,dy,dz
        nx_gen,ny_gen,nz_gen=nx,ny,nz
        matrix_gen=epsi_3d

        if raf=='x':
            dx_gen,nx_gen=dx_raf,nx_raf
            matrix_gen=epsi_3d_x_raf
        if raf=='y':
            dy_gen,ny_gen=dy_raf,ny_raf
            matrix_gen=epsi_3d_y_raf
        if raf=='z':
            dz_gen,nz_gen=dz_raf,nz_raf
            matrix_gen=epsi_3d_z_raf

        max_z,max_y,max_x=0,0,0

        for p,k in eq_storage.items():
            if p[0]=='z':
                if k[5]>max_z:
                    max_z=k[5]
            if p[0]=='y':
                if k[5]>max_y:
                    max_y=k[5]
            if p[0]=='x':
                if k[5]>max_x:
                    max_x=k[5]

        max_x,max_y,max_z = int(max_x/dx_gen),int(max_y/dy_gen),int(max_z/dz_gen)    

        if plane == 'zy':
            axis1, min_1, max_1, d1 = str(f'z{identif}'), math.ceil(eq_storage[f'z{identif}'][4]/dz_gen), int(eq_storage[f'z{identif}'][5]/dz_gen), dz_gen
            axis2, min_2, max_2, d2 = str(f'y{identif}'), math.ceil(eq_storage[f'y{identif}'][4]/dy_gen), int(eq_storage[f'y{identif}'][5]/dy_gen), dy_gen
            axis3, min_3, max_3, d3 = str(f'x{identif}'), math.ceil(eq_storage[f'x{identif}'][4]/dx_gen), nx_gen, dx_gen

        if plane == 'xz':
            axis1, min_1, max_1, d1 = str(f'x{identif}'), math.ceil(eq_storage[f'x{identif}'][4]/dx_gen), int(eq_storage[f'x{identif}'][5]/dx_gen), dx_gen
            axis2, min_2, max_2, d2 = str(f'z{identif}'), math.ceil(eq_storage[f'z{identif}'][4]/dz_gen), int(eq_storage[f'z{identif}'][5]/dz_gen), dz_gen
            axis3, min_3, max_3, d3 = str(f'y{identif}'), math.ceil(eq_storage[f'y{identif}'][4]/dy_gen), ny_gen, dy_gen

        if plane == 'xy':
            axis1, min_1, max_1, d1 = str(f'x{identif}'), math.ceil(eq_storage[f'x{identif}'][4]/dx_gen), int(eq_storage[f'x{identif}'][5]/dx_gen), dx_gen
            axis2, min_2, max_2, d2 = str(f'y{identif}'), math.ceil(eq_storage[f'y{identif}'][4]/dy_gen), int(eq_storage[f'y{identif}'][5]/dy_gen), dy_gen
            axis3, min_3, max_3, d3 = str(f'z{identif}'), math.ceil(eq_storage[f'z{identif}'][4]/dz_gen), nz_gen, dz_gen

        grau= max(eq_storage[f'z{identif}'][6],eq_storage[f'z{identif}'][7])

        bar = progressbar.ProgressBar(widgets=[f'#{identif} ({(max_2+1-min_2)*(max_1+1-min_1)} knot², order {grau}): ',
                                               progressbar.AnimatedMarker(),
                                               progressbar.Percentage(),
                                               progressbar.Bar(),'  ',
                                               progressbar.Timer(),], 
                                               max_value=(max_1+1-min_1)*(max_2+1-min_2)).start()

        for c1 in range(min_1,max_1+1,1):
            for c2 in range(min_2,max_2+1,1):
                bar+=1
                try:
                    args_list=[]
                    intersec = nonlinsolve([eq_storage[f'{axis1}'][1][0]-c1*d1,eq_storage[f'{axis2}'][1][0]-c2*d2],[u,v])
                    for prmt in range(0,len(intersec.args)):
                        if intersec.args[prmt][0].is_real == True and 0<=round(intersec.args[prmt][0],5)<=1:
                            if intersec.args[prmt][1].is_real == True and 0<=round(intersec.args[prmt][1],5)<=1:
                                args_list+=intersec.args[prmt]

                    for c3 in range(min_3,max_3+1,1):
                        if surface_type == 'entry+exit and/or exit':
                            if len(args_list)==4:
                                if eq_storage[f'{axis3}'][2](args_list[0],args_list[1])<=c3*d3<eq_storage[f'{axis3}'][2](args_list[2],args_list[3]):
                                        if plane == 'zy':
                                            matrix_gen[c3][c2][c1] = 1
                                        if plane == 'xz':
                                            matrix_gen[c1][c3][c2] = 1
                                        if plane == 'xy':
                                            matrix_gen[c1][c2][c3] = 1
                            if len(args_list)==2:
                                if c3*d3>eq_storage[f'{axis3}'][2](args_list[0],args_list[1]):
                                    if plane == 'zy':
                                        matrix_gen[c3][c2][c1] = 0
                                    if plane == 'xz':
                                        matrix_gen[c1][c3][c2] = 0
                                    if plane == 'xy':
                                        matrix_gen[c1][c2][c3] = 0

                        if surface_type == 'entry+exit and/or entry':
                            if len(args_list)==4:
                                if eq_storage[f'{axis3}'][2](args_list[0],args_list[1])<=c3*d3<eq_storage[f'{axis3}'][2](args_list[2],args_list[3]):
                                        if plane == 'zy':
                                            matrix_gen[c3][c2][c1] = 1
                                        if plane == 'xz':
                                            matrix_gen[c1][c3][c2] = 1
                                        if plane == 'xy':
                                            matrix_gen[c1][c2][c3] = 1
                            if len(args_list)==2:
                                if c3*d3>=eq_storage[f'{axis3}'][2](args_list[0],args_list[1]):
                                    if plane == 'zy':
                                        matrix_gen[c3][c2][c1] = 1
                                    if plane == 'xz':
                                        matrix_gen[c1][c3][c2] = 1
                                    if plane == 'xy':
                                        matrix_gen[c1][c2][c3] = 1

                except: 
                    pass

        bar.finish()
    
def gen_epsi_mirror(direction, mirror_raf_path=False):
    
    """
    not updated
    
    """
    
    if mirror_raf_path==True:
        loop_path=['normal','x','y','z']
    if mirror_raf_path==False:
        loop_path=['normal']
        
    for raf in loop_path:
        dx_gen,dy_gen,dz_gen=dx,dy,dz
        nx_gen,ny_gen,nz_gen=nx,ny,nz
        matrix_gen=epsi_3d

        try:
            if raf=='x':
                dx_gen,nx_gen=dx_raf,nx_raf
                matrix_gen=epsi_3d_x_raf
            if raf=='y':
                dy_gen,ny_gen=dy_raf,ny_raf
                matrix_gen=epsi_3d_y_raf
            if raf=='z':
                dz_gen,nz_gen=dz_raf,nz_raf
                matrix_gen=epsi_3d_z_raf
        except:
            pass

        if direction=='y':
            if (ny_gen%2!=0) == True: #impar
                zero_side=int(ny_gen/2)
                processed_side=int(ny_gen/2)
                for cy in range(int(ny_gen/2),ny_gen-1):
                    zero_side+=1
                    processed_side-=1
                    matrix_gen[:,zero_side,:] = matrix_gen[:,processed_side,:]

            if (ny_gen%2!=0) == False: #par
                zero_side=int(ny_gen/2-1)
                processed_side=int(ny_gen/2)
                for cy in range(int(ny_gen/2)-1,ny_gen-1):
                    zero_side+=1
                    processed_side-=1
                    matrix_gen[:,zero_side,:] = matrix_gen[:,processed_side,:]

        if direction=='x':
            if (nx_gen%2!=0) == True:
                zero_side=int(nx_gen/2)
                processed_side=int(nx_gen/2)
                for cx in range(int(nx_gen/2),nx_gen-1):
                    zero_side+=1
                    processed_side-=1
                    matrix_gen[zero_side,:,:] = matrix_gen[processed_side,:,:]

            if (nx_gen%2!=0) == False:
                zero_side=int(nx_gen/2-1)
                processed_side=int(nx_gen/2)
                for cx in range(int(nx_gen/2)-1,nx_gen-1):
                    zero_side+=1
                    processed_side-=1
                    matrix_gen[zero_side,:,:] = matrix_gen[processed_side,:,:]

        if direction=='z':
            if (nz_gen%2!=0) == True:
                zero_side=int(nz_gen/2)
                processed_side=int(nz_gen/2)
                for cz in range(int(nz_gen/2),nz_gen-1):
                    zero_side+=1
                    processed_side-=1
                    matrix_gen[:,:,zero_side] = matrix_gen[:,:,processed_side]

            if (nz_gen%2!=0) == False:
                zero_side=int(nz_gen/2-1)
                processed_side=int(nz_gen/2)
                for cz in range(int(nz_gen/2)-1,nz_gen-1):
                    zero_side+=1
                    processed_side-=1
                    matrix_gen[:,:,zero_side] = matrix_gen[:,:,processed_side]
    
    
def gen_epsi_cylinder(identif, surface_type, cyl_raf_path=False):
    
    """
    not updated
    
    """
    
    if cyl_raf_path==True:
        loop_path=['normal','x','y','z']
    if cyl_raf_path==False:
        loop_path=['normal']
        
    for raf in loop_path:

        dx_gen,dy_gen,dz_gen=dx,dy,dz
        nx_gen,ny_gen,nz_gen=nx,ny,nz
        matrix_gen=epsi_3d

        if raf=='x':
            dx_gen,nx_gen=dx_raf,nx_raf
            matrix_gen=epsi_3d_x_raf
        if raf=='y':
            dy_gen,ny_gen=dy_raf,ny_raf
            matrix_gen=epsi_3d_y_raf
        if raf=='z':
            dz_gen,nz_gen=dz_raf,nz_raf
            matrix_gen=epsi_3d_z_raf

        x=np.linspace(0.,lx,nx_gen,dtype=np.float32)
        y=np.linspace(0.,ly,ny_gen,dtype=np.float32)
        z=np.linspace(0.,lz,nz_gen,dtype=np.float32)

        X = np.zeros_like(matrix_gen)
        Y = np.zeros_like(matrix_gen)
        Z = np.zeros_like(matrix_gen)

        for j in range(y.size):
            for k in range(z.size):
                X[:,j,k] = x
        for i in range(x.size):
            for k in range(z.size):
                Y[i,:,k] = y
        for i in range(x.size):
            for j in range(y.size):
                Z[i,j,:] = z
                

        if eq_storage[f'c{identif}'][4]=='xy':
            bar = progressbar.ProgressBar(widgets=[f'#{identif}: ',
                                               progressbar.AnimatedMarker(),
                                               progressbar.Percentage(),
                                               progressbar.Bar(),'  ',
                                               progressbar.Timer(),], 
                                               max_value=(int(eq_storage[f'c{identif}'][9]/dz_gen)+1-math.ceil(eq_storage[f'c{identif}'][8]/dz_gen))).start()
            X, Y = np.meshgrid(x, y)
            epsi = np.zeros_like(X)
            if surface_type=='solid':
                for cz in range(math.ceil(eq_storage[f'c{identif}'][8]/dz_gen),int(eq_storage[f'c{identif}'][9]/dz_gen)+1,1):
                    bar+=1
                    epsi=matrix_gen[:,:,cz].T
                    dis = np.sqrt((X-eq_storage[f'c{identif}'][6])**2.+(Y-eq_storage[f'c{identif}'][7])**2.)
                    epsi[dis<=eq_storage[f'c{identif}'][5]] = 1
                    matrix_gen[:,:,cz]=epsi.T.copy()

            if surface_type=='contour':
                for cz in range(math.ceil(eq_storage[f'c{identif}'][8]/dz_gen),int(eq_storage[f'c{identif}'][9]/dz_gen)+1,1):
                    bar+=1
                    epsi=matrix_gen[:,:,cz].T
                    dis = np.sqrt((X-eq_storage[f'c{identif}'][6])**2.+(Y-eq_storage[f'c{identif}'][7])**2.)
                    epsi[dis<=eq_storage[f'c{identif}'][5]] = 0
                    matrix_gen[:,:,cz]=epsi.T.copy()

        if eq_storage[f'c{identif}'][4]=='xz':
            bar = progressbar.ProgressBar(widgets=[f'#{identif}: ',
                                               progressbar.AnimatedMarker(),
                                               progressbar.Percentage(),
                                               progressbar.Bar(),'  ',
                                               progressbar.Timer(),], 
                                               max_value=(int(eq_storage[f'c{identif}'][9]/dy_gen)+1-math.ceil(eq_storage[f'c{identif}'][8]/dy_gen))).start()
            X, Z = np.meshgrid(x, z)
            epsi = np.zeros_like(X)
            if surface_type=='solid':
                for cy in range(math.ceil(eq_storage[f'c{identif}'][8]/dy_gen),int(eq_storage[f'c{identif}'][9]/dy_gen)+1,1):
                    bar+=1
                    epsi=matrix_gen[:,cy,:].T
                    dis = np.sqrt((X-eq_storage[f'c{identif}'][6])**2.+(Z-eq_storage[f'c{identif}'][7])**2.)
                    epsi[dis<=eq_storage[f'c{identif}'][5]] = 1
                    matrix_gen[:,cy,:]=epsi.T.copy()

            if surface_type=='contour':
                for cy in range(math.ceil(eq_storage[f'c{identif}'][8]/dy_gen),int(eq_storage[f'c{identif}'][9]/dy_gen)+1,1):
                    bar+=1
                    epsi=matrix_gen[:,cy,:].T
                    dis = np.sqrt((X-eq_storage[f'c{identif}'][6])**2.+(Z-eq_storage[f'c{identif}'][7])**2.)
                    epsi[dis<=eq_storage[f'c{identif}'][5]] = 0
                    matrix_gen[:,cy,:]=epsi.T.copy()

        if eq_storage[f'c{identif}'][4]=='zy':
            bar = progressbar.ProgressBar(widgets=[f'#{identif}: ',
                                               progressbar.AnimatedMarker(),
                                               progressbar.Percentage(),
                                               progressbar.Bar(),'  ',
                                               progressbar.Timer(),], 
                                               max_value=(int(eq_storage[f'c{identif}'][9]/dx_gen)+1-math.ceil(eq_storage[f'c{identif}'][8]/dx_gen))).start()
            Z, Y = np.meshgrid(z, y)
            epsi = np.zeros_like(Z)
            if surface_type=='solid':
                for cx in range(math.ceil(eq_storage[f'c{identif}'][8]/dx_gen),int(eq_storage[f'c{identif}'][9]/dx_gen)+1,1):
                    bar+=1
                    epsi=matrix_gen[cx,:,:]
                    dis = np.sqrt((Z-eq_storage[f'c{identif}'][6])**2.+(Y-eq_storage[f'c{identif}'][7])**2.)
                    epsi[dis<=eq_storage[f'c{identif}'][5]] = 1
                    matrix_gen[cx,:,:]=epsi.copy()

            if surface_type=='contour':
                for cx in range(math.ceil(eq_storage[f'c{identif}'][8]/dx_gen),int(eq_storage[f'c{identif}'][9]/dx_gen)+1,1):
                    bar+=1
                    epsi=matrix_gen[cx,:,:]
                    dis = np.sqrt((Z-eq_storage[f'c{identif}'][6])**2.+(Y-eq_storage[f'c{identif}'][7])**2.)
                    epsi[dis<=eq_storage[f'c{identif}'][5]] = 0
                    matrix_gen[cx,:,:]=epsi.copy()
                                          
        bar.finish()

def gen_epsi_sphere(identif, surface_type, sph_raf_path=False):
    
    """
    not updated
    
    """
    
    if sph_raf_path==True:
        loop_path=['normal','x','y','z']
    if sph_raf_path==False:
        loop_path=['normal']
        
    for raf in loop_path:
        dx_gen,dy_gen,dz_gen=dx,dy,dz
        nx_gen,ny_gen,nz_gen=nx,ny,nz
        matrix_gen=epsi_3d

        if raf=='x':
            dx_gen,nx_gen=dx_raf,nx_raf
            matrix_gen=epsi_3d_x_raf
        if raf=='y':
            dy_gen,ny_gen=dy_raf,ny_raf
            matrix_gen=epsi_3d_y_raf
        if raf=='z':
            dz_gen,nz_gen=dz_raf,nz_raf
            matrix_gen=epsi_3d_z_raf

        x=np.linspace(0.,lx,nx_gen,dtype=np.float32)
        y=np.linspace(0.,ly,ny_gen,dtype=np.float32)
        z=np.linspace(0.,lz,nz_gen,dtype=np.float32)

        X = np.zeros_like(matrix_gen)
        Y = np.zeros_like(matrix_gen)
        Z = np.zeros_like(matrix_gen)

        for j in range(y.size):
            for k in range(z.size):
                X[:,j,k] = x
        for i in range(x.size):
            for k in range(z.size):
                Y[i,:,k] = y
        for i in range(x.size):
            for j in range(y.size):
                Z[i,j,:] = z

        dis = np.sqrt((X-eq_storage[f's{identif}'][4])**2.+
                      (Y-eq_storage[f's{identif}'][5])**2.+
                      (Z-eq_storage[f's{identif}'][6])**2.)

        if surface_type=='solid':
            matrix_gen[dis<=eq_storage[f's{identif}'][7]] = 1

        if surface_type=='contour':
            matrix_gen[dis<=eq_storage[f's{identif}'][7]] = 0


def epsi_plot(direction, grid=True, integral=False, raf='normal'):
    
    """
    Confira se os limites estão corretos, camada por camada ou por amostragem, em qualquer direção.
    
    Args:
        direction (:obj:`str`): Poderá assumir os seguintes valores: :obj:`'x', 'y', 'z'`.
        grid (:obj:`Bool`, optional): Caso houver número demasiado de nós (>250), setar como :obj:`False` auxiliará na visualização. 
        integral (:obj:`Bool`, optional): Se o usuário quiser conferir meticulosamente todas as camadas, sete como :obj:`True`.
        raf (:obj:`str`, optional): Se o usuário quiser conferir alguma Epsi Refinada, setar com :obj:`'x','y','z'`.

    """
    dx_show,dy_show,dz_show=dx,dy,dz
    nx_show,ny_show,nz_show=nx,ny,nz
    matrix_show=epsi_3d
    
    
    try:
        if raf=='x':
            dx_show,nx_show=dx_raf,nx_raf
            matrix_show=epsi_3d_x_raf
        if raf=='y':
            dy_show,ny_show=dy_raf,ny_raf
            matrix_show=epsi_3d_y_raf
        if raf=='z':
            dz_show,nz_show=dz_raf,nz_raf
            matrix_show=epsi_3d_z_raf
    except:
        pass
            
    if direction == 'z':
        n1,d1,l2,name_l2,l3,name_l3,d2,d3,plane,n2,n3 = nz_show,dz_show,lx,'lx',ly,'ly',dx_show,dy_show,'xy',nx_show,ny_show
    if direction == 'x':
        n1,d1,l2,name_l2,l3,name_l3,d2,d3,plane,n2,n3 = nx_show,dx_show,lz,'lz',ly,'ly',dz_show,dy_show,'zy',nz_show,ny_show
    if direction == 'y':
        n1,d1,l2,name_l2,l3,name_l3,d2,d3,plane,n2,n3 = ny_show,dy_show,lx,'lx',lz,'lz',dx_show,dz_show,'xz',nx_show,nz_show
    
    loop=np.arange(0,n1,1)
    
    if integral==False:
        loop=np.arange(int(n1/6),n1-int(n1/6),int(n1/6))
    
    for c1 in loop:
        fig_epsi, a2 = plt.subplots(figsize = (25/2,12/2))
        fig_epsi.suptitle(f'{plane} plane, {direction} = {round(c1*d1,1)}', fontsize=25)
        a2.set_xlabel(name_l2, fontsize=15), a2.set_ylabel(name_l3, fontsize=15)
        a2.set_xlim(0,l2), a2.set_ylim(0,l3)
        a2.set_xticks(np.arange(0, l2+d2/2, d2)), a2.set_xticks(np.arange(d2/2, l2, d2), minor=True)
        a2.set_yticks(np.arange(0, l3+d3/2, d3)), a2.set_yticks(np.arange(d3/2, l3, d3), minor=True)
        xticks=[]
        for a in range(0,n2,1):
            xticks.append('')
        xticks[0] = '0'
        xticks[-1] = f'{l2}'
        
        yticks=[]
        for a in range(0,n3,1):
            yticks.append('')
        yticks[0] = '0'
        yticks[-1] = f'{l3}'
        
        a2.set_xticklabels(xticks), a2.set_yticklabels(yticks)
        
        if grid==True:
            a2.grid(which='minor', zorder=1), a2.grid(which='major', alpha=0.3, zorder=1)  
        
        if direction == 'z':
            epsi_dependente = matrix_show[:,:,c1].T
        if direction == 'x':
            epsi_dependente = matrix_show[c1,:,:]
        if direction == 'y':
            epsi_dependente = matrix_show[:,c1,:].T
            
        a2.imshow(epsi_dependente, cmap = 'jet', origin='lower',extent=[-d2/2, l2+d2/2, -d3/2, l3+d3/2])
        plt.show()
           
        
def gen_output(names, out_raf_path=False):
    
    """
    Geração dos arquivos de saída. Tornam possível a visualização no ParaView da Epsi, bem como a resolução das equações
    de Navier Stokes nas redondezas do sólido criado.
    
    Args:
        names (:obj:`str`): Entre com o name que será dado aos arquivos gerado pelo programa.
        raf (:obj:`str`): Não há necessidade alguma de manipulação por parte do usuário. 
    
    """
    global count
    
    if out_raf_path==True:
        loop_path=['normal','x','y','z']

    if out_raf_path==False:
        loop_path=['normal']

    for raf in loop_path:
    
        if raf=='normal':
            count+=1
            if count==1:
                if not os.path.exists(f'./{names}/'):
                    os.makedirs(f'./{names}/')
                os.chdir(f'./{names}/')

        dx_print,dy_print,dz_print=dx,dy,dz
        nx_print,ny_print,nz_print=nx,ny,nz
        matrix_print=epsi_3d
        name = ''.join((names,f'_(generation_{count})'))

        if raf=='x':
            dx_print,nx_print=dx_raf,nx_raf
            matrix_print=epsi_3d_x_raf
            name = ''.join((names,f'_xraf_(generation_{count})'))
        if raf=='y':
            dy_print,ny_print=dy_raf,ny_raf
            matrix_print=epsi_3d_y_raf
            name = ''.join((names,f'_yraf_(generation_{count})'))
        if raf=='z':
            dz_print,nz_print=dz_raf,nz_raf
            matrix_print=epsi_3d_z_raf
            name = ''.join((names,f'_zraf_(generation_{count})'))

        matrix_print.T.tofile(name)

        open(f'{name}.xdmf', 'w').close()

        with open(f'{name}.xdmf', 'a') as the_file:
            the_file.write('<?xml version="1.0" ?>\n')
            the_file.write(' <!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
            the_file.write(' <Xdmf xmlns:xi="http://www.w3.org/2001/XInclude" Version="2.0">\n')
            the_file.write(' <Domain>\n')
            the_file.write('     <Topology name="topo" TopologyType="3DCoRectMesh"\n')
            the_file.write(f'         Dimensions="{nz_print} {ny_print} {nx_print}">\n')
            the_file.write('     </Topology>\n')
            the_file.write('     <Geometry name="geo" Type="ORIGIN_DXDYDZ">\n')
            the_file.write('         <!-- Origin -->\n')
            the_file.write('         <DataItem Format="XML" Dimensions="3">\n')
            the_file.write('         0.0 0.0 0.0\n')
            the_file.write('         </DataItem>\n')
            the_file.write('         <!-- DxDyDz -->\n')
            the_file.write('         <DataItem Format="XML" Dimensions="3">\n')
            the_file.write(f'           {dz_print}  {dy_print}  {dx_print}\n')
            the_file.write('         </DataItem>\n')
            the_file.write('     </Geometry>\n')
            the_file.write('\n')
            the_file.write('     <Grid Name="0000" GridType="Uniform">\n')
            the_file.write('         <Topology Reference="/Xdmf/Domain/Topology[1]"/>\n')
            the_file.write('         <Geometry Reference="/Xdmf/Domain/Geometry[1]"/>\n')
            the_file.write('         <Attribute Name="ibm" Center="Node">\n')
            the_file.write('            <DataItem Format="Binary"\n')
            the_file.write('             DataType="Float" Precision="4" Endian="little" \n')
            the_file.write('Seek="0"\n')
            the_file.write(f'             Dimensions="{nz_print} {ny_print} {nx_print}">\n')
            the_file.write(f'               {name}\n')
            the_file.write('            </DataItem>\n')
            the_file.write('         </Attribute>\n')
            the_file.write('     </Grid>\n')
            the_file.write('\n')
            the_file.write(' </Domain>\n')
            the_file.write('</Xdmf>\n')

        fo = FortranFile(''.join((name,'_fortran')), 'w')
        fo.write_record(matrix_print.T.astype(np.float32))
        fo.close()
    
    
def gen_raf_information(nraf):
    
    """
    Geração da Epsi refinada, importante arquivo para o :obj:`Incompact3d`. O objetivo é obter maior precisão em cada dimensão por vez.
    
    Args:
        nraf (:obj:`int`): Entre com o número de vezes que gostaria de multiplicar os nós (refinar a malha).
        
    """
    global nx_raf,dx_raf,epsi_3d_x_raf,raf,ny_raf,dy_raf,epsi_3d_y_raf,nz_raf,dz_raf,epsi_3d_z_raf
    
    nx_raf = nx*nraf
    dx_raf = lx/(nx_raf-1)
    epsi_3d_x_raf = np.zeros((nx_raf,ny,nz),dtype=np.float32)

    ny_raf = ny*nraf
    dy_raf = ly/(ny_raf-1)
    epsi_3d_y_raf = np.zeros((nx,ny_raf,nz),dtype=np.float32)

    nz_raf = nz*nraf
    dz_raf=lz/(nz_raf-1)
    epsi_3d_z_raf = np.zeros((nx,ny,nz_raf),dtype=np.float32)
