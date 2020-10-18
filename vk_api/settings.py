from os import environ

from vkwave.api import API
from vkwave.client import AIOHTTPClient


vk_api_session = API(
    tokens=environ.get('VK_TOKEN', '13c4022e2aaa8f730efe1ecf6849c9085583267e38fee04d35546c82c9a4ccb8edbf30ac5ca09ac341585'),
    clients=AIOHTTPClient()
)

vk_api = vk_api_session.get_context()
