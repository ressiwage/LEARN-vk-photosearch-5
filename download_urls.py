from config import token, headers
import requests as r
import asyncio
import aiohttp  # pip install aiohttp aiodns
from pick import pick
from db import *


async def post(*args, **kwargs) -> dict:
    # session: aiohttp.ClientSession
    print(kwargs)
    session = kwargs.get("session")
    if session is None:
        raise Exception("session not found in kwargs")
    del kwargs["session"]

    async def __make_request():
        print(f"Requesting {args[0]}")
        resp = await session.request("POST", *args, **kwargs)
        d = await resp.json()
        return d

    data = await __make_request()
    print(f"Received data for {args[0]}")
    # print()
    while "error" in data.keys() and data["error"]["error_code"] == 6:
        print(f"429, retrying...")
        await asyncio.sleep(1)
        data = await __make_request()

    only_urls = [
        {"url": i["sizes"][-1]["url"], "date": i["date"]}
        for i in data["response"]["items"]
    ]
    return only_urls


async def download_links():
    create()
    # get userid
    response = r.post(
        "https://api.vk.com/method/account.getProfileInfo",
        headers=headers,
        data={
            "access_token": token,
            "v": "5.199",
        },
    )
    user_id = response.json()["response"]["id"]
    # get available albums
    data = {
        "owner_id": user_id,
        "access_token": token,
        "v": "5.199",
    }
    response = r.post(
        "https://api.vk.com/method/photos.getAlbums", headers=headers, data=data
    ).json()
    album_names = ["сохранённые"] + [i["title"] for i in response["response"]["items"]]
    album_ids = ["saved"] + [i["id"] for i in response["response"]["items"]]
    _, index = pick(album_names, "выберите альбом", indicator="=>", default_index=0)
    album_id = album_ids[index]
    # get album length
    data = {
        "owner_id": user_id,
        "album_id": album_id,
        "rev": "1",
        "extended": "0",
        "access_token": token,
        "v": "5.199",
        "offset": 0,
        "count": 1,
    }

    first_50_photos = r.post(
        "https://api.vk.com/method/photos.get", headers=headers, data=data
    )
    length = first_50_photos.json()["response"]["count"]
    limit = int(input(f'введите лимит фотографий. максимальное возможное значение: {length} '))
    data["count"] = min(limit, 1000)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for offset in range(0, length, 1000):
            data["offset"] = offset
            tasks.append(
                post(
                    "https://api.vk.com/method/photos.get",
                    headers=dict(headers),
                    data=dict(data),
                    session=session,
                )
            )

        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls