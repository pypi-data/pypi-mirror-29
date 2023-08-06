import aiohttp
import asyncio
import json
import logging
import platform

from .user import User, UserConnection
from .guild import Guild, GuildMember
from .base import DiscordObject
from .version import VERSION_STR
from .constants import DISCORD_API_URL
from .channel import Channel, ChannelMessage
from .emoji import Emoji
from .exceptions import WebSocketCreationError, AuthorizationError, UnhandledEndpointStatusError
from .enums import GatewayOpcodes

import logging
logger = logging.getLogger(__name__)


class RateLimit(DiscordObject):
    def __init__(self, message="", retry_after=0, _global=False):
        self.message = message
        self.retry_after = retry_after
        self._global = _global


class HTTPHandler:
    def __init__(self, token, discord_client):
        self.token: str = token
        self.loop = asyncio.get_event_loop()
        self.headers: dict = None
        self.update_headers()
        self.session: aiohttp.ClientResponse = None
        self.discord_client = discord_client

    async def create_session(self):
        self.update_headers()
        self.session = aiohttp.ClientSession(
            headers=self.headers, auto_decompress=True)

    async def close_session(self):
        await self.session.close()
        logger.debug('Session closed!')

    def update_headers(self):
        self.headers = {'Authorization': 'Bot ' + self.token,
                        'User-Agent': f'DiscordBot (https://github.com/Ryozuki/discord.aio, {VERSION_STR})'}
    
    def get_client(self):
        return self.discord_client

    async def request_url(self, url, type='GET', data=None):
        while True:
            operation = None
            if type == 'GET':
                operation = self.session.get(DISCORD_API_URL + url)
            elif type == 'POST':
                operation = self.session.post(DISCORD_API_URL + url, data=data)
            elif type == 'DELETE':
                operation = self.session.delete(DISCORD_API_URL + url)

            async with operation as res:
                if res.status == 429:
                    limit = await RateLimit.from_api_res(res)

                    if 'X-RateLimit-Remaining' in res.headers and int(res.headers['X-RateLimit-Remaining']) > 0:
                        logger.debug(
                            f"Status is {res.status} but i have {res.headers['X-RateLimit-Remaining']} ratelimits remaining, ")
                        continue

                    logger.debug(
                        f"Status is {res.status} so we must wait {limit.retry_after / 1000} seconds!")
                    await asyncio.sleep(limit.retry_after / 1000)
                    logger.debug("Done waiting! Requesting again")
                elif res.status < 300 and res.status >= 200:
                    return await res.json()
                elif res.status == 401:
                    raise AuthorizationError
                else:
                    raise UnhandledEndpointStatusError
