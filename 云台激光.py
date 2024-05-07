import sensor, image, time, math
from pyb import Pin

red_thresholds = (29, 11, 45, 0, -9, 16) # 激光灯在纸上颜色的阈值，可以执行调节
green_thresholds = (17, 100, -63, 4, 37, -7)

ain1 = Pin('P0',Pin.OUT_PP)#激光模块的引脚
ain1.high()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240)) # 240x240 center pixels of VGA
sensor.set_auto_exposure(False,2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) #如果使用彩图读取，则白平衡需要关闭，即sensor.set_auto_whitebal(False)
sensor.skip_frames(20)
clock = time.clock()

def central_blob(threshold):
    blobs = img.find_blobs([threshold])
    if len(blobs) >= 1:
        # Draw a rect around the blob.
        b = blobs[0]

        cx = b[5]
        cy = b[6]

        for i in range(len(blobs)-1):
            cx = blobs[i][5]+cx
            cy = blobs[i][6]+cy
        cx=int(cx/len(blobs))
        cy=int(cy/len(blobs))

        print(cx, cy)
        return int(cx), int(cy)
    return None, None

#def green_blob(threshold):
#    blobs = img.find_blobs([threshold])
#    if len(blobs) >= 1:
#        # Draw a rect around the blob.
#        b = blobs[0]
#
#        cx = b[5]
#        cy = b[6]
#
#        for i in range(len(blobs)-1):
#            cx = blobs[i][5]+cx
#            cy = blobs[i][6]+cy
#        cx=int(cx/len(blobs))
#        cy=int(cy/len(blobs))
#
#        print(cx, cy)
#        return int(cx), int(cy)
#    return None, None

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.draw_cross(120, 120, color=(255, 128, 255))  # 中心位置绘制十字
    blob1 = img.find_blobs([red_thresholds])

    blob2 = img.find_blobs([green_thresholds])

    if blob1:
        cx1,cy1 = central_blob(red_thresholds)
        img.draw_cross(cx1, cy1,color = (255,0,0)) # cx, cy

    if blob2:
        cx2,cy2 = central_blob(green_thresholds)
        img.draw_cross(cx2, cy2,color = (0,255,0)) # cx, cy

    else:
        print("don't have")
    #print(clock.fps())
