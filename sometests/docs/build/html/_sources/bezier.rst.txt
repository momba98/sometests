Abordagem de Bézier
***************************

.. figure:: images/bez.gif
   :align: center
   :scale: 80%

A abordagem de Bézier baseia-se na construção suave de superfícies ou curvas
paramétricas através pontos de controle determinados pelo usuário. Basicamente,
é uma interpolação entre vetores. É um método extremamente simples que torna
a criação de sólidos complexos fácil.
Tem seu nome oriundo do engenheiro/matemático Pierre Bézier, muito embora
tenha sido desenvolvida também por Paul de Casteljau.
As curvas e superfícies de Bézier são usadas em muitas partes
do ``geo_bezier_3d`` e, portanto, terão suas teorias
brevemente desenvolvidas nessa
página. Dessa forma, o usuário terá maior facilidade em construir sólidos de
maneira correta, sem desperdício computacional.

1. Formulação
==============

*A matemática da abordagem de Bézier será desenvolvida através de matrizes,
o que facilita tanto a compreensão quanto a demonstração.*

Uma **curva de Bézier**, se 2D, é definida por duas equações e um parâmetro:

.. math::
   x(t),\: y(t)

Uma **superfície de Bézier**, se 3D, é definida por três equações e dois
parâmetros:

.. math::
   x(u,v),\: y(u,v),\: z(u,v)

Todos os três parâmetros :obj:`t`, :obj:`u` e :obj:`v` variam apenas no intervalo
:obj:`[0,1]`.
Uma curva de Bézier pode ser 3D e uma superfície pode ser 2D,
mas isso será ignorado por agora.

O grau de qualquer uma dessas equações depende diretamente da quantidade de pontos
que o usuário definiu:

.. math::
   Order = Number \: of \: Points - 1

A partir de agora, usaremos como exemplo uma curva de Bézier 2D
caso forem inputados 3 pontos para a criação.
Portanto, teremos :obj:`x(t)` e :obj:`y(t)` de ordem 2.

A formulação da totalidade da **curva** se da por

.. math::
   Bézier^{n}(t)=\sum_{i=0}^{n} b_{i}^{n}(t)*P_{i} \\
   Bézier^{2}(t)=\sum_{i=0}^{2} b_{i}^{2}(t)*P_{i}

Como dito anteriormente, uma curva de Bézier 2D possui 2 equações.
Para obter tais equações, a seguinte operação matricial deverá ser realizada:

.. math::
   x(t)=T*M*P_x\\
   y(t)=T*M*P_y

Onde :obj:`T` é a matriz composta por

.. math::
   t^n

onde

.. math::
   n=[0,1,2...Order]

logo, no exemplo,

.. math::
   T=[t^0, t^1, t^2]

A mágica por trás da criação de curvas/superfícies através de pontos
se encontra no *Polinômio de Berstein*:

.. math::
   b_{i}^{n}(t)={n \choose i}t^{i}(1-t)^{{n-i}}

Dele, retiramos a matriz :obj:`M`, chave para obtenção das equações que governam o objeto.
É composta pelos coeficientes dos termos desse polinômio e varia de acordo com
o grau (ou então o número de pontos) da curva/superfície de Bézier.

No exemplo anteriormente citado, o Polinômio de Berstein se expressaria na forma

.. math::
   b_{0}^{2}(t)={2 \choose 0}t^{0}(1-t)^{{2-0}} = +1t^2 - 2t + 1 \\
   b_{1}^{2}(t)={2 \choose 1}t^{1}(1-t)^{{2-1}} = -2t^2 + 2t + 0 \\
   b_{2}^{2}(t)={2 \choose 2}t^{2}(1-t)^{{2-2}} = +1t^2 + 0t + 0


Logo, a matriz :obj:`m` obtida é:

.. math::

   M =
   \begin{bmatrix}
   1 & 0 & 0 \\
   -2 & 2 & 0 \\
   1 & -2 & 1
   \end{bmatrix}

Por último, se define a matriz :obj:`P` com os pontos fornecidos pelo usuário

.. math::

   P =
   \begin{bmatrix}
   P_0 \\
   P_1 \\
   P_2
   \end{bmatrix}

onde, nesse exemplo,

.. math::
   P_0=(x_0,y_0)=(0,2)\\
   P_1=(x_1,y_1)=(3,1)\\
   P_2=(x_2,y_2)=(5,6)

Definidas todas matrizes, é possível se obter as equações da curva paramétrica:

.. math::

   x(t)=
   \begin{bmatrix}
   t^0 & t^1 & t^2
   \end{bmatrix}
   *
   \begin{bmatrix}
   1 & 0 & 0 \\
   -2 & 2 & 0 \\
   1 & -2 & 1
   \end{bmatrix}
   *
   \begin{bmatrix}
   0 \\
   3 \\
   5
   \end{bmatrix}
   =-1t^2+6t+0\\

   y(t)=
   \begin{bmatrix}
   t^0 & t^1 & t^2
   \end{bmatrix}
   *
   \begin{bmatrix}
   1 & 0 & 0 \\
   -2 & 2 & 0 \\
   1 & -2 & 1
   \end{bmatrix}
   *
   \begin{bmatrix}
   2 \\
   1 \\
   6
   \end{bmatrix}
   =+6t^2-2t+2

A curva do exemplo se parece com a figura:

.. figure:: images/bez1.png
   :align: center
   :scale: 65%

**Perceba:** a curva inicia e termina nos pontos extremos, porém não encosta no
ponto intermediário (este apenas dita a curvatura suave!). Essa é a principal
característica da abordagem de Bézier. O mesmo ocorre nas superfícies.

Na verdade, há uma maneira de *hackear* isso e fazer com que a curva/superfície
encoste em seus pontos intermediários. Essa artimanha está implementado no código
como argumento :obj:`deflection` em diversas funções, mas não será comentada aqui.

2. Interpolação
================

Mas onde podemos visualizar/entender a interpolação anteriormente citada?

A figura facilitará a explicação posterior:

.. figure:: images/bez3.gif
   :align: center
   :scale: 100%

*É um gif satisatório. Mais adiante serão mostrados outros mais ainda.*

Novamente, **perceba:** foram plotados 2 vetores

.. math::
   \overrightarrow{P_0 P_1} \\
   \overrightarrow{P_1 P_2}

O parâmetro :obj:`t` pode ser entendido como um afastamento percentual do início desses
vetores. Em outras palavras, quando :obj:`t=0.1`, nos afastamos 10% da distância
total do vetor do início próprio vetor. Nessa distância, criamos outros 2 pontos.

Desses pontos criados, geramos outro vetor. Novamente, quando :obj:`t=0.1`
, estamos a 10% da distância total do vetor do início dele mesmo.
Criamos mais um ponto. **Esse ponto (vermelho),
para o nosso exemplo, representa a curva.**

Fim. Representamos a abordagem de Bézier de forma simples, com um exemplo simples.
Podemos complicar muito mais, com ordens maiores e pontos interacalados. Isso
complicará - e muito - a convergência das equações e o custo delas para o computador.
Normalmente se usa Béziers de grau 2 até 4, no máximo.

**As superfícies funcionam da mesma forma.** Devemos apenas fazer uma pequena
diferença: criar curvas de Bézier de forma ortogonal. A formulação se da por

.. math::
   Bézier^{n}(u,v)=\sum_{i=0}^{m} \sum_{j=0}^{n} b_{i}^{m}(u) b_{j}^{n}(v) *P_{i,j}

Ou, na forma matricial, por

.. math::
   x(u,v)=U*M*P_x*M^T*V\\
   y(u,v)=U*M*P_y*M^T*V\\
   z(u,v)=U*M*P_z*M^T*V\\

Onde U e V são as matrizes compostas pelos parâmetros u e v, bem como a matriz T.
M é a matriz do Polinômio de Berstein de cada parâmetro e P é a matriz dos pontos.

Podemos enxergar o parâmetro :obj:`u` como uma direção perpendicular ao parâmetro
:obj:`v`.

É possível perceber que cada parâmetro tem seu próprio Polinômio de Berstein, logo o número
de pontos em cada um deles não precisa ser igual.

Se a direção/parâmetro :obj:`u` tiver 2 pontos (o usuário é quem define), serão
criadas 2 curvas de Bézier a partir desses pontos na direção de :obj:`v`. O mesmo
para :obj:`v`.

Analise a figura:

.. figure:: images/bez4.png
   :align: center
   :scale: 50%

Temos 3 pontos na direção/parâmetro :obj:`u` e 2 em :obj:`v`. Logo, são 3 Béziers
de grau 2 em :obj:`v` e 2 Béziers de grau 3 em :obj:`u`.

Os valores intermediários entre eles são calculados através de interpolações
entre esses parâmetros.

A formulação matricial para :obj:`x(u,v)` ficaria

.. math::
   x(u,v)=
   \begin{bmatrix}
   u^0 & u^1 & u^2
   \end{bmatrix}
   *
   \begin{bmatrix}
   1 & 0 & 0 \\
   -2 & 2 & 0 \\
   1 & -2 & 1
   \end{bmatrix}
   *
   \begin{bmatrix}
   P_{x,0,0} & P_{x,0,1} \\
   P_{x,1,0} & P_{x,1,1} \\
   P_{x,2,0} & P_{x,2,1}
   \end{bmatrix}
   *
   \begin{bmatrix}
   1 & -1 \\
   0 & 1
   \end{bmatrix}
   *
   \begin{bmatrix}
   v^0 \\
   v^1
   \end{bmatrix}

3. Algumas Imagens Legais
==========================

Todas imagens foram feitas no ``geo_bezier_3d`` ou através de um script do
autor.

.. figure:: images/bez6.png
   :align: center

   *Superfície visualizada pelo Mayavi;*

.. figure:: images/bez10.gif
   :align: center

.. figure:: images/bez20.gif
   :align: center

.. figure:: images/bez30.gif
   :align: center
