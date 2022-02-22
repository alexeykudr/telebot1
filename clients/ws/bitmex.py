import aiohttp
import asyncio
import json

url_to_connect = 'wss://ws.bitmex.com/realtime'
async def fetch_10() -> list[float]:
    price_list = list()
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url_to_connect) as ws:
            await ws.send_json({"op": "subscribe", "args": ["instrument:XBTUSD"]})
            async for msg in ws:
                non_formated_data = (msg[1])
                # print(non_formated_data)
                if len(price_list) == 10:
                    break
                else: price_list.append(non_formated_data)

            await ws.close()
        await session.close()
    return price_list
