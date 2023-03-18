// base class GxEPD2_GFX can be used to pass references or pointers to the display instance as parameter, uses ~1.2k more code
// enable or disable GxEPD2_GFX base class
#define ENABLE_GxEPD2_GFX 0

#include <GxEPD2_BW.h>
#include <GxEPD2_3C.h>
#include <Fonts/FreeMonoBold9pt7b.h>
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

//wiring :
// ESP8266 SS=15,SCL(SCK)=14,SDA(MOSI)=13,BUSY=16,RST=5,DC=4

// 2.9'' EPD Module
GxEPD2_BW<GxEPD2_290_BS, GxEPD2_290_BS::HEIGHT> display(GxEPD2_290_BS(/*CS=5*/ 15, /*DC=*/ 4, /*RST=*/ 5, /*BUSY=*/ 16)); // DEPG0290BS 128x296, SSD1680

const char *ssid = "xxx";
const char *password = "xxxx";

StaticJsonDocument<200> price;

WiFiClientSecure client;
 

String getBinancePrice(String pair)
{
  client.setInsecure();
   
  HTTPClient http;
  String lastPrice="0";
  http.begin(client,"https://api.binance.com/api/v3/ticker/price?symbol="+pair);
  //http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.GET();
  Serial.println(httpResponseCode);
  if(httpResponseCode>0){
    // handle good server response
    String response = http.getString();
    Serial.println(response);
    deserializeJson(price, response);
    const char* assetPrice = price["price"];
    Serial.println(assetPrice);
    String lastPrice{assetPrice};
    Serial.println(lastPrice);
  }else{
    Serial.print("Error on sending Request: ");
    Serial.println(httpResponseCode);
  }
  http.end();
  return lastPrice;
}

void displayIP(String monIP)
{
  display.setRotation(1);
  display.setFont(&FreeMonoBold9pt7b);
  display.setTextColor(GxEPD_BLACK);
  int16_t tbx, tby; uint16_t tbw, tbh;

  display.getTextBounds(monIP, 0, 0, &tbx, &tby, &tbw, &tbh);
  // center the bounding box by transposition of the origin:
  uint16_t x = ((display.width() - tbw) / 2) - tbx;
  uint16_t y = ((display.height() - tbh) / 2) - tby;
  display.setFullWindow();
  display.firstPage();
  do
  {
    display.fillScreen(GxEPD_WHITE);
    display.setCursor(x, y-tbh);
    display.print(monIP);
  }
  while (display.nextPage());
}


void PrintScreen(String monIP,int ligne)
{
  display.setRotation(1);
  display.setFont(&FreeMonoBold9pt7b);
  display.setTextColor(GxEPD_BLACK);
  display.setFullWindow();
  display.firstPage();
  do
  {
    display.fillScreen(GxEPD_WHITE);
    display.setCursor(0, ligne);
    display.print(monIP+" "+String(ligne));
  }
  while (display.nextPage());
}

void PrintScreenFull(String monIP,int ligne)
{
  display.setRotation(1);
  display.setFont(&FreeMonoBold9pt7b);
  display.setTextColor(GxEPD_BLACK);
  display.setFullWindow();
  display.firstPage();
  do
  {
    display.fillScreen(GxEPD_WHITE);
    display.setCursor(0, ligne);
    display.print(monIP+" "+String(ligne));
    display.setCursor(0, ligne*2);
    display.print(monIP+" "+String(ligne*2));
    display.setCursor(0, ligne*3);
    display.print(monIP+" "+String(ligne*3));
  }
  while (display.nextPage());
}

void printLignePartialMode(String text, int line)
{
  //Serial.println("helloFullScreenPartialMode");
  //const char fullscreen[] = "full screen update";
  //const char fpm[] = "fast partial mode";
  //const char spm[] = "slow partial mode";
  //const char npm[] = "no partial mode";

  display.setPartialWindow(0, 0, display.width(), display.height());
  display.setRotation(1);
  display.setFont(&FreeMonoBold9pt7b);
  display.setTextColor(GxEPD_BLACK);
  //const char* updatemode= fpm;
  //updatemode = fpm;
  //updatemode = spm;
  display.firstPage();
  do
  {
    display.fillScreen(GxEPD_WHITE);
    display.setCursor(0, line);
    display.print(text);
  }
  while (display.nextPage());
}


void connectToWiFi() {
//Connect to WiFi Network
   Serial.println();
   Serial.println();
   Serial.print("Connecting to WiFi");
   Serial.println("...");
   WiFi.begin(ssid, password);
   int retries = 0;
while ((WiFi.status() != WL_CONNECTED) && (retries < 15)) {
   retries++;
   delay(500);
   Serial.print(".");
}
if (retries > 14) {
    Serial.println(F("WiFi connection FAILED"));
}
if (WiFi.status() == WL_CONNECTED) {
    Serial.println(F("WiFi connected!"));
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
    Serial.println(F("Setup ready"));
}

void setup()
{
  display.init(9600,true,50,false);
  connectToWiFi();
  display.print(WiFi.localIP());
  
  //helloWorld();
  //helloFullScreenPartialMode();
  delay(5000);
  //if (display.epd2.hasFastPartialUpdate)
  //{
    //showPartialUpdate();
    //delay(1000);
  //}
  //display.hibernate();
}

String ipToString(IPAddress& ip) { // IP v4 only
  String ips;
  ips.reserve(16);
  ips = ip[0];  ips += ':';
  ips += ip[1]; ips += ':';
  ips += ip[2]; ips += ':';
  ips += ip[3];
  return ips;
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  IPAddress myIp=WiFi.localIP();
  String myIpS=ipToString(myIp);
  //displayIP(myIpS);
  //delay(30000);
  PrintScreen(myIpS+"------",12);
  delay(10000);
  //PrintScreen(myIpS,24);
  //delay(10000);
  //PrintScreen(myIpS,36);
  //delay(10000);
  //PrintScreenFull(myIpS,12);
  //delay(10000);
  //printLignePartialMode("titi",12);
  //delay(5000);
  //printLignePartialMode("toto",12);
  //delay(5000);
  //printLignePartialMode("titi toto",12);
  //delay(5000);
  String btcPrice=getBinancePrice("BTCUSDT");
  Serial.println(btcPrice);
  printLignePartialMode(btcPrice,12);
  //printLignePartialMode(getBinancePrice("ETHUSDT"),24);
  //printLignePartialMode(getBinancePrice("PIVXBTC"),36);
  delay(1000000);  
}