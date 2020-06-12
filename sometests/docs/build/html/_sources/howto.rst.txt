.. _howto:

How To
*******

Ideal para os iniciantes, essa página é um **tutorial** e apresenta o código e todas as suas
funcionalidades, funções e particularidades. Para definições mais específicas
sobre as funções, acessar a pagina :ref:`docstring`.

1. Primeiros Passos
====================

Nada de construção de sólidos. Por agora, apenas setagem de parâmetros do domínio e
criação de arquivos auxiliares. A ordem da criação das células importa.
**O usuário deve usar as mesmas variáveis descritas nos blocos de código para que
o código funcione corretamente.**

**Caso o usuário tenha o desejo de alterar o domínio, seu nome ou seu parâmetro de refinamento,
a kernel do Jupyter deverá ser reiniciada.**

1.1 Domínio
++++++++++++

Inicialmente, o usuário deverá definir os parâmetros para seu domínio, determinando
o comprimento nas 3 direções :math:`{lx}`, :math:`{ly}` e :math:`{lz}`, bem como o número de nós de malha
:math:`{nx}`, :math:`{ny}` e :math:`{nz}`.

.. code-block:: python
   :linenos:

   lx,ly,lz=4,2,3 #valores arbitrados

   #no incompact3d, x representa comprimento, z representa largura e y representa altura.

   nx,ny,nz=81,41,61 #valores também arbitrados

Dessa forma, o espaçamento entre nós pode ser calculado:

.. code-block:: python
   :linenos:

   dx,dy,dz=lx/(nx-1),ly/(ny-1),lz/(nz-1)

1.2 Nomeação
+++++++++++++

Um nome deve ser dado ao projeto em início. Quando acabado, uma pasta com esse
mesmo nome será criada no ambiente onde o código está rodando.

.. code-block:: python
   :linenos:

   name=str(input('Give your project a name: '))

   #ou

   name='nome_do_projeto' #dessa forma, o risco de sobrescrever projetos é grande


1.3 Arquivos Auxiliares e Bibliotecas
++++++++++++++++++++++++++++++++++++++

O usuário não precisa fazer nada além de rodar a célula para criação dos arquivos
auxiliares:

.. code-block:: python
   :linenos:

   open(f'inputs.py', 'w').close()
   with open(f'inputs.py', 'a') as the_file:
       the_file.write(f'lx={lx}\n'), the_file.write(f'ly={ly}\n'), the_file.write(f'lz={lz}\n')
       the_file.write(f'nx={nx}\n'), the_file.write(f'ny={ny}\n'), the_file.write(f'nz={nz}\n')
       the_file.write(f'dx={dx}\n'), the_file.write(f'dy={dy}\n'), the_file.write(f'dz={dz}\n')
       the_file.write('name='),the_file.write(f'"'), the_file.write(f'{name}'), the_file.write(f'"')

O mesmo para bibliotecas:

.. code-block:: python
   :linenos:

   from infos import *
   from inputs import *
   from creating_solid import *
   import inputs as i
   import infos as s
   import creating_solid as c #guarde essa denominação

1.4 Parâmetro de Refinamento de Malha
++++++++++++++++++++++++++++++++++++++

Por fim, setar o parâmetro de refinamento de malha, o ``nraf``. O ``incompact3d``
precisa desse refinamento para entender melhor onde é sólido e onde não é. ``nraf``
multiplica :math:`{nx}`, :math:`{ny}` e :math:`{nz}` um de cada vez.

A matriz onde todas as informaçõe geradas pelo ``geo_bezier_3d`` são armazenadas
é denominada de :math:`{\epsilon}` (pronunciada como Epsi). Essa matriz é binária e representa
um plano cartesiano tridimensional.

Nela, **onde existe sólido o índice é setado como 1 e onde o fluido escoa livremente
é setado como 0.** Essa é a metodologia do ``geo_bezier_3d`` para representar
sólidos que interceptam um escoamento.

No final do projeto, serão geradas 4 :math:`{\epsilon}` por conta do refinamento de malha:

#. :math:`{\epsilon}` com dimensões :math:`{nx}` x :math:`{ny}` x :math:`{nz}`
#. :math:`{\epsilon_x}` com dimensões :math:`{nx_{raf}}` x :math:`{ny}` x :math:`{nz}`
#. :math:`{\epsilon_y}` com dimensões :math:`{nx}` x :math:`{ny_{raf}}` x :math:`{nz}`
#. :math:`{\epsilon_z}` com dimensões :math:`{nx}` x :math:`{ny}` x :math:`{nz_{raf}}`

O subíndice em :math:`{\epsilon}` indica a direção do refinamento de malha, enquanto
o subíndice :math:`{raf}` indica a multiplicação do número de nós por ``nraf``.

.. code-block:: python
   :linenos:

   gen_raf_information(nraf=algum_valor) #nraf pode assumir qualquer valor inteiro maior que 1.

.. _features:

2. Features
============

Partindo para a parte interessante do código, nessa seção serão explanadas todas as
funções que auxiliam na criação de sólidos, superfícies e partes.

Algumas funções usam superfícies possuem aplicação ampla: usam curvas/superfícies de Bézier (relativamente lentas).
Outras usam a abordagem de *fancy indexing* do Python, tendo aplicação restrita mas compensando com rapidez.

.. Warning::

   A troca de informações entre as funções existentes no código se dá através do
   argumento comum ``identif``. **Esse argumento está presente em todas as funções a partir
   deste ponto e merece atenção especial para evitar sobrescrtitos.**

2.0 Limpando a Memória
+++++++++++++++++++++++

Antes de tudo e para evitar possíveis confusões, é ideal zerar todos os parâmetros
que envolvem a criação de sólidos:

.. code-block:: python
   :linenos:

   #limpando os dicionários auxiliares

   #o c é a invocação do módulo creating_solid

   c.eq_storage={}

   c.list_storage={}

   c.solid_storage={}

   #limpar as matrizes que representam o sólido

   c.epsi_3d=np.zeros((c.nx,c.ny,c.nz),dtype=np.float32)

   c.epsi_3d_x_raf=np.zeros((c.nx_raf,c.ny,c.nz),dtype=np.float32)

   c.epsi_3d_y_raf=np.zeros((c.nx,c.ny_raf,c.nz),dtype=np.float32)

   c.epsi_3d_z_raf=np.zeros((c.nx,c.ny,c.nz_raf),dtype=np.float32)

Caso o usuário tenha errado algum parâmetro, pode chamar essas linhas de
código para resetar os parâmetros do script.


2.1 Superfície de Bézier
++++++++++++++++++++++++++

.. Note::

   Na documentação, há uma área especial para as superfícies/curvas de Bézier:
   :ref:`bezier`. Caso o usuário tenha dúvidas de como funcionam, é melhor dar
   uma pausa nesta página e voltar após breve entendimento.

As superfícies de Bézier são o trunfo do ``geo_bezier_3d``. Permitem criar
superfícies complexas que são dificilmente representadas por equações bem conhecidas.
Pórem, o usuário deve ter cuidado. Muita complexidade pode complicar o solver do script
e a superfície pode ser representada de modo falho.

Para criar uma superfície de Bézier com 3 pontos na direção de :math:`{u}` e 2 na direção de :math:`{v}`:

.. code-block:: python
   :linenos:

   set_point_matrix(num_u_points=3,num_v_points=2) #prepara a matriz dos pontos a serem recebidos

   point_storage['P00']=[0,0,1.0] #setar os pontos como lista, [x,y,z]
   point_storage['P01']=[0,0,2.0]

   point_storage['P10']=[2,2,1.0]
   point_storage['P11']=[2,2,2.0]

   point_storage['P20']=[3,1,1.0]
   point_storage['P21']=[3,1,2.0]

   create_point_matrix() #definição final da matriz dos pontos

   gen_bezier_surface(identif='0',name='superficie_3u_2v') #calculo matricial de Bézier

**Sempre que o usuário for criar uma superfície de Bézier, esse processo será repetido.**

Essa superfície, denominada de *superficie_3u_2v*, recebeu a identificação única
correspondente ao valor de 0, como demonstra o primeiro argumento de ``gen_bezier_surface()``,
na linha 14.

Para visualizar a superfície criada, o usuário deve executar a seguinte célula:

.. code-block:: python
   :linenos:

   surface_plot(init_identif='0',final_identif='1',points=True,alpha=0.4)

   #informar à função qual superfície é desejada no plot. No caso, '0'.

E obterá o plot:

.. figure:: images/bezier_surf1.png
   :height: 450px
   :align: center

   A visualização da superfície auxilia no entendimento do papel dos pontos governantes.

Para continuar com o exemplo, mais uma superfície será criada. Dessa vez, serão 2 pontos
na direção de :math:`{u}` e 3 pontos na direção de :math:`{v}`:

.. code-block:: python
   :linenos:

   set_point_matrix(num_u_points=2,num_v_points=3) #prepara a matriz dos pontos a serem recebidos

   point_storage['P00']=[3,1,1.0] #setar os pontos como lista, [x,y,z]
   point_storage['P01']=[2,1,1.5]
   point_storage['P02']=[3,1,2.0]

   point_storage['P10']=[3,0,1.0]
   point_storage['P11']=[2,0,1.5]
   point_storage['P12']=[3,0,2.0]

   #repare na diferença de denominação entre os pontos das duas superfícies

   create_point_matrix() #definição final da matriz dos pontos

   gen_bezier_surface(identif='1',name='superficie_2u_3v') #calculo matricial de Bézier

O plot de ambas superfícies é obtido da mesma forma, apenas mudando o argumento de identificação:

.. code-block:: python
   :linenos:

   surface_plot(init_identif='0',final_identif='2',points=True,alpha=0.4)

   #informar à função quais superfícies são desejadas no plot. No caso, '0' e '1'.

.. figure:: images/bezier_surf2.png
   :height: 450px
   :align: center

   Mais uma superfície foi adicionada ao plot.

A validação dessas superfícies como limites na matriz :math:`{\epsilon}` deverá ser feita com uma função
a parte, chamada de ``gen_epsi_bezier_surface()``. Nessa função, será determinada se a superfície é
considerada uma entrada do sólido ou uma saída, bem como qual o melhor plano para validar tal informação.

Inicialmente só sera validada no domínio a *superficie_3u_2v*:

.. code-block:: python
   :linenos:

   gen_epsi_bezier_surface(surface_type='entry+exit and/or entry',plane='zy',identif='0')

Os argumentos podem parecer confusos inicialmente. Por conta disso, explicaremos cada um
separadamente (há também bastante informação em :ref:`docstring`):

O argumento ``surface_type`` indica que tipo de limite a superfície em questão é. Pode assumir
apenas 2 valores, ``'entry+exit and/or entry'`` ou ``'entry+exit and/or exit'``. Assumindo
o primeiro deles, todos os índices da :math:`{\epsilon}` que estiverem **depois** da superfície (partindo de um plano específico)
serão considerados sólidos, ou seja, serão setados como 1. É isso o que a parte
"entry" quer dizer. A lógica se aplica também ao segundo valor possível, porém ao invés dos índices
serem setados como 1, serão setados como 0, o que explica a parte "exit". Caso a superfície em
questão seja entrada e saída ao mesmo tempo, o usuário não deve se preocupar: o código está pronto
para entender tal problema e é isso o que a parte "entry+exit" significa.

Já o argumento ``plane`` indica qual sentido essa varredura feita por ``surface_type``
será feita. Só pode assumir ``xy``, ``xz`` ou ``zy``. O usuário só poderá resolver
as superfícies nos planos quais a superfície tem alguma dimensão. No caso deste exemplo,
a superfície indicada com 0, *superficie_3u_2v*, não tem dimensão alguma no plano :math:`{xy}`,
enquanto a superfície indicada com 1 não tem dimensão alguma no plano :math:`{xz}`.

Portanto, para o exemplo, tudo o que estiver depois da superfície (ou entre seus limites) tomando
como referência o plano de origem :math:`{zy}` será setado como 1.

Continunando com o exemplo e gerando os arquivos de saída:

.. code-block:: python
   :linenos:

   gen_output(names=name) #essa é a função que gera os arquivos de saída.

E visualizando no software `ParaView <https://www.paraview.org/>`_ (exemplos de como visualizar
a :math:`{\epsilon}` no software ao longo desta página):

.. figure:: images/bezier_surf_paraview_1.png
   :align: center

   Como esperado, temos um sólido representado pela superfície construída.

Adicionando a outra superfície na matriz e gerando seu output:

.. code-block:: python
   :linenos:

   #validando limites

   gen_epsi_bezier_surface(surface_type='entry+exit and/or exit',plane='zy',identif='1')

   #gerando arquivos de saída

   gen_output(names=name)

O usuário deve observar que essa superfície vai ser resolvida exatamente da mesma forma
que a primeira, exceto pelo fato de que **será considerada uma saída do sólido.**

Pode-se então visualizar o trabalho feito no `ParaView <https://www.paraview.org/>`_:

.. figure:: images/bezier_surf_paraview_2.png
   :align: center

Para gerar essa visualização:

#. Abrir dentro do ParaView o arquivo .xdmf presente na pasta do projeto;
#. Open data with... **XDMF reader**;
#. Apply;
#. Mudar o tipo de visualização de Outline para Volume.

Pronto. O sólido delimitado pelas 2 superfícies criadas foi representado. O usuário
consegue perceber a infinidade de opções que as superfícies de Bézier proporcionam
para a criação de sólidos.

Como mencionado no início da seção, superfícies muito complexas podem ser um problema
para o solver da função. Caso o usuário não tenha escapatória, é recomendado dividir
essa grande superície complexa em várias pequenas, ou usar uma das funções
que serão apresentadas nas próximas seções.

2.1.1 Transladar
-----------------

Para transladar uma superfície de Bézier, basta adicionar um comando **entre as funções**
``create_point_matrix()`` e ``gen_bezier_surface()``:

.. code-block:: python
   :linenos:

   set_point_matrix(3,2)

   point_storage['P00']=[0,0,1.0]
   point_storage['P01']=[0,0,2.0]

   point_storage['P10']=[2,2,1.0]
   point_storage['P11']=[2,2,2.0]

   point_storage['P20']=[3,1,1.0]
   point_storage['P21']=[3,1,2.0]

   create_point_matrix()

   translate('x',0.5) #fora dessa linha, a função não terá funcionalidade.

   gen_bezier_surface(identif='0',name='superficie_3u_3v')

2.1.2 Rotacionar
-----------------

Para rotacionar uma superfície de Bézier, basta adicionar um comando **entre as funções**
``create_point_matrix()`` e ``gen_bezier_surface()``:

.. code-block:: python
   :linenos:

   set_point_matrix(3,2)

   point_storage['P00']=[0,0,1.0]
   point_storage['P01']=[0,0,2.0]

   point_storage['P10']=[2,2,1.0]
   point_storage['P11']=[2,2,2.0]

   point_storage['P20']=[3,1,1.0]
   point_storage['P21']=[3,1,2.0]

   create_point_matrix()

   rotate(plane='zy',origin=[1.5,1.5],angle=45) #o solver sofre um pouco com essa função, usar com cuidado

   gen_bezier_surface(identif='0',name='superficie_3u_3v')

2.1.2 Deflexão
---------------

Provavelmente o usuário já entende um pouco sobre curvas/superfícies de Bézier e
já sabe que **os pontos intermediários só servem para ditar a curvatura da
superfície/curva**, ou seja, a superfície/curva só realmente "enconsta" nos pontos
iniciais e finais.

Porém, há um jeito de burlar isso, num caso específico. Caso uma das direções :math:`{u}`
ou :math:`{u}` tenham 3 pontos (somente uma delas), o usuário pode setar como ``True`` o único
argumento da função ``create_point_matrix``:

.. code-block:: python
   :linenos:

   set_point_matrix(3,2)

   point_storage['P00']=[0,0,1.0]
   point_storage['P01']=[0,0,2.0]

   point_storage['P10']=[2,2,1.0]
   point_storage['P11']=[2,2,2.0]

   point_storage['P20']=[3,1,1.0]
   point_storage['P21']=[3,1,2.0]

   create_point_matrix(deflection=True) #aqui onde a deflexão é ativada

   gen_bezier_surface(identif='0',name='superficie_3u_3v')

A diferença entre usar ou não a deflexão:

.. figure:: images/bezier_surf_deflection.png
   :align: center

   À esquerda a superfície com a deflexão ligada, à direta com a deflexão desligada.

.. Note::

   Deflexão também está presente nas outras funções que usam a abordagem de Bézier:
   revolve e extrude.

2.2 Extrude
++++++++++++

.. Note::

   Na documentação, há uma área especial para as superfícies/curvas de Bézier:
   :ref:`bezier`. Caso o usuário tenha dúvidas de como funcionam, é melhor dar
   uma pausa nesta página e voltar após breve entendimento.

Para criar um extrude, primeiro é necessário setar os pontos governantes
de seu perfil, construído com curvas de Bézier. **Esse processo se repetirá
toda vez que o usuário queira criar um extrude.**

A setagem é feita através de um dicionário (ver também :ref:`docstring`):

.. code-block:: python
   :linenos:

   #setagem dos parâmetros de duas curvas com 4 pontos governantes cada:

   c.extrude_information={'1':['entry+exit and/or exit' ,'v',[[2.5,1],[1,1.75],[0.5,1.5],[1.5,1]]],
                          '0':['entry+exit and/or entry','v',[[2.5,1],[1,0.25],[0.5,0.5],[1.5,1]]]}

   #a identificação dentro do dicionário é independente da identificação das features!

   #criados os pontos e as informações sobre as curvas, cria-se de fato a feature:

   gen_extrude_profile(identif='1',name='primeiro_extrude',
                       direction='x',init_height=0,final_height=3)

Neste caso, está sendo construído um perfil para o extrude com 2 curvas, identificadas
como 0 e 1. Nenhuma identificação no dicionário deve ser igual a outra e sempre deve começar em 0 e somar 1 a cada nova curva.
Além de identificar, esse termo tem o papel de setar a ordem em que as curvas serão resolvidas. Normalmente o usuário
vai querer resolver primeiro todas entradas.

Ambas curvas serão validadas como limites de modo **vertical**, é isso o que a variável :math:`{v}` no dicionário indica.
De modo simples (aprofundamento em :ref:`docstring`), a cada nó existente
no eixo horizontal, um vetor **vertical** será gerado. Quando esse vetor cruzar uma curva,
ele validará um limite.

O tipo do limite é o usuário quem determina, seja ele entrada ou saída: ``'entry+exit and/or exit'`` ou
``'entry+exit and/or entry'``. Para o caso que a superfície seja ambos, o código já está pronto para lidar.

Observando a imagem gerada pela função, a informações ficam mais evidentes:

.. figure:: images/extrude_1.png
   :height: 450px
   :align: center

   Cada linha pontilhada vermelha representa um dos vetores verticais que criam os limites.

De baixo para cima (lógica da solução vertical), a curva :math:`{0}` é uma entrada e a curva
:math:`{1}` é uma saída.

Em :math:`{lz=1.0}` até :math:`{lz=1.5}`, ambas curvas se comportam como entrada e saída ao mesmo tempo,
e o código está preparado para entender isso.

Para resolver essas curvas **usando vetores horizontais**:

.. code-block:: python
   :linenos:

   #perceba a diferença no segundo argumento do dicionário:

   c.extrude_information={'1':['entry+exit and/or entry','h',[[2.5,1],[1,1.75],[0.5,1.5],[1.5,1]]],
                          '0':['entry+exit and/or entry','h',[[2.5,1],[1,0.25],[0.5,0.5],[1.5,1]]]}

   #a identificação dentro do dicionário é independente da identificação das features

   #observar que agora ambas curvas serão consideradas entradas/saídas simultâneas.

   gen_extrude_profile(identif='1',name='primeiro_extrude',
                       direction='x',init_height=0,final_height=3)

   #o extrude começará em 0 e terminará em 3, na direção do eixo x.

.. figure:: images/extrude_2.png
   :height: 450px
   :align: center

   Cada linha pontilhada vermelha representa um dos vetores horizontais que criam os limites.

Agora, a lógica da solução é da esquerda para a direita. Ambas curvas são consideradas
entradas e saídas simultâneas. O usuário pode escolher se quer setar o tipo de limite como
``'entry+exit and/or entry'`` ou ``'entry+exit and/or exit'``, tanto faz.

Explicados os métodos possíveis para a criação dos limites de um extrude, deve-se validá-lo
na matriz :math:`{\epsilon}`:

.. code-block:: python
   :linenos:

   gen_epsi_extrude('1')

Essa célula deverá ter um output, que é um plot. Independente do modo como o usuário
decidiu resolver os limites de seu extrude (vertical ou horizontalmente), a validação
deve ser a mesma na :math:`{\epsilon}`:

.. figure:: images/extrude_3.png
   :height: 450px
   :align: center

Gerando os arquivos de output:

.. code-block:: python
   :linenos:

   gen_output(names=name) #geração dos arquivos de saída


E visualizando no software `ParaView <https://www.paraview.org/>`_:

.. figure:: images/extrude_paraview.png
   :height: 450px
   :align: center

   Como previsto, o sólido tem um limite extamente em 3.

Para gerar essa visualização:

#. Abrir dentro do ParaView o arquivo .xdmf presente na pasta do projeto;
#. Open data with... **XDMF reader**;
#. Apply;
#. Mudar o tipo de visualização de Outline para Volume;
#. Selecionar a feature Contour.


2.3 Revolve
++++++++++++

.. Note::

   Na documentação, há uma área especial para as superfícies/curvas de Bézier:
   :ref:`bezier`. Caso o usuário tenha dúvidas de como funcionam, é melhor dar
   uma pausa nesta página e voltar após breve entendimento.

Para que seja possível a criação de um revolve, o usuário deverá setar dois dicionários
de entrada (maior detalhamento em :ref:`docstring`) bem como foi feito na criação de um extrude.
**Esse processo se repetirá toda vez que o usuário queira criar um extrude.**

Esses dicionários ditarão o perfil que será revolucionado, num plano cartesiano onde o eixo horizontal
é chamado de *axis* e o eixo vertical é chamado de *radius*.

O primeiro dicionário é relacionado às curvas inferiores do revolve, ou seja,
num sentido de baixo para cima, a partir dessas curvas se entra no perfil que será revolucionado.

O segundo dicionário é relacionado às curvas superiores do revolve, ou seja,
num sentido de baixo para cima, a partir dessas curvas se sai do perfil que será revolucionado.

Novamente, haverá uma identificação para as curvas de Bézier e a setagem de seus pontos governantes:

.. code-block:: python
   :linenos:

   c.list_storage={}

   c.superior_revolve_info={
                            '0':[[[0.0,0.5],[0.25,0.5]]],
                            '1':[[[0.25,0.5],[0.5,1.0],[1.0,1.0]]],
                           }

   c.inferior_revolve_info={
                            '0':[[[0.0,0.25],[0.5,0.5]]],
                            '1':[[[0.5,0.5],[0.75,0.75]]],
                            '2':[[[0.75,0.75],[0.9,0.7],[1.0,0.25]]]
                           }

   #a identificação dentro do dicionário é independente da identificação das features

   #uma vez construídos os dicionários, podemos setar a feature em si

   gen_revolve_profile(identif='2',name='um_revolve',direction='x',
                       center_1=1.5,center_2=1.0,init_height=1.5)

   #center_1 e center_2 são relacionados à direção que foi escolhida. Nesse caso,
   #como o revolve acontece na direção de x, referem-se aos eixos z e y, respectivamente.

**As primeiras curvas que ditam o perfil o revolve devem sempre começar em 0** (ver
também :ref:`docstring`).

O output dessa célula será um plot:

.. figure:: images/revolve_plot.png
   :height: 450px
   :align: center

   Destaca-se que o existem 3 curvas inferiores e 2 curvas superiores, bem como nos dicionários.

O usuário deve checar se para cada linha vermelha há uma linha cinza na área que sofrerá
revolução.

Para conferência dos limites do revolve no domínio, o usuário pode invocar a
``surface_plot()``. O plot representará dois cilindros, que correspondem ao máximo
e ao mínimo do revolve.

Criada a feature, é necessário a validação desses limites na :math:`{\epsilon}`. Para que
isso seja feito, executar a célula:

.. code-block:: python
   :linenos:

   gen_epsi_revolve(identif='2') #processo de setagem onde é e onde não é sólido

Para finalizar o projeto, chamar ``gen_output()``:

.. code-block:: python
   :linenos:

   gen_output(names=name) #geração dos arquivos de saída

Pronto. O usuário pode visualizar o projeto no software `ParaView
<https://www.paraview.org/>`_:

.. figure:: images/revolve_paraview.png
   :align: center

   Visualização do meio do sólido por meio da feature Slice.

Para gerar essa visualização:

#. Abrir dentro do ParaView o arquivo .xdmf presente na pasta do projeto;
#. Open data with... **XDMF reader**;
#. Apply;
#. Mudar o tipo de visualização de Outline para Volume;
#. Selecionar a feature Slice, visualizar como Points com tamanho 8.25.


.. _toroide:

2.4 Toróide
++++++++++++

A função de toróide é um caso específico de um revolve. O autor prevê pouca aplicação
para essa geometria, mas resolveu criá-la para testar a flexibilidade do código.

Para **criar** um toróide:

.. code-block:: python
   :linenos:

   gen_toroid(identif='3',name='toroide',bases_plane='zy',
              external_radius=0.95,profile_circle_radius=0.425,
              center_1=1,center_2=1,init_height=1)

O output da célula deverá ser um plot, bem como no caso de um revolve:

.. figure:: images/toroide_plot.png
   :height: 450px
   :align: center

   O plot comprova que o toróide nada mais é do que um caso de revolve.

Para visualizar os limites simplificados:

.. code-block:: python
   :linenos:

   surface_plot('3','4','mayavi')

.. figure:: images/toroide_2.png
   :align: center

   Novamente, o revolve foi simplificado para dois cilindros.

Uma vez criada a feature e conferidos seus limites, deve-se trasmitir toda essa
informação para a :math:`{\epsilon}`. Para validar os limites do toróide criado na :math:`{\epsilon}`:

.. code-block:: python
   :linenos:

   gen_epsi_revolve('3')

Gerando os arquivos de saída com ``gen_output()`` e visualizando no `ParaView
<https://www.paraview.org/>`_:

.. figure:: images/toroide_paraview.png
   :height: 450px
   :align: center

   Visualização da isosuperfície = 0.5 dos dados da **:math:`{\epsilon}`**.

Para gerar a visualização no ParaView:

#. Abrir dentro do ParaView o arquivo .xdmf presente na pasta do projeto;
#. Open data with... **XDMF reader**;
#. Apply;
#. Mudar o tipo de visualização de Outline para Volume;
#. Selecionar a feature Contour.

2.5 Cilindro
+++++++++++++

.. Note::

   Essa função usa *fancy indexing*, abordagem extremamente efetiva do Python.

Um cilíndro pode ser considerado um sólido (adicionar material) ou um contorno (remover material).
Não pode ser rotacionado, ou seja, será sempre paralelo a um dos eixos :math:`{x}`, :math:`{y}` ou :math:`{z}`.

Para criar a feature, rodar o seguinte bloco:

.. code-block:: python
   :linenos:

   #primeiro cilindro, chamado de cilindro_ao_longo_de_y e identificado como 4

   gen_cylinder(identif='4',name='cilindro_ao_longo_de_y',bases_plane='xz',
                radius=1,center_1=2,center_2=1.5,init_height=0.5,final_height=1.5)

   #segundo cilindro, chamado de cilindro_ao_longo_de_x e identificado como 5

   gen_cylinder(identif='5',name='cilindro_ao_longo_de_x',bases_plane='zy',
                radius=0.2,center_1=1.5,center_2=1,init_height=0.5,final_height=3.5)

   #novamente center_1 e center_2 depende da direção longitudinal da feature.


Visualizando ambos cilindros:

.. figure:: images/cilindros_plot.png
   :height: 450px
   :align: center

Para demonstração da variedade da função, setaremos *cilindro_ao_longo_de_y* como
um sólido e *cilindro_ao_longo_de_x* como um contorno na validação das superfícies
na :math:`{\epsilon}`:

.. code-block:: python
   :linenos:

   gen_epsi_cylinder(identif='4',surface_type='solid')

   gen_epsi_cylinder(identif='5',surface_type='contour')

   #perceba a velocidade com que a validação será realizada.

Gerando os arquivos de saída com ``gen_output()`` e visualizando o arquivo
.xdmf no `ParaView <https://www.paraview.org/>`_:

.. figure:: images/cilindros_paraview.png
   :height: 450px
   :align: center

   Bonita visualização com auxílio de Ray Tracing

Para gerar a visualização no ParaView:

#. Abrir dentro do ParaView o arquivo .xdmf presente na pasta do projeto;
#. Open data with... **XDMF reader**;
#. Apply;
#. Mudar o tipo de visualização de Outline para Volume;
#. Selecionar a feature Contour;
#. Em Proprieties, Enable Ray Tracing;
#. Ativar Shadows e aumentar Light Scale.

.. _esfera:

2.6 Esfera
+++++++++++

.. Note::

   Essa função usa *fancy indexing*, abordagem extremamente efetiva do Python.

Uma esfera pode ser considerada um sólido (adicionar material) ou um contorno (remover material),
bem como um cilindro.

Para criar a feature:

.. code-block:: python
   :linenos:

   gen_sphere(identif='6',name='uma_esfera',radius=0.75,cex=2,cey=1,cez=1.5)

Para visualizar:

.. code-block:: python
   :linenos:

   surface_plot(init_identif='6',final_identif='7',engine='mayavi',alpha=1)

Obtendo o output:

.. figure:: images/esfera_plot.png
   :align: center

Validando os limites e gerando os arquivos de saída com o bloco:

.. code-block:: python
   :linenos:

   gen_epsi_sphere(identif='6',surface_type='solid')

   #perceba a velocidade com que a validação será realizada.

   gen_output(name)

No `ParaView <https://www.paraview.org/>`_:

.. figure:: images/esfera_paraview.png
   :height: 450px
   :align: center

O processo de criação dessa cena no software foi igual à :ref:`toroide`.

2.7 Prisma Quadrangular
++++++++++++++++++++++++

.. Note::

   Essa função usa *fancy indexing*, abordagem extremamente efetiva do Python.

Um retângulo pode ser considerado um sólido (adicionar material) ou um contorno (remover material),
assim como a esfera e o cilindro.

Como um paralelepípedo, o usuário deverá definir as arestas :math:`{a}`, :math:`{b}` e :math:`{c}`
da feature, que correspondem as dimensões na direção :math:`{x}`, :math:`{y}` e :math:`{z}`, respectivamente.

Um prisma quadrangular não pode ser rotacionado.

Como exemplo, serão construídos 3 prismas quadrangulares:

.. code-block:: python
   :linenos:

   gen_quad_prism(identif='7',name='um_retângulo_3d_largo'   ,a=0.50,b=0.45,c=0.75,reference_point=[1.00,1.00,1.00])

   gen_quad_prism(identif='8',name='um_retângulo_3d_alto'    ,a=0.25,b=1.45,c=0.25,reference_point=[1.00,0.00,1.25])

   gen_quad_prism(identif='9',name='um_retângulo_3d_profundo',a=2.25,b=1.15,c=0.05,reference_point=[1.00,0.00,1.35])

   #reference_point é o vértice mais próximo da origem (0,0,0)!

Na visualização, observa-se a diferença entre eles:

.. figure:: images/prism_quad_plot.png
   :height: 450px
   :align: center

   Uma abstração criada pelo autor.

Novamente validando os limites, criando os arquivos de saída e visualizando no
`ParaView <https://www.paraview.org/>`_:

.. code-block:: python
   :linenos:

   #validando as 3 features como sólido

   gen_epsi_quad_prism(identif='7',surface_type='solid')

   gen_epsi_quad_prism(identif='8',surface_type='solid')

   gen_epsi_quad_prism(identif='9',surface_type='solid')

   #criando os outputs

   gen_output(name)

.. figure:: images/prism_quad_paraview.png
   :height: 450px
   :align: center

O processo de criação dessa cena no software foi igual à :ref:`toroide`.

.. _intersec:

2.8 Normalização/Intersecções
++++++++++++++++++++++++++++++

Intersecções podem ser criadas com a função ``normalize_epsi()``. De forma
sucinta, a função capta todos os índices da matriz :math:`{\epsilon}` que tenham um valor
específico e os seta como 1, enquanto todo o resto é setado como 0, ou seja,
tudo que é intersecção vira um sólido normal e tudo que nao é some.

Para exemplificação, vamos gerar um sólido que será a intersecção de 3
cilindros perpendiculares entre si:

.. code-block:: python
   :linenos:

   #criação dos cilindros perpendiculares

   gen_cylinder(identif='8',name='ao_longo_de_y',bases_plane='xz',
                radius=0.75,center_1=2,center_2=2,init_height=0,final_height=2)

   gen_cylinder(identif='9',name='ao_longo_de_x',bases_plane='zy',
                radius=0.75,center_1=2,center_2=1,init_height=0,final_height=3)

   gen_cylinder(identif='10',name='ao_longo_de_z',bases_plane='xy',
                radius=0.75,center_1=2,center_2=1,init_height=0,final_height=3)

A visualização pela biblioteca ``matplotlib`` desses sólidos feita pela célula:

.. code-block:: python
   :linenos:

   surface_plot(init_identif='8',final_identif='11',engine='matplotlib')

E resulta em:

.. figure:: images/intersec_plot.png
   :height: 450px
   :align: center

Validando tais limites na :math:`{\epsilon}`, há uma novidade: o argumento ``add_or_sub`` na função
``gen_epsi_cylinder()``. Tal argumento comanda a comunicação das superfícies com a :math:`{\epsilon}`. Pode assumir dois valores,
``add`` ou ``sub``.

Caso assuma ``sub``, trata-se do procedimento padrão: onde é sólido
vira 1, onde não é vira 0.

Se assumir ``add``, ao invés de simplesmente substituir o valor
do índice da matriz :math:`{\epsilon}` de 0 para 1, o script somará 1. Portanto, caso haja duas superfícies
que ocupam o mesmo espaço, **o valor dos índices da :math:`{\epsilon}` em tal espaço não será 1, mas sim 2.**

Porém, o ``incompact3d`` só está preparado para receber a matriz :math:`{\epsilon}` com valores
correspondentes a 0 e 1. Portanto, tudo que é 2 no sólido seria "ilegal" no solver.
Para resolver isso, chama-se a função ``normalize_epsi()``. Caso o primeiro termo dessa função (``intersection``)
for setado como ``True``, o usuário deverá indicar qual é o valor correspondente
da intersecção por meio do segundo argumento, ``target``.

O usuário pode concluir que a opção ``add`` no argumento ``add_or_sub`` é perfeita para
criação de intersecções, e é isso que o exemplo comprovará.

Agora sim, validando tais limites na :math:`{\epsilon}`:

.. code-block:: python
   :linenos:

   c.epsi_3d=np.zeros((c.nx,c.ny,c.nz),dtype=np.float32) #limpar possível bagunça

   gen_epsi_cylinder(identif='8' ,surface_type='solid',add_or_sub='add')
   gen_epsi_cylinder(identif='9' ,surface_type='solid',add_or_sub='add')
   gen_epsi_cylinder(identif='10',surface_type='solid',add_or_sub='add')


Antes de efetuar a intersecção como um sólido, a visualização da :math:`{\epsilon}` sem a chamada de ``normalize_epsi()``
será apresentada.

Gerando o output:

.. code-block:: python
   :linenos:

   gen_output(name)

Obtém-se a visualização no ParaView:

.. figure:: images/intersec_cru.png
   :height: 450px
   :align: center

   Perceber a diferença entre as cores e o que isso significa: somatório de valores.

Como esperado, temos outros valores além de 0 e 1 na :math:`{\epsilon}`: 2 e 3.

Para validar a intersecção dos 3 cilindros, todos os valores maiores ou iguais a 2
serão setados como 1 e o resto como 0, através de ``normalize_epsi()``:

.. code-block:: python
   :linenos:

   normalize_epsi(intersection=True,target=2)

   gen_output(name)

Resultando no seguinte caso:

.. figure:: images/intersec2.png
   :height: 450px
   :align: center

   Todos os valores que eram 2 se tornaram 1 e a intersecção foi validada como um sólido normal.

Para obter tal visualização, o usuário deverá dar Rescale na seção Coloring.

Para validar a região do espaço em que necessariamente os 3 cilindros estão,
o usuário deve **rodar novamente o código** (dar restart na kernel) apenas alterando o valor de ``target``
de 2 para 3.

.. code-block:: python
   :linenos:

   normalize_epsi(intersection=True,target=3)


.. figure:: images/intersec3.png
   :height: 450px
   :align: center

   Todos os valores que eram 3 se tornaram 1 e a intersecção foi validada como um sólido normal.


.. Note::

   ``add_or_sub`` é um argumento comum entre validação de **esferas, cilindros, prismas
   quandrangulares e superfícies de Béizer**!


2.9 Espelhamento
+++++++++++++++++

Espelhamento é uma feature de criação de sólidos/limites indireta. Nessa função, não será
setado nenhum raio, aresta ou ponto governante.

Importante frisar que o espelhamento será feito na própria matriz :math:`{\epsilon}` e não
nas superfícies delimitadoras. Portanto, para criar um espelhamento, todas as superfícies
já devem ter sidos validadas na :math:`{\epsilon}`.

O espelhamento pode ser feito em apenas um sólido ou no domínio inteiro.

2.9.1 Sólido
-------------

Num espelhamento em relação a um sólido, o que será feito é a determinação de um
sólido único com quantas superfícies forem necessárias, por meio da função
``bounds_into_single_solid()``. Depois, haverá espelhamento desse mesmo sólido
em relação a um dos eixos :math:`{x}`, :math:`{y}` e :math:`{z}`.

Para o estudo de caso, criaremos uma esfera e uma superfície de Bézier que
interceptará a esfera, cortando uma fração dela fora:

.. code-block:: python
   :linenos:

   #criando a esfera

   gen_sphere(identif='10',name='uma_esfera',radius=0.5,cex=0.5,cey=1.0,cez=0.5)

   #criando a superfície de Bézier

   set_point_matrix(num_u_points=2,num_v_points=2) #prepara a matriz dos pontos a serem recebidos

   point_storage['P00']=[0,1,0] #setar os pontos como lista, [x,y,z]
   point_storage['P01']=[0,1,1]

   point_storage['P10']=[1,1.5,0]
   point_storage['P11']=[1,1.5,1]

   create_point_matrix() #definição final da matriz dos pontos

   gen_bezier_surface(identif='11',name='fatiador_de_esferas') #calculo matricial de Bézier

   #sobre visualização

   surface_plot('10','12','mayavi',alpha=0.5)

O plot gerado pela célula deverá ser:

.. figure:: images/mirror_plot.png
   :align: center

   Visualize a superfície de Bézier como algo que fatiará a esfera.

Para validação das features criadas na matriz :math:`{\epsilon}`:

.. code-block:: python
   :linenos:

   #validar a esfera como um sólido

   gen_epsi_sphere(identif='10',surface_type='solid')

   #validar a superfície de Bézier como uma saída de um sólido, ou seja, a partir da superfície não existe mais sólido

   gen_epsi_bezier_surface(surface_type='entry+exit and/or exit',plane='xz',identif='11',add_or_sub='sub')

   #prestar atenção que variando o plane que a superfície é resolvida, o resultado também varia

   #criando um output intermediário para melhor explicação

   gen_output(name)

A visualização da :math:`{\epsilon}` intermediária, no ParaView, é:

.. figure:: images/mirror_solid_1.png
   :align: center

   O esperado se confirma: a superfície fatiou a esfera!

Como mencionado anteriormente, para realização do espelhamento de um sólido
é necessária a invocação da função ``bounds_into_single_solid()`` antes:

.. code-block:: python
   :linenos:

   bounds_into_single_solid(identif_list=['10'],identif='12')

   #essa função seta os limites do sólido 10, a esfera, como os limites de um sólido independente

   #a identificação desse novo sólido é 12

Criado o sólido a parte, torna-se possível a realização do espelhamento dele em relação
a seus limites:

.. code-block:: python
   :linenos:

   gen_epsi_mirror(target='12', direction='x')

   #outra forma de ler: espelhe o sólido 12 ao longo do eixo x

**Um momento antes** de gerar os arquivos de saída, o usuário deve normalizar a :math:`{\epsilon}`:

.. code-block:: python
   :linenos:

   normalize_epsi()

Motivo: toda vez que o usuário criar um sólido com ``bounds_into_single_solid()``,
toda a informação desse sólido na :math:`{\epsilon}` deixará de ter o valor 1 para ter o valor
da própria identificação desse sólido.

No caso do exemplo, tudo que estava dentro os limites da esfera foi setado
com o valor de 12 na :math:`{\epsilon}`. Essa abordagem foi criada para tentar
proteger o espelhamento, ou seja, espelhar apenas o que o usuário deseja, sem
interferências de possíveis sólidos nas proximidades.

Por fim, a geração dos arquivos de saída pode ser realizada com ``gen_output()``.
A visualização no software ParaView:

.. figure:: images/mirror_solid_2.png
   :align: center

   Observar que a esfera foi repetida imediatamente após seu próprio fim na direção do eixo x.

**Uma vez criado um mirror**, os limites do sólido criado com ``bounds_into_single_solid()``
se atualizam. Portanto, caso o ``gen_epsi_mirror()`` seja chamada duas vezes **antes da Espi ser normalizada**,
a nossa primeira esfera fatiada será quadruplicada:

.. figure:: images/mirror_solid_duplo.png
   :align: center

Caso o usuário tenha dúvidas em relação aos limites gerados pela função ``bounds_into_single_solid``,
executar a seguinte célula:

.. code-block:: python
   :linenos:

   c.solid_storage

   #o output será uma lista com 6 elementos: máximo em x, máximo em y, máximo z, mínimo em x, mínimo em y e mínimo em z.

2.9.2 Domínio
--------------

Num espelhamento em relação a um domínio, o usuário não deve se preocupar
em criar um sólido único. Tudo que há no lado do domínio mais próximo da origem
será copiado para o outro lado, na direção de qualquer um dos eixos x, y ou z.

Partindo do mesmo ponto onde foi parado na seção anterior, chamar a função de espelhamento
novamente, dessa vez mudando apenas o argumento ``target``:

.. code-block:: python
   :linenos:

   gen_epsi_mirror(target='whole_domain', direction='z')

Chamando novamente a função que gera os arquivos de saída, a visualização do ParaView:

.. figure:: images/mirror_solid_3.png
   :align: center

   Notar que dessa vez o espelhamento não se deu no exato limite da esfera, sim no exato meio do domínio.

Chamando uma última vez ``gen_epsi_mirror()``, só que dessa vez em relação à direção :math:`{y}`:

.. figure:: images/mirror_solid_y.png
   :align: center

Obviamente, o conjunto das esferas fatiadas se tornou num conjunto de esferas completas uma
vez que as esferas tiveram sua fração retirada apenas na parte superior, que foi
substituída pelo espelhamento.

3. Refinamento de Malha
=======================

O usuário deve estar se perguntando onde o refinamento de malha entra, já que não
foi mencionado em nenhum das subseções presentes em :ref:`features`.

A resposta é simples: o refinamento está presente em todas as situações.

Obviamente, gerar uma :math:`{\epsilon}` refinada nas 3 direções é custoso para o computador,
uma vez que as dimensões da matriz estão sendo escalonadas por um fator. Essa complicação
pode ser evitada na parte de desenvolvimento do projeto, na qual o usuário ainda está definido como
será o objeto que interceptará o fluxo.

Uma vez terminado a etapa de construção dos sólidos, o usuário irá querer partir
para a simulação numérica através do ``incompact3d``. Porém, como já
mencionado anteriormente, o *solver* necessita das :math:`{\epsilon}` refinadas para entender
melhor onde realmente está o sólido.

Para construir as :math:`{\epsilon}` refinadas, o usuário deve apenas setar o argumento ``rav_path=True``
quando existir dentro das funções que validam os limites na :math:`{\epsilon}`.

**Lista de funções que geram refinamento de malha:**

#. ``gen_toroid()``
#. ``gen_revolve_profile()``
#. ``gen_epsi_bezier_surface()``
#. ``gen_epsi_mirror()``
#. ``gen_epsi_cylinder()``
#. ``gen_epsi_quad_prism()``
#. ``gen_epsi_sphere()``
#. ``bounds_into_single_solid()``
#. ``normalize_epsi()``
#. ``gen_output()``

.. hint::

   O usuário pode conferir quais são os argumentos das funções com o comando
   **shift+tab** dentro dos parênteses!

Por default, todos os argumentos ``rav_path`` são ``False`` (economia de tempo
na etapa de desenvolvimento do projeto).

**Obviamente, para que o refinamento seja efetuado corretamente, todas essas funções
devem ter o argumento setado como verdadeiro ao final do projeto.**

O usuário pode perceber que quando o refinamento de malha estiver ativo, a mesma
função será repetida 4 vezes, uma para cada :math:`{\epsilon}`.

Para exemplificar, vamos pegar o mesmo exemplo de :ref:`esfera`:

.. code-block:: python
   :linenos:

   #não necessita refinamento:

   gen_sphere(identif='6',name='uma_esfera',radius=0.75,cex=2,cey=1,cez=1.5)

   #necessita refinamento:

   gen_epsi_sphere(identif='6',surface_type='solid', sph_raf_path=True)

   gen_output(names=name, out_raf_path=True)


A visualização no ParaView facilita muito a compreensão do refinamento de malha:

.. figure:: images/raf_1.png
   :height: 450px
   :align: center

   Sem refinamento (topo esquerda), refinamento em x (topo direita), refinamento em y (baixo esquerda) e refinamento em z (baixo direita).

A figura deixa evidente a diferença entre os 4 arquivos de :math:`{\epsilon}` e como o refinamento
ocorre em cada uma das direções, separadamente.
