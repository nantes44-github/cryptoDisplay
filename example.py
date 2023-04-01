import ticker


myPivx=ticker.pivxTicker()
myPivx.updatePivxPrice()
myPivx.setWalletAddress("DPivuj3Fk6qD9kkNHsTU3jwj1r1UZsEtP6")
myPivx.setTimeArea="Europe"
myPivx.setTimeLocation="Paris"
myPivx.updateWalletValue()
myPivx.updateBtcPrice()
myPivx.updateEthPrice()
myPivx.getTime()

#print(myPivx.walletValue)
#print(myPivx.pivxPrice)
#print(myPivx.btcPrice)
#print(myPivx.ethPrice)
#print(myPivx.pivxPriceInDollars)
#print(myPivx.date)
#print(myPivx.time)
print("-------------------")
print("Pivx price in sat",myPivx.returnPivxPrice())
print("Pivx price in dollars",myPivx.returnPivxPriceInDollars())
print("Btc price in dollars",myPivx.returnBtcPrice())
print("Eth price in dollar",myPivx.returnEthPrice())
print("Wallet value in Pivx",myPivx.returnWalletValue())
print("Wallet value in dollars",myPivx.returnWalletValueInDollars())
print("Date is",myPivx.returnDate())
print("Time is",myPivx.returnTime())

