# IotFarm

### upload images

```
import requests as rq
url = "http://140.117.71.98:8000/api/plantimg/"
data = {'name' : <value>, 'sensor' : <value>} 
files= {'img' : open(<filename>, 'rb')}
headers= {'Authorization': 'Token 6f912937f328aebb0e50fafe9f7b0fcf4e2a466a'}
rq.post(url, data=data, files=files, headers=headers)
```
> data key的名稱可能會改
