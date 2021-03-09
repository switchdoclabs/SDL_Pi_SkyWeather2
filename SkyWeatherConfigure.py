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

# radio button

class LabelForInputs(gui.Widget, gui._MixinTextualWidget):
    """ Non editable text label widget. Specifically designed to be used in conjunction with checkboxes and radiobuttons
    """

    def __init__(self, text, widget_for_instance, *args, **kwargs):
        """
        Args:
            text (str): The string content that have to be displayed in the Label.
            widget_for_instance (gui.Widget): checkbox or radiobutton instance
            kwargs: See Container.__init__()
        """
        super(LabelForInputs, self).__init__(*args, **kwargs)
        self.type = 'label'
        self.attributes['for'] = widget_for_instance.identifier
        self.set_text(text)

class InputCheckable(gui.Input):
    """It is the base class for checkable widgets (Switch, RadioButton, Checkbox).
        Checkable are the widgets that contains attribute 'checked' to determine the status
        The developer has to pass the the argument _type to the constructor
        to determine the kind of widget.
    """

    def __init__(self, status_on=False, input_type='checkbox', *args, **kwargs):
        """
        Args:
            status_on (bool):
            kwargs: See Widget.__init__()
        """
        super(InputCheckable, self).__init__(input_type, *args, **kwargs)
        self.set_value(status_on)
        self.attributes[gui.Widget.EVENT_ONCHANGE] = \
            "var params={};params['value']=document.getElementById('%(emitter_identifier)s').checked;" \
            "sendCallbackParam('%(emitter_identifier)s','%(event_name)s',params);" % \
            {'emitter_identifier': str(self.identifier), 'event_name': gui.Widget.EVENT_ONCHANGE}

    @gui.decorate_event
    def onchange(self, value):
        value = value in ('True', 'true')
        self.set_value(value)
        self._set_updated()
        return (value,)

    def set_value(self, status_on):
        if status_on:
            self.attributes['checked'] = 'checked'
        else:
            if 'checked' in self.attributes:
                del self.attributes['checked']

    def get_value(self):
        """
        Returns:
            bool:
        """
        return 'checked' in self.attributes



class RadioButton(InputCheckable):
    """RadioButton widget, useful for exclusive selection.
        different radiobuttons have to be assigned to the
        same group name in order to switch exclusively.
    """

    @property
    def attr_name(self):
        return self.attributes.get('name', '')

    @attr_name.setter
    def attr_name(self, value):
        self.attributes['name'] = str(value)

    def __init__(self, status_on=False, group='group', *args, **kwargs):
        """
        Args:
            status_on (bool): the initial value
            group (str): the group name. RadioButtons with same group will be exclusively activated
            kwargs: See Widget.__init__()
        """
        super(RadioButton, self).__init__(status_on, input_type='radio', *args, **kwargs)
        self.attr_name = group

    def set_value(self, status_on):
        InputCheckable.set_value(self, status_on)

        # if on and has a parent, all other radios with same group name are switched off
        if status_on and self.get_parent():
            for w in self.get_parent().children.values():
                if isinstance(w, type(self)):
                    if w.identifier != self.identifier:
                        if w.get_group() == self.get_group():
                            w.set_value(False)

    def set_group(self, group_name):
        self.attr_name = group_name

    def get_group(self):
        return self.attr_name

class RadioButtonWithLabel(gui.Container):
    _radio = None
    _label = None

    @property
    def text(self):
        return self._label.get_text()

    @text.setter
    def text(self, value):
        self._label.set_text(value)

    @property
    def attr_name(self):
        return self._radio.attr_name

    @attr_name.setter
    def attr_name(self, value):
        self._radio.attr_name = str(value)

    def __init__(self, text='radiobutton', status_on=False, group='group', *args, **kwargs):
        """
        Args:
            text (str): the text label
            status_on (bool): the initial value
            group (str): the group name. RadioButtons with same group will be exclusively activated
            kwargs: See Widget.__init__()
        """
        super(RadioButtonWithLabel, self).__init__(*args, **kwargs)

        self._radio = RadioButton(status_on, group=group)
        self.append(self._radio, key='radio')

        self._label = LabelForInputs(text, self._radio)
        self.append(self._label, key='label')

        self._radio.onchange.connect(self.onchange)

    @gui.decorate_event
    def onchange(self, widget, value):
        self.__update_other_radios()
        return (value,)

    def get_text(self):
        return self._label.text

    def set_text(self, text):
        self._label.text = text

    def set_group(self, group_name):
        self.attr_name = group_name

    def get_group(self):
        return self.attr_name

    def get_value(self):
        return self._radio.get_value()

    def set_value(self, value):
        """ Args:
                value (bool): defines the checked status for the radio button
        """
        self._radio.set_value(value)
        self.__update_other_radios()

    def __update_other_radios(self):
        # if on and has a parent,
        # all other radios, in the same container,
        # with same group name are switched off
        if self.get_value() and self.get_parent():
            for w in self.get_parent().children.values():
                if isinstance(w, type(self)):
                    if w.identifier != self.identifier:
                        if w.get_group() == self.get_group():
                            w.set_value(False)



#############
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
        self.USEWSLIGHTNING = False
        self.USEWSAQI = False
        self.USEWSSKYCAM = False
        self.ALTWSSKYCAM = False
        self.DustSensorSCL = 20
        self.DustSensorSDA = 21
        self.DustSensorPowerPin = 5
        self.GPIO_Pin_PowerDrive_Sig1 = 4
        self.GPIO_Pin_PowerDrive_Sig2 = 4
        self.WATCHDOGTRIGGER = 6
        self.Camera_Night_Enable =  False
        self.Camera_Rotation =  0
        self.REST_Enable = False 
        self.MQTT_Enable = False 
        self.MQTT_Server_URL = "localhost" 
        self.MQTT_Port_Number = 1883 
        self.MQTT_Send_Seconds = 500 
        self.English_Metric = False
       
       
        self.dataDefaults = {} 

        self.dataDefaults['SWDEBUG'] = self.SWDEBUG 
        self.dataDefaults['enable_MySQL_Logging'] = self.enable_MySQL_Logging 
        self.dataDefaults['MySQL_Password'] = self.MySQL_Password 
        self.dataDefaults['enable_WLAN_Detection'] = self.enable_WLAN_Detection 
        self.dataDefaults['PingableRouterAddress'] = self.PingableRouterAddress 
        self.dataDefaults['mailUser'] = self.mailUser 
        self.dataDefaults['mailPassword'] = self.mailPassword 
        self.dataDefaults['notifyAddress'] = self.notifyAddress 
        self.dataDefaults['fromAddress'] = self.fromAddress 
        self.dataDefaults['enableText'] = self.enableText 
        self.dataDefaults['textnotifyAddress'] = self.textnotifyAddress 
        self.dataDefaults['runLEDs'] = self.runLEDs 
        self.dataDefaults['SolarMAX_Present'] = self.SolarMAX_Present 
        self.dataDefaults['BMP280_Altitude_Meters'] = self.BMP280_Altitude_Meters 
        self.dataDefaults['Sunlight_Gain'] = self.Sunlight_Gain 
        self.dataDefaults['USEWEATHERSTEM'] = self.USEWEATHERSTEM 
        self.dataDefaults['INTERVAL_CAM_PICS__SECONDS'] = self.INTERVAL_CAM_PICS__SECONDS 
        self.dataDefaults['STATIONKEY'] = self.STATIONKEY 
        self.dataDefaults['WeatherUnderground_Present'] = self.WeatherUnderground_Present 
        self.dataDefaults['WeatherUnderground_StationID'] = self.WeatherUnderground_StationID 
        self.dataDefaults['WeatherUnderground_StationKey'] = self.WeatherUnderground_StationKey 
        self.dataDefaults['USEBLYNK'] = self.USEBLYNK 
        self.dataDefaults['USEWSLIGHTNING'] = self.USEWSLIGHTNING 
        self.dataDefaults['USEWSAQI'] = self.USEWSAQI 
        self.dataDefaults['USEWSSKYCAM'] = self.USEWSSKYCAM 
        self.dataDefaults['ALTWSSKYCAM'] = self.ALTWSSKYCAM 
        self.dataDefaults['BLYNK_AUTH'] = self.BLYNK_AUTH 
        self.dataDefaults['DustSensorSCL'] = self.DustSensorSCL 
        self.dataDefaults['DustSensorSDA'] = self.DustSensorSDA 
        self.dataDefaults['DustSensorPowerPin'] = self.DustSensorPowerPin 
        self.dataDefaults['GPIO_Pin_PowerDrive_Sig1'] = self.GPIO_Pin_PowerDrive_Sig1 
        self.dataDefaults['GPIO_Pin_PowerDrive_Sig2'] = self.GPIO_Pin_PowerDrive_Sig2 
        self.dataDefaults['WATCHDOGTRIGGER'] = self.WATCHDOGTRIGGER 
        self.dataDefaults['Camera_Rotation'] = self.Camera_Rotation 
        self.dataDefaults['Camera_Night_Enable'] = self.Camera_Night_Enable 
        self.dataDefaults['REST_Enable'] = self.REST_Enable 
        self.dataDefaults['MQTT_Enable'] = self.MQTT_Enable 
        self.dataDefaults['MQTT_Server_URL'] = self.MQTT_Server_URL 
        self.dataDefaults['MQTT_Port_Number'] = self.MQTT_Port_Number 
        self.dataDefaults['MQTT_Send_Seconds'] = self.MQTT_Send_Seconds 
        self.dataDefaults['English_Metric'] = self.English_Metric 

    def getJSONValue(self, entry):
        try:
            returnData = self.JSONData[entry]
            return returnData
        except:
            print("JSON value not found - Set to Defaults:", entry)
            return self.dataDefaults[entry]



    def readJSON(self):

        self.setDefaults()

        if os.path.isfile('SkyWeather2.JSON'):
            print ("SkyWeather2.JSON File exists")
            with open('SkyWeather2.JSON') as json_file:
                self.JSONData = json.load(json_file)


                self.SWDEBUG = self.getJSONValue('SWDEBUG')
                self.enable_MySQL_Logging = self.getJSONValue('enable_MySQL_Logging')
                self.MySQL_Password = self.getJSONValue('MySQL_Password')
                self.enable_WLAN_Detection = self.getJSONValue('enable_WLAN_Detection')
                self.PingableRouterAddress = self.getJSONValue('PingableRouterAddress')
                self.mailUser = self.getJSONValue('mailUser')
                self.mailPassword = self.getJSONValue('mailPassword')
                self.notifyAddress = self.getJSONValue('notifyAddress')
                self.fromAddress = self.getJSONValue('fromAddress')
                self.enableText = self.getJSONValue('enableText')
                self.textnotifyAddress = self.getJSONValue('textnotifyAddress')
                self.runLEDs = self.getJSONValue('runLEDs')
                self.SolarMAX_Present = self.getJSONValue('SolarMAX_Present')
                self.BMP280_Altitude_Meters = self.getJSONValue('BMP280_Altitude_Meters')
                self.Sunlight_Gain = self.getJSONValue('Sunlight_Gain')
                self.USEWEATHERSTEM = self.getJSONValue('USEWEATHERSTEM')
                self.INTERVAL_CAM_PICS__SECONDS = self.getJSONValue('INTERVAL_CAM_PICS__SECONDS')
                self.STATIONKEY = self.getJSONValue('STATIONKEY')
                self.WeatherUnderground_Present = self.getJSONValue('WeatherUnderground_Present')
                self.WeatherUnderground_StationID = self.getJSONValue('WeatherUnderground_StationID')
                self.WeatherUnderground_StationKey = self.getJSONValue('WeatherUnderground_StationKey')
                self.USEBLYNK = self.getJSONValue('USEBLYNK')
                self.BLYNK_AUTH = self.getJSONValue('BLYNK_AUTH')
                self.USEWSLIGHTNING = self.getJSONValue('USEWSLIGHTNING')
                self.USEWSAQI = self.getJSONValue('USEWSAQI')
                self.USEWSSKYCAM = self.getJSONValue('USEWSSKYCAM')
                self.ALTWSSKYCAM = self.getJSONValue('ALTWSSKYCAM')
                self.DustSensorSCL = self.getJSONValue('DustSensorSCL')
                self.DustSensorSDA = self.getJSONValue('DustSensorSDA')
                self.DustSensorPowerPin = self.getJSONValue('DustSensorPowerPin')
                self.GPIO_Pin_PowerDrive_Sig1 = self.getJSONValue('GPIO_Pin_PowerDrive_Sig1')
                self.GPIO_Pin_PowerDrive_Sig2 = self.getJSONValue('GPIO_Pin_PowerDrive_Sig2')
                self.WATCHDOGTRIGGER = self.getJSONValue('WATCHDOGTRIGGER')
                self.Camera_Night_Enable = self.getJSONValue('Camera_Night_Enable')
                self.Camera_Rotation = self.getJSONValue('Camera_Rotation')
                self.REST_Enable = self.getJSONValue('REST_Enable')
                self.MQTT_Enable = self.getJSONValue('MQTT_Enable')
                self.MQTT_Server_URL = self.getJSONValue('MQTT_Server_URL')
                self.MQTT_Port_Number = self.getJSONValue('MQTT_Port_Number')
                self.MQTT_Send_Seconds = self.getJSONValue('MQTT_Send_Seconds')
                self.English_Metric = self.getJSONValue('English_Metric')

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
        data['USEWSLIGHTNING'] = self.F_USEWSLIGHTNING.get_value()
        data['USEWSAQI'] = self.F_USEWSAQI.get_value()
        data['USEWSSKYCAM'] = self.F_USEWSSKYCAM.get_value()
        data['ALTWSSKYCAM'] = self.F_ALTWSSKYCAM.get_value()
        data['DustSensorSCL'] = self.F_DustSensorSCL.get_value()
        data['DustSensorSDA'] = self.F_DustSensorSDA.get_value()
        data['DustSensorPowerPin'] = self.F_DustSensorPowerPin.get_value()
        data['GPIO_Pin_PowerDrive_Sig1'] = self.F_GPIO_Pin_PowerDrive_Sig1.get_value()
        data['GPIO_Pin_PowerDrive_Sig2'] = self.F_GPIO_Pin_PowerDrive_Sig2.get_value()
        data['WATCHDOGTRIGGER'] = self.F_WATCHDOGTRIGGER.get_value()
        data['REST_Enable'] = self.F_REST_Enable.get_value()
        data['Camera_Night_Enable'] = self.F_Camera_Night_Enable.get_value()
        data['Camera_Rotation'] = self.Camera_Rotation
        data['MQTT_Enable'] = self.F_MQTT_Enable.get_value()
        data['MQTT_Server_URL'] = self.F_MQTT_Server_URL.get_value()
        data['MQTT_Port_Number'] = self.F_MQTT_Port_Number.get_value()
        data['MQTT_Send_Seconds'] = self.F_MQTT_Send_Seconds.get_value()
        data['English_Metric'] = self.F_English_Metric.get_value()

        json_data = json.dumps(data)        
        
        with open('SkyWeather2.JSON', 'w') as outfile:
            json.dump(data, outfile)

    # screen builds

    def buildScreen1(self):


        #screen 1

        vbox = VBox(width=600, height=510, style="background: LightGray")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'


        #screen 1

       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=70, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=70, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=70, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=70, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-WS', width=70, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=70, height=30)
        m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('MQTTR', width=70, height=30)
        m7.onclick.do(self.menu_screen7_clicked)
        m8 = gui.MenuItem('Camera', width=70, height=30)
        m8.onclick.do(self.menu_screen8_clicked)

        menu.append([m1, m2, m3, m4, m5, m6, m7, m8])
    
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)
        vbox.append(menubar)


        screen1header = gui.Label("Debug / MySQL / WLAN Tab", style='margin:10px; background: LightGray')
        vbox.append(screen1header)

        #debug config

        debugheader = gui.Label("Debug Configuration", style='position:absolute; left:5px; top:30px; '+self.headerstyle)
        vbox.append(debugheader,'debugheader') 
        self.F_SWDEBUG = gui.CheckBoxLabel( 'enable SW Debugging', self.SWDEBUG, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_SWDEBUG,'self.F_SWDEBUG') 
       
        # mysql configurattion 
        mysqlheader = gui.Label("MySQL Configuration", style='position:absolute; left:5px; top:40px;'+self.headerstyle)
        vbox.append(mysqlheader,'mysqlheader') 
        self.F_enable_MySQL_Logging = gui.CheckBoxLabel('enable MySQL Logging ', self.enable_MySQL_Logging , height=30, style='margin:5px; background:LightGray')
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

        P6NTheader = gui.Label("English or Metric Units", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P6NTheader,'P6NTheader') 

        self.F_English_Metric = gui.CheckBoxLabel( 'English (not checked) or Metric (checked)', self.English_Metric, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_English_Metric,'self.F_English_Metric') 



        return vbox


    def buildScreen2(self):

        #screen 2

        vbox = VBox(width=600, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
       
    
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=70, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=70, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=70, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=70, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-WS', width=70, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=70, height=30)
        m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('MQTTR', width=70, height=30)
        m7.onclick.do(self.menu_screen7_clicked)
        m8 = gui.MenuItem('Camera', width=70, height=30)
        m8.onclick.do(self.menu_screen8_clicked)

        menu.append([m1, m2, m3, m4, m5, m6, m7, m8])
    
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

        vbox = VBox(width=600, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       

       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=70, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=70, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=70, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=70, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-WS', width=70, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=70, height=30)
        m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('MQTTR', width=70, height=30)
        m7.onclick.do(self.menu_screen7_clicked)
        m8 = gui.MenuItem('Camera', width=70, height=30)
        m8.onclick.do(self.menu_screen8_clicked)

        menu.append([m1, m2, m3, m4, m5, m6, m7, m8])
    
    
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

        vbox = VBox(width=600, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
   
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=70, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=70, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=70, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=70, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-WS', width=70, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=70, height=30)
        m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('MQTTR', width=70, height=30)
        m7.onclick.do(self.menu_screen7_clicked)
        m8 = gui.MenuItem('Camera', width=70, height=30)
        m8.onclick.do(self.menu_screen8_clicked)

        menu.append([m1, m2, m3, m4, m5, m6, m7, m8])
    

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

        vbox = VBox(width=600, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'

   
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=70, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=70, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=70, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=70, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-WS', width=70, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=70, height=30)
        m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('MQTTR', width=70, height=30)
        m7.onclick.do(self.menu_screen7_clicked)
        m8 = gui.MenuItem('Camera', width=70, height=30)
        m8.onclick.do(self.menu_screen8_clicked)

        menu.append([m1, m2, m3, m4, m5, m6, m7, m8])

    

        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 1
        screen1header = gui.Label("Blynk / WeatherSense Tab", style='margin:10px')
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
        P1Nheader = gui.Label("WeatherSense Sensors", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P1Nheader,'P1Nheader') 
        self.F_USEWSLIGHTNING = gui.CheckBoxLabel( 'Use WS Lightning ', self.USEWSLIGHTNING, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_USEWSLIGHTNING,'self.F_USEWSLIGHTNING') 
        self.F_USEWSAQI = gui.CheckBoxLabel( 'Use WS Air Quality ', self.USEWSAQI, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_USEWSAQI,'self.F_USEWSAQI') 
        self.F_USEWSSKYCAM = gui.CheckBoxLabel( 'Use WS Sky Camera ', self.USEWSSKYCAM, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_USEWSSKYCAM,'self.F_USEWSSKYCAM') 
        self.F_ALTWSSKYCAM = gui.CheckBoxLabel( 'Alternate SkyCam/WS SkyCamera ', self.ALTWSSKYCAM, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_ALTWSSKYCAM,'self.F_ALTWSSKYCAM') 



        return vbox

    def buildScreen6(self):
        #screen 6

        vbox = VBox(width=600, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
   
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=70, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=70, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=70, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=70, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-WS', width=70, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=70, height=30)
        m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('MQTTR', width=70, height=30)
        m7.onclick.do(self.menu_screen7_clicked)
        m8 = gui.MenuItem('Camera', width=70, height=30)
        m8.onclick.do(self.menu_screen8_clicked)

        menu.append([m1, m2, m3, m4, m5, m6, m7, m8])
    

        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 
        screenheader = gui.Label("Pin Config Tab", style='margin:10px')
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


    def buildScreen7(self):
        #screen 7

        vbox = VBox(width=600, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=70, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=70, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=70, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=70, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-WS', width=70, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=70, height=30)
        m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('MQTTR', width=70, height=30)
        m7.onclick.do(self.menu_screen7_clicked)
        m8 = gui.MenuItem('Camera', width=70, height=30)
        m8.onclick.do(self.menu_screen8_clicked)

        menu.append([m1, m2, m3, m4, m5, m6, m7, m8])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 
        screenheader = gui.Label("MQTT / Rest Tab", style='margin:10px')
        vbox.append(screenheader)
        
        # short headers

        shortlabelstyle = 'font-family:monospace; width:200; font-size:15px; margin:5px; background:LightGray' 



        P7Nheader = gui.Label("REST Interface", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P7Nheader,'P7Nheader') 
        self.F_REST_Enable = gui.CheckBoxLabel( 'REST Enable', self.REST_Enable, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_REST_Enable,'self.F_REST_Enable') 


        P6Nheader = gui.Label("MQTT Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P6Nheader,'P6Nheader') 

        self.F_MQTT_Enable = gui.CheckBoxLabel( 'MQTT Enable', self.MQTT_Enable, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_MQTT_Enable,'self.F_MQTT_Enable') 

        p4label = gui.Label("MQTT Server URL ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p4label,'p4label') 
        
        self.F_MQTT_Server_URL = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_MQTT_Server_URL.set_value(self.MQTT_Server_URL)
        vbox.append(self.F_MQTT_Server_URL,'MQTT_Server_URL') 

        p3label = gui.Label("MQTT Server Port Number ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p3label,'p3label') 
        
        self.F_MQTT_Port_Number = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_MQTT_Port_Number.set_value(str(self.MQTT_Port_Number))
        vbox.append(self.F_MQTT_Port_Number,'MQTT_Port_Number') 

        p2label = gui.Label("How Often MQTT Sent in Seconds ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p2label,'p2label') 
        
        self.F_MQTT_Send_Seconds = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_MQTT_Send_Seconds.set_value(str(self.MQTT_Send_Seconds))
        vbox.append(self.F_MQTT_Send_Seconds,'MQTT_Send_Seconds') 


        return vbox



    def buildScreen8(self):
        #screen 8

        vbox = VBox(width=600, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        menu = gui.Menu(width='100%', height='30px')
        m1 = gui.MenuItem('DMW', width=70, height=30)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('MTN', width=70, height=30)
        m2.onclick.do(self.menu_screen2_clicked)
        m3 = gui.MenuItem('PSMax', width=70, height=30)
        m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('WS-WU', width=70, height=30)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('B-WS', width=70, height=30)
        m5.onclick.do(self.menu_screen5_clicked)
        m6 = gui.MenuItem('Pins', width=70, height=30)
        m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('MQTTR', width=70, height=30)
        m7.onclick.do(self.menu_screen7_clicked)
        m8 = gui.MenuItem('Camera', width=70, height=30)
        m8.onclick.do(self.menu_screen8_clicked)

        menu.append([m1, m2, m3, m4, m5, m6, m7, m8])
    
        menubar = gui.MenuBar(width='100%', height='30px')
        menubar.append(menu)

        vbox.append(menubar)

        #screen 
        screenheader = gui.Label("Camera Options", style='margin:10px')
        vbox.append(screenheader)
        
        # short headers

        shortlabelstyle = 'font-family:monospace; width:200; font-size:15px; margin:5px; background:LightGray' 



        P5Nheader = gui.Label("Night Camera Enable", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 
        self.F_Camera_Night_Enable = gui.CheckBoxLabel( 'Night Vision Enable', self.Camera_Night_Enable, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_Camera_Night_Enable,'self.F_Camera_Night_Enable') 

        P5Nheader = gui.Label("Camera Rotation", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 
        if (self.Camera_Rotation == 0):
            self.CR_Radio_1 = RadioButtonWithLabel(' 0',True, 'groupCR')
        else:
            self.CR_Radio_1 = RadioButtonWithLabel(' 0',False, 'groupCR')
        
        vbox.append(self.CR_Radio_1,'self.F_Camera_Rotation1') 
        if (self.Camera_Rotation == 90):
            self.CR_Radio_2 = RadioButtonWithLabel(' 90',True, 'groupCR')
        else:
            self.CR_Radio_2 = RadioButtonWithLabel(' 90',False, 'groupCR')
        vbox.append(self.CR_Radio_2,'self.F_Camera_Rotation2') 
        if (self.Camera_Rotation == 180):
            self.CR_Radio_3 = RadioButtonWithLabel(' 180',True, 'groupCR')
        else:
            self.CR_Radio_3 = RadioButtonWithLabel(' 180',False, 'groupCR')
        vbox.append(self.CR_Radio_3,'self.F_Camera_Rotation3') 
        if (self.Camera_Rotation == 270):
            self.CR_Radio_4 = RadioButtonWithLabel(' 270',True, 'groupCR')
        else:
            self.CR_Radio_4 = RadioButtonWithLabel(' 270',False, 'groupCR')
        vbox.append(self.CR_Radio_4,'self.F_Camera_Rotation4') 


        self.CR_Radio_1.onchange.do(self.radio_changed)
        self.CR_Radio_2.onchange.do(self.radio_changed)
        self.CR_Radio_3.onchange.do(self.radio_changed)
        self.CR_Radio_4.onchange.do(self.radio_changed)

        return vbox

#################RadioButton
    def radio_changed(self, emitter, value):
        self.Camera_Rotation =  int(emitter.get_text())
     


###################

    def main(self):

        self.readJSON()


        widthBox = 700
        heightBox = 800
        self.mainContainer = Container(width=widthBox, height=heightBox, margin='0px auto', style="position: relative")
        self.mainContainer.style['justify-content'] = 'flex-start'
        self.mainContainer.style['align-items'] = 'flex-start'


        logo = SuperImage("./static/SkyWeatherLogo.png", width=400, height =200)
        header = gui.Label("SkyWeather2 Configuration Tool", style='position:absolute; left:5px; top:30px')
        version = gui.Label("Version 003",style='position:absolute; left:5px; top:50px') 
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
        self.screen7 = self.buildScreen7()
        self.screen8 = self.buildScreen8()


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
        self.mainContainer.remove_child(self.screen7)
        self.mainContainer.remove_child(self.screen8)
        
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


    def menu_screen7_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen7,'screen7')
        print("menu screen7 clicked")

    def menu_screen8_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen8,'screen8')
        print("menu screen8 clicked")


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
        self.screen7 = self.buildScreen7()
        self.screen8 = self.buildScreen8()


        self.mainContainer.append(self.screen1,'screen1')
        
        
    def onSave(self, widget, name='', surname=''):
        print("onSave clicked")
        self.saveJSON()


#Configuration
configuration = {'config_enable_file_cache': True, 'config_multiple_instance': True, 'config_port': 8001, 'config_address': '0.0.0.0', 'config_start_browser': False, 'config_project_name': 'untitled', 'config_resourcepath': './res/'}

# starts the web server
#start(SkyWeatherConfigure, address='0.0.0.0', port=8001)

start(SkyWeatherConfigure, address=configuration['config_address'], port=configuration['config_port'],
                        multiple_instance=configuration['config_multiple_instance'],
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])

