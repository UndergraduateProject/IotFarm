#include "DHT.h"
#define DHTPIN 2// 連接至感測器的Pin=2
#define DHTTYPE DHT22// 使用感測器=DHT22

DHT dht(DHTPIN, DHTTYPE);
int soilPin = A0;//土壤濕度感測器pin=A0
int thresholdValue = 800;//澆水門檻值
//之後要加可自己設定門檻值&自動調整

void setup(){
  pinMode(soilPin, INPUT);
  Serial.begin(9600);//使用序列埠(鮑率)
  dht.begin();
}

void loop() {
  delay(2000);//2000毫秒測量一次
  float h = dht.readHumidity();//濕度
  float t = dht.readTemperature();//C度
  int sensorValue = analogRead(soilPin);//土壤濕度
  if(isnan(h)||isnan(t)) {//檢查有無讀取錯誤
    Serial.println(F("讀取失敗"));
    return;
  }
  float hic = dht.computeHeatIndex(t, h, false);//計算Heat Index in 克氏溫標(isFahreheit = false)
  Serial.print(F("Humidity: "));//print濕度於序列埠
  Serial.print(h);
  Serial.print(F("%  "));
  Serial.print(F("Temperature: "));//print溫度於序列埠
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(F("Heat index: "));//print Heat index 於序列埠
  Serial.print(hic);
  Serial.println(F("°C "));
  Serial.println(sensorValue);//print土壤濕度於序列埠
  //之後要從絕對數值改成百分比
  if(sensorValue < thresholdValue){//判斷澆水門檻
    Serial.println("不澆水");
  }
  else {
    Serial.println("澆水");
  }
}
