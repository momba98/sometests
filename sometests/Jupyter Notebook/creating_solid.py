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

armz_pt=s.armz_pt
npsu=s.npsu
npsv=s.npsv
u=s.u
v=s.v
mu=s.mu
mv=s.mv
mpx=s.mpx
mpy=s.mpy
mpz=s.mpz
lz=s.lz
lx=s.lx
ly=s.ly
armz_eq=s.armz_eq
nz_visualizacao,ny_visualizacao,nx_visualizacao=s.nz_visualizacao,s.ny_visualizacao,s.nx_visualizacao
dz_visualizacao,dy_visualizacao,dx_visualizacao=s.dz_visualizacao,s.dy_visualizacao,s.dx_visualizacao
contador=s.contador
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
nome=s.nome
dx=s.dx
dy=s.dy
dz=s.dz
ny=s.ny
nx=s.nx
nz=s.nz
epsi_3d=s.epsi_3d
armz_nomenclt_epsi=s.armz_nomenclt_epsi

def prepara_matriz_pontos(pontos_u,pontos_v):
    
    """
    Importante função em que o usuário determinará o número de pontos em cada direção :obj:`[u,v]`.
    
    Caso fique em dúvida da nomenclatura de quais pontos serão necessários setar, execute uma célula (após executar a função em pauta) com :obj:`print(armz_pt)`::
        
        #exemplo de como tirar a dúvida dos pontos que devem receber algum input
        prepara_matriz_pontos(3,3)
        print(armz_pt)
    
    Basicamente, os pontos a serem determinados possuem 2 sub-índices: :obj:`i` e :obj:`j` → :obj:`Pij`.
    
    Note:
        Os sub-índices começarão em :obj:`0` e irão até :obj:`i-1` e/ou :obj:`j-1`.
    
    Args:
        pontos_u (:obj:`int`): Determine o número de pontos que a direção :obj:`u` terá.
        pontos_v (:obj:`int`): Determine o número de pontos que a direção :obj:`v` terá.
    
    Exemplo:
        Será explicitado quais pontos deverão ser setados de acordo com as entradas::
        
            prepara_matriz_pontos(3,2) #função é chamada
            
            armz_pt['P00'] = [x,y,z] #declara-se as informações do ponto
            armz_pt['P01'] = [x,y,z] #qualquer ponto de 3 coordenadas dentro do domínio
            armz_pt['P10'] = [x,y,z]
            armz_pt['P11'] = [x,y,z]
            armz_pt['P20'] = [x,y,z]
            armz_pt['P21'] = [x,y,z]
            
        Note que o primeiro subíndice, :obj:`i`, começa em :obj:`0` e termina em :obj:`2`, que é o correspondente a :obj:`pontos_u=3-pontos_v=1`.
        
        O dicionário :obj:`armz_pt` faz parte da mecânica do código, não deve ser alterado. Auxilia na setagem e no armazenamento das informações.

    """
        
    armz_pt={}
    
    s.npsu=pontos_u
    global npsv
    s.npsv=pontos_v
    
    for i in range(0,s.npsu,1):
        for j in range(0,s.npsv,1):
            armz_pt[f'P{i}{j}'] = [0,0,0]
    
    mut=np.array([s.u**0,s.u**1,s.u**2,s.u**3,s.u**4,s.u**5,s.u**6,s.u**7,s.u**8,s.u**9])
    mvt=np.array(([s.v**0],[s.v**1],[s.v**2],[s.v**3],[s.v**4],[s.v**5],[s.v**6],[s.v**7],[s.v**8],[s.v**9]))
    
    s.mu=mut[:s.npsu]
    s.mv=mvt[:s.npsv]
    s.mpx=np.empty((s.npsu,s.npsv))
    s.mpy=np.empty((s.npsu,s.npsv))
    s.mpz=np.empty((s.npsu,s.npsv))


def cria_matriz_pontos(desvio=False):
    
    """
    Auxílio na hora de setar os pontos necessários para as equações da função :obj:`gen_bezi()`.
    
    Args: 
        desvio (:obj:`Bool`, optional): Sete como :obj:`True` caso queira que a superfície passe pelos pontos de controle 
            (pontos intermediários, os que normalmente dão a curvatura suave à superfície). Baseia-se num artifício
            matemático que *hackeia* a Bézier, forçando-a a fazer algo que normalmente não faria.
    Warning:
        :obj:`desvio=True` **não demonstrará efeito em todos os casos!**
        
        O parâmetro pode ficar setado como True sem danificar o código, porém só efetivamente desviará a superfície 
        caso :obj:`n_pontos_u=3` ao mesmo tempo que :obj:`n_pontos_v=2` ou vice-versa.
        
        **O porquê da restrição:** 
        
        Como pode-se imaginar, não há necessidade de desviar a superfície para passar em pontos intermediários caso existam apenas 2 
        pontos na direção :obj:`[u,v]` pois não há pontos intermediários. Também, caso a superfície tenha 3 pontos em cada direção 
        :obj:`[u,v]` ou mais, torna-se *matematicamente complicado* descrever o desvio.
            
    """
    for i in range(s.npsu):
        for j in range(s.npsv):
            s.mpx[i][j] = s.armz_pt[f'P{i}{j}'][0]
            s.mpy[i][j] = s.armz_pt[f'P{i}{j}'][1]
            s.mpz[i][j] = s.armz_pt[f'P{i}{j}'][2]
            
    s.mpx_sem_desvio, s.mpy_sem_desvio, s.mpz_sem_desvio= s.mpx.copy(), s.mpy.copy(), s.mpz.copy()
    
    if desvio==True:
        if s.npsu==3:
            if s.npsv==2:
                s.mpx[1][0] = s.mpx[1][0]*2 - (s.mpx[0][0]+s.mpx[2][0])/2
                s.mpx[1][1] = s.mpx[1][1]*2 - (s.mpx[0][1]+s.mpx[2][1])/2
                s.mpy[1][0] = s.mpy[1][0]*2 - (s.mpy[0][0]+s.mpy[2][0])/2
                s.mpy[1][1] = s.mpy[1][1]*2 - (s.mpy[0][1]+s.mpy[2][1])/2
                s.mpz[1][0] = s.mpz[1][0]*2 - (s.mpz[0][0]+s.mpz[2][0])/2
                s.mpz[1][1] = s.mpz[1][1]*2 - (s.mpz[0][1]+s.mpz[2][1])/2

        if s.npsu==2:
            if s.npsv==3:
                s.mpx[0][1] = s.mpx[0][1]*2 - (s.mpx[0][0]+s.mpx[0][2])/2
                s.mpx[1][1] = s.mpx[1][1]*2 - (s.mpx[1][0]+s.mpx[1][2])/2
                s.mpy[0][1] = s.mpy[0][1]*2 - (s.mpy[0][0]+s.mpy[0][2])/2
                s.mpy[1][1] = s.mpy[1][1]*2 - (s.mpy[1][0]+s.mpy[1][2])/2
                s.mpz[0][1] = s.mpz[0][1]*2 - (s.mpz[0][0]+s.mpz[0][2])/2
                s.mpz[1][1] = s.mpz[1][1]*2 - (s.mpz[1][0]+s.mpz[1][2])/2
                
def transladar(direcao,quantidade):
    
    """
    Caso tenha se precipitado em relação à posição de sua superfície, translade seus pontos de forma eficiente 
    em qualquer direção. 

    Args:
        direcao (:obj:`str`): Defina em qual direção a translação será feita. Deve assumir :obj:`'x', 'y', 'z'`.
        quantidade (:obj:`int`): Assume quantas unidades de comprimento de domínio o usuário quer transladar sua superfície.
        
    Note: 
        Deverá ser obrigatoriamente chamada entre a função :obj:`cria_matriz_pontos()` e a função :obj:`gen_bezi()`.
        
    Exemplo::
        
        prepara_matriz_pontos(2,2)
            
        armz_pt['P00'] = [x,y,z] 
        armz_pt['P01'] = [x,y,z] 
        armz_pt['P10'] = [x,y,z]
        armz_pt['P11'] = [x,y,z]
        
        cria_matriz_pontos()
        
        transladar('y',1.5)

        transladar('x',-0.5)

        gen_bezi('0',capô)

    """
    
    if direcao=='x':
        for i in range(s.npsu):
            for j in range(s.npsv):
                s.mpx_sem_desvio[i][j] = s.mpx_sem_desvio[i][j]+quantidade
                s.mpx[i][j] = s.mpx[i][j]+quantidade
    
    if direcao=='y':
        for i in range(s.npsu):
            for j in range(s.npsv):
                s.mpy_sem_desvio[i][j] = s.mpy_sem_desvio[i][j]+quantidade
                s.mpy[i][j] = s.mpy[i][j]+quantidade
    
    if direcao=='z':
        for i in range(s.npsu):
            for j in range(s.npsv):
                s.mpz_sem_desvio[i][j] = s.mpz_sem_desvio[i][j]+quantidade
                s.mpz[i][j] = s.mpz[i][j]+quantidade

                
def gen_bezi(identif, nome, show_equation=False):
    
    """
    
    As equações de Bézier são governadas pelos parâmetros :obj:`u` e :obj:`v` e fornecem leis para curvas/superfícies. 
    
    São definidas por pontos arbitrados pelo usuário, tendo um mínimo de 2 em cada direção :obj:`[u,v]` e sem algum máximo pré-determinado.
    
    Os pontos iniciais e finais determinam onde a curva começa e termina, obviamente. *São os únicos pontos por onde a Bézier (naturalmente) passará com certeza*. 
    Os pontos intermediários estão encarregados de fornecer à Bézier uma curvatura suave, sem canto vivo/descontinuidade, 
    portanto a curva/superfície nunca *encosta* neles.
    
    Como o grau das equações é definido por :obj:`número de pontos definidos pelo usuário - 1`, recomenda-se usar no máximo 3 pontos em cada direção, 
    para que assim os cálculos se tornem baratos. Caso um objeto seja extremamente complexo, recomenda-se dividí-lo em várias superfícies de grau 2.
    
    Warning:
        É importante frisar que, caso construída uma superfície muito complexa (com variações não lineares entre os pontos em mais de 2 direções :obj:`xyz`), 
        a convergência das equações não é garantida - por enquanto.
    
    Args:
        identif (:obj:`str`): Crie a *identificação* da sua superfície com :obj:`'n'`, onde :obj:`n=0,1,2,3...` (começar em '0' e somar '1' a cada nova superfície).
    
    Note:
        :obj:`identif()` **necessita atenção especial**: o usuário voltará a chamar o parâmetro por diversas vezes ao decorrer do código.
        
    Args:
        nome (:obj:`str`): Crie um nome para a superfície. Não há regras. 
        show_equations (:obj:`Bool`, optional): Sete como :obj:`True` caso queira visualizar as equações governantes da superfície em questão.

    """
    
    for matriz_base,tipo,matriz_sem_desvio in [s.mpx,'x',s.mpx_sem_desvio],[s.mpy,'y',s.mpy_sem_desvio],[s.mpz,'z',s.mpz_sem_desvio]:
    
        s.mm = np.empty((s.npsu,s.npsu), dtype=float)

        berstein(s.npsu)

        mf_parcial=s.mu.dot(s.mm[::-1,:]).dot(matriz_base)

        s.mm = np.empty((s.npsv,s.npsv), dtype=float)

        berstein(s.npsv)

        mf=mf_parcial.dot(s.mm[::-1,:].T).dot(s.mv)

        eq=lambdify([s.u,s.v],mf[0])

        matriz_plot=np.empty((s.u_plot.size,s.v_plot.size))

        for up in s.u_plot:
            for vp in s.v_plot:
                matriz_plot[int(up*(s.u_plot.size-1))][int(vp*(s.v_plot.size-1))]=eq(up,vp)

        s.armz_eq[f'{tipo}{identif}'] = [nome,mf,eq,matriz_plot,np.amin(matriz_plot),np.amax(matriz_plot),s.npsu,s.npsv,matriz_sem_desvio.copy()]
        
        if show_equation==True:
            print(f'Equação para {tipo}(u,v) do objeto #{identif}: '),display(mf[0]),print('\n')
            
            
def berstein(n_p):
    
    """
    Matemática chave por trás das curvas/superfícies de Bézier, dentro da própria função :obj:`gen_bezi()`. 
    
    Args:
        n_p(:obj:`int`): Não há necessidade alguma de manipulação por parte do usuário.
    
    """
    
    for i in range(n_p): #berstein poly
        Bint = sp.expand((math.factorial(n_p-1) / (math.factorial(i)*math.factorial(n_p-1-i)))*s.u**i*(1-s.u)**(n_p-1-i))
        coef = sp.Poly(Bint, s.u)
        aux = coef.coeffs()
        for c in range(i):
            aux.append(0)
        for j in range(n_p):
            s.mm[i][j]=aux[j] #matriz chave do polinomio d
                
                
def gen_bezi_cylinder(bases_plane,radius,center_1,center_2,init_height,final_height,identif_inicial):
    
    """
    Uma função derivada de :obj:`gen_bezi()` que facilita a criação de cilíndros. De saída são geradas
    4 Béziers diferentes que juntas formam um cilíndro. Caso esta função seja chamada, no momento de solução
    da Epsi será necessário usar a função :obj:`gen_epsi_cylinder()`.
    
    Args:
        bases_plane (:obj:`str`): Defina o plano paralelo à base. Pode assumir :obj:`'xy','xz','zy'`.
        radius (:obj:`float`): Defina o raio do cilíndro
        center_1 (:obj:`float`): Coordenada do eixo correspondente à primeira letra do :obj:`bases_plane`.
        center_2 (:obj:`float`): Coordenada do eixo correspondente à segunda letra do :obj:`bases_plane`.
        init_height (:obj:`float`): Altura da base inferior do cilíndro.
        final_height (:obj:`float`): Altura da base superior do cilíndro.
        identif_inicial (:obj:`str`): O mesmo :obj:`identif` do resto do código. O usuário deverá criar a identificação da primeira
            das quatro Béziers geradas na função, as outras identificações são automáticas.
        
    Exemplo:
        Para criar um cilíndro de raio 1 e altura 2 no plano :obj:`xz` caso alguma superfície já tenha sido criada e 
        identificada com :obj:`identif='0'`::
        
            gen_bezi_cylinder(bases_plane='xz',radius=1,
                              center_1=3, center_2=3
                              init_height=2,final_height=4,
                              identif_inicial='1')
                              
    Warning:
        Como já descrito, são geradas 4 Béziers nesta função. Portanto, caso haja alguma geração de Bézier depois dessa em questão,
        o argumento :obj:`identif` deverá ser igual ao desta função somadas mais 4 unidades. No exemplo descrito logo acima, o próximo
        :obj:`identif`, quaisquer que seja, deveria ser :obj:`'5'`.

    """
    
    identif_inicial=int(identif_inicial)
    cos=math.cos(math.radians(45))
    sin=math.sin(math.radians(45))
    
    if bases_plane=='xy':

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[center_1-radius,center_2,init_height]
        armz_pt['P01']=[center_1-radius,center_2,final_height]
        armz_pt['P10']=[center_1-radius*cos,center_2+radius*sin,init_height]
        armz_pt['P11']=[center_1-radius*cos,center_2+radius*sin,final_height]
        armz_pt['P20']=[center_1,center_2+radius,init_height]
        armz_pt['P21']=[center_1,center_2+radius,final_height]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial}','rs,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[center_1,center_2+radius,init_height]
        armz_pt['P01']=[center_1,center_2+radius,final_height]
        armz_pt['P10']=[center_1+radius*cos,center_2+radius*sin,init_height]
        armz_pt['P11']=[center_1+radius*cos,center_2+radius*sin,final_height]
        armz_pt['P20']=[center_1+radius,center_2,init_height]
        armz_pt['P21']=[center_1+radius,center_2,final_height]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial+1}','rs,saida')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[center_1-radius,center_2,init_height]
        armz_pt['P01']=[center_1-radius,center_2,final_height]
        armz_pt['P10']=[center_1-radius*cos,center_2-radius*sin,init_height]
        armz_pt['P11']=[center_1-radius*cos,center_2-radius*sin,final_height]
        armz_pt['P20']=[center_1,center_2-radius,init_height]
        armz_pt['P21']=[center_1,center_2-radius,final_height]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial+2}','ri,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[center_1,center_2-radius,init_height]
        armz_pt['P01']=[center_1,center_2-radius,final_height]
        armz_pt['P10']=[center_1+radius*cos,center_2-radius*sin,init_height]
        armz_pt['P11']=[center_1+radius*cos,center_2-radius*sin,final_height]
        armz_pt['P20']=[center_1+radius,center_2,init_height]
        armz_pt['P21']=[center_1+radius,center_2,final_height]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial+3}','ri,saida')
        
    if bases_plane=='xz':
    
        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[center_1-radius,init_height,center_2]
        armz_pt['P01']=[center_1-radius,final_height,center_2]
        armz_pt['P10']=[center_1-radius*cos,init_height,center_2+radius*sin]
        armz_pt['P11']=[center_1-radius*cos,final_height,center_2+radius*sin]
        armz_pt['P20']=[center_1,init_height,center_2+radius]
        armz_pt['P21']=[center_1,final_height,center_2+radius]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial}','rs,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[center_1,init_height,center_2+radius]
        armz_pt['P01']=[center_1,final_height,center_2+radius]
        armz_pt['P10']=[center_1+radius*cos,init_height,center_2+radius*sin]
        armz_pt['P11']=[center_1+radius*cos,final_height,center_2+radius*sin]
        armz_pt['P20']=[center_1+radius,init_height,center_2]
        armz_pt['P21']=[center_1+radius,final_height,center_2]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial+1}','rs,saida')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[center_1-radius,init_height,center_2]
        armz_pt['P01']=[center_1-radius,final_height,center_2]
        armz_pt['P10']=[center_1-radius*cos,init_height,center_2-radius*sin]
        armz_pt['P11']=[center_1-radius*cos,final_height,center_2-radius*sin]
        armz_pt['P20']=[center_1,init_height,center_2-radius]
        armz_pt['P21']=[center_1,final_height,center_2-radius]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial+2}','ri,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[center_1,init_height,center_2-radius]
        armz_pt['P01']=[center_1,final_height,center_2-radius]
        armz_pt['P10']=[center_1+radius*cos,init_height,center_2-radius*sin]
        armz_pt['P11']=[center_1+radius*cos,final_height,center_2-radius*sin]
        armz_pt['P20']=[center_1+radius,init_height,center_2]
        armz_pt['P21']=[center_1+radius,final_height,center_2]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial+3}','ri,saida')

        
    if bases_plane=='zy':

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[init_height,center_2,center_1-radius]
        armz_pt['P01']=[final_height,center_2,center_1-radius]
        armz_pt['P10']=[init_height,center_2+radius*sin,center_1-radius*cos]
        armz_pt['P11']=[final_height,center_2+radius*sin,center_1-radius*cos]
        armz_pt['P20']=[init_height,center_2+radius,center_1]
        armz_pt['P21']=[final_height,center_2+radius,center_1]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial}','rs,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[init_height,center_2+radius,center_1]
        armz_pt['P01']=[final_height,center_2+radius,center_1]
        armz_pt['P10']=[init_height,center_2+radius*sin,center_1+radius*cos]
        armz_pt['P11']=[final_height,center_2+radius*sin,center_1+radius*cos]
        armz_pt['P20']=[init_height,center_2,center_1+radius]
        armz_pt['P21']=[final_height,center_2,center_1+radius]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial+1}','rs,saida')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[init_height,center_2,center_1-radius]
        armz_pt['P01']=[final_height,center_2,center_1-radius]
        armz_pt['P10']=[init_height,center_2-radius*sin,center_1-radius*cos]
        armz_pt['P11']=[final_height,center_2-radius*sin,center_1-radius*cos]
        armz_pt['P20']=[init_height,center_2-radius,center_1]
        armz_pt['P21']=[final_height,center_2-radius,center_1]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial+2}','ri,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[init_height,center_2-radius,center_1]
        armz_pt['P01']=[final_height,center_2-radius,center_1]
        armz_pt['P10']=[init_height,center_2-radius*sin,center_1+radius*cos]
        armz_pt['P11']=[final_height,center_2-radius*sin,center_1+radius*cos]
        armz_pt['P20']=[init_height,center_2,center_1+radius]
        armz_pt['P21']=[final_height,center_2,center_1+radius]
        cria_matriz_pontos(desvio=True)
        gen_bezi(f'{identif_inicial+3}','ri,saida')
                
def plota_superficie(identif_inicial,identif_final, pontos=False, alpha=0.3):
    
    """
    Args:
        identif_inicial (:obj:`str`): Determine o início do intervalo de superfícies a serem plotadas através da identificação :obj:`identif`.
        identif_final (:obj:`str`): Determine o final do intervalo (endpoint não incluido) de superfícies a serem plotadas através da identificação :obj:`identif`
        pontos (:obj:`Bool`, optional): Caso queira visualizar os pontos que governam sua superfície, sete como :obj:`True`.
        alpha (:obj:`float`, optional): Controlador da opacidade da superfície em questão. Pode assumir qualquer valor entre :obj:`0` (transparente) e :obj:`1` (opaco).

    """
    identif_inicial=int(identif_inicial)
    identif_final=int(identif_final)
    
    global fig,ax
    
    fig = plt.figure(figsize=(9,9))
    ax = fig.add_subplot(1, 1, 1, projection='3d', proj_type='ortho')
    
    ax.set_xlabel('x'),ax.set_ylabel('y'),ax.set_zlabel('z'),ax.set_xlim(0,max([lx,ly,lz])),ax.set_ylim(0,max([lx,ly,lz])),ax.set_zlim(0,max([lx,ly,lz])),
    ax.view_init(25,-145),ax.set_title('Superfície/Pontos de controle',size=20)
    
    for z in [0,lz]: #domínio
        ax.plot([0,0],[0,ly],[z,z],   'k--',linewidth=0.5,alpha=0.7)
        ax.plot([0,lx],[0,0],[z,z],   'k--',linewidth=0.5,alpha=0.7)
        ax.plot([0,lx],[ly,ly],[z,z], 'k--',linewidth=0.5,alpha=0.7)
        ax.plot([lx,lx],[ly,0],[z,z], 'k--',linewidth=0.5,alpha=0.7)
        ax.plot([lx,lx],[0,0],[0,z],  'k--',linewidth=0.5,alpha=0.7)
        ax.plot([0,0],[0,0],[0,z],    'k--',linewidth=0.5,alpha=0.7)
        ax.plot([0,0],[ly,ly],[0,z],  'k--',linewidth=0.5,alpha=0.7)
        ax.plot([lx,lx],[ly,ly],[0,z],'k--',linewidth=0.5,alpha=0.7)
    
    for plot in np.arange(identif_inicial,identif_final,1):
        ax.plot_surface(armz_eq[f'x{plot}'][3],armz_eq[f'y{plot}'][3],armz_eq[f'z{plot}'][3],color='c',antialiased=True,shade=True,alpha=alpha) #cmap='Wistia'
        if pontos == True:
            ax.scatter(armz_eq[f'x{plot}'][8],armz_eq[f'y{plot}'][8],armz_eq[f'z{plot}'][8],s=200)
            for i in range(0,armz_eq[f'x{plot}'][6],1):
                for j in range(0,armz_eq[f'x{plot}'][7],1):
                    ax.text(armz_eq[f'x{plot}'][8][i][j],armz_eq[f'y{plot}'][8][i][j],armz_eq[f'z{plot}'][8][i][j],f' P{i}{j}',size=12.5)
    
    plt.show()    


def previa_intersecçao(identif_inicial,identif_final):
    
    """
    Uma *mini simulação de Epsi*. Para poucos nós em cada direção será checado se os limites são coerentes ou não, 
    ou seja, **se as funções convergiram para o determinado espaçamento de nós ou não**.
    
    Args:
        identif_inicial (:obj:`str`): Determine o início do intervalo de superfícies a serem calculadas através da identificação :obj:`identif`.
        identif_final (:obj:`str`): Determine o final do intervalo (endpoint não incluido) de superfícies a serem calcuadas através da identificação :obj:`identif`.
        
    Note:
        Como dito anteriormente, é recomendado fugir de superfícies mais complexas com graus (ou então numero de pontos em cada direção :obj:`[u,v]`) 
        elevados e/ou com muitas variações em mais de duas direções :obj:`xyz`. Para enfatizar esse argumento, podemos trazer alguns números: imagine uma 
        primeira superfície de 1ª ordem (2 pontos em cada direção) com variações constantes/lineares em todas direções (um quadrado ou retângulo). Agora, 
        como segunda superfície, imagine outra superfície de 1ª ordem com variações não-constantes/não-lineares em todas direções, uma superfície mais 
        alta de um lado do que de outro, ao mesmo tempo que é mais larga em um lado do que em outro e que esteja sendo 'torcida'. O cálculo de limites 
        da Epsi da primeira demora cerca de **25%** do tempo quando comparada à segunda superfície, mesmo ambas tendo o mesmo grau. No primeiro caso, 
        das 3 equações, apenas 2 dependerão de apenas 1 variável e a outra será uma constante. No segundo caso, todas as 3 equações dependem de 2 variáveis, 
        o que se torna bastante custoso.
        Porém, caso não seja possível fugir destas complicações, na hora de plotar sua superfície, chame esta função para verificar se os vetores de cada
        plano estão reconhecendo a sua superfície como deveriam.
    
    """
    
    identif_inicial=int(identif_inicial)
    identif_final=int(identif_final)
    
    fig = plt.figure(figsize=(9,9))
    ax = fig.add_subplot(1, 1, 1, projection='3d', proj_type='ortho')
    
    ax.set_xlabel('x'),ax.set_ylabel('y'),ax.set_zlabel('z'),ax.set_xlim(0,max([lx,ly,lz])),ax.set_ylim(0,max([lx,ly,lz])),ax.set_zlim(0,max([lx,ly,lz])),
    ax.view_init(25,-145),(),ax.set_title('Superfície/Intersecções',size=20)
    
    for plot in np.arange(identif_inicial,identif_final,1):
        ax.plot_surface(armz_eq[f'x{plot}'][3],armz_eq[f'y{plot}'][3],armz_eq[f'z{plot}'][3],color='c',antialiased=True,shade=True, alpha=0.4) #cmap='Wistia'
        
        for n1,n2,d1,d2,e1,e2,cor in [nz_visualizacao,ny_visualizacao,dz_visualizacao,dy_visualizacao,f'z{plot}',f'y{plot}','magenta'],[nx_visualizacao,ny_visualizacao,dx_visualizacao,dy_visualizacao,f'x{plot}',f'y{plot}','blue'],[nx_visualizacao,nz_visualizacao,dx_visualizacao,dz_visualizacao,f'x{plot}',f'z{plot}','aqua']:
            nobj=0
            for c1 in range(0,n1,1):
                for c2 in range(0,n2,1):
                    try:
                        sol = nonlinsolve([armz_eq[e1][1][0]-c1*d1,armz_eq[e2][1][0]-c2*d2],[u,v])
                        for a in range(0,len(sol.args)):
                            if sol.args[a][0].is_real == True:
                                if 0<=sol.args[a][0]<=1:
                                    if sol.args[a][1].is_real == True:
                                        if 0<=sol.args[a][1]<=1:
                                            nobj+=1
                                            ax.scatter(armz_eq[f'x{plot}'][2](float(sol.args[a][0]),float(sol.args[a][1])),
                                                       armz_eq[f'y{plot}'][2](float(sol.args[a][0]),float(sol.args[a][1])),
                                                       armz_eq[f'z{plot}'][2](float(sol.args[a][0]),float(sol.args[a][1])),s=100,color=cor)
                    except: 
                        pass

            for cx in range(0,nx_visualizacao,1):
                for cy in range(0,ny_visualizacao,1):
                    ax.plot((cx*dx_visualizacao,cx*dx_visualizacao),(cy*dy_visualizacao,cy*dy_visualizacao),(0,lz),color='blue',linestyle='--', linewidth=1.2)

            for cx in range(0,nx_visualizacao,1):
                for cz in range(0,nz_visualizacao,1):
                    ax.plot((cx*dx_visualizacao,cx*dx_visualizacao),(0,ly),(cz*dz_visualizacao,cz*dz_visualizacao),color='aqua',linestyle='--', linewidth=1.2)

            for cy in range(0,ny_visualizacao,1):
                for cz in range(0,nz_visualizacao,1):
                    ax.plot((0,lx),(cy*dy_visualizacao,cy*dy_visualizacao),(cz*dz_visualizacao,cz*dz_visualizacao),color='magenta',linestyle='--', linewidth=1.2)

            if nobj>0:
                print(f'Objeto #{plot}: plano {str(e1[0]+e2[0])} encontra {nobj} intersecçoes','\n')
            else:
                print(f'Objeto #{plot}: plano {str(e1[0]+e2[0])} não encontra intersecçoes ou não convergiu','\n')


def gen_epsi(tipo,plano,identif,simetria='global',raf0='normal'):
    
    """
    O ponto crítico do código.
    
    Aqui, usamos as equações geradas pelos pontos fornecidos pelo usuário para setar os limites de onde é sólido (na Epsi, :obj:`1`) e onde
    não é sólido (na Epsi, :obj:`0`). Vamos setar o que é considerado entrada e saída, ou ambos ao mesmo tempo, **para todas as superfícies criadas**. 
    Vamos, também, tornar mais barata o cálculo de nossa Epsi com simetrias. Vamos definir qual o melhor plano para calcular os limites.
    
    Warning:
        **Preste atenção. Se algo pode dar errado, é aqui.**
        
    Args:
        tipo (:obj:`str`): Defina se a superfície em questão é considerada uma entrada, uma saída ou ambos em relação ao sólido.
        
            +-------------------------+------------------------------------+
            | Tipo                    | Sete  :obj:`tipo` como             | 
            +=========================+====================================+
            | Entrada                 | :obj:`'entrada+saída e/ou entrada'`|
            +-------------------------+------------------------------------+
            | Saída                   | :obj:`'entrada+saída e/ou saída'`  |
            +-------------------------+------------------------------------+
            | Entrada/Saída Pura      | Tanto faz                          |
            +-------------------------+------------------------------------+
            | Entrada/Saída + Entrada | :obj:`'entrada+saída e/ou entrada'`|
            +-------------------------+------------------------------------+
            | Entrada/Saída + Saída   | :obj:`'entrada+saída e/ou saída'`  |  
            +-------------------------+------------------------------------+
        
    Note:
        Caso a superfície identificada com :obj:`identif` seja *entrada*, a partir do momento em que a Epsi encontrar a superfície até o fim da 
        Epsi será setado como 1. Caso seja *saída*, 
        a partir do momento em que a Epsi encontrar a superfície até o fim da Epsi será setado como 0. 
        
        *É necessário perceber que a ordem com que essa 
        função é chamada tem muita importância:* caso o usuário chame primeiro as saídas, o código vai entender que a partir do encontro da superfície 
        é necessário marcar como 0 algo que já está setado como 0 (a matriz Epsi é setada inicialmente apemas com 0, com dimensões nx, ny e nz). Seguindo a lógica, 
        o usuário agora então chamaria as entradas. A partir do encontro da superfície, tudo será setado com 1 até o fim da matriz e assim ficará definido. 
        Ou seja, o sólido *não foi representado corretamente.*
    
    Warning:
        Caso construída uma superfície que possua segmentos com possíveis entradas/saídas (um U ou um 0), certificar que a superfície seja construída 
        no sentido positivo: os pontos iniciais devem ser mais próximos da origem do que os pontos finais, independente do plano.

    Args: 
        plano (:obj:`str`): Escolha o melhor plano para resolver sua superfície. Caso o plano xy seja o melhor, setar :obj:`plano='xy'`. Pode assumir apenas :obj:`'xz','xy','zy'`.
        
    Note:
        **Mas, como assim 'plano'?**\
        Para cada combinação de coordenada (xy, xz ou zy), imagine um vetor saíndo de cada nó existente.
        Como por exemplo, falaremos do plano xy. De cada posição x e de cada posição y possível, sairá um vetor em direção à z.
        Toda vez que esse vetor cruzar uma superfície, será contabilizado um limite para a Epsi. O usuário já determinou que 
        tipo de limite será no argumento anterior.
        *Logo, é de extrema importância que o usuário escolha o plano certo para resolver o seu sólido.*
        Imagine outro exemplo, onde o usuário construiu um quadrado no plano xy (ou seja, paralelo ao plano xy), com alguma altura constante qualquer.
        Esse quadrado não possui dimensão alguma para qualquer plano a não ser o plano xy.
        Em outras palavras, o plano zy e o plano zx nunca cruzarão este quadrado, logo a Epsi não será construída corretamente pois não haverá limite algum para isso.
        E isso é perfeitamente demonstrado pela :obj:`previa_intersecçao`. Inclusive, o retorno desta função explicita onde há interceptação dos vetores com a superfície, 
        tornando mais clara a escolha deste argumento.
        
        **Dica:** normalmente o plano com mais intersecções na :obj:`previa_intersecçao` é o mais correto a ser escolhido.
    
    Args:
        identif(:obj:`str`): Repita o argumento :obj:`identif` da superfície em questão.
        simetria(:obj:`str`, optional): Defina alguma simetria de auxílio para barateamento do cálculo da Epsi. Pode assumir :obj:`'simetria_x','simetria_y',simetria_z'`.
        
    Warning:
        Caso utilize a simetria, projete apenas metade das superfícies caso elas cruzem o eixo de simetria. Caso contrário, o método não resulta em ganhos significativos. 

    Args:
       raf0(:obj:`str`, optional): Não há necessidade alguma de manipulação por parte do usuário. 
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
        
    for p,k in armz_eq.items():
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
    
    if plano == 'zy':
        eixo1, min_1, max_1, d1 = str(f'z{identif}'), math.ceil(armz_eq[f'z{identif}'][4]/dz_gen), int(armz_eq[f'z{identif}'][5]/dz_gen), dz_gen
        eixo2, min_2, max_2, d2 = str(f'y{identif}'), math.ceil(armz_eq[f'y{identif}'][4]/dy_gen), int(armz_eq[f'y{identif}'][5]/dy_gen), dy_gen
        eixo3, min_3, max_3, d3 = str(f'x{identif}'), math.ceil(armz_eq[f'x{identif}'][4]/dx_gen), max_x, dx_gen
        
    if plano == 'xz':
        eixo1, min_1, max_1, d1 = str(f'x{identif}'), math.ceil(armz_eq[f'x{identif}'][4]/dx_gen), int(armz_eq[f'x{identif}'][5]/dx_gen), dx_gen
        eixo2, min_2, max_2, d2 = str(f'z{identif}'), math.ceil(armz_eq[f'z{identif}'][4]/dz_gen), int(armz_eq[f'z{identif}'][5]/dz_gen), dz_gen
        eixo3, min_3, max_3, d3 = str(f'y{identif}'), math.ceil(armz_eq[f'y{identif}'][4]/dy_gen), max_y, dy_gen
        
    if plano == 'xy':
        eixo1, min_1, max_1, d1 = str(f'x{identif}'), math.ceil(armz_eq[f'x{identif}'][4]/dx_gen), int(armz_eq[f'x{identif}'][5]/dx_gen), dx_gen
        eixo2, min_2, max_2, d2 = str(f'y{identif}'), math.ceil(armz_eq[f'y{identif}'][4]/dy_gen), int(armz_eq[f'y{identif}'][5]/dy_gen), dy_gen
        eixo3, min_3, max_3, d3 = str(f'z{identif}'), math.ceil(armz_eq[f'z{identif}'][4]/dz_gen), max_z, dz_gen
        
    grau= max(armz_eq[f'z{identif}'][6],armz_eq[f'z{identif}'][7])
    
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
                lista_args=[]
                intersec = nonlinsolve([armz_eq[f'{eixo1}'][1][0]-c1*d1,armz_eq[f'{eixo2}'][1][0]-c2*d2],[u,v])
                for prmt in range(0,len(intersec.args)):
                    if intersec.args[prmt][0].is_real == True and 0<=round(intersec.args[prmt][0],5)<=1:
                        if intersec.args[prmt][1].is_real == True and 0<=round(intersec.args[prmt][1],5)<=1:
                            lista_args+=intersec.args[prmt]

                for c3 in range(min_3,max_3+1,1):
                    if tipo == 'entrada+saída e/ou saída':
                        if len(lista_args)==4:
                            if armz_eq[f'{eixo3}'][2](lista_args[0],lista_args[1])<=c3*d3<armz_eq[f'{eixo3}'][2](lista_args[2],lista_args[3]):
                                    if plano == 'zy':
                                        matrix_gen[c3][c2][c1] = 1
                                    if plano == 'xz':
                                        matrix_gen[c1][c3][c2] = 1
                                    if plano == 'xy':
                                        matrix_gen[c1][c2][c3] = 1
                        if len(lista_args)==2:
                            if c3*d3>armz_eq[f'{eixo3}'][2](lista_args[0],lista_args[1]):
                                if plano == 'zy':
                                    matrix_gen[c3][c2][c1] = 0
                                if plano == 'xz':
                                    matrix_gen[c1][c3][c2] = 0
                                if plano == 'xy':
                                    matrix_gen[c1][c2][c3] = 0

                    if tipo == 'entrada+saída e/ou entrada':
                        if len(lista_args)==4:
                            if armz_eq[f'{eixo3}'][2](lista_args[0],lista_args[1])<=c3*d3<armz_eq[f'{eixo3}'][2](lista_args[2],lista_args[3]):
                                    if plano == 'zy':
                                        matrix_gen[c3][c2][c1] = 1
                                    if plano == 'xz':
                                        matrix_gen[c1][c3][c2] = 1
                                    if plano == 'xy':
                                        matrix_gen[c1][c2][c3] = 1
                        if len(lista_args)==2:
                            if c3*d3>=armz_eq[f'{eixo3}'][2](lista_args[0],lista_args[1]):
                                if plano == 'zy':
                                    matrix_gen[c3][c2][c1] = 1
                                if plano == 'xz':
                                    matrix_gen[c1][c3][c2] = 1
                                if plano == 'xy':
                                    matrix_gen[c1][c2][c3] = 1

            except: 
                pass
            
    if simetria=='simetria_y':
        if (ny_gen%2!=0) == True: #impar
            lado_zerado=int(ny_gen/2)
            lado_calculado=int(ny_gen/2)
            for cy in range(int(ny_gen/2),ny_gen-1):
                lado_zerado+=1
                lado_calculado-=1
                matrix_gen[:,lado_zerado,:] = matrix_gen[:,lado_calculado,:]
                
        if (ny_gen%2!=0) == False: #par
            lado_zerado=int(ny_gen/2-1)
            lado_calculado=int(ny_gen/2)
            for cy in range(int(ny_gen/2)-1,ny_gen-1):
                lado_zerado+=1
                lado_calculado-=1
                matrix_gen[:,lado_zerado,:] = matrix_gen[:,lado_calculado,:]
            
    if simetria=='simetria_x':
        if (nx_gen%2!=0) == True:
            lado_zerado=int(nx_gen/2)
            lado_calculado=int(nx_gen/2)
            for cx in range(int(nx_gen/2),nx_gen-1):
                lado_zerado+=1
                lado_calculado-=1
                matrix_gen[lado_zerado,:,:] = matrix_gen[lado_calculado,:,:]

        if (nx_gen%2!=0) == False:
            lado_zerado=int(nx_gen/2-1)
            lado_calculado=int(nx_gen/2)
            for cx in range(int(nx_gen/2)-1,nx_gen-1):
                lado_zerado+=1
                lado_calculado-=1
                matrix_gen[lado_zerado,:,:] = matrix_gen[lado_calculado,:,:]
            
    if simetria=='simetria_z':
        if (nz_gen%2!=0) == True:
            lado_zerado=int(nz_gen/2)
            lado_calculado=int(nz_gen/2)
            for cz in range(int(nz_gen/2),nz_gen-1):
                lado_zerado+=1
                lado_calculado-=1
                matrix_gen[:,:,lado_zerado] = matrix_gen[:,:,lado_calculado]
                
        if (nz_gen%2!=0) == False:
            lado_zerado=int(nz_gen/2-1)
            lado_calculado=int(nz_gen/2)
            for cz in range(int(nz_gen/2)-1,nz_gen-1):
                lado_zerado+=1
                lado_calculado-=1
                matrix_gen[:,:,lado_zerado] = matrix_gen[:,:,lado_calculado]
    
    armz_nomenclt_epsi[f'{identif}'] = (tipo,plano,identif,simetria)
    
    bar.finish()
    

def gen_epsi_cylinder(bases_plane,tipo,plano,identif_inicial,simetria='global',raf0='normal'):
    
    """
    Uma função derivada de :obj:`gen_epsi()` que facilita a geração da Epsi de cilíndros criados com a função
    :obj:`gen_bezi_cylinder()`. 
    
    Args:
        bases_plane (:obj:`str`): Pode assumir :obj:`'xy','xz','zy'`. Deverá ser igual ao definido para o cilíndro em questão na função :obj:`gen_bezi_cylinder()`.
        tipo (:obj:`str`): Defina se a superfície em questão é considerada um :obj:`'contorno'` (imagine posicionar um cilíndro dentro de
            um cubo e subtraí-lo, como se fosse uma tubulação) ou um :obj:`'sólido'`(ideal para pneus, rodas, etc).
        plano (:obj:`str`): Escolha o melhor plano para resolver sua superfície. Pode assumir apenas :obj:`'xz','xy','zy'`. Mais informações em :obj:`gen_epsi()`.
        identif_inicial (:obj:`str`): O mesmo :obj:`identif` setado para o cilíndro em questão na função :obj:`gen_bezi_cylinder()`.
        simetria(:obj:`str`, optional): Pode assumir :obj:`'simetria_x','simetria_y',simetria_z'`. Mais informações em :obj:`gen_epsi()`.
        raf0(:obj:`str`, optional): Não há necessidade alguma de manipulação por parte do usuário. 
        

    """
    
    identif_inicial=int(identif_inicial)
    
    if tipo=='sólido':
        if bases_plane=='xz':
            if plano=='zy':
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}')    
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                
            if plano=='xy':
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}') 
            
        if bases_plane=='xy':
            if plano=='xz':
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}') 
            if plano=='zy':
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}')    
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                
        if bases_plane=='zy':
            if plano=='xz':
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}') 
            if plano=='xy':
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}')    
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                
        
    if tipo=='contorno':
        if bases_plane=='xz':
            if plano=='zy':
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}')    
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                
            if plano=='xy':
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}') 
            
        if bases_plane=='xy':
            if plano=='xz':
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}') 
            if plano=='zy':
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}')    
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                
        if bases_plane=='zy':
            if plano=='xz':
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}') 
            if plano=='xy':
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial}', simetria=f'{simetria}') 
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+1}', simetria=f'{simetria}')    
                gen_epsi('entrada+saída e/ou saída',f'{plano}',f'{identif_inicial+2}', simetria=f'{simetria}')
                gen_epsi('entrada+saída e/ou entrada',f'{plano}',f'{identif_inicial+3}', simetria=f'{simetria}')    
    

def plot_epsi(direcao, grid=True ,integral=False, raf1='normal'):
    
    """
    Confira se os limites estão corretos, camada por camada ou por amostragem, em qualquer direção.
    
    Args:
        direcao (:obj:`str`): Poderá assumir os seguintes valores: :obj:`'x', 'y', 'z'`.
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
            
    if direcao == 'z':
        n1,d1,l2,nome_l2,l3,nome_l3,d2,d3,plano,n2,n3 = nz_show,dz_show,lx,'lx',ly,'ly',dx_show,dy_show,'xy',nx_show,ny_show
    if direcao == 'x':
        n1,d1,l2,nome_l2,l3,nome_l3,d2,d3,plano,n2,n3 = nx_show,dx_show,ly,'ly',lz,'lz',dy_show,dz_show,'zy',ny_show,nz_show
    if direcao == 'y':
        n1,d1,l2,nome_l2,l3,nome_l3,d2,d3,plano,n2,n3 = ny_show,dy_show,lx,'lx',lz,'lz',dx_show,dz_show,'xz',nx_show,nz_show
    
    loop=np.arange(0,n1,1)
    
    if integral==False:
        loop=np.arange(int(n1/6),n1-int(n1/6),int(n1/6))
    
    for c1 in loop:
        fig_epsi, a2 = plt.subplots(figsize = (25/2,12/2))
        fig_epsi.suptitle(f'Plano {plano}, posição {direcao} = {round(c1*d1,1)}', fontsize=25)
        a2.set_xlabel(nome_l2, fontsize=15), a2.set_ylabel(nome_l3, fontsize=15)
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
        
        if direcao == 'z':
            epsi_dependente = matrix_show[:,:,c1].T
        if direcao == 'x':
            epsi_dependente = matrix_show[c1,:,:].T
        if direcao == 'y':
            epsi_dependente = matrix_show[:,c1,:].T
            
        a2.imshow(epsi_dependente, cmap = 'jet', origin='lower',extent=[-d2/2, l2+d2/2, -d3/2, l3+d3/2])
        plt.show()
        
        
        
def gen_output(names, raf2='normal'):
    
    """
    Geraração do arquivo que torna possível a visualização no ParaView da Epsi.
    
    Args:
        names (:obj:`str`): Entre com o nome que será dado aos arquivos gerado pelo programa.
        raf2 (:obj:`str`): Não há necessidade alguma de manipulação por parte do usuário. 
    
    """
    global contador
    
    
    if raf2=='normal':
        contador+=1
        if contador==1:
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
        
    name = ''.join((names,f'_(geracao_{contador})'))
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
    for p,k in armz_nomenclt_epsi.items():
        gen_epsi(k[0],k[1],k[2],k[3],raf0='x')

    gen_output(f'{nome}_x_raf',raf2='x')

    ny_raf = ny*nraf
    dy_raf = ly/(ny_raf-1)
    epsi_3d_y_raf = np.zeros((nx,ny_raf,nz),dtype=np.float32)
    for p,k in armz_nomenclt_epsi.items():
        gen_epsi(k[0],k[1],k[2],k[3],raf0='y')

    gen_output(f'{nome}_y_raf',raf2='y')

    nz_raf = nz*nraf
    dz_raf=lz/(nz_raf-1)
    epsi_3d_z_raf = np.zeros((nx,ny,nz_raf),dtype=np.float32)
    for p,k in armz_nomenclt_epsi.items():
        gen_epsi(k[0],k[1],k[2],k[3],raf0='z')

    gen_output(f'{nome}_z_raf',raf2='z')