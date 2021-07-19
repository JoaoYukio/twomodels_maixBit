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

