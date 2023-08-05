import json
import asyncio
import aiohttp

import logging
logger = logging.getLogger(__name__)

class DiscordObject:
    """Base class for discord objects."""

    @classmethod
    async def from_api_res(cls, coro_or_json_or_str):
        """Parses a discord API response"""
        # TODO: Maybe make this asynchronous, search for async_generator object and how to handle them

        json_obj = coro_or_json_or_str

        if isinstance(coro_or_json_or_str, str):
            json_obj = json.loads(coro_or_json_or_str)
        elif asyncio.iscoroutine(coro_or_json_or_str):
            json_obj = await coro_or_json_or_str.json()

        if isinstance(json_obj, list):
            lst = []
            for item in json_obj:
                result = cls()
                for key, value in item.items():
                    if hasattr(result, key):
                        await result._from_api_ext(key, value)
                lst.append(result)
            return lst
        elif isinstance(json_obj, dict):
            result = cls()
            for key, value in json_obj.items():
                if hasattr(result, key):
                    await result._from_api_ext(key, value)
            return result
        else:
            raise ValueError('it must be a dictionary or a list.')

    async def _from_api_ext(self, key, value):
        """Api response decoding extensions, called automatically by DiscordObject.from_api_res().
        Used if the class contains a attribute that it's a class and must be initialized with info,
        also used if the class contains an array of classes as attribute."""
        setattr(self, key, value)
