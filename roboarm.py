
import ssc32
import math
ssc = ssc32.SSC32('/dev/ttyUSB0', 115200, count=32)
ssc[2].position = 2000
ssc[3].name = 'pan'
ssc[4].name = 'tilt'
pan_servo = ssc['pan']
tilt_servo = ssc['tilt']
pan_servo.degrees = 0
tilt_servo.radians = math.pi/4
ssc.commit(time=1000)
ssc.is_done()
