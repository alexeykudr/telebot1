import aiohttp
import asyncio


class ClientError(Exception):
    def __init__(self, response, content):
        self.response = response
        self.content = content


class Client:
    BASE_PATH = 'https://api.telegram.org/bot'
    TOKEN = '1972167855:AAHfbjW3B7DX6DWtfmJRH4_eOxPtx3TdkH4/'

    def __init__(self):
        self.session = aiohttp.ClientSession(trust_env=True)

    async def __aenter__(self):
        return self

    async def get_base_path(self):
        return self.BASE_PATH

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_path(self, url: str):
        '''чтоб не формировать урл каждый раз'''
        # print('{}{}/'.format(self.BASE_PATH, self.TOKEN, url))
        return '{}{}{}'.format(self.BASE_PATH, self.TOKEN, url)

    async def get_file_path(self, file_path: str):
        return 'https://api.telegram.org/file/bot1972167855:AAHfbjW3B7DX6DWtfmJRH4_eOxPtx3TdkH4/{}'.format(file_path)

    async def _handle_response(self, response):
        '''обработка ответа'''
        return await response.json()

    async def file_by_chunks_download(self, link:str , dest_path:str):
        async with self.session.get(link) as file_resp:
            # print(file_resp)
            with open(dest_path, 'wb') as fd:
                async for data in file_resp.content.iter_chunked(1024):
                    fd.write(data)

    async def _send_request(self, method, url, **kwargs):
        async with self.session.request(method, url, **kwargs) as resp:
            # print('main function')
            # print(await resp.json())
            # print('-------------')
            return await self._handle_response(resp)

