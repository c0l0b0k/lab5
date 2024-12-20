from fastapi import HTTPException, status, Depends, Body, FastAPI

from typing import *
from .auth import get_current_user
from .database.Neo4jDatabase import Neo4jDatabase
import logging
from .config import *
from dotenv import load_dotenv
from app.models import GraphSegment

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()


# Конфигурация подключения к базе данных Neo4j
db = Neo4jDatabase(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD, database=NE04J_DATABASE)

@app.get("/nodes/")
def get_all_nodes():

    return db.get_all_nodes()

@app.get("/nodes/{node_id}")
def get_node_with_relations(node_id: str):
    node_data = db.get_node_with_relations(node_id)
    if not node_data:
        raise HTTPException(status_code=404, detail="Node not found")
    return node_data

@app.post("/add/nodes/", dependencies=[Depends(get_current_user)])
def add_graph_segment(segment: GraphSegment):
    return db.add_graph_segment(segment)

@app.delete("/delete/nodes/", dependencies=[Depends(get_current_user)])
def delete_graph_segments_route(node_ids: List[str] = Body(...)):
    try:
        result = []
        for node_id in node_ids:
            try:
                db.delete_graph_segment(node_id)
                result.append({
                    "node_id": node_id,
                    "status": "success",
                    "message": f"Node {node_id} deleted successfully"
                })
            except HTTPException as e:
                # Если возникла ошибка на уровне базы данных
                result.append({"node_id": node_id, "status": "failed", "message": str(e.detail)})
            except Exception as e:
                # Обработка других исключений
                result.append({"node_id": node_id, "status": "failed", "message": f"Error: {str(e)}"})

        # Возвращаем результат об успешном удалении и ошибках
        return {"message": "Segments deletion completed", "details": result}
    except HTTPException as http_exc:
        # Обработка исключений HTTPException для ошибок, которые были выброшены внутри метода
        raise http_exc

    except Exception as e:
        # Если произошла ошибка на уровне базы данных или выполнения запроса
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting nodes: {str(e)}"
        )



