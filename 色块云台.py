import sensor, image, time, lcd, math, json
import pyb
from pyb import UART,LED
from pyb import Pin
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
lcd.init()
ROI=[(320//2)-(50//2), (240//2)-(50//2), 50, 50]
pin0 = Pin('P1', Pin.IN, Pin.PULL_DOWN)
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
thresholds1 =[(blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)]
uart = UART(3,115200)
while(True):
	clock.tick()
	img = sensor.snapshot()
	statistics=img.get_statistics(roi=ROI)
	color_l=statistics.l_mode()
	color_a=statistics.a_mode()
	color_b=statistics.b_mode()
	print("LAB:",color_l,color_a,color_b)
	key0 = pin0.value()
	print("KEY:",key0)
	if key0 == 1:
		pyb.delay(20)
		if key0 == 1:
			LED(3).on()
			LED(1).off()
			blue_L_min = Lmin
			blue_L_max = Lmax
			blue_A_min = Amin
			blue_A_max = Amax
			blue_B_min = Bmin
			blue_B_max = Bmax
			print("NEWLAB",blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)
			thresholds1 =  [(blue_L_min,blue_L_max,blue_A_min,blue_A_max,blue_B_min,blue_B_max)]
	if key0 == 0:
		LED(1).on()
		LED(3).on()
	flag = 0
	blobs = img.find_blobs(thresholds1, pixels_threshold=700)
	if blobs:
		flag = 1
		for b in blobs:
			if b[2]*b[3] > 800 and b[2]*b[3] < 50000:
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