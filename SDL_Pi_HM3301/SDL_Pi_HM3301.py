# HM3301 Laser Dust Sensor Driver
# SwitchDoc Labs 2020
# Version 1.0


import time
import pigpio
import aqi

SDA = 20
SCL = 19


DATA_CNT = 29


class SDL_Pi_HM3301(object):

    def __init__(self, SDA=20, SCL=19, I2C_Address =0x40):



        self.pi = pigpio.pi()
        self.SDA = SDA
        self.SCL = SCL
        self.I2C_Address = I2C_Address
        self.last_data = None

        self.PM_1_0_conctrt_std = 0         # PM1.0 Standard particulate matter concentration Unit:ug/m3
        self.PM_2_5_conctrt_std = 0         # PM2.5 Standard particulate matter concentration Unit:ug/m3
        self.PM_10_conctrt_std = 0          # PM10  Standard particulate matter concentration Unit:ug/m3
    
        self.PM_1_0_conctrt_atmosph = 0     #PM1.0 Atmospheric environment concentration ,unit:ug/m3
        self.PM_2_5_conctrt_atmosph = 0     #PM2.5 Atmospheric environment concentration ,unit:ug/m3
        self.PM_10_conctrt_atmosph = 0      #PM10  Atmospheric environment concentration ,unit:ug/m3
   
        # set pullups - not necessary with Pi2Grover

        self.pi.set_pull_up_down(self.SDA, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.SCL, pigpio.PUD_UP)
        h = self.pi.bb_i2c_open(self.SDA, self.SCL, 20000)    

        (count, data) = self.pi.bb_i2c_zip(
             self.SDA, [4, self.I2C_Address, 2,7,1, 0x80,2,7,1,0x88,3,0])
        time.sleep(10.0/1000.0)


    def read_HM3301_data(self):

        (count, data) = self.pi.bb_i2c_zip(
             self.SDA, [4,self.I2C_Address,2,7,1,0x81,3, 2,6,DATA_CNT,3,0   ])


        return list(data)

    def close(self):
        self.pi.bb_i2c_close(self.SDA)
        self.pi.stop()

        

            
    def checksum(self):
        sum = 0
        for i in range(DATA_CNT-1):
            sum += self.last_data[i]
        sum = sum & 0xff
        return (sum==self.last_data[28])

   
    def parse_data(self, data):

        self.PM_1_0_conctrt_std = data[4]<<8 | data[5]
        self.PM_2_5_conctrt_std = data[6]<<8 | data[7]
        self.PM_10_conctrt_std = data[8]<<8 | data[9]
        
        self.PM_1_0_conctrt_atmosph = data[10]<<8 | data[11]          
        self.PM_2_5_conctrt_atmosph = data[12]<<8 | data[13]
        self.PM_10_conctrt_atmosph  = data[14]<<8 | data[15]

    def get_data(self):
        data = self.read_HM3301_data()
        self.last_data = data
        self.parse_data(data)
        return list( (self.PM_1_0_conctrt_std, self.PM_2_5_conctrt_std,  self.PM_10_conctrt_std,  self.PM_1_0_conctrt_atmosph, self.PM_2_5_conctrt_atmosph, self.PM_10_conctrt_atmosph))

    def print_data(self):

        print("PM1.0 Standard particulate matter concentration Unit:ug/m3 = %d"
%self.PM_1_0_conctrt_std)
        print("PM2.5 Standard particulate matter concentration Unit:ug/m3 = %d"
%self.PM_2_5_conctrt_std)
        print("PM10  Standard particulate matter concentration Unit:ug/m3 = %d"
%self.PM_10_conctrt_std)

        print("PM1.0 Atmospheric environment concentration ,unit:ug/m3 = %d" %self.PM_1_0_conctrt_atmosph)
        print("PM2.5 Atmospheric environment concentration ,unit:ug/m3 = %d" %self.PM_2_5_conctrt_atmosph)
        print("PM10  Atmospheric environment concentration ,unit:ug/m3 = %d" %self.PM_10_conctrt_atmosph)
        print(" ")
        print(" ")
        print(" ")

    def get_aqi(self):


        myaqi = aqi.to_aqi([
         (aqi.POLLUTANT_PM25, self.PM_2_5_conctrt_std),
         (aqi.POLLUTANT_PM10, self.PM_10_conctrt_std)
        ])

        return str(myaqi)
