
SkyWeather2
SwitchDoc Labs

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
sudo mysql -u root -p < WeatherSenseWireless.sql 
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





