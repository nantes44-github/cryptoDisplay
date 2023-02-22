from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import network
import urequests
import json

ssid = 'SSID_HERE'
password = 'WIFI_KEY_HERE'
refresh=2

oledHeight=64
oledWidth=128

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(oledWidth, oledHeight, i2c)

def writeOnDisplay(lineOne="",lineTwo="",lineThree="", lineFour="",lineFive="",lineSix=""):
  oled.fill(0)
  oled.text(lineOne, 0, 0)
  oled.text(lineTwo, 0, 10)
  oled.text(lineThree, 0, 20)
  oled.text(lineFour, 0, 30)
  oled.text(lineFive, 0, 40)
  oled.text(lineSix, 0, 50)
  oled.show()

def loadBar():
    for i in range ((oledWidth+1)):
        oled.pixel(i, oledHeight-2, 1)
        oled.pixel(i+1, oledHeight-2, 1)
        oled.pixel(i+2, oledHeight-2, 1)
        oled.show()
        oled.pixel(i, oledHeight-2, 0)
        oled.pixel(i+1, oledHeight-2, 0)
        oled.pixel(i+2, oledHeight-2, 0)
        oled.show()

def scroll_out_screen(speed):
  time.sleep(2)
  for i in range ((oledWidth+1)/speed):
    for j in range (oledHeight):
      oled.pixel(i, j, 0)
    oled.scroll(speed,0)
    oled.show()

def connectToWifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
      if wlan.status() < 0 or wlan.status() >= 3:
        break
      max_wait -= 1
      writeOnDisplay("Waiting for","connection")
      time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
       writeOnDisplay("Connect fail","check wifi config")
       raise RuntimeError('network connection failed')
    else:
      status = wlan.ifconfig()
      writeOnDisplay("connected","IP is :",status[0])

def getBinanceData(symbol="ETH",currency="USDT"):
    req=urequests.get("https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-product-by-symbol?symbol="+symbol+currency)
    jsonSymbol=json.loads(req.content)
    return jsonSymbol["data"]#["c"]

def getCurrentPrice(data):
    return data["c"]

writeOnDisplay("Welcome to : ","Crypto Display!","Device starting","Please wait","a bit...coin")
loadBar()
scroll_out_screen(2)
connectToWifi()

while True:
    try:
        loadBar()
        pivxData=getBinanceData("PIVX","BTC")
        pivxBtcPrice=getCurrentPrice(pivxData)
        pivxSatPrice=str(float(pivxBtcPrice)*100000000)
        
        btcUsdData=getBinanceData("BTC","USDT")
        btcUsdPrice=str(getCurrentPrice(btcUsdData))

        ethUsdData=getBinanceData("ETH","USDT")
        ethUsdPrice=str(getCurrentPrice(ethUsdData))
        
        writeOnDisplay("-= PIVX Live =-",pivxSatPrice+" sat","-= BTC  Live =-",btcUsdPrice + " usd","-= ETH  Live =-",ethUsdPrice+" usd")
        
        
        
        #time.sleep(refresh)
    except:
        writeOnDisplay("-= ERROR Live =-","Error :-(","Retrying")
        time.sleep(10)
        pass





