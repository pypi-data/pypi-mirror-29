import aiohttp
import asyncio
from box import Box
from .errors import *

class AsyncClient:
    '''The Asynchronous client for brawl stars API.

    The Asynchronous client for brawl stars API.
    Methods are in snake_case.
    Attributes are in camelCase.
    '''

    def __init__(self, token, timeout=5):
        self.baseUrl = 'https://brawlstars-api.herokuapp.com/api/'
        self.session = aiohttp.ClientSession()
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Umbresp | Python (Async)',
            'Authorization': token
        }

    def __del__(self):
        self.session.close()

    def __repr__(self):
        return f'<Asynchronous BS Client timeout = {self.timeout}>'

    async def get_player(self, tag=None):
        if tag is None:
            raise MissingArg('tag')

        tag = tag.strip("#")
        tag = tag.upper()

        try:
            async with self.session.get(f'{self.baseUrl}players/{tag}', timeout=self.timeout, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                elif 500 > resp.status > 400:
                    raise HTTPError(resp.status)
                else:
                    raise Error()
        except asyncio.TimeoutError:
            raise Timeout()
        except Exception:
            raise InvalidArg('tag')


        data = Box(data)
        player = Player(data)
        return player

class Player(Box):

    async def get_id(self):
        try:
            ret = self.id
        except AttributeError:
            return None
        ret = Box(ret)
        ret = Id(ret)
        return ret

    async def get_brawlers(self):
        try:
            brawlers = self.brawlers
        except AttributeError:
            return None

        something = []
        for brawler in brawlers:
            thing = Box(brawler)
            thing = Brawler(thing)
            something.append(thing)

        return something

class Id(Box):
    pass

class Brawler(Box):
    pass
