from httpx import AsyncClient
from src.config.settings import settings

test_full_link = 'https://www.google.ru/search?q=first'
test_shorten_link = None

async def test_create_shorten_link(ac: AsyncClient):
    response = await ac.post("v1/shortener", params={'full_link': test_full_link})
    assert response.status_code == 201

    shorten_link = response.json()['shorten_link']
    assert shorten_link
    assert shorten_link.split('/')[0] == settings.BASE_URL
    assert len(shorten_link.split('/')[1]) == settings.URL_TAIL_LENGTH

    global test_shorten_link
    test_shorten_link = shorten_link


async def test_retrieve_shorten_link(ac: AsyncClient):
    response = await ac.get("v1/shortener", params={'shorten_link': test_shorten_link})
    assert response.status_code == 200
    
    full_link = response.json()['full_link']
    assert full_link == test_full_link


async def test_delete_shorten_link(ac: AsyncClient):
    response = await ac.delete("v1/shortener", params={'shorten_link': test_shorten_link})
    assert response.status_code == 204


async def test_retrieve_deleted_shorten_link(ac: AsyncClient):
    response = await ac.get("v1/shortener", params={'shorten_link': test_shorten_link})
    assert response.status_code == 404

