import sensor, image, time, lcd, math, json
import pyb
from pyb import UART,LED
from pyb import Pin

#red_threshold   = (25, 62, 19, 43, -14, 25)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False) # 颜色跟踪必须关闭白平衡
clock = time.clock()

lcd.init()

ROI=[(320//2)-(50//2), (240//2)-(50//2), 50, 50]

pin0 = Pin('P1', Pin.IN, Pin.PULL_DOWN)#定义输入引脚
#初始阈值
blue_L_min=25
blue_L_max=62
blue_A_min=19
blue_A_max=43
blue_B_min=-14
blue_B_max=25

Lmin = 0
Lmax = 0
Amin = 0
Amax = 0
Bmin = 0
Bmax = 0

#颜色跟踪阈值(L Min, L Max, A Min, A Max, B Min, B Max)
thresholds1 =[(blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)]

for i in range(60):
    img = sensor.snapshot()
    img.draw_rectangle(ROI)

print("Learning thresholds...")

#threshold = [50, 50, 0, 0, 0, 0] # Middle L, A, B values.

for i in range(60):
    img = sensor.snapshot()

    statistics=img.get_statistics(roi=ROI)#取目标区域
    color_l=statistics.l_mode()
    color_a=statistics.a_mode()
    color_b=statistics.b_mode()
    #print("LAB:",color_l,color_a,color_b)

    Lmin = color_l - 10
    Lmax = color_l + 10
    Amin = color_a - 10
    Amax = color_a + 10
    Bmin = color_b - 10
    Bmax = color_b + 10

    blue_L_min = Lmin
    blue_L_max = Lmax
    blue_A_min = Amin
    blue_A_max = Amax
    blue_B_min = Bmin
    blue_B_max = Bmax

    thresholds1 =  [(blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)]
    #for blob in img.find_blobs([threshold]):
    #    img.draw_rectangle(blob.rect())
    #    img.draw_cross(blob.cx(), blob.cy())
    img.draw_rectangle(ROI)

print("Thresholds Learned Over")
print("Tracking colors...")


uart = UART(3,115200)   #定义串口3变量


#寻找最大色块
#def find_max(blobs):
#    max_size=0
#    for blob in blobs:
#        if blob.pixels() > max_size:
#            max_blob = blob
#            max_size = blob.pixels()
#    return max_blob

while(True):
    clock.tick()
    img = sensor.snapshot()

    #statistics=img.get_statistics(roi=ROI)#取目标区域
    #color_l=statistics.l_mode()
    #color_a=statistics.a_mode()
    #color_b=statistics.b_mode()
    #print("LAB:",color_l,color_a,color_b)
    #
    #img.draw_rectangle(ROI)
    #
    #Lmin = color_l - 10
    #Lmax = color_l + 10
    #Amin = color_a - 10
    #Amax = color_a + 10
    #Bmin = color_b - 10
    #Bmax = color_b + 10

    key0 = pin0.value()
    print("KEY:",key0)

    if key0 == 1:
        pyb.delay(20)
        if key0 == 1:
            LED(3).on()
            LED(1).off()
            for i in range(60):
                img = sensor.snapshot()
                img.draw_rectangle(ROI)

            print("Learning thresholds...")

            for i in range(60):
                img = sensor.snapshot()

                statistics=img.get_statistics(roi=ROI)#取目标区域
                color_l=statistics.l_mode()
                color_a=statistics.a_mode()
                color_b=statistics.b_mode()
                #print("LAB:",color_l,color_a,color_b)

                Lmin = color_l - 10
                Lmax = color_l + 10
                Amin = color_a - 10
                Amax = color_a + 10
                Bmin = color_b - 10
                Bmax = color_b + 10

                blue_L_min = Lmin
                blue_L_max = Lmax
                blue_A_min = Amin
                blue_A_max = Amax
                blue_B_min = Bmin
                blue_B_max = Bmax

                thresholds1 =  [(blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)]
                #for blob in img.find_blobs([threshold]):
                #    img.draw_rectangle(blob.rect())
                #    img.draw_cross(blob.cx(), blob.cy())
                img.draw_rectangle(ROI)

            print("Thresholds Learned Over")
            print("Tracking colors...")

    if key0 == 0:
        LED(1).on()
        LED(3).on()

    flag = 0
    blobs = img.find_blobs(thresholds1, pixels_threshold=700)

    #find_blobs(thresholds, invert=False, roi=Auto),thresholds为颜色阈值，
    #是一个元组，需要用括号［ ］括起来。invert=1,反转颜色阈值，invert=False默认
    #不反转。roi设置颜色识别的视野区域，roi是一个元组， roi = (x, y, w, h)，代表
    #从左上顶点(x,y)开始的宽为w高为h的矩形区域，roi不设置的话默认为整个图像视野。
    #这个函数返回一个列表，[0]代表识别到的目标颜色区域左上顶点的x坐标，［1］代表
    #左上顶点y坐标，［2］代表目标区域的宽，［3］代表目标区域的高，［4］代表目标
    #区域像素点的个数，［5］代表目标区域的中心点x坐标，［6］代表目标区域中心点y坐标，
    #［7］代表目标颜色区域的旋转角度（是弧度值，浮点型，列表其他元素是整型），
    #［8］代表与此目标区域交叉的目标个数，［9］代表颜色的编号（它可以用来分辨这个
    #区域是用哪个颜色阈值threshold识别出来的）。

    #img.draw_line(143,0,143,240)
    #img.draw_line(0,91,360,91)

    if blobs:
        flag = 1
        for b in blobs:
            if b[2]*b[3] > 800 and b[2]*b[3] < 50000: #面积筛选（根据需求调即可识别）
                img.draw_rectangle(b[0:4])

                img.draw_cross(b[5], b[6])

                FH = bytearray([0x5C,0x21,flag,int(b[5]/100),int(b[5]%100/10),int(b[5]%100%10),0,int(b[6]/100),int(b[6]%100/10),int(b[6]%100%10)])
                uart.write(FH)

                print("BLOB:",b[5], b[6], flag,int(b[5]/100),int(b[5]%100/10),int(b[5]%100%10),int(b[6]/100),int(b[6]%100/10),int(b[6]%100%10))
    else:
        flag = 0
        FH = bytearray([0x5C,0x21,flag,0,0,0,0,0,0,0])
        uart.write(FH)

        print("FLAG:",flag)

    lcd.display(img)
