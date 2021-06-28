# IotFarm

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
