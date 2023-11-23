import json
import asyncio
import pytest
from app import app
from http import HTTPStatus
from httpx import AsyncClient
from collections.abc import AsyncGenerator, Generator
from utils.helpers import Const
from utils.router import Router


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Фикстура создания экземляра событийного цикла для каждого теста."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура получения сессии клиента."""
    async with AsyncClient(
        app=app.app, base_url="http://127.0.0.1:8000"
    ) as session:
        yield session


async def test_post_visited_links_status_404(ac: AsyncClient):
    response = await ac.post(
        Router.VISITED_LINKS,
        json=json.dumps(
            {
                Const.LINKS: {}
            }
        ),
    )
    assert response.status_code == HTTPStatus.OK
