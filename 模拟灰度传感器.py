THRESHOLD = (18, 47, 8, 49, -26, 44)
import sensor, image, time, ustruct
import pyb
from pyb import UART,LED
LED(1).on()
LED(2).on()
LED(3).on()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQQVGA)
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.skip_frames(time = 2000)
uart = UART(3,115200)
clock = time.clock()
roi1 = [(0,18,16,25),(16,18,16,25),(32,18,16,25),(48,18,16,25),(64,18,16,25)]
huidu_SBUF = [0,0,0,0,0]
while(True):
	clock.tick()
	img = sensor.snapshot().binary([THRESHOLD])
	line = img.get_regression([(100,100)], robust = True)
	for rec in roi1:
		img.draw_rectangle(rec, color=(255,0,0))
	if (line):
		if line.magnitude()>8:
			pixel1 = img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[0])
			pixel2 = img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[1])
			pixel3 = img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[2])
			pixel4 = img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[3])
			pixel5 = img.find_blobs([(96, 100, -13, 5, -11, 18)],roi=roi1[4])
			if pixel1:
				for blob1 in pixel1:
					if blob1.pixels() > 65:
						huidu_SBUF[0] = 1
					else:
						huidu_SBUF[0] = 0
			if pixel2:
				for blob2 in pixel2:
					if blob2.pixels() > 65:
						huidu_SBUF[1] = 1
					else:
						huidu_SBUF[1] = 0
			if pixel3:
				for blob3 in pixel3:
					if blob3.pixels() > 65:
						huidu_SBUF[2] = 1
					else:
						huidu_SBUF[2] = 0
			if pixel4:
				for blob4 in pixel4:
					if blob4.pixels() > 65:
						huidu_SBUF[3] = 1
					else:
						huidu_SBUF[3] = 0
			if pixel5:
				for blob5 in pixel5:
					if blob5.pixels() > 65:
						huidu_SBUF[4] = 1
					else:
						huidu_SBUF[4] = 0
		else:
			huidu_SBUF = [0,0,0,0,0]
	else:
		huidu_SBUF = [0,0,0,0,0]
	FH = bytearray([0x4A,0x06,huidu_SBUF[0],huidu_SBUF[1],huidu_SBUF[2],huidu_SBUF[3],huidu_SBUF[4]])
	uart.write(FH)
	print(huidu_SBUF)