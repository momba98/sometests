# -*- coding: utf-8 -*-
"""
O usuário recebe nessa página todas informações dos argumentos de todas as funções presentes no código.

"""
import matplotlib
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
from scipy.optimize import root    


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
xp=s.xp
yp=s.yp
zp=s.zp
eq_storage=s.eq_storage
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
list_storage=s.list_storage
solid_storage=s.solid_storage

def gen_raf_information(nraf):
    
    """
    Geração de informações para :math:`{\epsilon}` refinada, importante arquivo para o :obj:`Incompact3d`. O objetivo é obter maior precisão em cada dimensão por vez.
    
    Args:
        nraf (:obj:`int`): Entre com o número de vezes que gostaria de multiplicar os nós (refinar a malha).
        
    """
    global nx_raf,dx_raf,epsi_3d_x_raf,raf,ny_raf,dy_raf,epsi_3d_y_raf,nz_raf,dz_raf,epsi_3d_z_raf
    
    if xp==True:
        nx_raf = (nx*nraf)+1
        dx_raf = lx/nx_raf
        epsi_3d_x_raf = np.zeros((nx_raf,ny,nz),dtype=np.float32)
    else:
        nx_raf = ((nx-1)*nraf)+1
        dx_raf = lx/(nx_raf-1)
        epsi_3d_x_raf = np.zeros((nx_raf,ny,nz),dtype=np.float32)

    if yp==True:
        ny_raf = (ny*nraf)+1
        dy_raf = ly/ny_raf
        epsi_3d_y_raf = np.zeros((nx,ny_raf,nz),dtype=np.float32)
    else:
        ny_raf = ((ny-1)*nraf)+1
        dy_raf = ly/(ny_raf-1)
        epsi_3d_y_raf = np.zeros((nx,ny_raf,nz),dtype=np.float32)

    if zp==True:
        nz_raf = (nz*nraf)+1
        dz_raf = lz/nz_raf
        epsi_3d_z_raf = np.zeros((nx,ny,nz_raf),dtype=np.float32)
    else:
        nz_raf = ((nz-1)*nraf)+1
        dz_raf = lz/(nz_raf-1)
        epsi_3d_z_raf = np.zeros((nx,ny,nz_raf),dtype=np.float32)

def set_point_matrix(num_u_points,num_v_points):
    
    """
    
    Determinar o número de pontos em cada direção :math:`{u}` e :math:`{v}` numa superfície de Bézier.
    
    Caso fique em dúvida da nomenclatura de quais pontos serão necessários setar, execute uma célula (após executar a função em pauta) com ``print(point_storage)``::
        
        #exemplo de como tirar a dúvida dos pontos que devem receber algum input
        set_point_matrix(3,3)
        print(point_storage)
    
    Os pontos a serem determinados possuem 2 sub-índices: :math:`{i}` e :math:`{j}` → :math:`{P_{ij}}`
    
    Onde :math:`{i}` corresponde à :math:`{u}`, :math:`{j}` corresponde à :math:`{v}`.
    
    Os sub-índices começarão em :math:`{0}` e irão até :math:`{i-1}` and/or :math:`{j-1}`
    
    Args:
        num_u_points (:obj:`int`): Determine o número de pontos que a direção :math:`{u}` terá.
        num_v_points (:obj:`int`): Determine o número de pontos que a direção :math:`{v}` terá.
    
    Exemplo:
        Será explicitado quais pontos deverão ser setados de acordo com as entrys::
        
            set_point_matrix(3,2) #função é chamada
            
            point_storage['P00'] = [x,y,z] #declara-se as coordenadas do ponto
            point_storage['P01'] = [x,y,z] #seja qualquer ponto de 3 coordenadas dentro do domínio ou não
            point_storage['P10'] = [x,y,z]
            point_storage['P11'] = [x,y,z]
            point_storage['P20'] = [x,y,z]
            point_storage['P21'] = [x,y,z]
            
        O dicionário ``point_storage`` faz parte da mecânica do código, não deve ser alterado. Auxilia na setagem e no armazenamento das informações.

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
    Auxílio na hora de setar os pontos necessários para as equações da função :obj:`gen_bezier_surface()`.
    
    Args: 
        deflection (:obj:`Bool`, optional): Sete como ``True`` caso queira que a superfície passe necessariamente pelos pontos de controle 
            (pontos intermediários, os que normalmente dão a curvatura suave à superfície). Baseia-se num artifício
            matemático que *hackeia* a Bézier, forçando-a a fazer algo que normalmente não faria.
            
    Warning:
        ``deflection=True`` **não demonstrará efeito em todos os casos!**
        
        O parâmetro pode ficar setado como True sem danificar o código, porém só efetivamente desviará a superfície 
        caso ``num_u_points = 3`` ao mesmo tempo que ``num_v_points = 2`` ou vice-versa.
        
        **O porquê da restrição:** 
        
        Como pode-se imaginar, não há necessidade de desviar a superfície para passar em pontos intermediários caso existam apenas 2 
        pontos nas direççoes :math:`{u}` e :math:`{v}` pois não há pontos intermediários. Também, caso a superfície tenha 3 pontos em cada direção 
        :math:`{u}` e :math:`{v}` ou mais, torna-se *matematicamente complicado* descrever o desvio.
            
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
    Caso tenha se precipitado em relação à posição de sua superfície, translade os pontos governantes de uma superfície de Bézier de forma eficiente 
    em qualquer direção. 

    Args:
        direction (:obj:`str`): Defina em qual direção a translação será feita. Deve assumir ``'x'``, ``'y'`` ou ``'z'``.
        quantity (:obj:`int`): Assume quantas unidades de comprimento de domínio o usuário quer translate sua superfície.
        
    Warning: 
        Deverá ser obrigatoriamente chamada entre a função ``create_point_matrix()`` e a função ``gen_bezier_surface()``.

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
            

def rotate(plane,origin,angle):
    
    """
    Rotacione os pontos governantes de uma superfície de Bézier de forma eficiente em qualquer plano, ao redor de qualquer ponto. Função auxiliadora na hora
    da criação de patterns circulares.
    
    Args:
        plane (:obj:`str`): Defina em qual plano a rotação será feita. Deve assumir ``'xy'``, ``'xz'`` ou ``'zy'``.
        origin (:obj:`list,float`): Defina o ponto que será o centro de rotação.
        angle (:obj:`int`): Assume quantos graus o usuário quer rotacionar sua superfície.
        
    Warning: 
        Deverá ser obrigatoriamente chamada entre a função ``create_point_matrix()`` e a função ``gen_bezier_surface()``.

    """
    
    if plane=='xy':
        aux_point_matrix_x=point_matrix_x.copy()
        aux_point_matrix_y=point_matrix_y.copy()
        
        aux_point_matrix_x_no_deflection=point_matrix_x_no_deflection.copy()
        aux_point_matrix_y_no_deflection=point_matrix_y_no_deflection.copy()
        
        for i in range(number_points_u):
            for j in range(number_points_v):
                point_matrix_x_no_deflection[i][j] = (aux_point_matrix_x_no_deflection[i][j]-origin[0])*math.cos(math.radians(angle))-(aux_point_matrix_y_no_deflection[i][j]-origin[1])*math.sin(math.radians(angle))+origin[0]
                      
                point_matrix_x[i][j] = (aux_point_matrix_x[i][j]-origin[0])*math.cos(math.radians(angle))-(aux_point_matrix_y[i][j]-origin[1])*math.sin(math.radians(angle))+origin[0]
                        
                point_matrix_y_no_deflection[i][j] = (aux_point_matrix_y_no_deflection[i][j]-origin[1])*math.cos(math.radians(angle))+(aux_point_matrix_x_no_deflection[i][j]-origin[0])*math.sin(math.radians(angle))+origin[1]
                      
                point_matrix_y[i][j] = (aux_point_matrix_y[i][j]-origin[1])*math.cos(math.radians(angle))+(aux_point_matrix_x[i][j]-origin[0])*math.sin(math.radians(angle))+origin[1]
    
    elif plane=='xz':
        aux_point_matrix_x=point_matrix_x.copy()
        aux_point_matrix_z=point_matrix_z.copy()
        
        aux_point_matrix_x_no_deflection=point_matrix_x_no_deflection.copy()
        aux_point_matrix_z_no_deflection=point_matrix_z_no_deflection.copy()
        
        for i in range(number_points_u):
            for j in range(number_points_v):
                point_matrix_x_no_deflection[i][j] = (aux_point_matrix_x_no_deflection[i][j]-origin[0])*math.cos(math.radians(angle))-(aux_point_matrix_z_no_deflection[i][j]-origin[1])*math.sin(math.radians(angle))+origin[0]
                      
                point_matrix_x[i][j] = (aux_point_matrix_x[i][j]-origin[0])*math.cos(math.radians(angle))-(aux_point_matrix_z[i][j]-origin[1])*math.sin(math.radians(angle))+origin[0]
                        
                point_matrix_z_no_deflection[i][j] = (aux_point_matrix_z_no_deflection[i][j]-origin[1])*math.cos(math.radians(angle))+(aux_point_matrix_x_no_deflection[i][j]-origin[0])*math.sin(math.radians(angle))+origin[1]
                      
                point_matrix_z[i][j] = (aux_point_matrix_z[i][j]-origin[1])*math.cos(math.radians(angle))+(aux_point_matrix_x[i][j]-origin[0])*math.sin(math.radians(angle))+origin[1]
    
    elif plane=='zy':
        aux_point_matrix_z=point_matrix_z.copy()
        aux_point_matrix_y=point_matrix_y.copy()
        
        aux_point_matrix_z_no_deflection=point_matrix_z_no_deflection.copy()
        aux_point_matrix_y_no_deflection=point_matrix_y_no_deflection.copy()
        
        for i in range(number_points_u):
            for j in range(number_points_v):
                point_matrix_z_no_deflection[i][j] = (aux_point_matrix_z_no_deflection[i][j]-origin[0])*math.cos(math.radians(angle))+(aux_point_matrix_y_no_deflection[i][j]-origin[1])*math.sin(math.radians(angle))+origin[0]
                      
                point_matrix_z[i][j] = (aux_point_matrix_z[i][j]-origin[0])*math.cos(math.radians(angle))+(aux_point_matrix_y[i][j]-origin[1])*math.sin(math.radians(angle))+origin[0]
                        
                point_matrix_y_no_deflection[i][j] = (aux_point_matrix_y_no_deflection[i][j]-origin[1])*math.cos(math.radians(angle))-(aux_point_matrix_z_no_deflection[i][j]-origin[0])*math.sin(math.radians(angle))+origin[1]
                      
                point_matrix_y[i][j] = (aux_point_matrix_y[i][j]-origin[1])*math.cos(math.radians(angle))-(aux_point_matrix_z[i][j]-origin[0])*math.sin(math.radians(angle))+origin[1]

        
def gen_bezier_surface(identif, name, show_equation=False):
    
    """
    
    As equações de Bézier são governadas pelos parâmetros :math:`{u}` e :math:`{v}` e fornecem leis para curvas/superfícies. 
    
    São definidas por pontos arbitrados pelo usuário, tendo um mínimo de 2 em cada direção :math:`{u}` e :math:`{v}` e sem algum máximo pré-determinado.
    
    Os pontos iniciais e finais determinam onde a curva começa e termina. *São os únicos pontos por onde a Bézier (naturalmente) passará com certeza*. 
    Os pontos intermediários estão encarregados de fornecer à Bézier uma curvatura suave, sem canto vivo/descontinuidade, 
    portanto a curva/superfície nunca *encosta* neles (para burlar essa situação, veja a função :obj:`create_point_matrix()`).
    
    O grau das equações é definido por número de pontos definidos pelo usuário - 1.
    
    Args:
        identif (:obj:`str`): Crie a **identificação** da feature com :math:`{n}`, onde :math:`{n=0,1,2,3...}` (começar em ``'0'`` e somar ``'1'`` a cada nova superfície).
        name (:obj:`str`): Crie um name para a superfície. Não há regras. 
        show_equations (:obj:`Bool`, optional): Sete como ``True`` caso queira visualizar as equações governantes da superfície em questão.
        
    Warning:
        ``identif()`` **necessita atenção especial**: o usuário voltará a chamar o parâmetro por diversas vezes ao decorrer do código.
        
    É importante frisar que, caso construída uma superfície muito complexa (com variações não lineares entre os pontos em mais de 2 direções :math:`{xyz}`, uma
    superfície muito torcida), a convergência das equações não é garantida.
    
    .. image:: images/ex_supcomplexa.png
       :align: right
       :scale: 40%
                         
    A superfície ao lado possui seguintes equações::
    
        x(𝑢,𝑣) = 4𝑢²−2𝑢+𝑣²(3𝑢2−6𝑢+3)+𝑣(−6𝑢²+12𝑢−6)+3
        
        y(𝑢,𝑣) = 2𝑢²+𝑣²(2𝑢²+1)+𝑣(4−4𝑢²) 
        
        z(𝑢,𝑣) = −3𝑢²+4𝑢+𝑣²(−11𝑢²+14𝑢−7)+𝑣(18𝑢²−20𝑢+10)
        
    Evidentemente, são equações longas, não lineares e dependentes de mais de uma variável. O solver não se dá muito bem com isso. O usuário pode tentar a sorte, simplificar a superfície ou tentar outro tipo de solver na hora de gerar a matriz :math:`{\epsilon}` na função ``gen_epsi_bezier_surface()``.
    
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
    Matemática chave por trás das curvas/superfícies de Bézier, dentro da própria função ``gen_bezier_surface()``. 
    
    Args:
        n_p (:obj:`int`): Não há necessidade alguma de manipulação por parte do usuário.
    
    """
        
    for i in range(n_p): 
        Bint = sp.expand((math.factorial(n_p-1) / (math.factorial(i)*math.factorial(n_p-1-i)))*u**i*(1-u)**(n_p-1-i))
        coef = sp.Poly(Bint, u)
        aux = coef.coeffs()
        for c in range(i):
            aux.append(0)
        for j in range(n_p):
            berst_matrix[i][j]=aux[j] 
                    
    
def gen_extrude_profile(identif, name, direction, init_height, final_height, deflection=False):  
    
    """
    Criação de um perfil que será posteriormente extrudado. O input da função deve assumir a seguinte forma de um dicionário::
    
        #forma geral
        
        c.extrude_information={'#0 identif':['line type','direção da solução',[pontos de controle]],
                               '#1 identif':['line type','direção da solução',[pontos de controle]]} 
                               
        #forma aplicada
                               
        c.extrude_information={'1':['entry+exit and/or exit' ,'v',[[7,2],[2,4],[1,3],[3,2]]],
                               '0':['entry+exit and/or entry','v',[[7,2],[2,0],[1,1],[3,2]]]}
                               
    A key do dicionário, ``'#0 identif'``, é o identificador da curva criada. Também também carrega a função de determinar a ordem em que as curvas serãor resolvidas (*normalmente*
    o usuário vai querer resolver primeiro todas as entradas);
    
    O primeiro termo da lista do dicionário, ``'line type'``, determina que tipo de limite a curva em questão é - entrada ou saída. Deve assumir ``'entry+exit and/or exit'`` ou 
    ``'entry+exit and/or entry'``;
    
    O segundo termo da lista do dicionário - ``'direção da solução'`` - pode assumir ``'v'`` ou ``'h'``, que significam vertical e horizontal, respectivamente. Caso seja escolhido vertical,
    para cada nó no eixo vertical será disparado um vetor que interceptará as curvas. Caso essa curva seja entrada, a partir dessa intersecção o algorítmo interpretará como dentro do
    perfil de extrude. Caso essa curva seja saída, o algorítmo interpretará como fora do perfil de extrude.
    
    O terceiro e último termo do dicionário é uma lista, ``[pontos de controle]``, contendo todos os pontos de controle de cada curva de Bézier que setará o perfil de extrude.
    
    Note:
        Nessa função, as curvas de Bézier podem ser solucionadas na direção do eixo horizontal (da esquerda para a direita) ou pelo eixo vertical (de baixo para cima). Essa configuração é definida pelo termo ``'direção da solução'``, que pode assumir ``'h'`` ou ``'v'``.
    
    Args:
        identif (:obj:`str`): Crie a **identificação** da feature com :math:`{n}`, onde :math:`{n=0,1,2,3...}` (começar em ``'0'`` e somar ``'1'`` a cada nova superfície).
        name (:obj:`str`): Crie um name para a feature. Não há regras. 
        direction (:obj:`str`): Direção na qual o extrude ocorrerá. Deve assumir ``'x'``, ``'y'`` ou ``'z'``.
        init_height (:obj:`float`): Início do extrude, relacionado à ``direction``
        final_height (:obj:`float`): Final do extrude, relacionado à ``direction``
        deflection (:obj:`Bool`, optional): Sete como ``True`` caso queira que a curva passe pelo ponto de controle intermediário (o que normalmente dá curvatura suave à curva). Baseia-se num artifício matemático que *hackeia* a Bézier, forçando-a a fazer algo que normalmente não faria. **Funcional apenas para curvas com 3 pontos**.
                       
    """
    max_x,max_y,max_z=0,0,0
    min_x,min_y,min_z=lx,ly,lz
    
    fig, ax = plt.subplots(figsize=(10,10))
    
    for info, (strct,resolution_axis,points) in extrude_information.items():
        
        number_points=len(points)
        
        point_matrix_x_2d,point_matrix_y_2d=np.empty((len(points),1)),np.empty((len(points),1))
        
        for count in range(number_points):
            
            point_matrix_x_2d[count][0] = points[count][0]
            point_matrix_y_2d[count][0] = points[count][1]    
            
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
            
            eq_storage[f'ext,{direc}{identif},Bezier{info}'] = [eq,
                                                               final_matrix,
                                                               matrix_base.copy(),
                                                               matrix_no_deflection.copy(),
                                                               number_points,
                                                               direction,
                                                               strct,
                                                               name,
                                                               type(eq(t_plot)),
                                                               len(extrude_information),
                                                               resolution_axis,
                                                               init_height,
                                                               final_height
                                                               ]

        if strct=='entry+exit and/or exit':
            line='--'
        elif strct=='entry+exit and/or entry':
            line='-'
        
        #plotting all curves
        
        if eq_storage[f'ext,y{identif},Bezier{info}'][8] == np.ndarray:
            try:
                ax.plot(eq_storage[f'ext,x{identif},Bezier{info}'][0](t_plot),eq_storage[f'ext,y{identif},Bezier{info}'][0](t_plot),linestyle=line,zorder=0,label=''.join(('#',info,', ',strct)))
                ax.legend(loc='best',fontsize = '14')
                ax.scatter(eq_storage[f'ext,x{identif},Bezier{info}'][3],eq_storage[f'ext,y{identif},Bezier{info}'][3], color='black',zorder=2)
            except:
                pass

        if eq_storage[f'ext,y{identif},Bezier{info}'][8] != np.ndarray:
            try:
                subs = np.full((eq_storage[f'ext,x{identif},Bezier{info}'][0](t_plot).size,1),
                                eq_storage[f'ext,y{identif},Bezier{info}'][0](t_plot))
                ax.plot(eq_storage[f'ext,x{identif},Bezier{info}'][0](t_plot),subs,linestyle=line,zorder=0,label=''.join(('#',info,', ',strct)))
                ax.legend(loc='best',fontsize = '14')
                ax.scatter(eq_storage[f'ext,x{identif},Bezier{info}'][3],eq_storage[f'ext,y{identif},Bezier{info}'][3], color='black',zorder=2)
            except:
                pass
        
        elif eq_storage[f'ext,x{identif},Bezier{info}'][8] != np.ndarray:
            try:
                subs = np.full((eq_storage[f'ext,y{identif},Bezier{info}'][0](t_plot).size,1),
                                eq_storage[f'ext,x{identif},Bezier{info}'][0](t_plot))
                ax.plot(subs, eq_storage[f'ext,y{identif},Bezier{info}'][0](t_plot),linestyle=line,zorder=0,label=''.join(('#',info,', ',strct)))
                ax.legend(loc='best',fontsize = '14')
                ax.scatter(eq_storage[f'ext,x{identif},Bezier{info}'][3],eq_storage[f'ext,y{identif},Bezier{info}'][3], color='black',zorder=2)
            except:
                pass
            
    #creating axis
        
    if direction=='z':
        l1,l2,l1n,l2n,n1,n2,d1,d2=lx,ly,'lx','ly',nx,ny,dx,dy

    if direction=='x':
        l1,l2,l1n,l2n,n1,n2,d1,d2=lz,ly,'lz','ly',nz,ny,dz,dy

    if direction=='y':
        l1,l2,l1n,l2n,n1,n2,d1,d2=lx,lz,'lx','lz',nx,nz,dx,dz
        
    if resolution_axis == 'v':
        for count in range(0,n1,1):
            ax.plot([d1*count,d1*count],[0,l2],linestyle='--',linewidth=0.75,color='red',alpha=0.2,zorder=0)
    
    if resolution_axis == 'h':
        for count in range(0,n2,1):
            ax.plot([0,l1],[d2*count,d2*count],linestyle='--',linewidth=0.75,color='red',alpha=0.2,zorder=0)

    ax.set_xlabel(f'{l1n}', fontsize=12),ax.set_ylabel(f'{l2n}', fontsize=12)
    ax.set_xlim(0,l1),ax.set_ylim(0,l2)
    ax.set_title(f'Extrude Profile',size=16)
    ax.grid(True, alpha=0.5,zorder=1)
    ax.set_aspect('equal')
    
    plt.show()
                
            
def gen_toroid(identif, name, bases_plane, external_radius, profile_circle_radius, center_1, center_2, init_height, tor_raf_path=False):
    
    """
    Função facilitadora para criação de um toróide por meio da função ``gen_revolve_profile()``. Não necessita de informações (dicionário) de entrada.
    
    Args:
        identif (:obj:`str`): Crie a **identificação** da feature com :math:`{n}`, onde :math:`{n=0,1,2,3...}` (começar em ``'0'`` e somar ``'1'`` a cada nova superfície).
        name (:obj:`str`): Crie um nome para a feature. Não há regras.
        bases_plane (:obj:`str`): O plano transversal ao toróide, plano no qual o círculo central é paralelo. Deverá assumir ``'xy'``, ``'xz'`` ou ``'zy'``.
        external_radius (:obj:`float`): Raio total do toróide, o ponto mais externo.
        profile_circle_radius (:obj:`float`):  Raio do perfil circular transversal do toróide.
        center_1 (:obj:`float`): 1ª coordenada do centro da base/topo. O eixo correspondende à coordenada dependerá de qual ``bases_plane`` foi definido.
        center_2 (:obj:`float`): 2ª coordenada do centro da base/topo. O eixo correspondende à coordenada dependerá de qual ``bases_plane`` foi definido.    
        init_height (:obj:`float`): Início do toróide na direção perpendicular ao ``bases_plane`` definido.
        tor_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
    
    """
    
    global superior_revolve_info
    
    superior_revolve_info={'0':[[[0,external_radius-profile_circle_radius],
                                 [0,external_radius-profile_circle_radius+profile_circle_radius*0.552284749831],
                                 [profile_circle_radius-profile_circle_radius*0.552284749831,external_radius],
                                 [profile_circle_radius,external_radius]]],
                           
                        '1':   [[[profile_circle_radius,external_radius],
                                 [profile_circle_radius+profile_circle_radius*0.552284749831,external_radius],
                                 [profile_circle_radius+profile_circle_radius,external_radius-profile_circle_radius+profile_circle_radius*0.552284749831],
                                 [profile_circle_radius+profile_circle_radius,external_radius-profile_circle_radius]]]}


    global inferior_revolve_info
    
    inferior_revolve_info={'0':[[[0,external_radius-profile_circle_radius],
                                 [0,external_radius-profile_circle_radius-profile_circle_radius*0.552284749831],
                                 [profile_circle_radius-profile_circle_radius*0.552284749831,external_radius-profile_circle_radius*2],
                                 [profile_circle_radius,external_radius-2*profile_circle_radius]]],
                           
                        '1':   [[[profile_circle_radius,external_radius-profile_circle_radius*2],
                                 [profile_circle_radius+profile_circle_radius*0.552284749831,external_radius-profile_circle_radius*2],
                                 [profile_circle_radius+profile_circle_radius,external_radius-profile_circle_radius-profile_circle_radius*0.552284749831],
                                 [profile_circle_radius+profile_circle_radius,external_radius-profile_circle_radius]]]}
    
    if bases_plane=='xy':
        dirct='z'
    if bases_plane=='xz':
        dirct='y'
    if bases_plane=='zy':
        dirct='x'
        
    gen_revolve_profile(identif, name, dirct, center_1, center_2, init_height, rev_raf_path=tor_raf_path)
    

def gen_revolve_profile(identif, name, direction, center_1, center_2, init_height, deflection=False, rev_raf_path=False):
    
    """
    Construa um perfil de revolve por meio de curvas de Bézier sempre no sentido positivo, sem idas e voltas (cada coordenada :math:`{axis}` so pode ter 1 :math:`{radius}` correspondente). 
    
    **Primeiro ponto de ambos limites (superior e inferior) sempre deve ser 0. Perfil superior e perfil inferior devem terminar no mesmo ponto.**
    
    Para confirmar a efetividade da função, checar que dentro da área do perfil de revolve (área limitada pelo perfil superior e inferior), para toda linha vermelha pontilhada deve existir uma linha cinza contínua.
    
    Note:
        Nessa função, diferentemente da função ``gen_extrude_profile()``, as curvas de Bézier serãos sempre solucionadas na direção do eixo vertical, de baixo para cima.
    
    As informações de entrada para as curvas devem ser feitas da seguinte forma (em dicionário)::
        
        #forma geral
        
        c.inferior_revolve_info={
                                 'n=0':  [[lista de p pontos]],
                                 'n+1':[[lista de p pontos]],
                                }

        c.superior_revolve_info={
                                 'n=0':  [[lista de p pontos]],
                                 'n+1':[[lista de p pontos]],
                                }
        
        #forma aplicada
        
        c.inferior_revolve_info={
                                 '0':[[[0,2],[1,2]]],
                                 '1':[[[1,2],[2,4],[3,2]]],
                                 '2':[[[3,2],[6,2]]]
                                }

        c.superior_revolve_info={
                                 '0':[[[0,5],[2,4]]],
                                 '1':[[[2,4],[4,4]]],
                                 '2':[[[4,4],[5,5]]],
                                 '3':[[[5,5],[6,5]]]
                                }
    
    A key do dicionário, ``n``, deve começar em 0 e aumentar 1 toda vez que uma nova curva for adicionada;
    
    O único termo do dicionário deve ser uma lista de :math:`{p}` pontos bidimensionais, onde :math:`{p}` pode assumir valores diferentes para cada curva (mínimo 2 e máximo (recomendado) 5);
    
    Args:
        identif (:obj:`str`): Crie a **identificação** da feature com :math:`{n}`, onde :math:`{n=0,1,2,3...}` (começar em ``'0'`` e somar ``'1'`` a cada nova superfície).
        name (:obj:`str`): Crie um nome para a feature. Não há regras.
        direction (:obj:`str`): Direção longitudinal do revolve. Deve assumir ``'x'``, ``'y'`` ou ``'z'``.
        center_1 (:obj:`float`): 1ª coordenada do centro da base/topo. O eixo correspondende à coordenada dependerá de qual ``direction`` foi definido.
        center_2 (:obj:`float`): 2ª coordenada do centro da base/topo. O eixo correspondende à coordenada dependerá de qual ``direction`` foi definido.    
        init_height (:obj:`float`): Início do revolve na direção longitudinal.
        deflection (:obj:`Bool`, optional): Sete como ``True`` caso queira que a curva passe pelo ponto de controle intermediário (o que normalmente dá curvatura suave à curva). Baseia-se num artifício matemático que *hackeia* a Bézier, forçando-a a fazer algo que normalmente não faria. **Funcional apenas para curvas com 3 pontos**.
        rev_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
    
    """
    
    #list_storage={}
    
    fig = plt.figure(figsize=(7,7))
    
    if rev_raf_path==False:
        ax = fig.add_subplot(1, 1, 1)
        
    maxi=0
    
    for profile_type in ['superior','inferior']:
        
        if profile_type=='superior':
            number_beziers=len(superior_revolve_info)
        if profile_type=='inferior':
            number_beziers=len(inferior_revolve_info)

        for amount in range(0,number_beziers,1):
            
            if profile_type=='superior':
                number_points=len(superior_revolve_info[f'{amount}'][0])
                
                point_matrix_x_2d,point_matrix_y_2d=np.empty((number_points,1)),np.empty((number_points,1))
                
                for count in range(number_points):
                    point_matrix_x_2d[count][0] = superior_revolve_info[f'{amount}'][0][count][0]
                    point_matrix_y_2d[count][0] = superior_revolve_info[f'{amount}'][0][count][1]
                    if point_matrix_x_2d[count][0]>maxi:
                        maxi=point_matrix_x_2d[count][0]
                    if point_matrix_y_2d[count][0]>maxi:
                        maxi=point_matrix_y_2d[count][0]

            if profile_type=='inferior':
                number_points=len(inferior_revolve_info[f'{amount}'][0])
                
                point_matrix_x_2d,point_matrix_y_2d=np.empty((number_points,1)),np.empty((number_points,1))
                
                for count in range(number_points):
                    point_matrix_x_2d[count][0] = inferior_revolve_info[f'{amount}'][0][count][0]
                    point_matrix_y_2d[count][0] = inferior_revolve_info[f'{amount}'][0][count][1]

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
            old_t=1000231

            for c1 in np.arange(0,n1,1):
                for amount4 in range(1,number_beziers+1,1):
                    sol = solveset(eq_storage[f'{profile_type}x{identif},Bezier{amount4}'][1][0] - c1*d1 , t, domain=S.Reals)
                    for i in range(0,len(sol.args),1):
                        if 0<=round(sol.args[i],6)<=1.0:
                            raio=eq_storage[f'{profile_type}y{identif},Bezier{amount4}'][0](sol.args[i])
                            
                            if old_t!=1:
                                radius_list.append(raio)                
                                    
                            old_t=sol.args[i]
                                    

            list_storage[f'{profile_type}{identif}_{raf}'] = [radius_list.copy()]

            for count in range(1,number_beziers+1,1):

                if eq_storage[f'{profile_type}y{identif},Bezier{count}'][8] == np.ndarray:
                    try:
                        ax.plot(eq_storage[f'{profile_type}x{identif},Bezier{count}'][0](t_plot),eq_storage[f'{profile_type}y{identif},Bezier{count}'][0](t_plot), color='grey')
                        ax.scatter(eq_storage[f'{profile_type}x{identif},Bezier{count}'][3],eq_storage[f'{profile_type}y{identif},Bezier{count}'][3], color='black')
                    except:
                        pass

                if eq_storage[f'{profile_type}y{identif},Bezier{count}'][8] != np.ndarray:
                    try:
                        subs = np.full((eq_storage[f'{profile_type}x{identif},Bezier{count}'][0](t_plot).size,1),
                                        eq_storage[f'{profile_type}y{identif},Bezier{count}'][0](t_plot))
                        
                        ax.plot(eq_storage[f'{profile_type}x{identif},Bezier{count}'][0](t_plot),subs, color='grey')
                        ax.scatter(eq_storage[f'{profile_type}x{identif},Bezier{count}'][3],eq_storage[f'{profile_type}y{identif},Bezier{count}'][3], color='black')
                    except:
                        pass
                    
                elif eq_storage[f'{profile_type}x{identif},Bezier{count}'][8] != np.ndarray:
                    try:
                        subs = np.full((eq_storage[f'{profile_type}y{identif},Bezier{count}'][0](t_plot).size,1),
                                        eq_storage[f'{profile_type}x{identif},Bezier{count}'][0](t_plot))
                        
                        ax.plot(subs, eq_storage[f'{profile_type}x{identif},Bezier{count}'][0](t_plot),color='grey')
                        ax.scatter(eq_storage[f'{profile_type}x{identif},Bezier{count}'][3],eq_storage[f'{profile_type}y{identif},Bezier{count}'][3], color='black')
                    except:
                        pass
        
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
                
            superior_radius = 0
            if np.amax(list_storage[f'superior{identif}_{raf}'])>superior_radius:
                superior_radius=np.amax(list_storage[f'superior{identif}_{raf}'])
                

    #gen_revolve_cylinder    
        
    if eq_storage[f'superiorx{identif},Bezier1'][5] =='x':
        bases_plane='zy'
    if eq_storage[f'superiorx{identif},Bezier1'][5] =='y':
        bases_plane='xz'
    if eq_storage[f'superiorx{identif},Bezier1'][5] =='z':
        bases_plane='xy'
        
    check = eq_storage[f'superiorx{identif},Bezier1'][6] 
    final_height = init_height + eq_storage[f'superiorx{identif},Bezier{check}'][3][-1][0]
    
    inferior_radius=100000
            
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
    Crie uma esfera em qualquer posição do domínio.
    
    Args:
        identif (:obj:`str`): Crie a **identificação** da feature com :math:`{n}`, onde :math:`{n=0,1,2,3...}` (começar em ``'0'`` e somar ``'1'`` a cada nova superfície).
        name (:obj:`str`): Crie um nome para a feature. Não há regras.
        radius (:obj:`float`): Raio da esfera.
        cex (:obj:`float`): Coordenada :math:`{x}` do centro.
        cey (:obj:`float`): Coordenada :math:`{y}` do centro.
        cez (:obj:`float`): Coordenada :math:`{z}` do centro.
        
    """
    
    pi = np.pi
    cos = np.cos
    sin = np.sin
    phi, theta = np.mgrid[0:pi:30j, 0:2*pi:30j]
    
    x = radius*sin(phi)*cos(theta) + cex
    y = radius*sin(phi)*sin(theta) + cey
    z = radius*cos(phi) + cez
        
    eq_storage[f's{identif}'] = [name,x.copy(),z.copy(),y.copy(),cex,cey,cez,radius,'sphere']
    
    
def gen_quad_prism(identif,name,a,b,c,reference_point):
    """
    Crie um cubóide (prisma quadrangular) em qualquer posição do domínio.
    
    Args:
        identif (:obj:`str`): Crie a **identificação** da feature com :math:`{n}`, onde :math:`{n=0,1,2,3...}` (começar em ``'0'`` e somar ``'1'`` a cada nova superfície).
        a (:obj:`float`): Aresta na direção de :math:`{x}`.
        b (:obj:`float`): Aresta na direção de :math:`{y}`.
        c (:obj:`float`): Aresta na direção de :math:`{z}`.
        reference_point (:obj:`list, float`): Coordenadas do ponto de referência para posicionamento do cubóide. É o vértice mais próximo da origem do plano cartesiano.
    
    """
    # parametrização
    
    phi = np.arange(1,10,2)*np.pi/4
    Phi, Theta = np.meshgrid(phi, phi)

    x = np.cos(Phi)*np.sin(Theta)
    y = np.sin(Phi)*np.sin(Theta)
    z = np.cos(Theta)/np.sqrt(2)


    dim_x = (x*a)+(a/2)+reference_point[0] 
    dim_y = (y*c)+(c/2)+reference_point[2] 
    dim_z = (z*b)+(b/2)+reference_point[1]
    
    begin_x,end_x = reference_point[0], reference_point[0]+a
    begin_z,end_z = reference_point[2], reference_point[2]+c
    begin_y,end_y = reference_point[1], reference_point[1]+b
    
    eq_storage[f'qp{identif}'] = [name,dim_x.copy(),dim_y.copy(),dim_z.copy(),begin_x,end_x,begin_y,end_y,begin_z,end_z,'quadrangular prism']
    
    
def gen_cylinder(identif,name,bases_plane,radius,center_1,center_2,init_height,final_height):
    
    """
    Crie um cilíndro ao longo de :math:`{x}`, :math:`{y}` ou :math:`{z}` em qualquer ponto do domínio. Não há possibilidade de rotações.
    
    Args:
        identif (:obj:`str`): Crie a **identificação** da feature com :math:`{n}`, onde :math:`{n=0,1,2,3...}` (começar em ``'0'`` e somar ``'1'`` a cada nova superfície).
        name (:obj:`str`): Crie um nome para a feature. Não há regras.
        bases_plane (:obj:`str`): O plano transversal ao cilindro: onde a base ou o topo ficam (são paralelos). Deverá assumir ``'xy'``, ``'xz'`` ou ``'zy'``.
        radius (:obj:`float`): Raio da base/topo.
        center1 (:obj:`float`): 1ª coordenada do centro da base/topo. O eixo correspondende à coordenada dependerá de qual ``bases_plane`` foi definido.
        center2 (:obj:`float`): 2ª coordenada do centro da base/topo. O eixo correspondende à coordenada dependerá de qual ``bases_plane`` foi definido.
        init_height (:obj:`float`): Início do cilindro. Deve ser menor do que ``final_height``.
        final_height (:obj:`float`): Final do cilindro. Deve ser maior do que ``init_height``.
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
        
    eq_storage[f'c{identif}'] = [name,axis1.copy(),axis2.copy(),axis3.copy(),bases_plane,radius,center_1,center_2,init_height,final_height,'cylinder'] #type must be last
    
                
def surface_plot (init_identif, final_identif, engine='matplotlib', points=False, domain=True, grids=True, legend=True, alpha=0.3):
    
    """
    Visualize as superfícies construídas desejadas. 
    
    Args:
        init_identif (:obj:`str`): Determine o início do intervalo de superfícies a serem plotadas através da identificação ``identif``
        final_identif (:obj:`str`): Determine o final do intervalo **(endpoint não incluso)** de superfícies a serem plotadas através da identificação ``identif``
        engine (:obj:`str`, optional): Escolha qual pacote renderizador de plot, ``'matplotlib'`` ou ``'mayavi'``. Mayavi displays better, matplotlib displays more information.
        points (:obj:`Bool`, optional): Caso queira visualizar os pontos que governam sua superfície, sete como ``True``. Válido apenas para ``engine='matplotlib'``
        domain (:obj:`Bool`, optional): Caso queira deixar de visualizar o domínio, sete como ``False``. Válido apenas para ``engine='matplotlib'``
        grids (:obj:`Bool`, optional): Caso queira retirar o grid de background, sete como ``False``. Válido apenas para ``engine='matplotlib'``
        legends (:obj:`Bool`, optional): Caso queira retirar as legendas das superfícies, sete como ``False``. Válido apenas para ``engine='matplotlib'``
        alpha (:obj:`float`, optional): Controlador da opacidade da superfície em questão. Pode assumir qualquer valor entre ``0`` (transparente) e ``1`` (opaco).

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
                    
                if p==f'qp{plot}':
                    surf=mlab.mesh(eq_storage[f'qp{plot}'][1], eq_storage[f'qp{plot}'][3], eq_storage[f'qp{plot}'][2],
                           colormap=colormaps[choice], opacity=alpha)

                if p==f'superiorrc{plot}':
                    surf=mlab.mesh(eq_storage[f'superiorrc{plot}'][1].astype(float), eq_storage[f'superiorrc{plot}'][3].astype(float),
                                   eq_storage[f'superiorrc{plot}'][2].astype(float), colormap=colormaps[choice], opacity=alpha)
                    
                if p==f'inferiorrc{plot}':
                    surf=mlab.mesh(eq_storage[f'inferiorrc{plot}'][1].astype(float), eq_storage[f'inferiorrc{plot}'][3].astype(float), 
                                   eq_storage[f'inferiorrc{plot}'][2].astype(float),colormap=colormaps[choice], opacity=alpha)
        
        
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

        ax.set_xlim(0,max([lx,ly,lz])),ax.set_ylim(0,max([lx,ly,lz])),ax.set_zlim(0,max([lx,ly,lz]))
        
        ax.view_init(25,-45),ax.set_title('Surface/Control Points',size=20)
        
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)),ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)),ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        
        if grids==False:
            ax.w_xaxis.line.set_color("white")
            ax.w_yaxis.line.set_color("white")
            ax.w_zaxis.line.set_color("white")
            ax.grid(False)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks([])
            
        else:
            ax.set_xlabel('x'),ax.set_ylabel('z'),ax.set_zlabel('y')
            
        if domain==True:
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
                    if legend==True:
                        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)
                    if points == True:
                        ax.scatter(eq_storage[f'x{plot}'][8],eq_storage[f'z{plot}'][8],eq_storage[f'y{plot}'][8],s=17.5,color='grey',edgecolor='grey')
                        for i in range(0,eq_storage[f'x{plot}'][6],1):
                            for j in range(0,eq_storage[f'x{plot}'][7],1):
                                
                                ax.text(eq_storage[f'x{plot}'][8][i][j],eq_storage[f'z{plot}'][8][i][j],eq_storage[f'y{plot}'][8][i][j],fr'$P_{{{i}{j}}}$',size=12.5)
                        
                        for i in range(0,eq_storage[f'x{plot}'][6],1):
                            for j in range(0,eq_storage[f'x{plot}'][7]-1,1):
                                ax.plot([eq_storage[f'x{plot}'][8][i][j],eq_storage[f'x{plot}'][8][i][j+1]],
                                        [eq_storage[f'z{plot}'][8][i][j],eq_storage[f'z{plot}'][8][i][j+1]],
                                        [eq_storage[f'y{plot}'][8][i][j],eq_storage[f'y{plot}'][8][i][j+1]], color='grey', linestyle='--', linewidth=1)

                        for i in range(0,eq_storage[f'x{plot}'][6]-1,1):
                            for j in range(0,eq_storage[f'x{plot}'][7],1):
                                ax.plot([eq_storage[f'x{plot}'][8][i][j],eq_storage[f'x{plot}'][8][i+1][j]],
                                        [eq_storage[f'z{plot}'][8][i][j],eq_storage[f'z{plot}'][8][i+1][j]],
                                        [eq_storage[f'y{plot}'][8][i][j],eq_storage[f'y{plot}'][8][i+1][j]], color='grey', linestyle='--', linewidth=1)

                if p==f's{plot}':
                    surf = ax.plot_surface(eq_storage[f's{plot}'][1], eq_storage[f's{plot}'][2], eq_storage[f's{plot}'][3], alpha=alpha, label=eq_storage[f's{plot}'][0])
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)
                    if legend==True:
                        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)

                if p==f'c{plot}':
                    surf = ax.plot_surface(eq_storage[f'c{plot}'][1], eq_storage[f'c{plot}'][2], eq_storage[f'c{plot}'][3], alpha=alpha, label=eq_storage[f'c{plot}'][0])
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)
                    if legend==True:
                        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)
                        
                if p==f'qp{plot}':
                    surf = ax.plot_surface(eq_storage[f'qp{plot}'][1], eq_storage[f'qp{plot}'][2], eq_storage[f'qp{plot}'][3], alpha=alpha, label=eq_storage[f'qp{plot}'][0])
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)
                    if legend==True:
                        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=10)

                if p==f'superiorrc{plot}':
                    surf=ax.plot_surface(eq_storage[f'superiorrc{plot}'][1].astype(float), eq_storage[f'superiorrc{plot}'][2].astype(float),
                                         eq_storage[f'superiorrc{plot}'][3].astype(float), alpha=alpha)
                    
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)
                
                if p==f'inferiorrc{plot}':
                    surf=ax.plot_surface(eq_storage[f'inferiorrc{plot}'][1].astype(float), eq_storage[f'inferiorrc{plot}'][2].astype(float),
                                         eq_storage[f'inferiorrc{plot}'][3].astype(float), alpha=alpha)
                    
                    surf._facecolors2d=surf._facecolors3d
                    surf._edgecolors2d=surf._edgecolors3d
                    fig.tight_layout()
                    fig.subplots_adjust(right=0.8)

        ax.invert_yaxis()

        plt.show()    
    
def gen_epsi_extrude(identif,ext_raf_path=False):
    
    """
    Geração da :math:`{\epsilon}` do Extrude criado anteriormente.
    
    Args:
        identif (:obj:`str`): Repita o argumento ``identif`` do extrude em questão.
        ext_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
        
    """

    if ext_raf_path==True:
        loop_path=['normal','x','y','z']
    if ext_raf_path==False:
        loop_path=['normal']
        
    for raf in loop_path:
        
        fig_epsi, a2 = plt.subplots(figsize=(8,8))
        a2.set_title(f'Raf {raf}')
        
        dx_gen,dy_gen,dz_gen=dx,dy,dz
        nx_gen,ny_gen,nz_gen=nx,ny,nz
        matrix_gen=epsi_3d

        if raf=='x':
            dx_gen,nx_gen=dx_raf, nx_raf
            matrix_gen= epsi_3d_x_raf
        if raf=='y':
            dy_gen,ny_gen= dy_raf, ny_raf
            matrix_gen= epsi_3d_y_raf
        if raf=='z':
            dz_gen,nz_gen= dz_raf, nz_raf
            matrix_gen= epsi_3d_z_raf
            
        if  eq_storage[f'ext,x{identif},Bezier0'][5] == 'z':
            
            d3,n3 = dz_gen,nz_gen
            d1,n1 = dx_gen,nx_gen
            d2,n2 = dy_gen,ny_gen

        if  eq_storage[f'ext,x{identif},Bezier0'][5] == 'x':
            
            d3,n3 = dx_gen,nx_gen
            d1,n1 = dz_gen,nz_gen
            d2,n2 = dy_gen,ny_gen
                
        if  eq_storage[f'ext,x{identif},Bezier0'][5] == 'y':
            
            d3,n3 = dy_gen,ny_gen
            d1,n1 = dx_gen,nx_gen
            d2,n2 = dz_gen,nz_gen
        
        matrix_aux=np.zeros((n1,n2),dtype=np.float32)
        
        bar = progressbar.ProgressBar(widgets=[f'#{identif} (raf {raf}): ', progressbar.AnimatedMarker(), progressbar.Percentage(), progressbar.Bar(),'  ', 
                                                   progressbar.Timer()],max_value=( eq_storage[f'ext,x{identif},Bezier0'][9]*(n1*n2))).start()
        
        for bez_qtt in range(0, eq_storage[f'ext,x{identif},Bezier0'][9]): #number of beziers present in profile, doesnt make difference if its related to x or y
            
            if  eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][8] == np.ndarray:
                try:
                    a2.plot( eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](t_plot), eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](t_plot), color='white')
                except:
                    pass

            if  eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][8] != np.ndarray:
                try:
                    subs = np.full(( eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](t_plot).size,1),
                                     eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](t_plot))
                    a2.plot( eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](t_plot),subs, color='white')
                except:
                    pass

            elif  eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][8] != np.ndarray:
                try:
                    subs = np.full(( eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](t_plot).size,1),
                                     eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](t_plot))
                    a2.plot(subs,  eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](t_plot), color='white')
                except:
                    pass

            if  eq_storage[f'ext,x{identif},Bezier0'][10] == 'v': #the resolution axis's choice, for each vertical position ask the limits to horizontal lines
                
                for c1 in range(0,n1,1):
                    #try:
                    args_list=[]
                    intersec = solveset(eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][1][0]-c1*d1,t,domain=S.Reals)
                    for prmt in range(0,len(intersec.args)):
                        if 0<=round(intersec.args[prmt],5)<=1:
                            args_list+=[intersec.args[prmt]] #the t where it exists the intersection

                    for c2 in range(0,n2,1):
                        bar+=1
                        if len(args_list)==2:
                            mini=min( eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](max(args_list)), eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](min(args_list)))
                            maxi=max( eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](max(args_list)), eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](min(args_list)))

                            if maxi>=c2*d2>=mini:
                                matrix_aux[c1][c2] = 1
                                
                        if  eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][6] == 'entry+exit and/or entry':
                            if len(args_list)==1:
                                if c2*d2>= eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](args_list[0]):
                                    matrix_aux[c1][c2] = 1

                        if  eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][6] == 'entry+exit and/or exit':
                            if len(args_list)==1:
                                if c2*d2> eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][0](args_list[0]):
                                    matrix_aux[c1][c2] = 0
                                    
            if  eq_storage[f'ext,x{identif},Bezier0'][10] == 'h': #the resolution axis's choice, for each vertical position ask the limits to horizontal lines
                
                for c2 in range(0,n2,1):
                    #try:
                    args_list=[]
                    intersec = solveset( eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][1][0]-c2*d2, t, domain=S.Reals)
                    for prmt in range(0,len(intersec.args)):
                        if 0<=round(intersec.args[prmt],5)<=1:
                            args_list+=[intersec.args[prmt]]

                    for c1 in range(0,n1,1):
                        bar+=1
                        if len(args_list)==2:
                            mini=min( eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](max(args_list)), eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](min(args_list)))
                            maxi=max( eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](max(args_list)), eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](min(args_list)))

                            if maxi>=c1*d1>=mini:
                                matrix_aux[c1][c2] = 1
                                
                        if  eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][6] == 'entry+exit and/or entry':
                            if len(args_list)==1:
                                if c1*d1>= eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](args_list[0]):
                                    matrix_aux[c1][c2] = 1

                        if  eq_storage[f'ext,y{identif},Bezier{bez_qtt}'][6] == 'entry+exit and/or exit':
                            if len(args_list)==1:
                                if c1*d1> eq_storage[f'ext,x{identif},Bezier{bez_qtt}'][0](args_list[0]):
                                    matrix_aux[c1][c2] = 0
                                      
        bar.finish()
                                    
        #plotting matrix_aux
                                    
        if  eq_storage[f'ext,x{identif},Bezier0'][5] == 'z':
            n1,d1,l2,name_l2,l3,name_l3,d2,d3,plane,n2,n3 = nz_gen,dz_gen,lx,'lx',ly,'ly',dx_gen,dy_gen,'xy',nx_gen,ny_gen
        if  eq_storage[f'ext,x{identif},Bezier0'][5] == 'x':
            n1,d1,l2,name_l2,l3,name_l3,d2,d3,plane,n2,n3 = nx_gen,dx_gen,lz,'lz',ly,'ly',dz_gen,dy_gen,'zy',nz_gen,ny_gen
        if  eq_storage[f'ext,x{identif},Bezier0'][5] == 'y':
            n1,d1,l2,name_l2,l3,name_l3,d2,d3,plane,n2,n3 = ny_gen,dy_gen,lx,'lx',lz,'lz',dx_gen,dz_gen,'xz',nx_gen,nz_gen

        a2.set_xlabel(name_l2, fontsize=15), a2.set_ylabel(name_l3, fontsize=15)
        a2.set_xlim(0,l2), a2.set_ylim(0,l3)
        a2.set_xticks(np.arange(0, l2+d2/2, d2)), a2.set_xticks(np.arange(d2/2, l2, d2), minor=True)
        a2.set_yticks(np.arange(0, l3+d3/2, d3)), a2.set_yticks(np.arange(d3/2, l3, d3), minor=True)
        a2.set_xticklabels((np.arange(0, l2+d2/2, d2)).round(decimals=2),fontsize=8), a2.set_yticklabels((np.arange(0, l3+d3/2, d3)).round(decimals=2),fontsize=8)
        a2.tick_params(axis='x', rotation=45)
        a2.grid(which='minor', zorder=1,alpha=0.6), a2.grid(which='major', alpha=0.3, zorder=1)  
        a2.imshow(matrix_aux.T, cmap = 'jet', origin='lower',extent=[-d2/2, l2+d2/2, -d3/2, l3+d3/2])
            
        #passing it to epsi matrix
        
        if  eq_storage[f'ext,x{identif},Bezier0'][5] == 'z': #if the extrude longitudinal direction is z
            initial_knot = math.ceil( eq_storage[f'ext,x{identif},Bezier0'][11]/dz_gen)
            final_knot   = int( eq_storage[f'ext,x{identif},Bezier0'][12]/dz_gen)
            for counter in range(initial_knot,final_knot+1,1):
                matrix_gen[:,:,counter]+=matrix_aux
                
        if  eq_storage[f'ext,x{identif},Bezier0'][5] == 'x': #if the extrude longitudinal direction is x
            initial_knot = math.ceil( eq_storage[f'ext,x{identif},Bezier0'][11]/dx_gen)
            final_knot   = int( eq_storage[f'ext,x{identif},Bezier0'][12]/dx_gen)
            for counter in range(initial_knot,final_knot+1,1):
                matrix_gen[counter,:,:]+=matrix_aux.T
                
        if  eq_storage[f'ext,x{identif},Bezier0'][5] == 'y': #if the extrude longitudinal direction is y
            initial_knot = math.ceil( eq_storage[f'ext,x{identif},Bezier0'][11]/dy_gen)
            final_knot   = int( eq_storage[f'ext,x{identif},Bezier0'][12]/dy_gen)
            for counter in range(initial_knot,final_knot+1,1):
                matrix_gen[:,counter,:]+=matrix_aux
        
    plt.show()

def gen_epsi_revolve(identif):
    
    """
    Geração da :math:`{\epsilon}` do Revolve criado anteriormente.
    
    Args:
        identif (:obj:`str`): Repita o argumento ``identif`` do revolve em questão.
    
    """
    
    if eq_storage[f'superiorrc{identif}'][10]==True:
        loop_path=['normal','x','y','z']
    if eq_storage[f'superiorrc{identif}'][10]==False:
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

def gen_epsi_bezier_surface(surface_type,plane,identif,solver='scipy',add_or_sub='sub',interval=np.arange(-0.1,1+0.2,0.1),bez_raf_path=False):
    
    """
    
    Nesta função, usa-se as equações geradas pelos pontos fornecidos pelo usuário para setar os limites de onde é sólido (na :math:`{\epsilon}`, ``1``) e onde
    não é sólido (na :math:`{\epsilon}`, ``0``). Também se seta o que é considerado entrada e saída, ou ambos.  
        
    Args:
        surface_type (:obj:`str`): Defina se a superfície em questão é considerada uma entrada, uma saída ou ambos em relação ao domínio.
        
                            +-----------------------------------+---------------------------------+
                            | tipo de limite da superfície      | Setar ``surface_type`` como     | 
                            +===================================+=================================+
                            | entrada                           | ``'entry+exit and/or entry'``   |
                            +-----------------------------------+---------------------------------+
                            | saída                             | ``'entry+exit and/or exit'``    |
                            +-----------------------------------+---------------------------------+
                            | entrada e saída simult.           |  ambos, tanto faz               |
                            +-----------------------------------+---------------------------------+
                            | entrada e saída simult. + entrada | ``'entry+exit and/or entry'``   |
                            +-----------------------------------+---------------------------------+
                            | entrada e saída simult. + saída   | ``'entry+exit and/or exit'``    |  
                            +-----------------------------------+---------------------------------+

    Args: 
        plane (:obj:`str`): Escolha o melhor plane para resolver sua superfície. Pode assumir apenas ``'xz'``, ``'xy'`` ou ``'zy'``. Uma superfície sem espessura em relação a um plano não pode ser resolvida por esse plano.
        identif (:obj:`str`): Repita o argumento ``identif`` da superfície em questão. 
        solver (:obj:`str`, optional): Deve assumir ``'scipy'`` or ``'sympy'``. Normalmente ``'scipy'`` é mais eficiente e barato.
        add_or_sub(:obj:`str`): Defina o mecanismo de criação da :math:`{\epsilon}`. Caso assuma ``'add'``, o fluxo de informação da superfície para a :math:`{\epsilon}` será através de adição (ou subtração, caso seja uma ``entry/exit and/or exit``), caso ideal para obtenção de intersecções (não esquecer de usar a função ``normalize_epsi()`` para correção). Caso assuma ``'sub'``, o fluxo será através de substituição (metodologia padrão).
        interval (:obj:`list, np.arange`, optional): Intervalo no qual o solver ``'scipy'`` vai buscar as raízes. O padrão é o que apresenta melhores resultados.
        bez_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
    
    **Exemplo:**
        .. figure:: images/ex_entradasaidasaida.png
           :scale: 70%
           :align: center
           
        Podemos notar 2 supefícies na figura, uma verde, ``identif='0'``, e outra roxa ``identif='1'``. 
        De acordo com esta situação, a invocação da função ``gen_epsi()`` pode se dar na seguinte forma::
            
            gen_epsi('entry+exit and/or entry','zy','0')
            gen_epsi('entry+exit and/or exit','zy','1')
           
        Podemos notar também um ponto que é o início de um vetor perpendicular ao plane :math:`{zy}`. Este vetor é a representação do que define o ``surface_type`` de cada superfície.
        Toda vez que o vetor encontrar alguma superfícies, será definido um limite para a criação da :math:`{\epsilon}`.
        Devemos imaginar que para cada combinação de coordenada :math:`{z}` e :math:`{y}` (espaçamento definido por :math:`{dz}` e :math:`{dy}`) um vetor desses é originado. Portanto: 
        
            1. O sólido verde é considerado somente entrada pois, no instante em que é interceptado pelos vetores, 
            **entra-se no sólido**. 
            
            2. O sólido roxo deve ser dividido em 2 partes e é considerado entrada e sáida + saída. A primeira parte é a superior, logo acima da superfície verde.
            Toda esta parte será interceptada pelos vetores duas vezes e **por isso é considerada entrada e saída**. A segunda parte é a inferior, que 'compartilha'
            altura com a superfície verde. Esta parte será interceptada pelos vetores apenas uma vez e em todas elas o sólido já terá acabado, por isso é considerada
            como **saída**.
        
    Warning:
        Caso construída uma superfície que possua segmentos com possíveis entradas e saídas simultâneas (superfície roxa), certificar que a superfície seja construída 
        no sentido positivo: os pontos iniciais devem ser mais próximos da origem do que os pontos finais, independente do plane.
        
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
                args_list=[]
                if solver=='scipy':
                    intersec = lambdify(((u,v),),[eq_storage[f'{axis1}'][1][0]-c1*d1, eq_storage[f'{axis2}'][1][0]-c2*d2])
                    for cs in interval:
                        for cp in interval:
                            sol=root(intersec,[cs,cp])
                            if sol.success==True:
                                if np.any(np.round(sol.qtf,5)) == 0:
                                    if 0<=sol.x[0]<=1 and 0<=sol.x[1]<=1:
                                        if len(args_list)==0:
                                            args_list+=[np.round(sol.x,8)]
                                        if len(args_list)>0:
                                            true_list=[]
                                            for a in range(0,len(args_list),1):
                                                true_list.append(np.array_equal(np.round(sol.x,8),args_list[a]))
                                            if np.any(true_list)==False:
                                                args_list+=[np.round(sol.x,8)]

                    #print(args_list,c1,c2) 

                    if len(args_list)>2:
                        print('>>Probably<< theres a problem in convergence. Check it on ParaView. If so, try another knot combination or change your geometry. ')

                    for c3 in range(min_3,max_3,1):
                        if surface_type == 'entry+exit and/or exit':
                            if len(args_list)==2:
                                if eq_storage[f'{axis3}'][2](args_list[0][0],args_list[0][1])<=c3*d3<=eq_storage[f'{axis3}'][2](args_list[1][0],args_list[1][1]):
                                        if plane == 'zy':
                                            if add_or_sub=='add':
                                                matrix_gen[c3][c2][c1] += 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c3][c2][c1] = 1
                                            
                                        if plane == 'xz':
                                            if add_or_sub=='add':
                                                matrix_gen[c1][c3][c2] += 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c1][c3][c2] = 1
                                            
                                        if plane == 'xy':
                                            if add_or_sub=='add':
                                                matrix_gen[c1][c2][c3] += 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c1][c2][c3] = 1
                            if len(args_list)==1:
                                if c3*d3>eq_storage[f'{axis3}'][2](args_list[0][0],args_list[0][1]):
                                    if plane == 'zy':
                                        if add_or_sub=='add':
                                            matrix_gen[c3][c2][c1] -= 1
                                        elif add_or_sub=='sub':
                                            matrix_gen[c3][c2][c1] = 0
                                        
                                    if plane == 'xz':
                                        if add_or_sub=='add':
                                            matrix_gen[c1][c3][c2] -= 1
                                        elif add_or_sub=='sub':
                                            matrix_gen[c1][c3][c2] = 0
                                        
                                    if plane == 'xy':
                                        if add_or_sub=='add':
                                            matrix_gen[c1][c2][c3] -= 1
                                        elif add_or_sub=='sub':
                                            matrix_gen[c1][c2][c3] = 0
                                        
                        if surface_type == 'entry+exit and/or entry':
                            if len(args_list)==2:
                                if eq_storage[f'{axis3}'][2](args_list[0][0],args_list[0][1])<=c3*d3<=eq_storage[f'{axis3}'][2](args_list[1][0],args_list[1][1]):
                                        if plane == 'zy':
                                            if add_or_sub=='add':
                                                matrix_gen[c3][c2][c1] += 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c3][c2][c1] = 1
                                            
                                        if plane == 'xz':
                                            if add_or_sub=='add':
                                                matrix_gen[c1][c3][c2] += 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c1][c3][c2] = 1
                                            
                                        if plane == 'xy':
                                            if add_or_sub=='add':
                                                matrix_gen[c1][c2][c3] += 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c1][c2][c3] = 1
                                            
                            if len(args_list)==1:
                                if c3*d3>=eq_storage[f'{axis3}'][2](args_list[0][0],args_list[0][1]):
                                    if plane == 'zy':
                                        if add_or_sub=='add':
                                            matrix_gen[c3][c2][c1] += 1
                                        elif add_or_sub=='sub':
                                            matrix_gen[c3][c2][c1] = 1
                                        
                                    if plane == 'xz':
                                        if add_or_sub=='add':
                                            matrix_gen[c1][c3][c2] += 1
                                        elif add_or_sub=='sub':
                                            matrix_gen[c1][c3][c2] = 1
                                        
                                    if plane == 'xy':
                                        if add_or_sub=='add':
                                            matrix_gen[c1][c2][c3] += 1
                                        elif add_or_sub=='sub':
                                            matrix_gen[c1][c2][c3] = 1
                                        
                elif solver=='sympy':
                    try:
                        intersec = nonlinsolve([eq_storage[f'{axis1}'][1][0]-c1*d1,eq_storage[f'{axis2}'][1][0]-c2*d2],[u,v])
                        for prmt in range(0,len(intersec.args)):
                            if intersec.args[prmt][0].is_real == True and 0<=round(intersec.args[prmt][0],5)<=1:
                                if intersec.args[prmt][1].is_real == True and 0<=round(intersec.args[prmt][1],5)<=1:
                                    args_list+=intersec.args[prmt]

                        #print(args_list,c1,c2)

                        for c3 in range(min_3,max_3+1,1):
                            if surface_type == 'entry+exit and/or exit':
                                if len(args_list)==4:
                                    if eq_storage[f'{axis3}'][2](args_list[0],args_list[1])<=c3*d3<=eq_storage[f'{axis3}'][2](args_list[2],args_list[3]):
                                            if plane == 'zy':
                                                if add_or_sub=='add':
                                                    matrix_gen[c3][c2][c1] += 1
                                                elif add_or_sub=='sub':
                                                    matrix_gen[c3][c2][c1] = 1
                                                
                                            if plane == 'xz':
                                                if add_or_sub=='add':
                                                    matrix_gen[c1][c3][c2] += 1
                                                elif add_or_sub=='sub':
                                                    matrix_gen[c1][c3][c2] = 1
                                                
                                            if plane == 'xy':
                                                if add_or_sub=='add':
                                                    matrix_gen[c1][c2][c3] += 1
                                                elif add_or_sub=='sub':
                                                    matrix_gen[c1][c2][c3] = 1
                                                
                                if len(args_list)==2:
                                    if c3*d3>eq_storage[f'{axis3}'][2](args_list[0],args_list[1]):
                                        if plane == 'zy':
                                            if add_or_sub=='add':
                                                matrix_gen[c3][c2][c1] -= 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c3][c2][c1] = 0
                                            
                                        if plane == 'xz':
                                            if add_or_sub=='add':
                                                matrix_gen[c1][c3][c2] -= 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c1][c3][c2] = 0
                                            
                                        if plane == 'xy':
                                            if add_or_sub=='add':
                                                matrix_gen[c1][c2][c3] -= 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c1][c2][c3] = 0

                            if surface_type == 'entry+exit and/or entry':
                                if len(args_list)==4:
                                    if eq_storage[f'{axis3}'][2](args_list[0],args_list[1])<=c3*d3<=eq_storage[f'{axis3}'][2](args_list[2],args_list[3]):
                                            if plane == 'zy':
                                                if add_or_sub=='add':
                                                    matrix_gen[c3][c2][c1] += 1
                                                elif add_or_sub=='sub':
                                                    matrix_gen[c3][c2][c1] = 1
                                                
                                            if plane == 'xz':
                                                if add_or_sub=='add':
                                                    matrix_gen[c1][c3][c2] += 1
                                                elif add_or_sub=='sub':
                                                    matrix_gen[c1][c3][c2] = 1
                                                
                                            if plane == 'xy':
                                                if add_or_sub=='add':
                                                    matrix_gen[c1][c2][c3] += 1
                                                elif add_or_sub=='sub':
                                                    matrix_gen[c1][c2][c3] = 1
                                if len(args_list)==2:
                                    if c3*d3>=eq_storage[f'{axis3}'][2](args_list[0],args_list[1]):
                                        if plane == 'zy':
                                            if add_or_sub=='add':
                                                matrix_gen[c3][c2][c1] += 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c3][c2][c1] = 1
                                        if plane == 'xz':
                                            if add_or_sub=='add':
                                                matrix_gen[c1][c3][c2] += 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c1][c3][c2] = 1
                                            
                                        if plane == 'xy':
                                            if add_or_sub=='add':
                                                matrix_gen[c1][c2][c3] += 1
                                            elif add_or_sub=='sub':
                                                matrix_gen[c1][c2][c3] = 1

                    except:
                        pass

        bar.finish()
    
def gen_epsi_mirror(target, direction, mirror_raf_path=False):
    
    """
    Espelhe o domínio inteiro ou apenas um sólido construído com ``bounds_into_single_solid()``.
    
    Após a criação de um espelhamento, normalizar a matriz :math:`{\epsilon}` com a função ``normalize_epsi``. Maiores informações em :ref:`howto`.
    
    Args:
        target (:obj:`str`): Pode assumir ``'whole_domain'`` (caso o mirror seja feito ao longo de todo domínio) ou a identificação do sólido criado com ``bounds_into_single_solid()`` (caso mirror seja feito em apenas uma parte do domínio).
        direction (:obj:`str`): Direção na qual o mirror será efetuado. Deve assumir ``'x'``, ``'y'`` ou ``'z'``.
        mirror_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
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
        
        if target=='whole_domain':
            
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
                        
        elif target!='whole_domain':
            
            if direction=='x':
                minimum_knot=math.ceil(solid_storage[f'{target}'][3]/dx_gen)
                medium_knot=int(solid_storage[f'{target}'][0]/dx_gen)
                maximum_knot=int((2*solid_storage[f'{target}'][0]-solid_storage[f'{target}'][3])/dx_gen)
                
                knot_range=maximum_knot-minimum_knot+1
                zero_side=medium_knot

                if (knot_range%2!=0) == True:
                    #print(raf,'knot_range',knot_range,'impar')
                    processed_side=medium_knot

                elif (knot_range%2!=0) == False:     #par
                    #print(raf,'knot_range',knot_range,'par')
                    processed_side=medium_knot+1
                    
                for cx in range(medium_knot,maximum_knot,1):
                    zero_side+=1
                    processed_side-=1
                    for cy in range(int(solid_storage[f'{target}'][4]/dy_gen),math.ceil(solid_storage[f'{target}'][1]/dy_gen)+1):
                        for cz in range(int(solid_storage[f'{target}'][5]/dz_gen),math.ceil(solid_storage[f'{target}'][2]/dz_gen)+1):
                            if matrix_gen[processed_side,cy,cz] == int(target):
                                matrix_gen[zero_side,cy,cz] = matrix_gen[processed_side,cy,cz]
                    
            if direction=='y':
                minimum_knot=math.ceil(solid_storage[f'{target}'][4]/dy_gen)
                medium_knot=int(solid_storage[f'{target}'][1]/dy_gen)
                maximum_knot=int((2*solid_storage[f'{target}'][1]-solid_storage[f'{target}'][4])/dy_gen)
                
                knot_range=maximum_knot-minimum_knot+1
                zero_side=medium_knot

                if (knot_range%2!=0) == True:
                    processed_side=medium_knot

                elif (knot_range%2!=0) == False:     #par
                    processed_side=medium_knot+1
                    
                for cy in range(medium_knot,maximum_knot,1):
                    zero_side+=1
                    processed_side-=1
                    for cx in range(int(solid_storage[f'{target}'][3]/dx_gen),math.ceil(solid_storage[f'{target}'][0]/dx_gen)+1):
                        for cz in range(int(solid_storage[f'{target}'][5]/dz_gen),math.ceil(solid_storage[f'{target}'][2]/dz_gen)+1):
                            if matrix_gen[cx,processed_side,cz] == int(target):
                                matrix_gen[cx,zero_side,cz] = matrix_gen[cx,processed_side,cz]
                
                
            if direction=='z':
                minimum_knot=math.ceil(solid_storage[f'{target}'][5]/dz_gen)
                medium_knot=int(solid_storage[f'{target}'][2]/dz_gen)
                maximum_knot=int((2*solid_storage[f'{target}'][2]-solid_storage[f'{target}'][5])/dz_gen)
                
                knot_range=maximum_knot-minimum_knot+1
                zero_side=medium_knot

                if (knot_range%2!=0) == True:
                    processed_side=medium_knot

                elif (knot_range%2!=0) == False:     #par
                    processed_side=medium_knot+1
                    
                for cz in range(medium_knot,maximum_knot,1):
                    zero_side+=1
                    processed_side-=1
                    for cy in range(int(solid_storage[f'{target}'][4]/dy_gen),math.ceil(solid_storage[f'{target}'][1]/dy_gen)+1): 
                        for cx in range(int(solid_storage[f'{target}'][3]/dx_gen),math.ceil(solid_storage[f'{target}'][0]/dx_gen)+1):
                            if matrix_gen[cx,cy,processed_side] == int(target):
                                matrix_gen[cx,cy,zero_side] = matrix_gen[cx,cy,processed_side]
                
                #print(' ')
                                    
    if target!='whole_domain':
        if direction=='x':
            solid_storage[f'{target}'][0]=2*solid_storage[f'{target}'][0]-solid_storage[f'{target}'][3]
        elif direction=='y':
            solid_storage[f'{target}'][1]=2*solid_storage[f'{target}'][1]-solid_storage[f'{target}'][4]
        elif direction=='z':
            solid_storage[f'{target}'][2]=2*solid_storage[f'{target}'][2]-solid_storage[f'{target}'][5]
    
    
def gen_epsi_cylinder(identif, surface_type, add_or_sub='sub', cyl_raf_path=False):
    
    """
    Geração da :math:`{\epsilon}` da esfera criada anteriormente.
    
    Args:
        identif (:obj:`str`): Repita o argumento ``identif`` do cilindro em questão.
        surface_type (:obj:`str`): Defina se o cilindro será um objeto (adição de "material") ou um contorno (subtração de "material") . Deve assumir ``'solid'`` ou ``'contour'``.
        add_or_sub (:obj:`str`): Defina o mecanismo de criação da :math:`{\epsilon}`. Caso assuma ``'add'``, o fluxo de informação da superfície para a :math:`{\epsilon}` será através de adição (ou subtração, caso seja um ``contour``), caso ideal para obtenção de intersecções (não esquecer de usar a função ``normalize_epsi()`` para correção). Caso assuma ``'sub'``, o fluxo será através de substituição (metodologia padrão).
        cyl_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
    
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
                    if add_or_sub=='add':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] += 1
                    elif add_or_sub=='sub':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] = 1
                        
                    matrix_gen[:,:,cz]=epsi.T.copy()

            if surface_type=='contour':
                for cz in range(math.ceil(eq_storage[f'c{identif}'][8]/dz_gen),int(eq_storage[f'c{identif}'][9]/dz_gen)+1,1):
                    bar+=1
                    epsi=matrix_gen[:,:,cz].T
                    dis = np.sqrt((X-eq_storage[f'c{identif}'][6])**2.+(Y-eq_storage[f'c{identif}'][7])**2.)
                    if add_or_sub=='add':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] -= 1
                    elif add_or_sub=='sub':
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
                    if add_or_sub=='add':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] += 1
                    elif add_or_sub=='sub':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] = 1
                        
                    matrix_gen[:,cy,:]=epsi.T.copy()

            if surface_type=='contour':
                for cy in range(math.ceil(eq_storage[f'c{identif}'][8]/dy_gen),int(eq_storage[f'c{identif}'][9]/dy_gen)+1,1):
                    bar+=1
                    epsi=matrix_gen[:,cy,:].T
                    dis = np.sqrt((X-eq_storage[f'c{identif}'][6])**2.+(Z-eq_storage[f'c{identif}'][7])**2.)
                    if add_or_sub=='add':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] -= 1
                    elif add_or_sub=='sub':
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
                    if add_or_sub=='add':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] += 1
                    elif add_or_sub=='sub':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] = 1
                        
                    matrix_gen[cx,:,:]=epsi.copy()

            if surface_type=='contour':
                for cx in range(math.ceil(eq_storage[f'c{identif}'][8]/dx_gen),int(eq_storage[f'c{identif}'][9]/dx_gen)+1,1):
                    bar+=1
                    epsi=matrix_gen[cx,:,:]
                    dis = np.sqrt((Z-eq_storage[f'c{identif}'][6])**2.+(Y-eq_storage[f'c{identif}'][7])**2.)
                    if add_or_sub=='add':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] -= 1
                    elif add_or_sub=='sub':
                        epsi[dis<=eq_storage[f'c{identif}'][5]] = 0
                    
                    matrix_gen[cx,:,:]=epsi.copy()
                                          
        bar.finish()
        

def gen_epsi_quad_prism(identif, surface_type, add_or_sub='sub', qp_raf_path=False):
    
    """
    Geração da :math:`{\epsilon}` do prisma criado anteriormente.
    
    Args:
        identif (:obj:`str`): Repita o argumento ``identif`` do cubóide em questão.
        surface_type (:obj:`str`): Defina se o cubóide será um objeto (adição de "material") ou um contorno (subtração de "material") . Deve assumir ``'solid'`` ou ``'contour'``.
        add_or_sub (:obj:`str`): Defina o mecanismo de criação da :math:`{\epsilon}`. Caso assuma ``'add'``, o fluxo de informação da superfície para a :math:`{\epsilon}` será através de adição (ou subtração, caso seja um ``contour``), caso ideal para obtenção de intersecções (não esquecer de usar a função ``normalize_epsi()`` para correção). Caso assuma ``'sub'``, o fluxo será através de substituição (metodologia padrão).
        qp_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
    
    """
    
    if qp_raf_path==True:
        loop_path=['normal','x','y','z']
    if qp_raf_path==False:
        loop_path=['normal']
        
    for raf in loop_path:
        dx_gen,dy_gen,dz_gen=dx,dy,dz
        nx_gen,ny_gen,nz_gen=nx,ny,nz
        matrix_gen=epsi_3d
        
        bar = progressbar.ProgressBar(widgets=[f'#{identif}: ',
                                               progressbar.AnimatedMarker(),
                                               progressbar.Percentage(),
                                               progressbar.Bar(),'  ',
                                               progressbar.Timer(),], 
                                               max_value=(1)).start()

        if raf=='x':
            dx_gen,nx_gen=dx_raf,nx_raf
            matrix_gen=epsi_3d_x_raf
        if raf=='y':
            dy_gen,ny_gen=dy_raf,ny_raf
            matrix_gen=epsi_3d_y_raf
        if raf=='z':
            dz_gen,nz_gen=dz_raf,nz_raf
            matrix_gen=epsi_3d_z_raf
            
        if surface_type=='solid':
            if add_or_sub=='add':
                bar+=1
                matrix_gen[math.ceil(eq_storage[f'qp{identif}'][4]/dx_gen):int(eq_storage[f'qp{identif}'][5]/dx_gen)+1,
                           math.ceil(eq_storage[f'qp{identif}'][6]/dy_gen):int(eq_storage[f'qp{identif}'][7]/dy_gen)+1,
                           math.ceil(eq_storage[f'qp{identif}'][8]/dz_gen):int(eq_storage[f'qp{identif}'][9]/dz_gen)+1] += 1
                            
            elif add_or_sub=='sub':
                bar+=1
                matrix_gen[math.ceil(eq_storage[f'qp{identif}'][4]/dx_gen):int(eq_storage[f'qp{identif}'][5]/dx_gen)+1,
                           math.ceil(eq_storage[f'qp{identif}'][6]/dy_gen):int(eq_storage[f'qp{identif}'][7]/dy_gen)+1,
                           math.ceil(eq_storage[f'qp{identif}'][8]/dz_gen):int(eq_storage[f'qp{identif}'][9]/dz_gen)+1] = 1

        if surface_type=='contour':
            if add_or_sub=='add':
                bar+=1
                matrix_gen[math.ceil(eq_storage[f'qp{identif}'][4]/dx_gen):int(eq_storage[f'qp{identif}'][5]/dx_gen)+1,
                           math.ceil(eq_storage[f'qp{identif}'][6]/dy_gen):int(eq_storage[f'qp{identif}'][7]/dy_gen)+1,
                           math.ceil(eq_storage[f'qp{identif}'][8]/dz_gen):int(eq_storage[f'qp{identif}'][9]/dz_gen)+1] -= 1
            if add_or_sub=='sub':
                bar+=1
                matrix_gen[math.ceil(eq_storage[f'qp{identif}'][4]/dx_gen):int(eq_storage[f'qp{identif}'][5]/dx_gen)+1,
                           math.ceil(eq_storage[f'qp{identif}'][6]/dy_gen):int(eq_storage[f'qp{identif}'][7]/dy_gen)+1,
                           math.ceil(eq_storage[f'qp{identif}'][8]/dz_gen):int(eq_storage[f'qp{identif}'][9]/dz_gen)+1] = 0
                
    bar.finish()
                


def gen_epsi_sphere(identif, surface_type, add_or_sub='sub', sph_raf_path=False):
    
    """
    Geração da :math:`{\epsilon}` da esfera criada anteriormente.
    
    Args:
        identif (:obj:`str`): Repita o argumento ``identif`` da esfera em questão.
        surface_type (:obj:`str`): Defina se a esfera será um objeto (adição de "material") ou um contorno (subtração de "material") . Deve assumir ``'solid'`` ou ``'contour'``.
        add_or_sub (:obj:`str`): Defina o mecanismo de criação da :math:`{\epsilon}`. Caso assuma ``'add'``, o fluxo de informação da superfície para a :math:`{\epsilon}` será através de adição (ou subtração, caso seja um ``contour``), caso ideal para obtenção de intersecções (não esquecer de usar a função ``normalize_epsi()`` para correção). Caso assuma ``'sub'``, o fluxo será através de substituição (metodologia padrão).
        sph_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
    
    """
    
    if sph_raf_path==True:
        loop_path=['normal','x','y','z']
    if sph_raf_path==False:
        loop_path=['normal']
        
    for raf in loop_path:
        dx_gen,dy_gen,dz_gen=dx,dy,dz
        nx_gen,ny_gen,nz_gen=nx,ny,nz
        matrix_gen=epsi_3d
        
        bar = progressbar.ProgressBar(widgets=[f'#{identif}: ',
                                               progressbar.AnimatedMarker(),
                                               progressbar.Percentage(),
                                               progressbar.Bar(),'  ',
                                               progressbar.Timer(),], 
                                               max_value=(1)).start()

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
            if add_or_sub=='add':
                bar+=1
                matrix_gen[dis<=eq_storage[f's{identif}'][7]] += 1
            elif add_or_sub=='sub':
                bar+=1
                matrix_gen[dis<=eq_storage[f's{identif}'][7]] = 1

        if surface_type=='contour':
            if add_or_sub=='add':
                bar+=1
                matrix_gen[dis<=eq_storage[f's{identif}'][7]] -= 1
            if add_or_sub=='sub':
                bar+=1
                matrix_gen[dis<=eq_storage[f's{identif}'][7]] = 0
                
    bar.finish()
            
def bounds_into_single_solid(identif_list, identif, solid_raf_path=False):
    
    """
    Função que agrega diversas features em apenas um sólido. Se faz necessário na hora de realizar um mirror atrelado a um ``'target'``.
    
    Args:
        identif_list (:obj:`list,strs`): Lista dos identificadores das features que farão parte do sólido: ``['0','3','2']``, por exemplo.
        identif (:obj:`str`): Crie a **identificação** da feature com :math:`{n}`, onde :math:`{n=0,1,2,3...}`.
        solid_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
    """
    
    
    if solid_raf_path==True:
        loop_path=['normal','x','y','z']
    if solid_raf_path==False:
        loop_path=['normal']
        
    solid_max_x=0
    solid_max_z=0
    solid_max_y=0

    solid_min_x=lx
    solid_min_z=lz
    solid_min_y=ly
    
    for count in identif_list:
        
        try:
            if eq_storage[f'x{count}'][5] > solid_max_x:
                solid_max_x=eq_storage[f'x{count}'][5]

            if eq_storage[f'x{count}'][4] < solid_min_x:
                solid_min_x=eq_storage[f'x{count}'][4]

            if eq_storage[f'z{count}'][5] > solid_max_z:
                solid_max_z=eq_storage[f'z{count}'][5]

            if eq_storage[f'z{count}'][4] < solid_min_z:
                solid_min_z=eq_storage[f'z{count}'][4]

            if eq_storage[f'y{count}'][5] > solid_max_y:
                solid_max_y=eq_storage[f'y{count}'][5]

            if eq_storage[f'y{count}'][4] < solid_min_y:
                solid_min_y=eq_storage[f'y{count}'][4]
        
        except:
            pass
        
        try:
            if eq_storage[f'qp{count}'][5] > solid_max_x:
                solid_max_x=eq_storage[f'qp{count}'][5]

            if eq_storage[f'qp{count}'][4] < solid_min_x:
                solid_min_x=eq_storage[f'qp{count}'][4]

            if eq_storage[f'qp{count}'][9] > solid_max_z:
                solid_max_z=eq_storage[f'qp{count}'][9]

            if eq_storage[f'qp{count}'][8] < solid_min_z:
                solid_min_z=eq_storage[f'qp{count}'][8]

            if eq_storage[f'qp{count}'][7] > solid_max_y:
                solid_max_y=eq_storage[f'qp{count}'][7]

            if eq_storage[f'qp{count}'][6] < solid_min_y:
                solid_min_y=eq_storage[f'qp{count}'][6]
        
        except:
            pass     
        
        try:
            
            if eq_storage[f'ext,x{count},Bezier0'][5]=='z':
                
                for counter in range(0,eq_storage[f'ext,x{count},Bezier0'][9],1):
                    
                    #about maxs
                    
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] == np.ndarray:
                        if max(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot)) > solid_max_x:
                            solid_max_x=max(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,x{count},Bezier{counter}'][1][0] > solid_max_x:
                            solid_max_x=eq_storage[f'ext,x{count},Bezier{counter}'][1][0]
       
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] == np.ndarray:
                        if max(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot)) > solid_max_y:
                            solid_max_y=max(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,y{count},Bezier{counter}'][1][0] > solid_max_y:
                            solid_max_y=eq_storage[f'ext,y{count},Bezier{counter}'][1][0]
                    
                    
                    if eq_storage[f'ext,x{count},Bezier{counter}'][12] > solid_max_z:
                        solid_max_z=eq_storage[f'ext,x{count},Bezier{counter}'][12]
                        
                    #about mins 
                        
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] == np.ndarray:
                        if min(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot)) < solid_min_x:
                            solid_min_x=min(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,x{count},Bezier{counter}'][1][0] < solid_min_x:
                            solid_min_x=eq_storage[f'ext,x{count},Bezier{counter}'][1][0]
                        
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] == np.ndarray:
                        if min(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot)) < solid_min_y:
                            solid_min_y=min(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,y{count},Bezier{counter}'][1][0] < solid_min_y:
                            solid_min_y=eq_storage[f'ext,y{count},Bezier{counter}'][1][0]
                        
                    if eq_storage[f'ext,x{count},Bezier{counter}'][11] < solid_min_z: #height is stored at x and y dict, it doesnt make difference which one to choose
                        solid_min_z=eq_storage[f'ext,x{count},Bezier{counter}'][11]
                        
            if eq_storage[f'ext,x{count},Bezier0'][5]=='x':
                
                for counter in range(0,eq_storage[f'ext,x{count},Bezier0'][9],1):
                    
                    #about maxs
                    
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] == np.ndarray:
                        if max(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot)) > solid_max_z:
                            solid_max_z=max(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,x{count},Bezier{counter}'][1][0] > solid_max_z:
                            solid_max_z=eq_storage[f'ext,x{count},Bezier{counter}'][1][0]
       
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] == np.ndarray:
                        if max(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot)) > solid_max_y:
                            solid_max_y=max(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,y{count},Bezier{counter}'][1][0] > solid_max_y:
                            solid_max_y=eq_storage[f'ext,y{count},Bezier{counter}'][1][0]
                    
                    
                    if eq_storage[f'ext,x{count},Bezier{counter}'][12] > solid_max_x:
                        solid_max_x=eq_storage[f'ext,x{count},Bezier{counter}'][12]
                        
                    #about mins 
                        
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] == np.ndarray:
                        if min(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot)) < solid_min_z:
                            solid_min_z=min(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,x{count},Bezier{counter}'][1][0] < solid_min_z:
                            solid_min_z=eq_storage[f'ext,x{count},Bezier{counter}'][1][0]
                        
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] == np.ndarray:
                        if min(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot)) < solid_min_y:
                            solid_min_y=min(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,y{count},Bezier{counter}'][1][0] < solid_min_y:
                            solid_min_y=eq_storage[f'ext,y{count},Bezier{counter}'][1][0]
                        
                    if eq_storage[f'ext,x{count},Bezier{counter}'][11] < solid_min_x: #height is stored at x and y dict, it doesnt make difference which one to choose
                        solid_min_x=eq_storage[f'ext,x{count},Bezier{counter}'][11]
                        
            if eq_storage[f'ext,x{count},Bezier0'][5]=='y':
                
                for counter in range(0,eq_storage[f'ext,x{count},Bezier0'][9],1):
                    
                    #about maxs
                    
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] == np.ndarray:
                        if max(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot)) > solid_max_x:
                            solid_max_x=max(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,x{count},Bezier{counter}'][1][0] > solid_max_x:
                            solid_max_x=eq_storage[f'ext,x{count},Bezier{counter}'][1][0]
       
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] == np.ndarray:
                        if max(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot)) > solid_max_z:
                            solid_max_z=max(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,y{count},Bezier{counter}'][1][0] > solid_max_z:
                            solid_max_z=eq_storage[f'ext,y{count},Bezier{counter}'][1][0]
                    
                    
                    if eq_storage[f'ext,x{count},Bezier{counter}'][12] > solid_max_y:
                        solid_max_y=eq_storage[f'ext,x{count},Bezier{counter}'][12]
                        
                    #about mins 
                        
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] == np.ndarray:
                        if min(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot)) < solid_min_x:
                            solid_min_x=min(eq_storage[f'ext,x{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,x{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,x{count},Bezier{counter}'][1][0] < solid_min_x:
                            solid_min_x=eq_storage[f'ext,x{count},Bezier{counter}'][1][0]
                        
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] == np.ndarray:
                        if min(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot)) < solid_min_z:
                            solid_min_z=min(eq_storage[f'ext,y{count},Bezier{counter}'][0](t_plot))
                    if eq_storage[f'ext,y{count},Bezier{counter}'][8] != np.ndarray:
                        if eq_storage[f'ext,y{count},Bezier{counter}'][1][0] < solid_min_z:
                            solid_min_z=eq_storage[f'ext,y{count},Bezier{counter}'][1][0]
                        
                    if eq_storage[f'ext,x{count},Bezier{counter}'][11] < solid_min_y: #height is stored at x and y dict, it doesnt make difference which one to choose
                        solid_min_y=eq_storage[f'ext,x{count},Bezier{counter}'][11]
        
        except:
            pass
        
        
        try:
            
            if eq_storage[f'c{count}'][4]=='xz':
                loc_min_x=eq_storage[f'c{count}'][6]-eq_storage[f'c{count}'][5]
                loc_min_y=eq_storage[f'c{count}'][8]
                loc_min_z=eq_storage[f'c{count}'][7]-eq_storage[f'c{count}'][5]
                
                loc_max_x=eq_storage[f'c{count}'][6]+eq_storage[f'c{count}'][5]
                loc_max_y=eq_storage[f'c{count}'][9]
                loc_max_z=eq_storage[f'c{count}'][7]+eq_storage[f'c{count}'][5]
                
            if eq_storage[f'c{count}'][4]=='xy':
                loc_min_x=eq_storage[f'c{count}'][6]-eq_storage[f'c{count}'][5]
                loc_min_z=eq_storage[f'c{count}'][8]
                loc_min_y=eq_storage[f'c{count}'][7]-eq_storage[f'c{count}'][5]
                
                loc_max_x=eq_storage[f'c{count}'][6]+eq_storage[f'c{count}'][5]
                loc_max_z=eq_storage[f'c{count}'][9]
                loc_max_y=eq_storage[f'c{count}'][7]+eq_storage[f'c{count}'][5]
                
            if eq_storage[f'c{count}'][4]=='zy':
                loc_min_z=eq_storage[f'c{count}'][6]-eq_storage[f'c{count}'][5]
                loc_min_x=eq_storage[f'c{count}'][8]
                loc_min_y=eq_storage[f'c{count}'][7]-eq_storage[f'c{count}'][5]
                
                loc_max_z=eq_storage[f'c{count}'][6]+eq_storage[f'c{count}'][5]
                loc_max_x=eq_storage[f'c{count}'][9]
                loc_max_y=eq_storage[f'c{count}'][7]+eq_storage[f'c{count}'][5]
                
            
            if loc_max_x > solid_max_x:
                solid_max_x=loc_max_x

            if loc_min_x < solid_min_x:
                solid_min_x=loc_min_x

            if loc_max_y > solid_max_y:
                solid_max_y=loc_max_y

            if loc_min_y < solid_min_y:
                solid_min_y=loc_min_y
                
            if loc_max_z > solid_max_z:
                solid_max_z=loc_max_z

            if loc_min_z < solid_min_z:
                solid_min_z=loc_min_z
        
        except:
            pass
        
        try:
            loc_min_x=eq_storage[f's{count}'][4]-eq_storage[f's{count}'][7]
            loc_min_y=eq_storage[f's{count}'][5]-eq_storage[f's{count}'][7]
            loc_min_z=eq_storage[f's{count}'][6]-eq_storage[f's{count}'][7]
                
            loc_max_x=eq_storage[f's{count}'][4]+eq_storage[f's{count}'][7]
            loc_max_y=eq_storage[f's{count}'][5]+eq_storage[f's{count}'][7]
            loc_max_z=eq_storage[f's{count}'][6]+eq_storage[f's{count}'][7]
                
            if loc_max_x > solid_max_x:
                solid_max_x=loc_max_x

            if loc_min_x < solid_min_x:
                solid_min_x=loc_min_x

            if loc_max_y > solid_max_y:
                solid_max_y=loc_max_y

            if loc_min_y < solid_min_y:
                solid_min_y=loc_min_y
                
            if loc_max_z > solid_max_z:
                solid_max_z=loc_max_z

            if loc_min_z < solid_min_z:
                solid_min_z=loc_min_z
                
        except:
            pass
        
        try:
            if eq_storage[f'superiorrc{count}'][4]=='xz':
                loc_min_x=eq_storage[f'superiorrc{count}'][6]-eq_storage[f'superiorrc{count}'][5]
                loc_min_y=eq_storage[f'superiorrc{count}'][8]
                loc_min_z=eq_storage[f'superiorrc{count}'][7]-eq_storage[f'superiorrc{count}'][5]
                
                loc_max_x=eq_storage[f'superiorrc{count}'][6]+eq_storage[f'superiorrc{count}'][5]
                loc_max_y=eq_storage[f'superiorrc{count}'][9]
                loc_max_z=eq_storage[f'superiorrc{count}'][7]+eq_storage[f'superiorrc{count}'][5]
                
            if eq_storage[f'superiorrc{count}'][4]=='xy':
                loc_min_x=eq_storage[f'superiorrc{count}'][6]-eq_storage[f'superiorrc{count}'][5]
                loc_min_z=eq_storage[f'superiorrc{count}'][8]
                loc_min_y=eq_storage[f'superiorrc{count}'][7]-eq_storage[f'superiorrc{count}'][5]
                
                loc_max_x=eq_storage[f'superiorrc{count}'][6]+eq_storage[f'superiorrc{count}'][5]
                loc_max_z=eq_storage[f'superiorrc{count}'][9]
                loc_max_y=eq_storage[f'superiorrc{count}'][7]+eq_storage[f'superiorrc{count}'][5]
                
            if eq_storage[f'superiorrc{count}'][4]=='zy':
                loc_min_z=eq_storage[f'superiorrc{count}'][6]-eq_storage[f'superiorrc{count}'][5]
                loc_min_x=eq_storage[f'superiorrc{count}'][8]
                loc_min_y=eq_storage[f'superiorrc{count}'][7]-eq_storage[f'superiorrc{count}'][5]
                
                loc_max_z=eq_storage[f'superiorrc{count}'][6]+eq_storage[f'superiorrc{count}'][5]
                loc_max_x=eq_storage[f'superiorrc{count}'][9]
                loc_max_y=eq_storage[f'superiorrc{count}'][7]+eq_storage[f'superiorrc{count}'][5]
                
            
            if loc_max_x > solid_max_x:
                solid_max_x=loc_max_x

            if loc_min_x < solid_min_x:
                solid_min_x=loc_min_x

            if loc_max_y > solid_max_y:
                solid_max_y=loc_max_y

            if loc_min_y < solid_min_y:
                solid_min_y=loc_min_y
                
            if loc_max_z > solid_max_z:
                solid_max_z=loc_max_z

            if loc_min_z < solid_min_z:
                solid_min_z=loc_min_z
                
        except:
            pass
        
    solid_storage[f'{identif}']=[solid_max_x,solid_max_y,solid_max_z,solid_min_x,solid_min_y,solid_min_z]
        
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
            
        for cx in range(int(solid_min_x/dx_gen), math.ceil(solid_max_x/dx_gen)+1,1):
            for cz in range(int(solid_min_z/dz_gen), math.ceil(solid_max_z/dz_gen)+1,1):
                for cy in range(int(solid_min_y/dy_gen), math.ceil(solid_max_y/dy_gen)+1,1):
                    if matrix_gen[cx][cy][cz] == 1:
                        matrix_gen[cx][cy][cz] = int(identif)

def epsi_plot(direction, grid=True, ticks='full', integral=False, raf='normal'):
    
    """
    Confira se os limites estão corretos, camada por camada ou por amostragem, em qualquer direção.
    
    Args:
        direction (:obj:`str`): Poderá assumir os seguintes valores: ``'x'``, ``'y'`` ou ``'z'``.
        grid (:obj:`Bool`, optional): Caso houver número demasiado de nós (>250), setar como ``False`` auxiliará na visualização. 
        ticks(:obj:`str`, optional): Definição dos ticks da imagem (números que acompanham os eixos). Pode assumir ``full`` (ideal para poucos nós), ``some`` (ideal para número alto de nós), ``none`` (imagem limpa).
        integral (:obj:`Bool`, optional): Se o usuário quiser conferir meticulosamente todas as camadas, sete como ``True``.
        raf (:obj:`str`, optional): Se o usuário quiser conferir alguma :math:`{\epsilon}` refinada, setar com ``'x'``, ``'y'`` ou ``'z'``.

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
        fig_epsi, a2 = plt.subplots(figsize=(6,6))
        fig_epsi.suptitle(f'{plane} plane, {direction} = {round(c1*d1,1)}', fontsize=25)
        a2.set_xlabel(name_l2, fontsize=15), a2.set_ylabel(name_l3, fontsize=15)
        a2.set_xlim(0,l2), a2.set_ylim(0,l3)
        a2.set_xticks(np.arange(0, l2+d2/2, d2)), a2.set_xticks(np.arange(d2/2, l2, d2), minor=True)
        a2.set_yticks(np.arange(0, l3+d3/2, d3)), a2.set_yticks(np.arange(d3/2, l3, d3), minor=True)
        if ticks=='some':
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
            
        elif ticks=='none':
            xticks=[]
            yticks=[]
            a2.set_xticklabels(xticks), a2.set_yticklabels(yticks)
            
        elif ticks=='full':
            a2.set_xticklabels((np.arange(0, l2+d2/2, d2)).round(decimals=2),fontsize=8), a2.set_yticklabels((np.arange(0, l3+d3/2, d3)).round(decimals=2),fontsize=8)
            a2.tick_params(axis='x', rotation=45)
        
        if grid==True:
            a2.grid(which='minor', zorder=1), a2.grid(which='major', alpha=0.3, zorder=1)  
        
        if direction == 'z':
            epsi_dependente = matrix_show[:,:,c1].T
        if direction == 'x':
            epsi_dependente = matrix_show[c1,:,:]
        if direction == 'y':
            epsi_dependente = matrix_show[:,c1,:].T
            
        epsi_map = a2.imshow(epsi_dependente, cmap = 'tab20', origin='lower',extent=[-d2/2, l2+d2/2, -d3/2, l3+d3/2])
        #fig_epsi.colorbar(epsi_map)
        #epsi_map.set_clim(vmin=0, vmax=10)
        plt.show()
           
def normalize_epsi(intersection=False, target=2, epsi_raf_path=False):
    
    """
    Ideal chamar essa função antes de gerar os arquivos de saída. Corrige qualquer valor inadequado da :math:`{\epsilon}` (menor do que 0 ou maior do que 1) que podem ser gerados ao decorrer do projeto.
    
    Args:
        intersection (:obj:`Bool`, optional): Setar como ``True`` para validar intersecções entre superfícies. Maiores informações em :ref:`intersec`.
        target (:obj:`Bool`, optional): Caso ``intersection=True``, setar nesse argumento qual valor será considerado o alvo para transformar as intersecções em sólidos independentes. Caso assuma ``2``, por exemplo, todos os valores na :math:`{\epsilon}` que forem menor do que 2 serão setados como 0, enquanto todos valores iguais ou superiores a 2 serão setados como 1.
        epsi_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
        
    """
    
    if epsi_raf_path==True:
        loop_path=['normal','x','y','z']

    if epsi_raf_path==False:
        loop_path=['normal']
        
    for raf in loop_path:

        nx_print,ny_print,nz_print=nx,ny,nz
        matrix_print=epsi_3d

        if raf=='x':
            nx_print=nx_raf
            matrix_print=epsi_3d_x_raf
        if raf=='y':
            ny_print=ny_raf
            matrix_print=epsi_3d_y_raf
        if raf=='z':
            nz_print=nz_raf
            matrix_print=epsi_3d_z_raf
            
        if intersection==False:
            matrix_print[matrix_print>1]=1
            matrix_print[matrix_print<0]=0
                            
        if intersection==True:
            matrix_print[matrix_print< target]=0
            matrix_print[matrix_print>=target]=1
            
def gen_output(names, out_raf_path=False):
    
    """
    Geração dos arquivos de saída. Tornam possível a visualização no ParaView da :math:`{\epsilon}`, bem como a resolução das equações
    de Navier Stokes nas redondezas do sólido criado.
    
    Args:
        names (:obj:`str`): Entre com o name que será dado aos arquivos gerado pelo programa.
        out_raf_path (:obj:`Bool`, optional): Sete como ``True`` para criar as informações para o refinamento de malha. Ideal para o final do projeto, no qual todas as features já estão definidas.
    
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
