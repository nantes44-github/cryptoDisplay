import requests
import math

class pivxTicker:
    def __init__(self):
        print("init")
        print("getting setting from json file <to do>")
        self.walletAddress="DPivuj3Fk6qD9kkNHsTU3jwj1r1UZsEtP6" #the wallet address to check
        self.coef=100000000 #to convert btc to satoshi
        self.timeArea="Europe" #to get right time from http://worldtimeapi.org. here it's the area (Europe for example)
        self.timeLocation="Paris" #to get right time from http://worldtimeapi.org. here it's the location (Paris for example)
        # init vars to zero in case of problem
        self.pivxPrice=0
        self.walletValue=0
        self.btcPrice=0
        self.ethPrice=0
        self.pivxPriceInDollars=0
        self.date="1980-01-27"
        self.time="22:10:59"

    def setWalletAddress(self,walletAddress):
        self.walletAddress=walletAddress
    
    def setTimeArea(self,timeArea):
        self.timeArea=timeArea
    
    def setTimeLocation(self,timeLocation):
        self.timeLocation=timeLocation

    def getTime(self):
        try:
            print("retrieve time from internet")
            req=requests.get("http://worldtimeapi.org/api/timezone/"+self.timeArea+"/"+self.timeLocation+".json")
            data=req.json()
            self.date=data["datetime"].split("T")[0]
            self.time=data["datetime"].split("T")[1].split(".")[0]
        except:
            print("Error while getting time and/or date.")
            print("Shit happens but show must go on!")
            pass

    def updatePivxPrice(self):
        try:
            print("call api and update Pivx price")
            priceData=requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PIVXBTC")
            priceJson=priceData.json()
            self.pivxPrice=float(priceJson["price"])*self.coef
            priceData.close()
        except:
            print("Error while getting Pivx price with Binance API")
            print("Shit happens but show must go on!")
            pass

    def updateWalletValue(self):
        try:
            print("call api and get wallet value")
            walletData=requests.get("https://explorer.rockdev.org/api/v2/address/"+self.walletAddress+"?details=basic")
            walletJson=walletData.json()
            self.walletValue=float(walletJson["balance"])/self.coef
            walletData.close()
        except:
            print("Error while getting wallet data on rockdev explorer.")
            print("Shit happens but show must go on!")
            pass

    def updateBtcPrice(self):
        try:
            print("call api and get Btc price")
            priceData=requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
            priceJson=priceData.json()
            self.btcPrice=float(priceJson["price"])
            priceData.close()
            #update pivx price in dollars too
            self.pivxPriceInDollars=self.pivxPrice*self.btcPrice/self.coef
        except:
            print("Error while getting Btc price on Binance API or while converting Pivx price to dollar.")
            print("Shit happens but show must go on!")
            pass

    def updateEthPrice(self):
        try:
            print("call api and get Eth price")
            priceData=requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
            priceJson=priceData.json()
            self.ethPrice=float(priceJson["price"])
            priceData.close()
        except:
            print("Error while getting Eth price on Binance API.")
            print("Shit happens but show must go on!")
            pass
        
    def returnPivxPrice(self):
        return int(self.pivxPrice)

    def returnBtcPrice(self):
        return int(self.btcPrice)

    def returnEthPrice(self):
        return int(self.ethPrice)

    def returnPivxPriceInDollars(self):
        return round(self.pivxPriceInDollars,2)

    def returnWalletValue(self):
        return int(self.walletValue)

    def returnWalletValueInDollars(self):
        return int(self.walletValue*self.pivxPriceInDollars)

    def returnWalletAddress(self):
        return self.setWalletAddress

    def returnDate(self):
        return self.date

    def returnTime(self):
        return self.time