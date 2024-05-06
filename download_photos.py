import asyncio
import aiohttp
import aiofiles
import socket
from config import headers, timeout

async def download(url, idx, session, path):
    correct_idx = "{:06d}".format(idx)
    filename = f"{path}{correct_idx}.jpg"
    try:
        async with session.get(url) as response:
            content = await response.read()
            await asyncio.sleep(0)
            async with aiofiles.open(filename, "wb") as f:
                await f.write(content)
    except aiohttp.client_exceptions.InvalidURL:
        print("invalid url: ", url)
    except aiohttp.client_exceptions.ClientPayloadError:
        print("error downloading: ", url)
    except (aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError):
        pass
        


async def download_all(urls, indexes, path):
    images =[{'url':urls[i], 'idx':indexes[i]} for i in range(len(urls))]
    conn = aiohttp.TCPConnector(
        family=socket.AF_INET,
        verify_ssl=False,
    )
    async with aiohttp.ClientSession(connector=conn, trust_env=True, timeout=aiohttp.ClientTimeout(total=None,sock_connect=timeout,sock_read=timeout)) as session:
        await asyncio.gather(
            *[download(img['url'], img['idx'], session, path) for img in images]
        )


