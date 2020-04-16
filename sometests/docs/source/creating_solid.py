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
u_plot=s.u_plot
v_plot=s.v_plot
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
    Auxílio na hora de setar os pontos necessários para as equações da função :obj:`gen_bezi()`.
    
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
        Deverá ser obrigatoriamente chamada entre a função :obj:`create_point_matrix()` e a função :obj:`gen_bezi()`.
        
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

            gen_bezi('0',capô)

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

                
def gen_bezi(identif, name, show_equation=False):
    
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
    
    .. image:: ex_supcomplexa.png
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

        eq_storage[f'{direction}{identif}'] = [name,final_matrix,eq,matrix_plot,np.amin(matrix_plot),np.amax(matrix_plot),number_points_u,number_points_v,matrix_no_deflection.copy()]
        
        if show_equation==True:
            print(f'{direction}(u,v) #{identif} surface parametric equation: '),display(final_matrix[0]),print('\n')
            
            
def berstein(n_p):
    
    """
    Matemática chave por trás das curvas/superfícies de Bézier, dentro da própria função :obj:`gen_bezi()`. 
    
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
                
                
def gen_bezi_cylinder(name, bases_plane,radius,center_1,center_2,init_height,final_height,init_identif):
    
    """
    Uma função derivada de :obj:`gen_bezi()` que facilita a criação de cilíndros. De exit são geradas
    4 Béziers (seen as a quadrant) diferentes que juntas formam um cilíndro. Caso esta função seja chamada, no momento de solução
    da Epsi será necessário usar a função :obj:`gen_epsi_cylinder()`.
    
    Args:
        name (:obj:`str`): Set cylinder's name (a short one).
        bases_plane (:obj:`str`): Defina o plane paralelo à base. Pode assumir :obj:`'xy','xz','zy'`.
        radius (:obj:`float`): Defina o raio do cilíndro.
        center_1 (:obj:`float`): Coordenada do axis correspondente à primeira letra do :obj:`bases_plane`.
        center_2 (:obj:`float`): Coordenada do axis correspondente à segunda letra do :obj:`bases_plane`.
        init_height (:obj:`float`): Altura da base inferior do cilíndro.
        final_height (:obj:`float`): Altura da base superior do cilíndro.
        init_identif (:obj:`str`): O mesmo :obj:`identif` do resto do código. O usuário deverá criar apenas a identificação da primeira
            das quatro Béziers geradas na função. Todas as outras identificações são definidas automaticamente.
        
    Exemplo:
        Para criar um cilíndro de raio 1 e altura 2 no plane :obj:`xz` caso alguma superfície já tenha sido criada e 
        identificada com :obj:`identif='0'`::
        
            gen_bezi_cylinder(bases_plane='xz',radius=1,
                              center_1=3, center_2=3
                              init_height=2,final_height=4,
                              init_identif='1')
                              
    Warning:
        Como já descrito, são geradas 4 Béziers nesta função. Portanto, caso haja alguma geração de Bézier depois dessa em questão,
        o argumento :obj:`identif` deverá ser igual ao desta função somadas mais 4 unidades. No exemplo descrito logo acima, o próximo
        :obj:`identif`, quaisquer que seja, deveria ser :obj:`'5'`.

    """
    
    init_identif=int(init_identif)
    cos=math.cos(math.radians(45))
    sin=math.sin(math.radians(45))
    
    if bases_plane=='xy':

        set_point_matrix(3,2)
        point_storage['P00']=[center_1-radius,center_2,init_height]
        point_storage['P01']=[center_1-radius,center_2,final_height]
        point_storage['P10']=[center_1-radius*cos,center_2+radius*sin,init_height]
        point_storage['P11']=[center_1-radius*cos,center_2+radius*sin,final_height]
        point_storage['P20']=[center_1,center_2+radius,init_height]
        point_storage['P21']=[center_1,center_2+radius,final_height]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif}',"".join((name,' 2nd q')))

        set_point_matrix(3,2)
        point_storage['P00']=[center_1,center_2+radius,init_height]
        point_storage['P01']=[center_1,center_2+radius,final_height]
        point_storage['P10']=[center_1+radius*cos,center_2+radius*sin,init_height]
        point_storage['P11']=[center_1+radius*cos,center_2+radius*sin,final_height]
        point_storage['P20']=[center_1+radius,center_2,init_height]
        point_storage['P21']=[center_1+radius,center_2,final_height]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif+1}',"".join((name,' 1st q')))

        set_point_matrix(3,2)
        point_storage['P00']=[center_1-radius,center_2,init_height]
        point_storage['P01']=[center_1-radius,center_2,final_height]
        point_storage['P10']=[center_1-radius*cos,center_2-radius*sin,init_height]
        point_storage['P11']=[center_1-radius*cos,center_2-radius*sin,final_height]
        point_storage['P20']=[center_1,center_2-radius,init_height]
        point_storage['P21']=[center_1,center_2-radius,final_height]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif+2}',"".join((name,' 3rd q')))

        set_point_matrix(3,2)
        point_storage['P00']=[center_1,center_2-radius,init_height]
        point_storage['P01']=[center_1,center_2-radius,final_height]
        point_storage['P10']=[center_1+radius*cos,center_2-radius*sin,init_height]
        point_storage['P11']=[center_1+radius*cos,center_2-radius*sin,final_height]
        point_storage['P20']=[center_1+radius,center_2,init_height]
        point_storage['P21']=[center_1+radius,center_2,final_height]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif+3}',"".join((name,' 4th q')))
        
    if bases_plane=='xz':
    
        set_point_matrix(3,2)
        point_storage['P00']=[center_1-radius,init_height,center_2]
        point_storage['P01']=[center_1-radius,final_height,center_2]
        point_storage['P10']=[center_1-radius*cos,init_height,center_2+radius*sin]
        point_storage['P11']=[center_1-radius*cos,final_height,center_2+radius*sin]
        point_storage['P20']=[center_1,init_height,center_2+radius]
        point_storage['P21']=[center_1,final_height,center_2+radius]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif}',"".join((name,' 2nd q')))

        set_point_matrix(3,2)
        point_storage['P00']=[center_1,init_height,center_2+radius]
        point_storage['P01']=[center_1,final_height,center_2+radius]
        point_storage['P10']=[center_1+radius*cos,init_height,center_2+radius*sin]
        point_storage['P11']=[center_1+radius*cos,final_height,center_2+radius*sin]
        point_storage['P20']=[center_1+radius,init_height,center_2]
        point_storage['P21']=[center_1+radius,final_height,center_2]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif+1}',"".join((name,' 1st q')))

        set_point_matrix(3,2)
        point_storage['P00']=[center_1-radius,init_height,center_2]
        point_storage['P01']=[center_1-radius,final_height,center_2]
        point_storage['P10']=[center_1-radius*cos,init_height,center_2-radius*sin]
        point_storage['P11']=[center_1-radius*cos,final_height,center_2-radius*sin]
        point_storage['P20']=[center_1,init_height,center_2-radius]
        point_storage['P21']=[center_1,final_height,center_2-radius]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif+2}',"".join((name,' 3rd q')))

        set_point_matrix(3,2)
        point_storage['P00']=[center_1,init_height,center_2-radius]
        point_storage['P01']=[center_1,final_height,center_2-radius]
        point_storage['P10']=[center_1+radius*cos,init_height,center_2-radius*sin]
        point_storage['P11']=[center_1+radius*cos,final_height,center_2-radius*sin]
        point_storage['P20']=[center_1+radius,init_height,center_2]
        point_storage['P21']=[center_1+radius,final_height,center_2]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif+3}',"".join((name,' 4th q')))

        
    if bases_plane=='zy':

        set_point_matrix(3,2)
        point_storage['P00']=[init_height,center_2,center_1-radius]
        point_storage['P01']=[final_height,center_2,center_1-radius]
        point_storage['P10']=[init_height,center_2+radius*sin,center_1-radius*cos]
        point_storage['P11']=[final_height,center_2+radius*sin,center_1-radius*cos]
        point_storage['P20']=[init_height,center_2+radius,center_1]
        point_storage['P21']=[final_height,center_2+radius,center_1]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif}',"".join((name,' 2nd q')))

        set_point_matrix(3,2)
        point_storage['P00']=[init_height,center_2+radius,center_1]
        point_storage['P01']=[final_height,center_2+radius,center_1]
        point_storage['P10']=[init_height,center_2+radius*sin,center_1+radius*cos]
        point_storage['P11']=[final_height,center_2+radius*sin,center_1+radius*cos]
        point_storage['P20']=[init_height,center_2,center_1+radius]
        point_storage['P21']=[final_height,center_2,center_1+radius]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif+1}',"".join((name,' 1st q')))

        set_point_matrix(3,2)
        point_storage['P00']=[init_height,center_2,center_1-radius]
        point_storage['P01']=[final_height,center_2,center_1-radius]
        point_storage['P10']=[init_height,center_2-radius*sin,center_1-radius*cos]
        point_storage['P11']=[final_height,center_2-radius*sin,center_1-radius*cos]
        point_storage['P20']=[init_height,center_2-radius,center_1]
        point_storage['P21']=[final_height,center_2-radius,center_1]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif+2}',"".join((name,' 3rd q')))

        set_point_matrix(3,2)
        point_storage['P00']=[init_height,center_2-radius,center_1]
        point_storage['P01']=[final_height,center_2-radius,center_1]
        point_storage['P10']=[init_height,center_2-radius*sin,center_1+radius*cos]
        point_storage['P11']=[final_height,center_2-radius*sin,center_1+radius*cos]
        point_storage['P20']=[init_height,center_2,center_1+radius]
        point_storage['P21']=[final_height,center_2,center_1+radius]
        create_point_matrix(deflection=True)
        gen_bezi(f'{init_identif+3}',"".join((name,' 4th q')))
                
def surface_plot(init_identif,final_identif, points=False, alpha=0.3):
    
    """
    Args:
        init_identif (:obj:`str`): Determine o início do intervalo de superfícies a serem plotadas através da identificação :obj:`identif`.
        final_identif (:obj:`str`): Determine o final do intervalo (endpoint não incluido) de superfícies a serem plotadas através da identificação :obj:`identif`
        points (:obj:`Bool`, optional): Caso queira visualizar os pontos que governam sua superfície, sete como :obj:`True`.
        alpha (:obj:`float`, optional): Controlador da opacidade da superfície em questão. Pode assumir qualquer valor entre :obj:`0` (transparente) e :obj:`1` (opaco).

    """
    init_identif=int(init_identif)
    final_identif=int(final_identif)
    
    global fig,ax
    
    fig = plt.figure(figsize=(11,9))
    ax = fig.add_subplot(1, 1, 1, projection='3d', proj_type='ortho')
    
    ax.set_xlabel('x'),ax.set_ylabel('z'),ax.set_zlabel('y'),ax.set_xlim(0,max([lx,ly,lz])),ax.set_ylim(0,max([lx,ly,lz])),ax.set_zlim(0,max([lx,ly,lz])),
    ax.view_init(25,-145),ax.set_title('Surface/Control Poimts',size=20)
    
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
    
    plt.show()    


def intersection_preview(init_identif,final_identif):
    
    """
    Uma *mini simulação de Epsi*. Para poucos nós em cada direção será checado se os limites são coerentes ou não, 
    ou seja, **se as funções convergiram para o determinado espaçamento de nós ou não**. Cada ponto no gráfico significa uma intersecção entre o vetor e a superfície.
    Se todos forem razoáveis, a superfície será bem entendida pelo solver.
    
    Args:
        init_identif (:obj:`str`): Determine o início do intervalo de superfícies a serem calculadas através da identificação :obj:`identif`.
        final_identif (:obj:`str`): Determine o final do intervalo (endpoint não incluido) de superfícies a serem calcuadas através da identificação :obj:`identif`.
    
    """
    
    init_identif=int(init_identif)
    final_identif=int(final_identif)
    
    fig = plt.figure(figsize=(9,9))
    ax = fig.add_subplot(1, 1, 1, projection='3d', proj_type='ortho')
    
    ax.set_xlabel('x'),ax.set_ylabel('z'),ax.set_zlabel('y'),ax.set_xlim(0,max([lx,ly,lz])),ax.set_ylim(0,max([lx,ly,lz])),ax.set_zlim(0,max([lx,ly,lz])),
    ax.view_init(25,-145),(),ax.set_title('Surface/Intersections',size=20)
    
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


def gen_epsi(surface_type,plane,identif,symmetry='global',raf0='normal'):
    
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
        identif(:obj:`str`): Repita o argumento :obj:`identif` da superfície em questão.
        symmetry(:obj:`str`, optional): Defina alguma simetria de auxílio para barateamento do cálculo da Epsi. Pode assumir :obj:`'symmetry_x','symmetry_y',symmetry_z'`.
            Caso utilize este termo, projete apenas metade das superfícies caso elas cruzem o axis de simetria. Caso contrário, o método não resulta em ganhos significativos.
        raf0(:obj:`str`, optional): Não há necessidade alguma de manipulação por parte do usuário. 
    
    **Exemplo:**
        .. figure:: ex_entradasaidasaida.png
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
    dx_gen,dy_gen,dz_gen=dx,dy,dz
    nx_gen,ny_gen,nz_gen=nx,ny,nz
    matrix_gen=epsi_3d
    
    try:
        if raf0=='x':
            dx_gen,nx_gen=dx_raf,nx_raf
            matrix_gen=epsi_3d_x_raf
        if raf0=='y':
            dy_gen,ny_gen=dy_raf,ny_raf
            matrix_gen=epsi_3d_y_raf
        if raf0=='z':
            dz_gen,nz_gen=dz_raf,nz_raf
            matrix_gen=epsi_3d_z_raf
    except:
        pass
    
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
        axis3, min_3, max_3, d3 = str(f'x{identif}'), math.ceil(eq_storage[f'x{identif}'][4]/dx_gen), max_x, dx_gen
        
    if plane == 'xz':
        axis1, min_1, max_1, d1 = str(f'x{identif}'), math.ceil(eq_storage[f'x{identif}'][4]/dx_gen), int(eq_storage[f'x{identif}'][5]/dx_gen), dx_gen
        axis2, min_2, max_2, d2 = str(f'z{identif}'), math.ceil(eq_storage[f'z{identif}'][4]/dz_gen), int(eq_storage[f'z{identif}'][5]/dz_gen), dz_gen
        axis3, min_3, max_3, d3 = str(f'y{identif}'), math.ceil(eq_storage[f'y{identif}'][4]/dy_gen), max_y, dy_gen
        
    if plane == 'xy':
        axis1, min_1, max_1, d1 = str(f'x{identif}'), math.ceil(eq_storage[f'x{identif}'][4]/dx_gen), int(eq_storage[f'x{identif}'][5]/dx_gen), dx_gen
        axis2, min_2, max_2, d2 = str(f'y{identif}'), math.ceil(eq_storage[f'y{identif}'][4]/dy_gen), int(eq_storage[f'y{identif}'][5]/dy_gen), dy_gen
        axis3, min_3, max_3, d3 = str(f'z{identif}'), math.ceil(eq_storage[f'z{identif}'][4]/dz_gen), max_z, dz_gen
        
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
            
    if symmetry=='symmetry_y':
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
            
    if symmetry=='symmetry_x':
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
            
    if symmetry=='symmetry_z':
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
    
    format_storage[f'{identif}'] = (surface_type,plane,identif,symmetry)
    
    bar.finish()
    

def gen_epsi_cylinder(bases_plane,surface_type,plane,init_identif,symmetry='global',raf0='normal'):
    
    """
    Uma função derivada de :obj:`gen_epsi()` que facilita a geração da Epsi de cilíndros criados com a função
    :obj:`gen_bezi_cylinder()`. 
    
    Args:
        bases_plane (:obj:`str`): Pode assumir :obj:`'xy','xz','zy'`. Deverá ser igual ao definido para o cilíndro em questão na função :obj:`gen_bezi_cylinder()`.
        surface_type (:obj:`str`): Defina se a superfície em questão é considerada um :obj:`'contour'` (imagine posicionar um cilíndro dentro de
            um cubo e subtraí-lo, como se fosse uma tubulação) ou um :obj:`'solid'` (ideal para pneus, rodas, etc). A variável só pode assumir os dois termos destacados.
        plane (:obj:`str`): Escolha o melhor plane para resolver sua superfície. Pode assumir apenas :obj:`'xz','xy','zy'`. Mais informações em :obj:`gen_epsi()`.
        init_identif (:obj:`str`): O mesmo :obj:`identif` setado para o cilíndro em questão na função :obj:`gen_bezi_cylinder()`.
        symmetry(:obj:`str`, optional): Pode assumir :obj:`'symmetry_x','symmetry_y',symmetry_z'`. Mais informações em :obj:`gen_epsi()`.
        raf0(:obj:`str`, optional): Não há necessidade alguma de manipulação por parte do usuário. 
        

    """
    
    init_identif=int(init_identif)
    
    if surface_type=='solid':
        if bases_plane=='xz':
            if plane=='zy':
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}')    
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                
            if plane=='xy':
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}') 
            
        if bases_plane=='xy':
            if plane=='xz':
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}') 
            if plane=='zy':
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}')    
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                
        if bases_plane=='zy':
            if plane=='xz':
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}') 
            if plane=='xy':
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}')    
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                
        
    if surface_type=='contour':
        if bases_plane=='xz':
            if plane=='zy':
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}')    
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                
            if plane=='xy':
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}') 
            
        if bases_plane=='xy':
            if plane=='xz':
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}') 
            if plane=='zy':
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}')    
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                
        if bases_plane=='zy':
            if plane=='xz':
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}') 
            if plane=='xy':
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif}', symmetry=f'{symmetry}') 
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+1}', symmetry=f'{symmetry}')    
                gen_epsi('entry+exit and/or exit',f'{plane}',f'{init_identif+2}', symmetry=f'{symmetry}')
                gen_epsi('entry+exit and/or entry',f'{plane}',f'{init_identif+3}', symmetry=f'{symmetry}')    
    

def epsi_plot(direction, grid=True, integral=False, raf1='normal'):
    
    """
    Confira se os limites estão corretos, camada por camada ou por amostragem, em qualquer direção.
    
    Args:
        direction (:obj:`str`): Poderá assumir os seguintes valores: :obj:`'x', 'y', 'z'`.
        grid (:obj:`Bool`, optional): Caso houver número demasiado de nós (>250), setar como :obj:`False` auxiliará na visualização. 
        integral (:obj:`Bool`, optional): Se o usuário quiser conferir meticulosamente todas as camadas, sete como :obj:`True`.
        raf1 (:obj:`str`, optional): Se o usuário quiser conferir alguma Epsi Refinada, setar com :obj:`'x','y','z'`.

    """
    dx_show,dy_show,dz_show=dx,dy,dz
    nx_show,ny_show,nz_show=nx,ny,nz
    matrix_show=epsi_3d
    
    
    try:
        if raf1=='x':
            dx_show,nx_show=dx_raf,nx_raf
            matrix_show=epsi_3d_x_raf
        if raf1=='y':
            dy_show,ny_show=dy_raf,ny_raf
            matrix_show=epsi_3d_y_raf
        if raf1=='z':
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
        
        
        
def gen_output(names, raf2='normal'):
    
    """
    Geração dos arquivos de saída. Tornam possível a visualização no ParaView da Epsi, bem como a resolução das equações
    de Navier Stokes nas redondezas do sólido criado.
    
    Args:
        names (:obj:`str`): Entre com o name que será dado aos arquivos gerado pelo programa.
        raf2 (:obj:`str`): Não há necessidade alguma de manipulação por parte do usuário. 
    
    """
    global count
    
    
    if raf2=='normal':
        count+=1
        if count==1:
            if not os.path.exists(f'./{names}/'):
                os.makedirs(f'./{names}/')
            os.chdir(f'./{names}/')
    
    dx_print,dy_print,dz_print=dx,dy,dz
    nx_print,ny_print,nz_print=nx,ny,nz
    matrix_print=epsi_3d
    
    try:
        if raf2=='x':
            dx_print,nx_print=dx_raf,nx_raf
            matrix_print=epsi_3d_x_raf
        if raf2=='y':
            dy_print,ny_print=dy_raf,ny_raf
            matrix_print=epsi_3d_y_raf
        if raf2=='z':
            dz_print,nz_print=dz_raf,nz_raf
            matrix_print=epsi_3d_z_raf
    except:
        pass
        
    name = ''.join((names,f'_(generation_{count})'))
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
    
    
def gen_raf_epsi(nraf):
    
    """
    Geração da Epsi refinada, importante arquivo para o :obj:`Incompact3d`. O objetivo é obter maior precisão em cada dimensão por vez.
    
    Args:
        nraf (:obj:`int`): Entre com o número de vezes que gostaria de multiplicar os nós (refinar a malha).
        
    """
    global nx_raf,dx_raf,epsi_3d_x_raf,raf0,ny_raf,dy_raf,epsi_3d_y_raf,raf1,nz_raf,dz_raf,epsi_3d_z_raf,raf2
    
    nx_raf = nx*nraf
    dx_raf = lx/(nx_raf-1)
    epsi_3d_x_raf = np.zeros((nx_raf,ny,nz),dtype=np.float32)
    for p,k in format_storage.items():
        gen_epsi(k[0],k[1],k[2],k[3],raf0='x')

    gen_output(f'{name}_x_raf',raf2='x')

    ny_raf = ny*nraf
    dy_raf = ly/(ny_raf-1)
    epsi_3d_y_raf = np.zeros((nx,ny_raf,nz),dtype=np.float32)
    for p,k in format_storage.items():
        gen_epsi(k[0],k[1],k[2],k[3],raf0='y')

    gen_output(f'{name}_y_raf',raf2='y')

    nz_raf = nz*nraf
    dz_raf=lz/(nz_raf-1)
    epsi_3d_z_raf = np.zeros((nx,ny,nz_raf),dtype=np.float32)
    for p,k in format_storage.items():
        gen_epsi(k[0],k[1],k[2],k[3],raf0='z')

    gen_output(f'{name}_z_raf',raf2='z')