Grove HM3301 Dust Sensor Python3 Driver<BR>
SwitchDoc Labs 2020<BR>
Version 1.0<BR>

The Zero, W, Raspberry Pi 3B+ and the Raspberry Pi 4B have a problem with the standard I2C bus reading the HM3301 sensor.<BR>

You need to reduce the I2C bus speed to 20000 baud to get it to work on the Pi and due to a number of factors, you can't reliably set the baud rate on the Raspberry Pi architecture to 20000.<BR>

To solve this we build a new driver based on using pigpio and their bit banging i2c library on a straight GPIO.   The driver assumes SDA at 20 and SCL at 19. <BR>

The Default I2C address for the HM3301 is 0x40<BR>

use testHM3301.py to verify your unit <BR>

You must install the pigpio library and run the daemon.


<pre>

sudo apt-get update
sudo apt-get install pigpio
</pre>

Then run:

<pre>
sudo pigpiod
</pre>

Finally, run your test:
<pre>
sudo python3 testSDL_Pi_HM3301.py
</pre>
and you should see something like this:


