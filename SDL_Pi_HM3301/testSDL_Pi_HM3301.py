# test HM3301 Laser Dust Sensor

# must run "sudo pigpiod" before starting

import SDL_Pi_HM3301
import time
import traceback
import pigpio

mypi = pigpio.pi()

mySDA = 21
mySCL = 20

hm3301 = SDL_Pi_HM3301.SDL_Pi_HM3301(SDA=mySDA, SCL=mySCL, pi=mypi)
time.sleep(0.01)
try:
    while 1:


        myData = hm3301.get_data()
        print ("data=",myData)
        if (hm3301.checksum() != True):
            print("Checksum Error!")
        myAQI = hm3301.get_aqi()
        hm3301.print_data()
        print ("AQI=", myAQI)

        time.sleep(3)

except:
    print ("closing hm3301")
    print(traceback.format_exc())
    hm3301.close()
