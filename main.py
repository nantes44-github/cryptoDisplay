from machine import Pin, I2C
import sh1106
import time
import network
import urequests as requests

ssid = 'WIFI_KEY_HERE'
password = 'WIFI_PASS_HERE'
refresh=2

oledHeight=64
oledWidth=128

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=1600000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
display.sleep(False)

def printOled(a,b="",c="",d="",e="",f=""):
    display.rotate(False) 
    display.fill(0)
    display.text(a,0,0,1)
    display.text(b,0,10,1)
    display.text(c,0,20,1)
    display.text(d,0,30,1)
    display.text(e,0,40,1)
    display.text(f,0,50,1)
    display.show()

def loadBar():
    speed=3
    for i in range ((128/speed+1)):
        iSpeed=i*speed
        display.pixel(iSpeed, 62, 1)
        display.pixel(iSpeed+1, 62, 1)
        display.pixel(iSpeed+2, 62, 1)
        display.show()
        display.pixel(iSpeed, 62, 0)
        display.pixel(iSpeed+1, 62, 0)
        display.pixel(iSpeed+2, 62, 0)
        display.show()

def connectToWifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("connect to ",ssid)
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if not wlan.isconnected():
            print(wlan.status())
            printOled("Waiting for","connection to",ssid)
            loadBar()
        max_wait -= 1
        time.sleep(1)

    # Handle connection error
    if wlan.isconnected():
      status = wlan.ifconfig()
      printOled("connected","IP is :",status[0])
      loadBar()
    else:
       printOled("Connect fail","check wifi conf","and retry.")
       raise RuntimeError('network connection failed')

def getTicker(symbol):
    data=requests.get("https://data.binance.com/api/v3/ticker?symbol="+symbol)
    return data.json()

printOled("Hello Pivian","Welcome to : ","PIVX Live!","Device starting","Please wait","a bit...coin")
loadBar()
connectToWifi()

while True:
    try:
        pivxData=getTicker("PIVXBTC")
        ethData=getTicker("ETHUSDT")
        btcData=getTicker("BTCUSDT")
        pivxPrice=str(round(float(pivxData["lastPrice"])*100000000))
        ethPrice=str(round(float(ethData["lastPrice"])))
        btcPrice=str(round(float(btcData["lastPrice"])))
        printOled("-=PIVX Price=-",pivxPrice+ " sat","-=ETH  Price=-",ethPrice+" usdt","-=BTC  Price=-",btcPrice+" usdt")
        loadBar()
        time.sleep(refresh)
    except:
        printOled("-=   ERROR    =-","Wifi too far?","Binance down?","Retry in 10s","","Else reboot.")
        time.sleep(10)
        pass



