import os
import time
import random
import threading
import remi.gui as gui
import urllib.request
from urllib.request import urlopen

from remi.gui import *
from remi import start, App
import json

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

myURLOpener = AppURLopener()

class SuperImage(gui.Image):
    def __init__(self, file_path_name=None, **kwargs):
        super(SuperImage, self).__init__("/res/logo.png", **kwargs)
        
        self.imagedata = None
        self.mimetype = None
        self.encoding = None
        self.load(file_path_name)

    def load(self, file_path_name):
        self.mimetype, self.encoding = mimetypes.guess_type(file_path_name)
        with open(file_path_name, 'rb') as f:

            self.imagedata = f.read()
        self.refresh()

    def refresh(self):
        i = int(time.time() * 1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self), i)

    def get_image_data(self, update_index):
        headers = {'Content-type': self.mimetype if self.mimetype else 'application/octet-stream'}
        return [self.imagedata, headers]

class SkyWeatherConfigure(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')
        super(SkyWeatherConfigure, self).__init__(*args, static_file_path={'my_resources':res_path})


    def setDefaults(self):
        self.SWDEBUG = False
        self.enable_MySQL_Logging = False
        self.MySQL_Password = "password"
        self.enable_WLAN_Detection = False
        self.PingableRouterAddress = "192.168.1.1"
        self.mailUser = "yourusername"
        self.mailPassword = "yourmailpassword"
        self.notifyAddress = "you@example.com"
        self.fromAddress = "yourfromaddress@example.com"
        self.enableText = False
        self.textnotifyAddress = "yournumber@yourprovider"
        self.runLEDs = False
        self.SolarMAX_Present = False
        self.SolarMAX_Type = "LEAD"
        self.BMP280_Altitude_Meters = 626.0
        self.Sunlight_Gain = 0
        self.USEWEATHERSTEM = False
        self.INTERVAL_CAM_PICS__SECONDS = 60
        self.STATIONKEY = ""
        self.WeatherUnderground_Present = False
        self.WeatherUnderground_StationID = "KWXXXXX"
        self.WeatherUnderground_StationKey = "YYYYYY"
        self.USEBLYNK = False
        self.BLYNK_AUTH = ""
        self.AS3935_Lightning_Config = "[2,1,3,0,3,3]"
        self.DustSensorSCL = 20
        self.DustSensorSDA = 21
        self.DustSensorPowerPin = 12
        self.GPIO_Pin_PowerDrive_Sig1 = 4
        self.GPIO_Pin_PowerDrive_Sig2 = 4
        self.WATCHDOGTRIGGER = 6
        
        
    def readJSON(self):


        if os.path.isfile('SkyWeather2.JSON'):
            print ("SkyWeather2.JSON File exists")
            with open('SkyWeather2.JSON') as json_file:
                data = json.load(json_file)

                self.SWDEBUG = data['SWDEBUG']
                self.enable_MySQL_Logging = data['enable_MySQL_Logging']
                self.MySQL_Password = data['MySQL_Password']
                self.enable_WLAN_Detection = data['enable_WLAN_Detection']
                self.PingableRouterAddress = data['PingableRouterAddress']
                self.mailUser = data['mailUser']
                self.mailPassword = data['mailPassword']
                self.notifyAddress = data['notifyAddress']
                self.fromAddress = data['fromAddress']
                self.enableText = data['enableText']
                self.textnotifyAddress = data['textnotifyAddress']
                self.runLEDs = data['runLEDs']
                self.SolarMAX_Present = data['SolarMAX_Present']
                self.SolarMAX_Type = data['SolarMAX_Type']
                self.BMP280_Altitude_Meters = data['BMP280_Altitude_Meters']
                self.Sunlight_Gain = data['Sunlight_Gain']
                self.USEWEATHERSTEM = data['USEWEATHERSTEM']
                self.INTERVAL_CAM_PICS__SECONDS = data['INTERVAL_CAM_PICS__SECONDS']
                self.STATIONKEY = data['STATIONKEY']
                self.WeatherUnderground_Present = data['WeatherUnderground_Present']
                self.WeatherUnderground_StationID = data['WeatherUnderground_StationID']
                self.WeatherUnderground_StationKey = data['WeatherUnderground_StationKey']
                self.USEBLYNK = data['USEBLYNK']
                self.BLYNK_AUTH = data['BLYNK_AUTH']
                self.AS3935_Lightning_Config = data['AS3935_Lightning_Config']
                self.DustSensorSCL = data['DustSensorSCL']
                self.DustSensorSDA = data['DustSensorSDA']
                self.DustSensorPowerPin = data['DustSensorPowerPin']
                self.GPIO_Pin_PowerDrive_Sig1 = data['GPIO_Pin_PowerDrive_Sig1']
                self.GPIO_Pin_PowerDrive_Sig2 = data['GPIO_Pin_PowerDrive_Sig2']
                self.WATCHDOGTRIGGER = data['WATCHDOGTRIGGER']

        else:
            print ("SkyWeather2.JSON File does not exist")
            self.setDefaults()




    def saveJSON(self):


        data = {}
        data['key'] = 'value'
        
        data['ProgramName'] = 'SkyWeather2' 
        data['ConfigVersion'] = '001'        

        data['SWDEBUG'] = self.F_SWDEBUG.get_value()
        data['enable_MySQL_Logging'] = self.F_enable_MySQL_Logging.get_value()
        data['MySQL_Password'] = self.F_MySQL_Password.get_value()
        data['enable_WLAN_Detection'] = self.F_enable_WLAN_Detection.get_value()
        data['PingableRouterAddress'] = self.F_PingableRouterAddress.get_value()
        data['mailUser'] = self.F_mailUser.get_value()
        data['mailPassword'] = self.F_mailPassword.get_value()
        data['notifyAddress'] = self.F_notifyAddress.get_value()
        data['fromAddress'] = self.F_fromAddress.get_value()
        data['enableText'] = self.F_enableText.get_value()
        data['textnotifyAddress'] = self.F_textnotifyAddress.get_value()
        data['runLEDs'] = self.F_runLEDs.get_value()
        data['SolarMAX_Present'] = self.F_SolarMAX_Present.get_value()
        data['SolarMAX_Type'] = self.F_SolarMAX_Type.get_value()
        data['BMP280_Altitude_Meters'] = self.F_BMP280_Altitude_Meters.get_value()
        data['Sunlight_Gain'] = self.F_Sunlight_Gain.get_value()
        data['USEWEATHERSTEM'] = self.F_USEWEATHERSTEM.get_value()
        data['INTERVAL_CAM_PICS__SECONDS'] = self.F_INTERVAL_CAM_PICS__SECONDS.get_value()
        data['STATIONKEY'] = self.F_STATIONKEY.get_value()
        data['WeatherUnderground_Present'] = self.F_WeatherUnderground_Present.get_value()
        data['WeatherUnderground_StationID'] = self.F_WeatherUnderground_StationID.get_value()
        data['WeatherUnderground_StationKey'] = self.F_WeatherUnderground_StationKey.get_value()
        data['USEBLYNK'] = self.F_USEBLYNK.get_value()
        data['BLYNK_AUTH'] = self.F_BLYNK_AUTH.get_value()
        data['AS3935_Lightning_Config'] = self.F_AS3935_Lightning_Config.get_value()
        data['DustSensorSCL'] = self.F_DustSensorSCL.get_value()
        data['DustSensorSDA'] = self.F_DustSensorSDA.get_value()
        data['DustSensorPowerPin'] = self.F_DustSensorPowerPin.get_value()
        data['GPIO_Pin_PowerDrive_Sig1'] = self.F_GPIO_Pin_PowerDrive_Sig1.get_value()
        data['GPIO_Pin_PowerDrive_Sig2'] = self.F_GPIO_Pin_PowerDrive_Sig2.get_value()
        data['WATCHDOGTRIGGER'] = self.F_WATCHDOGTRIGGER.get_value()

        json_data = json.dumps(data)        
        print (json_data)
        
        with open('SkyWeather2.JSON', 'w') as outfile:
            json.dump(data, outfile)

    # screen builds

    def buildScreen1(self):


        #screen 1

        vbox = VBox(width=500, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=80, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=80, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=80, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=80, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-TB', width=80, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=80, height=30)
        m6.onclick.do(self.menu_screen6_clicked)

        menu.append([m1, m2, m3, m4, m5, m6])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 1
        screen1header = gui.Label("Debug / MySQL / WLAN Tab", style='margin:10px')
        vbox.append(screen1header)




        #debug config

        debugheader = gui.Label("Debug Configuration", style='position:absolute; left:5px; top:30px; '+self.headerstyle)
        vbox.append(debugheader,'debugheader') 
        self.F_SWDEBUG = gui.CheckBoxLabel( 'enable SW Debugging', self.SWDEBUG, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_SWDEBUG,'self.F_SWDEBUG') 
       
        # mysql configurattion 
        mysqlheader = gui.Label("MySQL Configuration", style='position:absolute; left:5px; top:40px;'+self.headerstyle)
        vbox.append(mysqlheader,'mysqlheader') 
        self.F_enable_MySQL_Logging = gui.CheckBoxLabel('enable MySQL Logging ', False , height=30, style='margin:5px; background:LightGray')
        vbox.append(self.F_enable_MySQL_Logging,'enable_MySQL_Logging') 

        plabel = gui.Label("MySQL Password", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        self.F_MySQL_Password = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_MySQL_Password.set_value(self.MySQL_Password)
        vbox.append(self.F_MySQL_Password,'MySQLPassword') 
        
        #WLAN Configuration 
        WLheader = gui.Label("WLAN Check in SkyWeather2 ", style=self.headerstyle)
        vbox.append(WLheader,'WLheader') 
        self.F_enable_WLAN_Detection = gui.CheckBoxLabel('enable WLAN Detection', self.enable_WLAN_Detection , height=30, style='margin:5px; background:LightGray')
        vbox.append(self.F_enable_WLAN_Detection,'enable_WLAN_Detection') 

        plabel = gui.Label("Pingable Router Address ", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        self.F_PingableRouterAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_PingableRouterAddress.set_value(self.PingableRouterAddress)
        
        vbox.append(self.F_PingableRouterAddress,'PingableRouterAddress') 

        return vbox


    def buildScreen2(self):

        #screen 2

        vbox = VBox(width=500, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=80, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=80, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=80, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=80, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-TB', width=80, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=80, height=30)
        m6.onclick.do(self.menu_screen6_clicked)

        menu.append([m1, m2, m3, m4, m5, m6])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 
        screenheader = gui.Label("Main and Text Notification Tab", style='margin:10px')
        vbox.append(screenheader)
        
        # mail and text notifications
        MTheader = gui.Label("Mail and Text Notification Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(MTheader,'MTheader') 

        plabel = gui.Label("Mail User", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        self.F_mailUser = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_mailUser.set_value(self.mailUser)
        vbox.append(self.F_mailUser,'mailUser') 

        p1label = gui.Label("Mail Password", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p1label,'p1label') 
        
        self.F_mailPassword = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_mailPassword.set_value(self.mailPassword)
        vbox.append(self.F_mailPassword,'mailPassword') 

        p3label = gui.Label("Notify Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p3label,'p3label') 
        
        self.F_notifyAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_notifyAddress.set_value(self.notifyAddress)
        vbox.append(self.F_notifyAddress,'notifyAddress') 

        p4label = gui.Label("From Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p4label,'p4label') 
        
        self.F_fromAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_fromAddress.set_value(self.fromAddress)
        vbox.append(self.F_fromAddress,'fromAddress') 

        self.F_enableText = gui.CheckBoxLabel( 'enable Text Messaging', self.SWDEBUG, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_enableText,'self.F_enableText') 

        p5label = gui.Label("Text Notify Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label,'p5label') 
        
        self.F_textnotifyAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_textnotifyAddress.set_value(self.textnotifyAddress)
        vbox.append(self.F_textnotifyAddress,'textnotifyAddress') 

        return vbox
    
    def buildScreen3(self):

        #screen 3

        vbox = VBox(width=500, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       

       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=80, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=80, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=80, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=80, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-TB', width=80, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=80, height=30)
        m6.onclick.do(self.menu_screen6_clicked)

        menu.append([m1, m2, m3, m4, m5, m6])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 1
        screen1header = gui.Label("Pixel / NeoPixel / SolarMAX Configuration Tab", style='margin:10px')
        vbox.append(screen1header)


        PNheader = gui.Label("Pixel/NeoPixel LED Support", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(PNheader,'PNheader') 

        self.F_runLEDs = gui.CheckBoxLabel( 'Enable Pixel/NeoPixel', self.runLEDs, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_runLEDs,'self.F_runLEDs') 

        P1Nheader = gui.Label("Solar Max Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P1Nheader,'P1Nheader') 

        self.F_SolarMAX_Present = gui.CheckBoxLabel( 'SolarMAX Present', self.SolarMAX_Present, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_SolarMAX_Present,'self.F_SolarMAX_Present') 


        self.F_SolarMAX_Type = gui.DropDown(width='200px')
        self.F_SolarMAX_Type.style.update({'font-size':'large'})
        self.F_SolarMAX_Type.add_class("form-control dropdown")
        item1 = gui.DropDownItem("LEAD")
        item2 = gui.DropDownItem("LIPO")
        self.F_SolarMAX_Type.append(item1,'item1')
        self.F_SolarMAX_Type.append(item2,'item2')
        self.F_SolarMAX_Type.select_by_value(self.SolarMAX_Type)
        vbox.append(self.F_SolarMAX_Type, 'self.F_SolarMAX_Type')

        P2Nheader = gui.Label("Station Height in Meters", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P2Nheader,'P2Nheader') 

        self.F_BMP280_Altitude_Meters = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_BMP280_Altitude_Meters.set_value(str(self.BMP280_Altitude_Meters))
        vbox.append(self.F_BMP280_Altitude_Meters,'BMP280_Altitude_Meters') 

        P3Nheader = gui.Label("Sunlight Gain", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P3Nheader,'P3Nheader') 

        self.F_Sunlight_Gain = gui.DropDown(width='200px')
        self.F_Sunlight_Gain.style.update({'font-size':'large'})
        self.F_Sunlight_Gain.add_class("form-control dropdown")
        item1 = gui.DropDownItem("High")
        item2 = gui.DropDownItem("Low")
        self.F_Sunlight_Gain.append(item1,'item1')
        self.F_Sunlight_Gain.append(item2,'item2')
        if (self.Sunlight_Gain == 0):
            self.F_Sunlight_Gain.select_by_value("Low")
        if (self.Sunlight_Gain == 1):
            self.F_Sunlight_Gain.select_by_value("High")
        vbox.append(self.F_Sunlight_Gain, 'self.F_Sunlight_Gain')




        return vbox

    def buildScreen4(self):
        #screen 4

        vbox = VBox(width=500, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=80, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=80, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=80, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=80, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-TB', width=80, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=80, height=30)
        m6.onclick.do(self.menu_screen6_clicked)

        menu.append([m1, m2, m3, m4, m5, m6])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 
        screen1header = gui.Label("WeatherSTEM / WeatherUnderGround Configuration Tab", style='margin:10px')
        vbox.append(screen1header)


        P3Nheader = gui.Label("WeatherSTEM Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P3Nheader,'P3Nheader') 

        self.F_USEWEATHERSTEM = gui.CheckBoxLabel( 'Enable WeatherSTEM', self.USEWEATHERSTEM, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_USEWEATHERSTEM,'self.F_USEWEATHERSTEM') 

        p5label = gui.Label("Interval between pictures (seconds)", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label,'p5label') 
        
        self.F_INTERVAL_CAM_PICS__SECONDS = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_INTERVAL_CAM_PICS__SECONDS.set_value(str(self.INTERVAL_CAM_PICS__SECONDS))
        vbox.append(self.F_INTERVAL_CAM_PICS__SECONDS,'INTERVAL_CAM_PICS__SECONDS') 

        p6label = gui.Label("SkyWeather Station Key", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p6label,'p6label') 
        
        self.F_STATIONKEY = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_STATIONKEY.set_value(str(self.STATIONKEY))
        vbox.append(self.F_STATIONKEY,'STATIONKEY') 

        #

        P4Nheader = gui.Label("WeatherUnderGround Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P4Nheader,'P4Nheader') 
        
        self.F_WeatherUnderground_Present = gui.CheckBoxLabel( 'Enable WeatherUnderground', self.WeatherUnderground_Present, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_WeatherUnderground_Present,'self.F_WeatherUnderground_Present') 

        p7label = gui.Label("Station ID", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p7label,'p7label') 
        
        self.F_WeatherUnderground_StationID = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_WeatherUnderground_StationID.set_value(self.WeatherUnderground_StationID)
        vbox.append(self.F_WeatherUnderground_StationID,'WeatherUnderground_StationID') 

        p8label = gui.Label("Station Key", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p8label,'p8label') 
        
        self.F_WeatherUnderground_StationKey = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_WeatherUnderground_StationKey.set_value(self.WeatherUnderground_StationKey)
        vbox.append(self.F_WeatherUnderground_StationKey,'WeatherUnderground_StationKey') 

        return vbox

    def buildScreen5(self):
        #screen 5

        vbox = VBox(width=500, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'

        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=80, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=80, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=80, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=80, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-TB', width=80, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=80, height=30)
        m6.onclick.do(self.menu_screen6_clicked)

        menu.append([m1, m2, m3, m4, m5, m6])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 1
        screen1header = gui.Label("Blynk / ThunderBoard AS3935 Tab", style='margin:10px')
        vbox.append(screen1header)



        P5Nheader = gui.Label("Blynk Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 

        self.F_USEBLYNK = gui.CheckBoxLabel( 'Enable Blynk', self.USEBLYNK, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_USEBLYNK,'self.F_USEBLYNK') 

        p8label = gui.Label("Blynk App Authorization", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p8label,'p8label') 
        
        self.F_BLYNK_AUTH = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_BLYNK_AUTH.set_value(self.BLYNK_AUTH)
        vbox.append(self.F_BLYNK_AUTH,'BLYNK_AUTH') 
        #
        P1Nheader = gui.Label("ThunderBoard AS3935 Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P1Nheader,'P1Nheader') 

        P2Nheader = gui.Label("Format:[NoiseFloor, Indoor, TuneCap, DisturberDetection, WatchDogThreshold, SpikeDetection] ", style='position:absolute; left:5px; top:30px;'+self.labelstyle)
        vbox.append(P2Nheader,'P2Nheader') 
        

        p9label = gui.Label("Thunderboard Configuration", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p9label,'p9label') 
        
        self.F_AS3935_Lightning_Config  = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_AS3935_Lightning_Config .set_value(self.AS3935_Lightning_Config )
        vbox.append(self.F_AS3935_Lightning_Config ,'AS3935_Lightning_Config ') 


        return vbox

    def buildScreen6(self):
        #screen 6

        vbox = VBox(width=500, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=80, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=80, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=80, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=80, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-TB', width=80, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=80, height=30)
        m6.onclick.do(self.menu_screen6_clicked)

        menu.append([m1, m2, m3, m4, m5, m6])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 
        screenheader = gui.Label("Pin Config", style='margin:10px')
        vbox.append(screenheader)
        
        # short headers

        shortlabelstyle = 'font-family:monospace; width:200; font-size:15px; margin:5px; background:LightGray' 



        P5Nheader = gui.Label("Pin Configurations", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 

        p8label = gui.Label("Dust Sensor SCL Pin", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p8label,'p8label') 
        
        self.F_DustSensorSCL = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_DustSensorSCL.set_value(str(self.DustSensorSCL))
        vbox.append(self.F_DustSensorSCL,'DustSensorSCL') 

        p9label = gui.Label("Dust Sensor SDA Pin", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p9label,'p9label') 
        
        self.F_DustSensorSDA = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_DustSensorSDA.set_value(str(self.DustSensorSDA))
        vbox.append(self.F_DustSensorSDA,'DustSensorSDA') 

        p1label = gui.Label("Dust Sensor Power Pin", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p1label,'p1label') 
        
        self.F_DustSensorPowerPin = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_DustSensorPowerPin.set_value(str(self.DustSensorPowerPin))
        vbox.append(self.F_DustSensorPowerPin,'DustSensorPowerPin') 

        p2label = gui.Label("GPIO Fan Power Pin Sig1", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p2label,'p2label') 
        
        self.F_GPIO_Pin_PowerDrive_Sig1 = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_GPIO_Pin_PowerDrive_Sig1.set_value(str(self.GPIO_Pin_PowerDrive_Sig1))
        vbox.append(self.F_GPIO_Pin_PowerDrive_Sig1,'GPIO_Pin_PowerDrive_Sig1') 

        p3label = gui.Label("GPIO Fan Power Pin Sig2", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p3label,'p3label') 
        
        self.F_GPIO_Pin_PowerDrive_Sig2 = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_GPIO_Pin_PowerDrive_Sig2.set_value(str(self.GPIO_Pin_PowerDrive_Sig2))
        vbox.append(self.F_GPIO_Pin_PowerDrive_Sig2,'GPIO_Pin_PowerDrive_Sig2') 

        p4label = gui.Label("WatchDog Trigger Pin", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p4label,'p4label') 
        
        self.F_WATCHDOGTRIGGER = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_WATCHDOGTRIGGER.set_value(str(self.WATCHDOGTRIGGER))
        vbox.append(self.F_WATCHDOGTRIGGER,'WATCHDOGTRIGGER') 


        return vbox



    def main(self):

        self.readJSON()


        widthBox = 700
        heightBox = 800
        self.mainContainer = Container(width=widthBox, height=heightBox, margin='0px auto', style="position: relative")
        self.mainContainer.style['justify-content'] = 'flex-start'
        self.mainContainer.style['align-items'] = 'flex-start'


        logo = SuperImage("./static/SkyWeatherLogo.png", width=400, height =200)
        header = gui.Label("SkyWeather2 Configuration Tool", style='position:absolute; left:5px; top:30px')
        version = gui.Label("Version 002",style='position:absolute; left:5px; top:50px') 
        # bottom buttons

        cancel = gui.Button('Cancel',style='position:absolute; left:550px; height: 30px; width:100px; margin:10px; top:5px')
        cancel.onclick.do(self.onCancel)
        save = gui.Button('Save',style='position:absolute; left:400px; height: 30px; width:100px;  margin: 10px;  top:5px')
        save.onclick.do(self.onSave)
        exit = gui.Button('Save and Exit',style='position:absolute; left:475px; height: 30px; width:100px;  margin: 10px;  top:95px')
        exit.onclick.do(self.onExit)
        reset = gui.Button('Reset to Defaults',style='position:absolute; left:400px;height: 30px;   width:250px; margin: 10px; top:50px')
        reset.onclick.do(self.onReset)
        # appending a widget to another
        self.mainContainer.append(logo)
        self.mainContainer.append(header)
        self.mainContainer.append(version)
        self.mainContainer.append(cancel)
        self.mainContainer.append(save)
        self.mainContainer.append(exit)
        self.mainContainer.append(reset)


        # configuation fields
       

        self.headerstyle= 'width:400px; font-family:monospace; font-size:20px; margin:10px; background:LightBlue'
        self.labelstyle = 'font-family:monospace; font-size:15px; margin:5px; background:LightGray' 

        # build screens


        self.screen1 = self.buildScreen1()
        self.screen2 = self.buildScreen2()
        self.screen3 = self.buildScreen3()
        self.screen4 = self.buildScreen4()
        self.screen5 = self.buildScreen5()
        self.screen6 = self.buildScreen6()


        self.mainContainer.append(self.screen1,'screen1')
        



        # returning the root widget
        
        return self.mainContainer


    # listener functions


    def removeAllScreens(self):
        
        self.mainContainer.remove_child(self.screen1)
        self.mainContainer.remove_child(self.screen2)
        self.mainContainer.remove_child(self.screen3)
        self.mainContainer.remove_child(self.screen4)
        self.mainContainer.remove_child(self.screen5)
        self.mainContainer.remove_child(self.screen6)
        
    # listener functions

    def menu_screen1_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen1,'screen1')
        print("menu screen1 clicked")  

    def menu_screen2_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen2,'screen2')
        print("menu screen2 clicked")

    def menu_screen3_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen3,'screen3')
        print("menu screen3 clicked")

    def menu_screen4_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen4,'screen4')
        print("menu screen4 clicked")

    def menu_screen5_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen5,'screen5')
        print("menu screen5 clicked")

    def menu_screen6_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen6,'screen6')
        print("menu screen6 clicked")


    def onCancel(self, widget, name='', surname=''):
        print("onCancel clicked")
        self.saveJSON()
        self.server.server_starter_instance._alive = False
        self.server.server_starter_instance._sserver.shutdown()
        print("server stopped") 
        exit()
        
    def onExit(self, widget, name='', surname=''):
        # save and exit
        print("onSaveExit clicked")
        self.saveJSON()
        self.server.server_starter_instance._alive = False
        self.server.server_starter_instance._sserver.shutdown()
        print("server stopped") 
        exit()

    def onReset(self, widget, name='', surname=''):
        print("Reset clicked")
        self.removeAllScreens()
        self.mainContainer.append(self.screen1,'screen1')
        self.setDefaults()

        self.screen1 = self.buildScreen1()
        self.screen2 = self.buildScreen2()
        self.screen3 = self.buildScreen3()
        self.screen4 = self.buildScreen4()
        self.screen5 = self.buildScreen5()
        self.screen6 = self.buildScreen6()


        self.mainContainer.append(self.screen1,'screen1')
        
        
    def onSave(self, widget, name='', surname=''):
        print("onSave clicked")
        self.saveJSON()


#Configuration
configuration = {'config_enable_file_cache': True, 'config_multiple_instance': True, 'config_port': 8001, 'config_address': '0.0.0.0', 'config_start_browser': True, 'config_project_name': 'untitled', 'config_resourcepath': './res/'}

# starts the web server
#start(SkyWeatherConfigure, address='0.0.0.0', port=8001)

start(SkyWeatherConfigure, address=configuration['config_address'], port=configuration['config_port'],
                        multiple_instance=configuration['config_multiple_instance'],
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])

