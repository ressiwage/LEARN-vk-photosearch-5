import requests as r
import json as j
import time as t
from ._imports import config
response = r.post(
    "https://api.vk.com/method/account.getProfileInfo",
    headers=config.headers,
    data={
        "access_token": config.token,
        "v": "5.199",
    },
)
user_id = response.json()["response"]["id"]
# get available albums
data = {
    "owner_id": user_id,
    "access_token": config.token,
    "v": "5.199",
}
response = r.post(
    "https://api.vk.com/method/photos.getAlbums", headers=config.headers, data=data
).json()
oldsaved = [i for i in response['response']['items'] if i['title']=='старые сохраненные'][0]['id']

print(user_id)

data = {
    "owner_id": user_id,
    "album_id": 'saved',
    "rev": "1",
    "extended": "0",
    "access_token": config.token,
    "v": "5.199",
    "offset": 0,
    "count": 1,
}

first_50_photos = r.post(
    "https://api.vk.com/method/photos.get", headers=config.headers, data=data
)
length = first_50_photos.json()["response"]["count"]
limit = int(input(f'введите лимит фотографий. максимальное возможное значение: {length} '))
data["count"] = min(limit, 1000)


all_ids=[]
for offset in range(0, length, 1000):
    data["offset"] = offset
    resp = r.post("https://api.vk.com/method/photos.get",
            headers=dict(config.headers),
            data=dict(data))
    # print(resp.json())
    j.dump(resp.json(), open('1.json', 'w+'), ensure_ascii=False, indent=2)
    ids = [i['id'] for i in resp.json()['response']['items']]
    print(ids)
    all_ids = all_ids+ids


data = {
        'owner_id': user_id,
        'target_album_id': oldsaved,
        'photo_id': None,
        'access_token': config.token,
        'v': '5.236',
    }
for i in all_ids:
    data['photo_id']=i
    response = r.post('https://api.vk.com/method/photos.move', headers=config.headers, data=data)
    t.sleep(1)