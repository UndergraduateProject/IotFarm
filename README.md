# IotFarm

感測器：
DHT22  空氣濕度&溫度感測器
YL69  土壤濕度感測器
GY30  光度感測器
WaterSensor  水位感測器

其他設備：
UPS HAT  供電模組
MCP3008 *2  數位類比轉換器
WS2812  LED燈條

Code in Pi：
test.py  感測環境溫溼度以及土壤濕度 顯示、回傳並以土壤濕度來開關水泵
test_GY30.py  感測環境光度並顯示
test_Relay.py  測試繼電器(每隔一秒進行開關)
test_WaterSensor  感測水位並顯示(有問題)
INA219.py  顯示電量等供電相關資訊


### upload images
```
import requests as rq
url = "http://140.117.71.98:8000/api/plantimg/"
data = {'sensor' : <value>} 
files= {'img' : open(<filename>, 'rb')}
headers= {'Authorization': 'Token 17d4c3dd078de641c04a464af97a5faca0733de8'}
rq.post(url, data=data, files=files, headers=headers)
```
> data key的名稱可能會改
