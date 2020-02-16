import os
import time
import random
import threading
import remi.gui as gui
import urllib.request
from urllib.request import urlopen

from remi.gui import *
from remi import start, App

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
        self_BLYNK_AUTH = ""
        
        
        
    def readJSON(self):
        self.setDefaults()


    # screen builds

    def buildScreen1(self):


        #screen 1

        vbox = VBox(width=500, height=500, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Screen 1', width=100, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('Screen 2', width=100, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('Screen 3', width=100, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('Screen 4', width=100, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('Screen 5', width=100, height=30)
        m5.onclick.do(self.menu_screen5_clicked)

        menu.append([m1, m2, m3, m4, m5])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 1
        screen1header = gui.Label("screen 1", style='margin:10px')
        vbox.append(screen1header)




        #debug config

        debugheader = gui.Label("Debug Configuration", style='position:absolute; left:5px; top:30px; '+self.headerstyle)
        vbox.append(debugheader,'debugheader') 
        F_SWDEBUG = gui.CheckBoxLabel( 'enable SW Debugging', self.SWDEBUG, height=30, style='margin:5px; background: LightGray ')
        vbox.append(F_SWDEBUG,'F_SWDEBUG') 
       
        # mysql configurattion 
        mysqlheader = gui.Label("MySQL Configuration", style='position:absolute; left:5px; top:40px;'+self.headerstyle)
        vbox.append(mysqlheader,'mysqlheader') 
        F_enable_MySQL_Logging = gui.CheckBoxLabel('enable MySQL Logging ', False , height=30, style='margin:5px; background:LightGray')
        vbox.append(F_enable_MySQL_Logging,'enable_MySQL_Logging') 

        plabel = gui.Label("MySQL Password", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        F_MySQL_Password = gui.TextInput(width=300, height=30, style="margin:5px")
        F_MySQL_Password.set_value(self.MySQL_Password)
        vbox.append(F_MySQL_Password,'MySQLPassword') 
        
        #WLAN Configuration 
        WLheader = gui.Label("WLAN Check in SkyWeather2 ", style=self.headerstyle)
        vbox.append(WLheader,'WLheader') 
        F_enable_WLAN_Detection = gui.CheckBoxLabel('enable WLAN Detection', self.enable_WLAN_Detection , height=30, style='margin:5px; background:LightGray')
        vbox.append(F_enable_WLAN_Detection,'enable_WLAN_Detection') 

        plabel = gui.Label("Pingable Router Address ", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        F_PingableRouterAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        F_PingableRouterAddress.set_value(self.PingableRouterAddress)
        
        vbox.append(F_PingableRouterAddress,'PingableRouterAddress') 

        return vbox


    def buildScreen2(self):

        #screen 2

        vbox = VBox(width=500, height=500, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Screen 1', width=100, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('Screen 2', width=100, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('Screen 3', width=100, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('Screen 4', width=100, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('Screen 5', width=100, height=30)
        m5.onclick.do(self.menu_screen5_clicked)

        menu.append([m1, m2, m3, m4, m5])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 
        screenheader = gui.Label("screen 2", style='margin:10px')
        vbox.append(screenheader)
        
        # mail and text notifications
        MTheader = gui.Label("Mail and Text Notification Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(MTheader,'MTheader') 

        plabel = gui.Label("Mail User", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        F_mailUser = gui.TextInput(width=300, height=30, style="margin:5px")
        F_mailUser.set_value(self.mailUser)
        vbox.append(F_mailUser,'mailUser') 

        p1label = gui.Label("Mail Password", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p1label,'p1label') 
        
        F_mailPassword = gui.TextInput(width=300, height=30, style="margin:5px")
        F_mailPassword.set_value(self.mailPassword)
        vbox.append(F_mailPassword,'mailPassword') 

        p3label = gui.Label("Notify Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p3label,'p3label') 
        
        F_notifyAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        F_notifyAddress.set_value(self.notifyAddress)
        vbox.append(F_notifyAddress,'notifyAddress') 

        p4label = gui.Label("From Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p4label,'p4label') 
        
        F_fromAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        F_fromAddress.set_value(self.fromAddress)
        vbox.append(F_fromAddress,'fromAddress') 

        F_enableText = gui.CheckBoxLabel( 'enable Text Messaging', self.SWDEBUG, height=30, style='margin:5px; background: LightGray ')
        vbox.append(F_enableText,'F_enableText') 

        p5label = gui.Label("Text Notify Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label,'p5label') 
        
        F_textnotifyAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        F_textnotifyAddress.set_value(self.textnotifyAddress)
        vbox.append(F_textnotifyAddress,'textnotifyAddress') 

        return vbox
    
    def buildScreen3(self):

        #screen 3

        vbox = VBox(width=500, height=500, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Screen 1', width=100, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('Screen 2', width=100, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('Screen 3', width=100, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('Screen 4', width=100, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('Screen 5', width=100, height=30)
        m5.onclick.do(self.menu_screen5_clicked)

        menu.append([m1, m2, m3, m4, m5])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 
        screenheader = gui.Label("screen 3", style='margin:10px')
        vbox.append(screenheader)

        PNheader = gui.Label("Pixel/NeoPixel LED Support", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(PNheader,'PNheader') 

        F_runLEDs = gui.CheckBoxLabel( 'Enable Pixel/NeoPixel', self.runLEDs, height=30, style='margin:5px; background: LightGray ')
        vbox.append(F_runLEDs,'F_runLEDs') 

        P1Nheader = gui.Label("Solar Max Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P1Nheader,'P1Nheader') 

        F_SolarMAX_Present = gui.CheckBoxLabel( 'SolarMAX Present', self.SolarMAX_Present, height=30, style='margin:5px; background: LightGray ')
        vbox.append(F_SolarMAX_Present,'F_SolarMAX_Present') 


        F_SolarMAX_Type = gui.DropDown(width='200px')
        F_SolarMAX_Type.style.update({'font-size':'large'})
        F_SolarMAX_Type.add_class("form-control dropdown")
        item1 = gui.DropDownItem("LEAD")
        item2 = gui.DropDownItem("LIPO")
        F_SolarMAX_Type.append(item1,'item1')
        F_SolarMAX_Type.append(item2,'item2')
        F_SolarMAX_Type.select_by_value(self.SolarMAX_Type)
        vbox.append(F_SolarMAX_Type, 'F_SolarMAX_Type')

        P2Nheader = gui.Label("Station Height in Meters", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P2Nheader,'P2Nheader') 

        F_BMP280_Altitude_Meters = gui.TextInput(width=300, height=30, style="margin:5px")
        F_BMP280_Altitude_Meters.set_value(str(self.BMP280_Altitude_Meters))
        vbox.append(F_BMP280_Altitude_Meters,'BMP280_Altitude_Meters') 

        P3Nheader = gui.Label("Sunlight Gain", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P3Nheader,'P3Nheader') 

        F_Sunlight_Gain = gui.DropDown(width='200px')
        F_Sunlight_Gain.style.update({'font-size':'large'})
        F_Sunlight_Gain.add_class("form-control dropdown")
        item1 = gui.DropDownItem("High")
        item2 = gui.DropDownItem("Low")
        F_Sunlight_Gain.append(item1,'item1')
        F_Sunlight_Gain.append(item2,'item2')
        if (self.Sunlight_Gain == 0):
            F_Sunlight_Gain.select_by_value("Low")
        if (self.Sunlight_Gain == 1):
            F_Sunlight_Gain.select_by_value("High")
        vbox.append(F_Sunlight_Gain, 'F_Sunlight_Gain')




        return vbox

    def buildScreen4(self):
        #screen 4

        vbox = VBox(width=500, height=500, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Screen 1', width=100, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('Screen 2', width=100, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('Screen 3', width=100, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('Screen 4', width=100, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('Screen 5', width=100, height=30)
        m5.onclick.do(self.menu_screen5_clicked)

        menu.append([m1, m2, m3, m4, m5])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)



        vbox.append(menubar)

        #screen 
        screenheader = gui.Label("screen 4", style='margin:10px')
        vbox.append(screenheader)


        P3Nheader = gui.Label("WeatherSTEM Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P3Nheader,'P3Nheader') 

        F_USEWEATHERSTEM = gui.CheckBoxLabel( 'Enable WeatherSTEM', self.USEWEATHERSTEM, height=30, style='margin:5px; background: LightGray ')
        vbox.append(F_USEWEATHERSTEM,'F_USEWEATHERSTEM') 

        P4Nheader = gui.Label("WeatherUnderGround Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P4Nheader,'P4Nheader') 
        
        F_WeatherUnderground_Present = gui.CheckBoxLabel( 'Enable WeatherUnderground', self.WeatherUnderground_Present, height=30, style='margin:5px; background: LightGray ')
        vbox.append(F_WeatherUnderground_Present,'F_WeatherUnderground_Present') 

        P5Nheader = gui.Label("Blynk Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 

        F_USEBLYNK = gui.CheckBoxLabel( 'Enable Blynk', self.USEBLYNK, height=30, style='margin:5px; background: LightGray ')
        vbox.append(F_USEBLYNK,'F_USEBLYNK') 

        return vbox

    def buildScreen5(self):
        #screen 5

        vbox = VBox(width=500, height=500, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('Screen 1', width=100, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('Screen 2', width=100, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('Screen 3', width=100, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('Screen 4', width=100, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('Screen 5', width=100, height=30)
        m5.onclick.do(self.menu_screen5_clicked)

        menu.append([m1, m2, m3, m4, m5])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 
        screenheader = gui.Label("screen 5", style='margin:10px')
        vbox.append(screenheader)

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

        cancel = gui.Button('Cancel',style='position:absolute; left:530px; height: 30px; width:100px; margin:10px; top:5px')
        save = gui.Button('Save',style='position:absolute; left:400px; height: 30px; width:100px;  margin: 10px;  top:5px')
        restart = gui.Button('Kill SkyWeather2 and Restart',style='position:absolute; left:400px;height: 30px;   width:250px; margin: 10px; top:50px')
        # appending a widget to another
        self.mainContainer.append(logo)
        self.mainContainer.append(header)
        self.mainContainer.append(version)
        self.mainContainer.append(cancel)
        self.mainContainer.append(save)
        self.mainContainer.append(restart)


        # configuation fields
       

        self.headerstyle= 'width:400px; font-family:monospace; font-size:20px; margin:10px; background:LightBlue'
        self.labelstyle = 'font-family:monospace; font-size:15px; margin:5px; background:LightGray' 

        # build screens


        self.screen1 = self.buildScreen1()
        self.screen2 = self.buildScreen2()
        self.screen3 = self.buildScreen3()
        self.screen4 = self.buildScreen4()
        self.screen5 = self.buildScreen5()


        #self.mainContainer.append(self.screen1,'screen1')
        self.mainContainer.append(self.screen4,'screen4')
        

        # setting the listener for the onclick event of the buttons
        cancel.onclick.do(self.on_button_pressed, "Name")
        save.onclick.do(self.on_button_pressed, "Name", "Surname")


        # returning the root widget
        
        return self.mainContainer


    # listener functions


    def removeAllScreens(self):
        
        self.mainContainer.remove_child(self.screen1)
        self.mainContainer.remove_child(self.screen2)
        self.mainContainer.remove_child(self.screen3)
        self.mainContainer.remove_child(self.screen4)
        self.mainContainer.remove_child(self.screen5)
        
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




    def on_button_pressed(self, widget, name='', surname=''):
        self.lbl.set_text('Button pressed!')
        widget.set_text('Hello ' + name + ' ' + surname)


#Configuration
configuration = {'config_enable_file_cache': True, 'config_multiple_instance': True, 'config_port': 8001, 'config_address': '0.0.0.0', 'config_start_browser': True, 'config_project_name': 'untitled', 'config_resourcepath': './res/'}

# starts the web server
#start(SkyWeatherConfigure, address='0.0.0.0', port=8001)

start(SkyWeatherConfigure, address=configuration['config_address'], port=configuration['config_port'],
                        multiple_instance=configuration['config_multiple_instance'],
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])

