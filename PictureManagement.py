# manage SkyCam Pictures

import os
import time
import datetime
import config

import MySQLdb as mdb
import traceback

import shutil


import subprocess

#No of days before which the files are to be deleted
DELETE_FILES_OLDER_THAN_DAYS = 14
#Start Time Lapse at this Time
TIME_LAPSE_START_HOUR = 5
# no of days to keep time lapses
DELETE_TIME_LAPSES_OLDER_THAN_DAYS = 14


def cleanPictures(source):

    #folder to clear from
    dir_path = 'static/SkyCam/'
    
    threshold = time.time() -DELETE_FILES_OLDER_THAN_DAYS  *86400
    print(f"threshold = {time.ctime(threshold)} ")
    devices = os.listdir(dir_path)
    print ("devices=", devices)
    for device in devices:
        device_dir_path = dir_path+device+"/"
        days = os.listdir(device_dir_path)
        print ("days=", days)
       
        for day in days:
            day_dir_path = device_dir_path+day+"/"
            print ("day_dir_path=", day_dir_path)
            files = os.listdir(day_dir_path)
            #creation_time = os.stat(os.path.join(dir_path,day)).st_ctime
            for myFile in files:
                myFilePath = day_dir_path+myFile
                creation_time = os.stat(myFilePath).st_ctime
                if creation_time < threshold:
                    print(f"threshold = {time.ctime(threshold)} ")
                    print(f"{myFilePath} is created on {time.ctime(creation_time)} and will be deleted")
                    os.remove(myFilePath)
            # check for no files left
            files = os.listdir(day_dir_path)
            if (len(files) == 0):
                print("delete empty directory ", day_dir_path)
                os.rmdir(day_dir_path)

        files = os.listdir(device_dir_path)
        if (len(files) == 0):
            print("delete empty directory ", device_dir_path)
            os.rmdir(device_dir_path)

    return

def cleanTimeLapses(source):

    try:
        #folder to clear from
        dir_path = 'static/TimeLapses/'
    
        threshold = time.time() -DELETE_TIME_LAPSES_OLDER_THAN_DAYS  *86400
        print(f"threshold = {time.ctime(threshold)} ")
        devices = os.listdir(dir_path)
        print ("devices=", devices)
        for device in devices:
            device_dir_path = dir_path+device+"/"
            files = os.listdir(device_dir_path)
            print ("files=", files)
       
            for myFile in files:
                    myFilePath = device_dir_path+myFile
                    creation_time = os.stat(myFilePath).st_ctime
                    if creation_time < threshold:
                        print(f"threshold = {time.ctime(threshold)} ")
                        print(f"{myFilePath} is created on {time.ctime(creation_time)} and will be deleted")
                        os.remove(myFilePath)
    except:
        pass

    return

def addzeros(count):
    if count < 10:
        return "000"
    if count < 100:
        return "00"
    if count < 1000:
        return "0"
    return ""

def buildTimeLapse(source):
    # grab a list of the file names from mySQL

    # start time
    #5am previous day
    yesterday = datetime.date.today () - datetime.timedelta (days=1)
    hourtime = datetime.time(hour=5, minute=0) 
    starttime = datetime.datetime.combine(yesterday, hourtime) 
    
    print("startime=", starttime)
    
    # end time
    #5am today
    today = datetime.date.today()
    hourtime = datetime.time(hour=5, minute=0)
    endtime = datetime.datetime.combine(today, hourtime) 
    
    print("endtime=", endtime)

    # loop thorough all of the devices (grab the directory)

    my_dir_path = 'static/SkyCam/'
    
    devices = os.listdir(my_dir_path)
    print ("devices=", devices)
    os.makedirs("static/TimeLapses", exist_ok=True)
    for device in devices:

        if (config.enable_MySQL_Logging == True):

            # open mysql database
            # write log
            # commit
            # close
            try:
    
                con = mdb.connect(
                    "localhost",
                    "root",
                    config.MySQL_Password,
                    "WeatherSenseWireless"
                )

                cur = con.cursor()
    

                query = "SELECT timestamp, cameraID, picturename  FROM  SkyCamPictures WHERE cameraID = '%s' AND timestamp >= '%s' AND timestamp < '%s' ORDER BY timestamp" % (device, starttime, endtime)
                #print("query=", query)
                cur.execute(query)
                filerecords = cur.fetchall()
                cur.execute(query)
                con.commit()
            except mdb.Error as e:
                traceback.print_exc()
                # sys.exit(1)
    
            finally:
                cur.close()
                con.close()
    
                del cur
                del con
    
        # rename them into the ffmpeg number format and copy them into the temp directory
        if (len(filerecords) == 0):
            print("device %s has no current pictures"%device)
        
        if (len(filerecords) > 0):
            dirpath = 'static/BuildTimeLapse'
            try:
                shutil.rmtree(dirpath) 
            except:
                traceback.print_exc()

            os.makedirs(dirpath, exist_ok=True)
            count = 0
            for record in filerecords:
                # get date for dirpath
                recordname = record[2]
                splitName= recordname.split("_")

                recordname2 = splitName[2]
                splitName= recordname2.split("-")
                dayname = splitName[0]+"-"+splitName[1]+"-"+splitName[2]

                fromPath = my_dir_path+device+"/"+dayname+"/"+recordname
                toPath = dirpath+"/pic_"+addzeros(count)+"%d"%(count)+".jpg"
                print("cp %s %s" % (fromPath, toPath))
                try:
                    shutil.copyfile(fromPath, toPath)
                    count = count +1 
                except:
                    pass

            # build the video
            # get full path name

            cwdir =os.getcwd() 
            print(cwdir)

            inputFiles = cwdir+"/"+dirpath+"/pic_%04d.jpg"
            outDir = cwdir+"/"+"static/TimeLapses/"+device
            os.makedirs(outDir, exist_ok=True)
            outputFile = outDir+ "/"+device+"_"+dayname+".mp4"
            try:
                os.remove(outputFile)
            except:
                pass 

            command ="/usr/bin/ffmpeg -r 20 -i %s -c:v libx264 %s " % (inputFiles, outputFile)

            print(command)
            cmd = command.split()

            print(cmd )
            os.system(command+"> /dev/null 2>&1" )
            #p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #print (p)

    # save it to timelapse directory 


    return
