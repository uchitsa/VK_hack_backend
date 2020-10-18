import json
from typing import List
from .settings import vk_api
from models import Host, Source, PotentialPost, Region, City
from asyncio import sleep
from news_classifier.news_classifier import news_classifier


def get_json(x) -> dict:
    return json.loads(x.json())


def get_json_items(x) -> List:
    return get_json(x)['response']['items']


async def parse_vk_groups():
    """Здесь будут парситься группы вк, пока что ограниченно БГД, просто для теста"""
    for city_id in [26]:
        city_name = (await City.get(id=city_id)).title
        pages = []
        try:
            pages.extend(get_json_items(await vk_api.groups.search(q='Новости', type='group', city_id=city_id))[:30])
        except:
            pass
        try:
            pages.extend(get_json_items(await vk_api.groups.search(q=city_name, type='group', city_id=city_id))[:30])
        except:
            pass
        for group in pages:
            try:
                wall = get_json_items(await vk_api.wall.get(owner_id=-group['id'], count=50))
                await sleep(1)
                for x in wall:
                    await news_classifier.predict(x['text'])
            except Exception as e:
                continue
