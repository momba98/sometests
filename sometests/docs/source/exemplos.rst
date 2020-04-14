.. _exemplos:

Exemplos
*********
Para que seja possível rodar os exemplos demonstrados na página,
**copie as linhas de código e cole nos locais indicados no** ``Notebook``.

Caso queira apenas obter os arquivos necessários para visualização no
ParaView (arquivo .xdmf lido com a opção XMDF Reader) e simulação numérica através
do ``incompact3d`` (arquivos Epsi), **faça o download disponível**.

1. Cybertruck
====================

.. figure:: cyber.jpg
   :align: center

   *Versão 3D do polêmico carro americano recriada em Epsi;*

Faça o :download:`download dos arquivos  <downloads/cyber.zip>` ou
**copie e cole onde é explicitado no** ``Notebook``:

Demanda do dr. FS: :download:`projeto Cyber em apenas 2D <downloads/cyber_2d.zip>`.

   **1.1. Domínio** ::

        lx,ly,lz=10,3,3
        nx,ny,nz=int(10*20),int(3*20),int(3*20)


   **1.3.1. Geração de Pontos de Controle** ::

        prepara_matriz_pontos(2,2) #from prepara_matriz_pontos to gen_bezi: creating a surface
        armz_pt['P00']=[2.40,0.89,1.9]
        armz_pt['P01']=[2.40,1.5,1.9]
        armz_pt['P10']=[5.9,0.57,1.4]
        armz_pt['P11']=[5.9,1.5,1.4]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('0','traseira_alta')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[5.9,0.57,1.4]
        armz_pt['P01']=[5.9,1.5,1.4]
        armz_pt['P10']=[5.75,0.625,0.5]
        armz_pt['P11']=[5.75,1.5,0.5]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('1','traseira_media')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[5.75,0.625,0.5]
        armz_pt['P01']=[5.75,1.5,0.5]
        armz_pt['P10']=[5.25,0.625,0.34]
        armz_pt['P11']=[5.25,1.5,0.34]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('2','traseira_baixa')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[5.25,0.625,0.34]
        armz_pt['P01']=[5.25,1.5,0.34]
        armz_pt['P10']=[0.25,0.625,0.34]
        armz_pt['P11']=[0.25,1.5,0.34]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('3','assoalho')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[2.40,0.89,1.9]
        armz_pt['P01']=[2.40,1.5,1.9]
        armz_pt['P10']=[0.2,0.57,1.2]
        armz_pt['P11']=[0.2,1.5,1.2]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('4','frente_alta')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.2,0.57,1.2]
        armz_pt['P01']=[0.2,0.87,1.2]
        armz_pt['P10']=[0,0.87,1.1]
        armz_pt['P11']=[0,0.87,1.1]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('5','triang_sup_dir')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.2,0.87,1.2]
        armz_pt['P01']=[0,0.87,1.1]
        armz_pt['P10']=[0.2,1.5,1.2]
        armz_pt['P11']=[0,1.5,1.1]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('6','retan_sup_meio')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.25,0.625,0.34]
        armz_pt['P01']=[0.25,0.825,0.34]
        armz_pt['P10']=[0.125,0.825,0.5]
        armz_pt['P11']=[0.125,0.825,0.5]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('7','triang_inf_dir', True)

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.125,0.825,0.5]
        armz_pt['P01']=[0.25,0.825,0.34]
        armz_pt['P10']=[0.125,1.5,0.5]
        armz_pt['P11']=[0.25,1.5,0.34]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('8','retan_inf_meio')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.2,0.57,1.2]
        armz_pt['P01']=[0,0.87,1.1]
        armz_pt['P10']=[0.25,0.625,0.34]
        armz_pt['P11']=[0.125,0.825,0.5]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('9','frent_dir', True)

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0,0.87,1.1]
        armz_pt['P01']=[0,1.5,1.1]
        armz_pt['P10']=[0.125,0.825,0.5]
        armz_pt['P11']=[0.125,1.5,0.5]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('10','frent_meio')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[2.40,0.89,1.9]
        armz_pt['P01']=[0.2,0.57,1.2]
        armz_pt['P10']=[5.9,0.57,1.4]
        armz_pt['P11']=[5.9,0.57,1.4]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('11','lat_sup_dir')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.25,0.625,0.34]
        armz_pt['P01']=[0.2,0.57,1.2]
        armz_pt['P10']=[5.75,0.625,0.5]
        armz_pt['P11']=[5.9,0.57,1.4]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('12','lat_inf_dir')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.25,0.625,0.34]
        armz_pt['P01']=[0.25,0.625,0.34]
        armz_pt['P10']=[5.75,0.625,0.5]
        armz_pt['P11']=[5.25,0.625,0.34]
        cria_matriz_pontos()
        transladar('x',2)
        gen_bezi('13','lat_chao_dir')

        gen_bezi_cylinder('xz',0.5,4.81+2,0.5,0.625,1.025,'14')

        gen_bezi_cylinder('xz',0.5,0.885+2,0.5,0.625,1.025,'18')

   **1.3.3. Geração da Epsi** ::

        c.epsi_3d=np.zeros((c.nx,c.ny,c.nz),dtype=np.float32)

        gen_epsi_cylinder('xz','sólido','zy','18',simetria='simetria_y')
        gen_epsi_cylinder('xz','sólido','zy','14',simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','4', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','5', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','6', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','7', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','8', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','9', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','10', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','15', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','14', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída','zy','11', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída','zy','12', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída','zy','0', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída','zy','1', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída','zy','2', simetria='simetria_y')


2. Esfinge
================

.. figure:: esfinge.jpg
   :align: center

   *Versão 3D do monumento egípcio recriada em Epsi;*

Faça o :download:`download dos arquivos  <downloads/sphinx.zip>` ou
**copie e cole onde é explicitado no** ``Notebook``:

   **1.1. Domínio** ::

         lx,ly,lz=74,20,21.5
         nx,ny,nz=int(74*4),int(20*4),int(21.5*4)

   **1.3.1. Geração de Pontos de Controle** ::

         prepara_matriz_pontos(3,2)
         armz_pt['P00']=[3,0,0]
         armz_pt['P01']=[3,3.20,0]
         armz_pt['P10']=[4,0,2.8]
         armz_pt['P11']=[4,3.20,2.8]
         armz_pt['P20']=[5,0,3.20]
         armz_pt['P21']=[5,3.20,3.20]
         cria_matriz_pontos(True)
         transladar('y',0.5)
         gen_bezi('0','pata frente entrada')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[21.6,0,0]
         armz_pt['P01']=[25.6,3.20,0]
         armz_pt['P10']=[21.6,0,3.20]
         armz_pt['P11']=[30.6,3.20,3.20]
         cria_matriz_pontos()
         transladar('y',0.5)
         gen_bezi('1','cotovelo, saida')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[21.6,3.20,0]
         armz_pt['P01']=[21.6,9.5,0]
         armz_pt['P10']=[21.6,3.2,3.20]
         armz_pt['P11']=[21.6,9.5,3.20]
         cria_matriz_pontos()
         transladar('y',0.5)
         gen_bezi('2','peito, entrada')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[21.6,0,3.2]
         armz_pt['P01']=[21.6,9.5,3.2]
         armz_pt['P10']=[25.6,3.2,8.4]
         armz_pt['P11']=[25.6,9.5,8.4]
         cria_matriz_pontos()
         transladar('y',0.5)
         gen_bezi('3','peito_2, entrada')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[21.6,0,3.2]
         armz_pt['P01']=[30.6,3.20,3.2]
         armz_pt['P10']=[25.6,3.2,8.4]
         armz_pt['P11']=[30.6,3.2,8.4]
         cria_matriz_pontos()
         transladar('y',0.5)
         gen_bezi('4','pata frente saida')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[22.5,9.5,     12]
         armz_pt['P01']=[22.5,7,   12]
         armz_pt['P10']=[23.5,9.5,19]
         armz_pt['P11']=[23.5,7,19]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('5','rosto, entrada', True)

         prepara_matriz_pontos(2,3)
         armz_pt['P00']=[25.6,9.5,     8.4]
         armz_pt['P01']=[26.6,7,     8.4]
         armz_pt['P02']=[27.6,6,     8.4]
         armz_pt['P10']=[24.6,9.5,     12]
         armz_pt['P11']=[25.6,7,   12]
         armz_pt['P12']=[27.6,6,   12]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('6','pescoço, entrada')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[27.6,1,     12]
         armz_pt['P01']=[27.6,7,     12]
         armz_pt['P10']=[27.6,5.5,     20.5]
         armz_pt['P11']=[27.6,7,   20.5]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('7','lenço_entrada')

         prepara_matriz_pontos(3,2)
         armz_pt['P00']=[27.6,1,     12]
         armz_pt['P01']=[27.6,5.5,     20.5]
         armz_pt['P10']=[34,5.5,     12]
         armz_pt['P11']=[30,5.5,   20.5]
         armz_pt['P20']=[35,9.5,     12]
         armz_pt['P21']=[31,9.5,   20.5]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('8','lenço_saída')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[27.6,3.5,8.4]
         armz_pt['P01']=[27.6,6,   8.4]
         armz_pt['P10']=[27.6,1,     12]
         armz_pt['P11']=[27.6,6,     12]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('9','lenço_entrada_embaixo')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[27.6,3.2,8.4]
         armz_pt['P01']=[27.6,9.5,8.4]
         armz_pt['P10']=[65,3.2,8.4]
         armz_pt['P11']=[65,9.5,8.4]
         cria_matriz_pontos()
         transladar('y',0.5)
         gen_bezi('10','lombo')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[65,3.2,8.4]
         armz_pt['P01']=[65,9.5,8.4]
         armz_pt['P10']=[70,0,3.2]
         armz_pt['P11']=[70,9.5,3.2]
         cria_matriz_pontos()
         transladar('y',0.5)
         gen_bezi('11','atras_saida')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[70,0,3.2]
         armz_pt['P01']=[70,9.5,3.2]
         armz_pt['P10']=[70,0,0]
         armz_pt['P11']=[70,9.5,0]
         cria_matriz_pontos()
         transladar('y',0.5)
         gen_bezi('12','atras2_saida')

         prepara_matriz_pontos(3,2)
         armz_pt['P00']=[53,0,0]
         armz_pt['P01']=[53,3.20,0]
         armz_pt['P10']=[54,0,2.8]
         armz_pt['P11']=[54,3.20,2.8]
         armz_pt['P20']=[55,0,3.20]
         armz_pt['P21']=[55,3.20,3.20]
         cria_matriz_pontos(True)
         transladar('y',0.5)
         gen_bezi('13','pata atras entrada')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[60,0,3.2]
         armz_pt['P01']=[60,3.20,3.2]
         armz_pt['P10']=[65,3.2,8.4]
         armz_pt['P11']=[65,3.20,8.4]
         cria_matriz_pontos()
         transladar('y',0.5)
         gen_bezi('14','joelho entrada')

         prepara_matriz_pontos(3,2)
         armz_pt['P00']=[27.6,1,     12]
         armz_pt['P01']=[27.6,3.5,     8.4]
         armz_pt['P10']=[34,5.5,     12]
         armz_pt['P11']=[33,5.5,   8.4]
         armz_pt['P20']=[35,9.5,     12]
         armz_pt['P21']=[34,9.5,   8.4]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('15','lenço_saída_embaixo')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[23.5,9.5,     19]
         armz_pt['P01']=[23.5,7,   19]
         armz_pt['P10']=[26,9.5,20.5]
         armz_pt['P11']=[26,7,20.5]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('16','rosto2, entrada')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[22.5,7,     12]
         armz_pt['P01']=[25,5.5,   12]
         armz_pt['P10']=[23.5,7,19]
         armz_pt['P11']=[25,5.5,19]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('17','rosto3, entrada')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[23.5,7,     19]
         armz_pt['P01']=[25,5.5,   19]
         armz_pt['P10']=[26,7,20.5]
         armz_pt['P11']=[26,7,20.5]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('18','rosto4, entrada')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[22.5,9.5,     12]
         armz_pt['P01']=[22.5,8.5,   12]
         armz_pt['P10']=[22.5,9.5,8]
         armz_pt['P11']=[22.5,9,8]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('19','barbixa, entrada')

         prepara_matriz_pontos(2,2)
         armz_pt['P00']=[23.5,9.5,     12]
         armz_pt['P01']=[23.5,8.5,   12]
         armz_pt['P10']=[23,9.5,8]
         armz_pt['P11']=[23,9,8]
         cria_matriz_pontos(desvio=True)
         transladar('y',0.5)
         gen_bezi('20','barbixa, saida')

   **1.3.3. Geração da Epsi** ::

        c.epsi_3d=np.zeros((c.nx,c.ny,c.nz),dtype=np.float32)

        gen_epsi('entrada+saída e/ou entrada','zy','19', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída'  ,'zy','20', simetria='simetria_y')

        gen_epsi('entrada+saída e/ou entrada','zy','0' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','2' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','3' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','5' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','6' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','7' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','9' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','16', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','17', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','18', simetria='simetria_y')

        gen_epsi('entrada+saída e/ou saída'  ,'zy','1' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída'  ,'zy','4' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída'  ,'zy','8' , simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída'  ,'zy','15', simetria='simetria_y')

        gen_epsi('entrada+saída e/ou entrada','zy','13', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou entrada','zy','14', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída'  ,'zy','11', simetria='simetria_y')
        gen_epsi('entrada+saída e/ou saída'  ,'zy','12', simetria='simetria_y')


3. McQueen
==========
.. figure:: marquinhos.jpg
   :width: 400px
   :align: center

   *Versão 2D do famoso Relâmpago McQueen recriada em Epsi;*

Faça o :download:`download dos arquivos  <downloads/mcqueen.zip>` ou
**copie e cole onde é explicitado no** ``Notebook``:

   **1.1. Domínio** ::

        lx,ly,lz=5,2,1
        nx,ny,nz=int(5*85),int(2*85),int(3)


   **1.3.1. Geração de Pontos de Controle** ::

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.5,0.1,0]
        armz_pt['P01']=[0.5,0.1,1]
        armz_pt['P10']=[0.25,0.16,0]
        armz_pt['P11']=[0.25,0.16,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('0','cd,entrada')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.25,0.16,0]
        armz_pt['P01']=[0.25,0.16,1]
        armz_pt['P10']=[0.13,0.46,0]
        armz_pt['P11']=[0.13,0.46,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('1','de,entrada')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[0.13,0.46,0]
        armz_pt['P01']=[0.13,0.46,1]
        armz_pt['P10']=[0.16,0.69,0]
        armz_pt['P11']=[0.16,0.69,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('2','ef,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[0.16,0.69,0]
        armz_pt['P01']=[0.16,0.69,1]
        armz_pt['P10']=[0.34,0.85,0]
        armz_pt['P11']=[0.34,0.85,1]
        armz_pt['P20']=[1.06,1.10,0]
        armz_pt['P21']=[1.06,1.10,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('3','fk1g,entrada')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[1.88,1.10,0]
        armz_pt['P01']=[1.88,1.10,1]
        armz_pt['P10']=[2.21,1.52,0]
        armz_pt['P11']=[2.21,1.52,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('4','hi,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[2.21,1.52,0]
        armz_pt['P01']=[2.21,1.52,1]
        armz_pt['P10']=[2.63,1.58,0]
        armz_pt['P11']=[2.63,1.58,1]
        armz_pt['P20']=[4.12,1.3,0]
        armz_pt['P21']=[4.12,1.3,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('5','ijk,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[4.76,1.28,0]
        armz_pt['P01']=[4.76,1.28,1]
        armz_pt['P10']=[4.87,1.55,0]
        armz_pt['P11']=[4.87,1.55,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('6','lm,entrada')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[4.87,1.55,0]
        armz_pt['P01']=[4.87,1.55,1]
        armz_pt['P10']=[4.97,1.51,0]
        armz_pt['P11']=[4.97,1.51,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('7','mn,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[4.97,1.51,0]
        armz_pt['P01']=[4.97,1.51,1]
        armz_pt['P10']=[4.73,0.87,0]
        armz_pt['P11']=[4.73,0.87,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('8','no,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[4.73,0.87,0]
        armz_pt['P01']=[4.73,0.87,1]
        armz_pt['P10']=[4.81,0.78,0]
        armz_pt['P11']=[4.81,0.78,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('9','op,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[4.81,0.78,0]
        armz_pt['P01']=[4.81,0.78,1]
        armz_pt['P10']=[4.79,0.63,0]
        armz_pt['P11']=[4.79,0.63,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('10','pq,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[4.79,0.63,0]
        armz_pt['P01']=[4.79,0.63,1]
        armz_pt['P10']=[4.58,0.49,0]
        armz_pt['P11']=[4.58,0.49,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('11','qr,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[4.58,0.49,0]
        armz_pt['P01']=[4.58,0.49,1]
        armz_pt['P10']=[4.58,0.38,0]
        armz_pt['P11']=[4.58,0.38,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('12','rs,saida')

        R = 0.54
        cos=math.cos(math.radians(45))
        sin=math.sin(math.radians(45))

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[3.78+R,0.38,0]
        armz_pt['P01']=[3.78+R,0.38,1]
        armz_pt['P10']=[3.78+R,0.46,0]
        armz_pt['P11']=[3.78+R,0.46,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('13','tu,entrada')


        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78+R,0.46,0]
        armz_pt['P01']=[3.78+R,0.46,1]
        armz_pt['P10']=[3.78+R*cos,0.46+R*sin,0]
        armz_pt['P11']=[3.78+R*cos,0.46+R*sin,1]
        armz_pt['P20']=[3.78,0.46+R,0]
        armz_pt['P21']=[3.78,0.46+R,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('14','uvw,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78,0.46+R,0]
        armz_pt['P01']=[3.78,0.46+R,1]
        armz_pt['P10']=[3.78-R*cos,0.46+R*sin,0]
        armz_pt['P11']=[3.78-R*cos,0.46+R*sin,1]
        armz_pt['P20']=[3.78-R,0.46,0]
        armz_pt['P21']=[3.78-R,0.46,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('15','wza1,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[3.78-R,0.46,0]
        armz_pt['P01']=[3.78-R,0.46,1]
        armz_pt['P10']=[3.78-R,0.3,0]
        armz_pt['P11']=[3.78-R,0.3,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('16','a1k1,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[3.78-R,0.3,0]
        armz_pt['P01']=[3.78-R,0.3,1]
        armz_pt['P10']=[2.62,0.15,0]
        armz_pt['P11']=[2.62,0.15,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('17','k1l1,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[1.15+R,0.15,0]
        armz_pt['P01']=[1.15+R,0.15,1]
        armz_pt['P10']=[1.15+R,0.46,0]
        armz_pt['P11']=[1.15+R,0.46,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('18','b1c1,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[1.15+R,0.46,0]
        armz_pt['P01']=[1.15+R,0.46,1]
        armz_pt['P10']=[1.15+R*cos,0.46+R*sin,0]
        armz_pt['P11']=[1.15+R*cos,0.46+R*sin,1]
        armz_pt['P20']=[1.15,0.46+R,0]
        armz_pt['P21']=[1.15,0.46+R,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('19','c1d1e1,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[1.15,0.46+R,0]
        armz_pt['P01']=[1.15,0.46+R,1]
        armz_pt['P10']=[1.15-R*cos,0.46+R*sin,0]
        armz_pt['P11']=[1.15-R*cos,0.46+R*sin,1]
        armz_pt['P20']=[1.15-R,0.46,0]
        armz_pt['P21']=[1.15*R,0.46,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('20','e1f1g1,saida')

        prepara_matriz_pontos(2,2)
        armz_pt['P00']=[1.15-R,0.46,0]
        armz_pt['P01']=[1.15-R,0.46,1]
        armz_pt['P10']=[1.15-R,0.22,0]
        armz_pt['P11']=[1.15-R,0.22,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('21','g1h1,saida')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[1.15-R,0.22,0]
        armz_pt['P01']=[1.15-R,0.22,1]
        armz_pt['P10']=[0.58,0.11,0]
        armz_pt['P11']=[0.58,0.11,1]
        armz_pt['P20']=[0.5,0.1,0]
        armz_pt['P21']=[0.5,0.1,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('22','h1l1c,saida')

        R=3.78-3.31

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78-R,0.46,0]
        armz_pt['P01']=[3.78-R,0.46,1]
        armz_pt['P10']=[3.78-R*cos,0.46+R*sin,0]
        armz_pt['P11']=[3.78-R*cos,0.46+R*sin,1]
        armz_pt['P20']=[3.78,0.46+R,0]
        armz_pt['P21']=[3.78,0.46+R,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('23','rs,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78,0.46+R,0]
        armz_pt['P01']=[3.78,0.46+R,1]
        armz_pt['P10']=[3.78+R*cos,0.46+R*sin,0]
        armz_pt['P11']=[3.78+R*cos,0.46+R*sin,1]
        armz_pt['P20']=[3.78+R,0.46,0]
        armz_pt['P21']=[3.78+R,0.46,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('24','rs,saida')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78-R,0.46,0]
        armz_pt['P01']=[3.78-R,0.46,1]
        armz_pt['P10']=[3.78-R*cos,0.46-R*sin,0]
        armz_pt['P11']=[3.78-R*cos,0.46-R*sin,1]
        armz_pt['P20']=[3.78,0.46-R,0]
        armz_pt['P21']=[3.78,0.46-R,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('25','ri,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78,0.46-R,0]
        armz_pt['P01']=[3.78,0.46-R,1]
        armz_pt['P10']=[3.78+R*cos,0.46-R*sin,0]
        armz_pt['P11']=[3.78+R*cos,0.46-R*sin,1]
        armz_pt['P20']=[3.78+R,0.46,0]
        armz_pt['P21']=[3.78+R,0.46,1]
        cria_matriz_pontos(desvio=True)
        gen_bezi('26','ri,saida')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78-R,0.46,0]
        armz_pt['P01']=[3.78-R,0.46,1]
        armz_pt['P10']=[3.78-R*cos,0.46+R*sin,0]
        armz_pt['P11']=[3.78-R*cos,0.46+R*sin,1]
        armz_pt['P20']=[3.78,0.46+R,0]
        armz_pt['P21']=[3.78,0.46+R,1]
        cria_matriz_pontos(desvio=True)
        transladar('x',-2.63)
        gen_bezi('27','rs,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78,0.46+R,0]
        armz_pt['P01']=[3.78,0.46+R,1]
        armz_pt['P10']=[3.78+R*cos,0.46+R*sin,0]
        armz_pt['P11']=[3.78+R*cos,0.46+R*sin,1]
        armz_pt['P20']=[3.78+R,0.46,0]
        armz_pt['P21']=[3.78+R,0.46,1]
        cria_matriz_pontos(desvio=True)
        transladar('x',-2.63)
        gen_bezi('28','rs,saida')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78-R,0.46,0]
        armz_pt['P01']=[3.78-R,0.46,1]
        armz_pt['P10']=[3.78-R*cos,0.46-R*sin,0]
        armz_pt['P11']=[3.78-R*cos,0.46-R*sin,1]
        armz_pt['P20']=[3.78,0.46-R,0]
        armz_pt['P21']=[3.78,0.46-R,1]
        cria_matriz_pontos(desvio=True)
        transladar('x',-2.63)
        gen_bezi('29','ri,entrada')

        prepara_matriz_pontos(3,2)
        armz_pt['P00']=[3.78,0.46-R,0]
        armz_pt['P01']=[3.78,0.46-R,1]
        armz_pt['P10']=[3.78+R*cos,0.46-R*sin,0]
        armz_pt['P11']=[3.78+R*cos,0.46-R*sin,1]
        armz_pt['P20']=[3.78+R,0.46,0]
        armz_pt['P21']=[3.78+R,0.46,1]
        cria_matriz_pontos(desvio=True)
        transladar('x',-2.63)
        gen_bezi('30','ri,saida')


   **1.3.3. Geração da Epsi** ::

        c.epsi_3d=np.zeros((c.nx,c.ny,c.nz),dtype=np.float32)

        gen_epsi('entrada+saída e/ou entrada','zy','0')
        gen_epsi('entrada+saída e/ou entrada','zy','1')
        gen_epsi('entrada+saída e/ou entrada','zy','2')
        gen_epsi('entrada+saída e/ou entrada','zy','3')
        gen_epsi('entrada+saída e/ou saída','zy','20')
        gen_epsi('entrada+saída e/ou saída','zy','21')
        gen_epsi('entrada+saída e/ou saída','zy','22')
        gen_epsi('entrada+saída e/ou entrada','zy','27')
        gen_epsi('entrada+saída e/ou entrada','zy','29')
        gen_epsi('entrada+saída e/ou saída','zy','28')
        gen_epsi('entrada+saída e/ou saída','zy','30')
        gen_epsi('entrada+saída e/ou entrada','zy','19')
        gen_epsi('entrada+saída e/ou entrada','zy','18')
        gen_epsi('entrada+saída e/ou entrada','zy','4')
        gen_epsi('entrada+saída e/ou saída','zy','5')
        gen_epsi('entrada+saída e/ou entrada','zy','6')
        gen_epsi('entrada+saída e/ou saída','zy','7')
        gen_epsi('entrada+saída e/ou saída','zy','17')
        gen_epsi('entrada+saída e/ou saída','zy','16')
        gen_epsi('entrada+saída e/ou saída','zy','15')
        gen_epsi('entrada+saída e/ou entrada','zy','23')
        gen_epsi('entrada+saída e/ou entrada','zy','25')
        gen_epsi('entrada+saída e/ou saída','zy','24')
        gen_epsi('entrada+saída e/ou saída','zy','26')
        gen_epsi('entrada+saída e/ou entrada','zy','14')
        gen_epsi('entrada+saída e/ou entrada','zy','13')
        gen_epsi('entrada+saída e/ou saída','zy','8')
        gen_epsi('entrada+saída e/ou saída','zy','9')
        gen_epsi('entrada+saída e/ou saída','zy','10')
        gen_epsi('entrada+saída e/ou saída','zy','12')
        gen_epsi('entrada+saída e/ou saída','zy','11')
