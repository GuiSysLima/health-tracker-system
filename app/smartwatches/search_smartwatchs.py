import aiohttp
import asyncio

async def fetch(session, base_url,  port, responses):
    url = f"{base_url}:{port}/data"
    print(f"Try to connect to : {url}")
    try:
        async with session.get(url) as response:
            if response.status == 200:
                sw = await response.json()
                sw["port"] = port
                responses.append(sw)
    except Exception as e:
        print(f"Inoperative port ({port})")


async def search(initial_port, interval, base_url):
    async with aiohttp.ClientSession() as session:
        ports = [initial_port + x for x in range(interval)]
        responses = []
        tasks = [fetch(session, base_url, port, responses) for port in ports]
        await asyncio.gather(*tasks)
        return responses