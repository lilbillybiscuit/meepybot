import requests
import random
import json

baseurl="https://oeis.org/search?q=id%3AA8J34TUMHW2ihsd&sort=&language=&go=Search&fmt=json"
max_id=349238
def randomid():
    return random.randrange(0, max_id)

async def getoeis(id):
    url = baseurl.replace("8J34TUMHW2ihsd", str(id))
    response = requests.get(url)
    data = json.loads(response.text)
    return data

async def getinfofromsequence(searchstr):
    url="https://oeis.org/search?q="+searchstr+"&sort=&language=&go=Search&fmt=json"
    response = requests.get(url)
    data = json.loads(response.text)
    if data['results'] == None:
        return "No result", "Try something else"
    return data['results'][0]['name'], data['results'][0]['data']

async def getinfo(id):
    data = await getoeis(id)
    
    if data['results'] == None:
        return "No result", "Try something else"
    return data['results'][0]['name'], data['results'][0]['data']
    
