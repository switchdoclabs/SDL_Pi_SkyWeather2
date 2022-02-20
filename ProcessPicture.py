# processes incoming pictures from multiple SkyCams and saves resulting files
# updates database

import traceback
import base64
import datetime
import config
import os, glob

from PIL import ImageFont, ImageDraw, Image

import MySQLdb as mdb

CameraChunkData = {}

def purge(dir, pattern):
    print("dir=", dir)
    print("pattern=", pattern)
    for f in os.listdir(dir):
        print ("f=", f)
        if re.search(pattern, f):
            print("fS=", f)
            os.remove(os.path.join(dir, f))

def saveChunk(jsonmsg):

    # store message in associative array keyed by camera ID
    cameraID = jsonmsg["id"]
    messageID = jsonmsg["messageid"]
    chunkNumber = jsonmsg["chunknumber"]
    totalChunks = jsonmsg["totalchunknumbers"]
    chunk = jsonmsg["chunk"]
    pictureSize = jsonmsg["picturesize"]
    resends = jsonmsg["totalchunkresends"]
    resolution = jsonmsg["resolution"]

    #print("Adding Chunk to Array")
    #print("----------------")
    #print("CameraID=", cameraID)
    #print("ChunkNumber=", chunkNumber)
    #print("TotalChunks=", totalChunks)
    #print("Chunksize=", len(chunk))
    #print("PictureSize", pictureSize)

    # clear data for ID if chunk number is 0
    try:
        if (chunkNumber == 0):
            try:
                # clear it
                del CameraChunkData[cameraID] 
            except:
                pass

        # add chunk
        try:
            currentIDList = CameraChunkData[cameraID]
        except:
            currentIDList = []
        currentIDList.append(dict( chunknumber= chunkNumber, totalchunks = totalChunks, picturesize = pictureSize, chunk=chunk, resends=resends, resolution=resolution)) 
        CameraChunkData[cameraID] = currentIDList
        #printFilteredCameraChunkData(CameraChunkData)
        # process picture if ID ChunkCount == last Chunk
        # then clear data
        if (int(chunkNumber)+1 == int(totalChunks)):
            #print("Process the Picture")
            processPicture(cameraID, messageID, CameraChunkData[cameraID])
            try:
                # clear it
                del CameraChunkData[cameraID] 
            except:
                pass

        #try:
        #    print("CameraChunkData Count=", len(CameraChunkData[cameraID]))
        #except:
        #    print("CameraChunkData Count=0")
            
    except:
        traceback.print_exc()
    


    return

def printFilteredCameraChunkData(CameraChunkList):
    
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for cameraID in CameraChunkList:
        print("CameraID =", cameraID)
        cameraChunkList = CameraChunkList[cameraID]
        for chunkItem in cameraChunkList:
            
            print("CN:%s CT: %s RS: %s CL:%s"% (chunkItem["chunknumber"], chunkItem["totalchunks"], chunkItem["resends"], len(chunkItem["chunk"])) )
            

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
    return

def processPicture(cameraID, messageID, CameraChunkList):
    
    try:

        
        # put together the file name
        fileDate = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileDay = datetime.datetime.now().strftime("%Y-%m-%d")
   
        singlefilename =cameraID+"_"+messageID +"_"+fileDate+".jpg"
        dirpathname="static/SkyCam/" + cameraID+ "/"+fileDay

        os.makedirs(dirpathname, exist_ok=True)
        os.makedirs("static/CurrentPicture", exist_ok=True)
        filename = dirpathname+"/"+singlefilename    

        
        # now build the full file 
        mutable_bytes = bytearray()
        for myChunk in CameraChunkList:
            theChunk = myChunk["chunk"]
            theChunk = theChunk.encode()
            mutable_bytes += base64.b64decode(theChunk)
    
        
        #print("Writing:"+filename)
        f=open(filename,"wb")
        f.write(mutable_bytes)
        f.close()
        
        # clear chunk
        del CameraChunkData[cameraID]
        
        pil_im = Image.open(filename) 

        try:
            myCameraRotation = config.SkyCamRotationArray[cameraID]
        except:
            myCameraRotation = config.DefaultCameraRotation
        print("CameraRotation=", myCameraRotation)

        if (myCameraRotation != 0):
            pil_im = pil_im.rotate(myCameraRotation)
      
        draw = ImageDraw.Draw(pil_im)
        
        # Choose a font
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 25)


        myText = "WeatherSense SkyCam-%s %s " % (cameraID, datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
        if (config.SWDEBUG):
            print("mySkyCameraText=", myText)

        # Draw the text
        color = 'rgb(255,255,255)'
        #draw.text((0, 0), myText,fill = color, font=font)

        # get text size
        text_size = font.getsize(myText)

        # set button size + 10px margins
        button_size = (text_size[0]+20, text_size[1]+10)

        # create image with correct size and black background
        button_img = Image.new('RGBA', button_size, "black")
    
        # put text on button with 10px margins
        button_draw = ImageDraw.Draw(button_img)
        button_draw.text((10, 5), myText, fill = color, font=font)

        # put button on source image in position (0, 0)

        pil_im.paste(button_img, (0, 0))
        bg_w, bg_h = pil_im.size 

        # SkyWeather log in lower right
        size = 64
        SWLimg = Image.open("static/SkyWeatherLogoSymbol.png")
        SWLimg.thumbnail((size,size),Image.ANTIALIAS)
        pil_im.paste(SWLimg, (bg_w-size, bg_h-size))


        # Save the image
        #pil_im.save(dirpathname+"/Test.jpg", format= 'JPEG')
        currentpicturefilename = "static/CurrentPicture/"+cameraID+".jpg"
        currentpicturedashfilename = "dash_app/assets/"+cameraID+"_"+messageID+".jpg"
        for name in glob.glob("dash_app/assets/"+cameraID+"_*.jpg"):
            os.remove(name)

        pil_im.save(filename, format= 'JPEG')
        pil_im.save(currentpicturefilename, format= 'JPEG')
        pil_im.save(currentpicturedashfilename, format= 'JPEG')


        first = CameraChunkList[0]
        FileSize = int(first["picturesize"] )
        resends = int(first["resends"] )
        resolution = int(first["resolution"])
        # send database entry to SQL
    
    
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
    
                fields = "cameraID, picturename, picturesize, messageID, resends,resolution"

                values = "\'%s\', \'%s\', %d, %d, %d, %d" % (cameraID, singlefilename, FileSize, int(messageID), int(resends), resolution)  
                query = "INSERT INTO SkyCamPictures (%s) VALUES(%s )" % (fields, values)
                print("query=", query)
                cur.execute(query)
                con.commit()
            except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0], e.args[1]))
                con.rollback()
                # sys.exit(1)
    
            finally:
                cur.close()
                con.close()
    
                del cur
                del con
    except mdb.Error as e:
         traceback.print_exc()

    return

    
from PIL import ImageFont, ImageDraw, Image

