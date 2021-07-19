# twomodels_maixBit
Uma descrição de como rodar dois modelos em "cascata" usando a placa MaixBit com o MCU k210, a plataforma AceleRate e um firmware customizado com o MaixHub

# Descrição
Esse projeto tem como objetivo mostrar como usar dois modelos treinados usando a plataforma [AxeleRate](https://github.com/AIWintermuteAI/aXeleRate) gerando dois arquivos .kmodel separados, usando a arquitetura MobileNet5_0 e ambos tendo o tamanho de 850kb aproximadamente.

Para ser possível de rodar esses dois modelos precisamos "enxutar" o firmware que vai ser usado na nossa placa, para isso usamos o "MaixPy Firmware Online Compilation" que gera um firmware customizado para as necessidades do usuário, já que os firmwares disponibilizados pela Sipeed podem não atender todas as necessidades, no nosso caso, precisamos de um firmware que tenha suporte para a IDE MaixPy e para modelos do formado kmodel v4. Como podemos observar [aqui](https://dl.sipeed.com/shareURL/MAIX/MaixPy/release/master) não temos nenhum firmware que atende essas necessidades sem acrescentar itens extras, como bibliotecas para coisas que não precisamos; então vamos usar o compilador de firmaware online mencionado anteriormente, ele é especialmente útil para usuários windows, já que o compilador de firware pode ser usado de forma offline mas somente para usuários linux.
