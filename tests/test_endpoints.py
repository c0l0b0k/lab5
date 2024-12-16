import logging
import pytest
from httpx import AsyncClient
from app.auth import TOKEN
from app.main import app

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Тест для получения всех узлов
@pytest.mark.asyncio
async def test_get_all_nodes():
    logger.warning("Запуск теста для получения всех узлов")
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/nodes/")
    logger.warning(f"Ответ сервера: {response.status_code}, тело ответа: {response.json()}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Тест для получения узла по ID с его связями
@pytest.mark.asyncio
async def test_get_node_with_relations():
    node_id = "266269575"
    logger.warning(f"Запуск теста для получения узла с ID: {node_id}")
    # Формируем URL запроса
    url = f"/nodes/{node_id}"

    # Логируем итоговый URL запроса
    logger.warning(f"Итоговый URL запроса: {url}")
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.get(url)
    #logger.warning(f"Ответ сервера: {response.status_code}, тело ответа: {response.json()}")

    assert response.status_code == 200
    node = response.json()

    # Correcting the access to match the data structure
    assert str(node[0]["node"]["id"]) == node_id


@pytest.mark.asyncio
async def test_add_graph_segment():
    segment_data = {
        "users": [{"id": "1"}, {"id": "2"}],
        "groups": [{"id": "3"}],
        "relations": [
            {"start_id": "1", "end_id": "2", "type": "follow"},
            {"start_id": "2", "end_id": "3", "type": "subscribe"}
        ]
    }

    #logger.warning("Запуск теста для добавления сегмента графа")
    #logger.warning(f"Данные сегмента: {segment_data}")
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.request(
            method="POST",
            url="/add/nodes/",
            json=segment_data,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
        )
    #logger.warning(f"Ответ сервера: {response.status_code}, тело ответа: {response.json()}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Segment added successfully"

# Тест для удаления графа
@pytest.mark.asyncio
async def test_delete_graph_segment():
    node_ids = ["1", "2"]
    #logger.warning("Запуск теста для удаления сегмента графа")
    #logger.warning(f"Удаляемые узлы: {node_ids}")
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.request(
            method="DELETE",
            url="/delete/nodes/",
            json=node_ids,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
        )
    #logger.warning(f"Ответ сервера: {response.status_code}, тело ответа: {response.json()}")

    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert isinstance(response_data, dict)
