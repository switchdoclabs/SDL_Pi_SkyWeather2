# update websites with Radiation Data
# configuration in updateWeb.conf

import traceback
import sys

try:
    import updateWebConfigLocal as updateWebConfig
    print("updateWebConfigLocal Found")
except:
    import updateWebConfig
    print ("using updateWebConfig")

    
import requests
import config

try:
    import SafecastPy
except:
    print("SafecastPy missing.  run:  sudo pip3 install SafecastPy ")
    sys.exit(1)
import datetime

safecast = SafecastPy.SafecastPy(
  api_key=updateWebConfig.SAFECASTAPI)




def sendCommandToIP(myIP, myCommand):
        myURL = 'http://'+myIP+'/'+myCommand

        try:
                if (config.SWDEBUG):
                    print("myURL=", myURL)
                req = requests.get(myURL,timeout=5)

                returnReq = req

        except Exception:
                traceback.print_exc()
                return 
        return returnReq


def update_SafeCast(CPM, uSVh):

    if (updateWebConfig.SAFECASTAPI != ""):

        print("Updating SafeCast")
        try:
            measurement = safecast.add_measurement(json={
            'latitude': updateWebConfig.RADLATITUDE, 
            'longitude': updateWebConfig.RADLONGITUDE,
            'value': CPM,
            'unit': SafecastPy.UNIT_CPM,
            'captured_at': datetime.datetime.utcnow().isoformat() + '+00:00',
            'device_id': 90,
            'location_name': updateWebConfig.RADLOCATIONNAME, 
            'height': updateWebConfig.RADHEIGHTINMETERS 
            })
            print("CPM measurement= ", measurement)
            print('New CPM measurement id: {0}'.format(measurement['id']))
    
            measurement = safecast.add_measurement(json={
            'latitude': updateWebConfig.RADLATITUDE, 
            'longitude': updateWebConfig.RADLONGITUDE,
            'value': uSVh,
            'unit': SafecastPy.UNIT_USV,
            'captured_at': datetime.datetime.utcnow().isoformat() + '+00:00',
            'device_id': 90,
            'location_name': updateWebConfig.RADLOCATIONNAME, 
            'height': updateWebConfig.RADHEIGHTINMETERS 
            })
            print("measurement= ", measurement)
            print('New measurement id: {0}'.format(measurement['id']))
        except Exception:
            traceback.print_exc()
            return 
 
    pass


def update_NETC(CPM):

    pass

def update_RadMon(CPM):
   
    if (updateWebConfig.RADMONUSER != ""):
        myCommand = "radmon.php?function=submit&user="+updateWebConfig.RADMONUSER +"&password="+updateWebConfig.RADMONPASSWORD+"&value="+str(CPM)+ "&unit=CPM" 
        print("myCommand=", myCommand)
        response = sendCommandToIP(updateWebConfig.RADMONIPADDRESS, myCommand) 
        print("response=", response)
        pass

def update_GMCMap(CPM, uSVh):
   

    if (updateWebConfig.GMCMAPUSERACCOUNTID != ""):

        myCommand = "log2.asp?AID="+updateWebConfig.GMCMAPUSERACCOUNTID+"&GID="+updateWebConfig.GMCMAPGEIGERCOUNTERID+"&CPM="+str(CPM)+"&uSV="+str(uSVh)
        print("myCommand=", myCommand)
        response = sendCommandToIP(updateWebConfig.GMCMAPIPADDRESS, myCommand) 
        print("response=", response)
    

    pass
