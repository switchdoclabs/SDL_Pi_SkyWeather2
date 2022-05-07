
SkyWeather2
SwitchDoc Labs

See full bug list and info on releases at:<BR>

https://forum.switchdoc.com/thread/1452/skyweather2-software-releases

May 7, 2022 - Version 027.6 - add required updateWeb files <BR> 

Run sudo pip3 install SafecastPy

Run SkyWeather2.py from the command line to test<BR>
sudo python3 SkyWeather2.py<BR>


To update SkyWeather2 database, run the following command:<BR>
<BR>
sudo mysql -u root -p SkyWeather2 < 27.3.DataBaseUpdate.sql<BR>

You also need to go into your https://github.com/switchdoclabs/rtl_433<BR>
directory, do a git pull and then rebuild rtl_433 as shown in the README.md<BR>
On the SDL SDCard, this is under /home/pi/SDR<BR>


to install on SDL SD Card do this:

sudo pip3 install python-aqi<BR>
sudo pip3 install ffmpeg<BR>

April 30, 2022 - Version 027.5 - RadSense Geiger Counter Support<BR> 
April 15, 2022 - Version 027.4 - Fixed Light Overflow bug<BR>
January 28, 2022 - Version 027.3 - WeatherRack2 signal strengths added in database<BR>
January 27, 2022 - Version 027.2 - Fixed Multiple WeatherRack2 Use Case - Serial Number stored in database<BR>
August 28, 2021 - Version 027.1 - MQTT typo fixes, split indoor T/H to seperate channels - thanks Zara<BR>
August 25, 2021 - Version 027 - Full support of Solar SkyCam and Time Lapse<BR>
July 28, 2021 - Version 026.6 - Second Typo in wirelessSensors.py fixed<BR>
July 28, 2021 - Version 026.5 - Typo in wirelessSensors.py fixed<BR>
July 24, 2021 - Version 026.4 - Various Small Bugs fixed and Blynk updated<BR>
June 16, 2021 - Version 026.3 - On Board Dust Sensor Problem Fixed<BR>
June 9, 2021 - Version 026.2 - dash_app Lightning Reporting Fixed<BR>
June 6, 2021 - Version 026.1 - Additional AfterShock added<BR>
June 6, 2021 - Version 026 - AfterShock added. fixes and reliability improvements <BR>
April 17, 2021 - Version 025 - fixes and updgrades<BR>
March 12, 2021 - Version 024 - minor fixes, update on README.md for rtl_433<BR>
March 7, 2021 - Version 023 - Major Update: New WeatherSense devices added<BR>
WeatherSense Air Quality <BR>
WeatherSense Lightning<BR>
WeatherSense SolarMAX2<BR>
Full MQTT Update<BR>
WeatherUnderground Added<BR>
Note:  You need to apply the following commands to upgrade:<BR>
<pre>
cd
cd SDL_Pi_SkyWeather2
git pull
sudo pip3 install vcgencmd

sudo mysql -u root -p < WeatherSenseWireless.sql 

sudo mysql -u root -p WeatherSenseWireless < updateWeatherSenseWireless.sql
</pre>
(the password that is asked from the mysql command is your mysql root password, by default "password")<BR>

Remember to go to your rtl_433 directory and do the following to update rtl_433:<BR>

cd rtl_433/<BR>
mkdir build<BR>
cd build<BR>
cmake ..<BR>
make clean <BR>
make<BR>
sudo make install<BR>



<BR>
February 15, 2021 - Version 022 - Minor Bug Fixes<BR>
February 2, 2021 - Version 021 - Minor MQTT Fix from Jason, master bugfinder<BR> 
January 29, 2021 - Version 020 - Minor fix to Pi shutdown<BR> 
December 14, 2020 - Version 019 - Added AQI Dust Sensor Detection<BR> 
December 12, 2020 - Version 018 - Corrected Wind Speed/Gust Calculations<BR> 
December 4, 2020 - Version 017 - Fixed Dust Sensor Power control<BR> 
November 29, 2020 - Version 016 - Fixed CPUTemperature<BR>
November 29, 2020 - Version 015 - Minor Fixes<BR>
November 27, 2020 - Version 014 - WeatherSTEM Fix <BR>
November 24, 2020 - Version 012 - Reliability rtl_433 improvements <BR>
November 22, 2020 - Version 011 - dash_app improvements <BR>
November 13, 2020 - Version 010 - various fixes and addtions<BR>
October 22, 2020 - Version 009 - Camera Orientation Support <BR>
October 10, 2020 - Version 008 - Added dash_app support<BR>
Ocober 8, 2020 - Version 007 - Initial Release<BR>

Recommended to use the pre-built SD Card for SkyWeather2.

https://shop.switchdoc.com/products/16gb-sd-card-with-stretch-smart-garden-system-groveweatherpi





