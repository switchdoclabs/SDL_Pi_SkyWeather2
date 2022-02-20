
# handles updating the WeatherRack2 Sensor Dictionary
import state
import datetime



def addWR2Reading(WR2JSON):

    if (len(state.MWR2Array) > 0):
        # check existing records, update if found 
        for singleChannel in state.MWR2Array:
            if (singleChannel["id"] == WR2JSON['id']):
                #print("update MWR2Array")
                state.MWR2Array.remove (singleChannel)
                state.MWR2Array.append(WR2JSON)
                #print("-----------------")
                #print ("state.MWR2ArrayUpdate=",state.MWR2Array)
                #print("-----------------")
                return
        state.MWR2Array.append(WR2JSON)  
        #print("-----------------")
        #print ("state.MWR2Array=",state.MWR2Array)
        #print("-----------------")
                    
    else:
        state.MWR2Array.append(WR2JSON)  
        #print("-----------------")
        #print ("state.MWR2Array=",state.MWR2Array)
        #print("-----------------")



