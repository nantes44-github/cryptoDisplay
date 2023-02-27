# cryptoDisplay
A simple crypto display based on a Wemos D1 and an oled screen sh1106

## Bill Of Material
1 - A wimos D1
2 - Some female to female dupont cable (shorts are good)
3 - An sh1106 oled screen

Optional:
4 - A 3D printer to print enclosure : https://www.thingiverse.com/thing:4657409

## Wiring
Only four dupont wire are needed.
First must connect GND to GND
Second VCC to 3V3 on the pico W
Third SCL to GP1 (the second pin on the left of the pico w)
Fourth SDA to GP0 (the first on the left of the pico)

if you are lost, look at google : "wems D1 I2C screen wiring"
:-)

## Loading code to board
1 - get the code from "main.py" to your local computer
2 - download Thonny (IDE to code) from thonny.org
3 - set all according to : https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/0

You are done ;-)
