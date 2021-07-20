# twomodels_maixBit
Uma descrição de como rodar dois modelos em "cascata" usando a placa MaixBit com o MCU k210, a plataforma AceleRate e um firmware customizado com o MaixHub

# Descrição
Esse projeto tem como objetivo mostrar como usar dois modelos treinados usando a plataforma [AxeleRate](https://github.com/AIWintermuteAI/aXeleRate) gerando dois arquivos .kmodel separados, usando a arquitetura MobileNet5_0 e ambos tendo o tamanho de 850kb aproximadamente.

Para ser possível de rodar esses dois modelos precisamos "enxutar" o firmware que vai ser usado na nossa placa, para isso usamos o "MaixPy Firmware Online Compilation" que gera um firmware customizado para as necessidades do usuário, já que os firmwares disponibilizados pela Sipeed podem não atender todas as necessidades, no nosso caso, precisamos de um firmware que tenha suporte para a IDE MaixPy e para modelos do formado kmodel v4. Como podemos observar [aqui](https://dl.sipeed.com/shareURL/MAIX/MaixPy/release/master) não temos nenhum firmware que atende essas necessidades sem acrescentar itens extras, como bibliotecas para coisas que não precisamos; então vamos usar o compilador de firmaware online mencionado anteriormente, ele é especialmente útil para usuários windows, já que o compilador de firware pode ser usado de forma offline mas somente para usuários linux. Antes de começarmos a usar a ferramenta é importante lembrar que é preciso ter uma conta no MaixHub.

Dentro da [ferramenta de compilação online](https://www.maixhub.com/onlineCompiler) teremos vários itens para "checar", você escolherá o que for preciso para o seu projeto, no caso iremos querer apenas suporte para a IDE e para kmodel v4.

![image](https://user-images.githubusercontent.com/74123993/126240239-d81774b7-781a-44a1-8c57-120c9c604d17.png)

O resto pode ser deixado com os valores padrôes. Após conferir se está tudo certo podemos submeter nosso firmware para compilação, e em alguns instantes você poderá fazer o download do arquivo .bin contendo seu firmware e poderá gravá-lo na sua placa usando a ferramenta kFlash, juntamente com seus dois modelos em seus respectivos endereços de memória.

O primeiro modelo será usado para detectar se uma folha de café é saudável ou se não é e o segundo para classificar três tipos de doença nessa folha. O dataset utilizado pode ser encontrado [aqui](https://github.com/francismontalbo/swatdcnn) ele é uma coleção de outros três datasets que foram expandidos usando [data augmentation](https://nanonets.com/blog/data-augmentation-how-to-use-deep-learning-when-you-have-limited-data-part-2/) e os dois modelos foram treinados usando o exemplo de classificador que pode ser encontrado no github do axelerate.

Com os modelos e o firmware gravados na placa podemos usar o seguinte script na plataforma maixpy para visualizar os resultados da inferência.

    import sensor, image, lcd, time
	import KPU as kpu
	import gc

	lcd.init()
	sensor.reset()
	sensor.set_pixformat(sensor.RGB565)
	sensor.set_framesize(sensor.QVGA)
	sensor.set_windowing((224, 224))
	sensor.set_brightness(0)
	sensor.set_auto_gain(1)
	sensor.set_vflip(1)
	lcd.clear()

	labels_stage1 = ['healthy', 'unhealthy']
	labels_stage2 = ['Rust', 'Brown_Spots', 'Sooty_Molds']
	task_stage1 = kpu.load(0x300000)
	task_stage2 = kpu.load(0x500000)
	kpu.set_outputs(task_stage1, 0, 1, 1, 2)
	kpu.set_outputs(task_stage2, 0, 1, 1, 3)

	while(True):
		kpu.memtest()
		img = sensor.snapshot()
		#img = img.rotation_corr(z_rotation=90.0)   uncomment if need rotation correction - only present in full maixpy firmware
		#a = img.pix_to_ai()

		#primeiro estágio


		fmap1 = kpu.forward(task_stage1, img)
		plist=fmap1[:]
		pmax=max(plist)
		max_index=plist.index(pmax)

		#segundo estágio


		fmap2 = kpu.forward(task_stage2, img)
		plist2=fmap2[:]
		pmax2=max(plist2)
		max_index2=plist2.index(pmax2)

		#Mostrar resultados
		a = img.draw_string(0,0, str(labels_stage1[max_index].strip()), color=(255,0,0), scale=2)
		a = img.draw_string(0,20, str(pmax), color=(255,0,0), scale=2)
		a = img.draw_string(0,40, str(labels_stage2[max_index2].strip()), color=(255,0,0), scale=2)
		a = img.draw_string(0,60, str(pmax2), color=(255,0,0), scale=2)




		a = lcd.display(img)
		gc.collect()

	a = kpu.deinit(task_stage1)
	a = kpu.deinit(task_stage2)
# Testes
Temos os seguinte resultados:
## Foto folha saudável
Como não temos uma classe "healthy" no segundo modelo ele não sabe exatamente como classificar essa folha.
![image](https://user-images.githubusercontent.com/74123993/126243057-e98f6547-b9b8-4974-8e11-8c486db6340c.png)

## Folha não saudável
![image](https://user-images.githubusercontent.com/74123993/126243153-7e1b7873-7237-479f-ab37-ab0288aa5b96.png)

## Rust
![image](https://user-images.githubusercontent.com/74123993/126243186-e8ff5e5f-563c-4939-9851-6010e8063da0.png)

## Brown Spots
![image](https://user-images.githubusercontent.com/74123993/126243223-b69684c5-acfb-40ae-ba21-b56d126f348e.png)

## Sooty molds
![image](https://user-images.githubusercontent.com/74123993/126243250-bcd0f1df-c546-44e0-8d60-5f5f4c26ca18.png)


