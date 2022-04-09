import requests
import time
api_url = "http://127.0.0.1:8080/predictions/sentiments"
text = "I liked this quick tutorial"
starttime = time.time()
response = requests.post(api_url, data=text.encode('utf-8'), headers={'Content-Type': 'text/plain'})

if response.status_code == 200: 
    predictionOut = str(response.content.decode())
    print(predictionOut)
    
    
print("call response received in (seconds) ", time.time() - starttime)     