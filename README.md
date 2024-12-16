
# VK API Lab5

VK API Lab5 — это проект на Python для работы с данными из социальной сети ВКонтакте с использованием базы данных Neo4j.

## Установка и Запуск Проекта

### Шаг 1: Клонирование Репозитория

1. Склонируйте репозиторий проекта:

   ```cmd
   git clone https://github.com/c0l0b0k/lab5.git
   ```

2. Перейдите в директорию проекта:

   ```cmd
   cd lab5
   ```

### Шаг 3: Создание и Активация Виртуального Окружения

1. Создайте виртуальное окружение:

   ```cmd
   python -m venv venv
   ```

2. Активируйте виртуальное окружение:
     ```cmd
     .\venv\Scripts\activate
     ```

### Шаг 4: Установка Зависимостей

Установите все зависимости проекта, используя команду:

```cmd
pip install -r requirements.txt
```

### Шаг 5: Настройка PYTHONPATH

Убедитесь, что переменная окружения `PYTHONPATH` настроена корректно:

```cmd
set PYTHONPATH=%PYTHONPATH%;C:\путь\к\вашему\проекту
```

### Шаг 6: Настройка Neo4j
загрузите дамп
настройте env:
NEO4J_URI=neo4j://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=K9V-kz2-5Am-gwD
NEO4J_DATABASE=lab4

### Шаг 8: Запуск Тестов

Для запуска тестов используйте команду **pytest**, будут проведены тесты для модели данных и тесты на каждую точку доступа:

```cmd
pytest
```

## Документация для точек доступа
запустите сервер
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

### 1. Получение всех узлов

#### HTTP-метод: `GET`

**URL**: `/nodes/`

**Описание**: Получить все узлы в базе данных.

**Пример запроса**:
```bash
curl -X GET "http://127.0.0.1:8000/nodes/"
```

### 2. Получение узла по ID с его связями

#### HTTP-метод: `GET`

**URL**: `/nodes/{node_id}`

**Описание**: Получить узел по указанному ID с его связями.

**Пример запроса**:
```bash
curl -X GET "http://127.0.0.1:8000/nodes/1"
```

### 3. Добавление новых узлов

#### HTTP-метод: `POST`

**URL**: `/add/nodes/`

**Описание**: Добавить новые узлы и их связи в базу данных.

**Пример запроса**:
```bash
curl -X POST "http://127.0.0.1:8000/add/nodes/" -H "Authorization: Bearer token" -H "Content-Type: application/json" -d "{"users": [{"id": "1"}, {"id": "2"}], "groups": [{"id": "3"}], "relations": [{"start_id": "1", "end_id": "2", "type": "follow"}, {"start_id": "2", "end_id": "3", "type": "subscribe"}]}"
```

### 4. Удаление узлов

#### HTTP-метод: `DELETE`

**URL**: `/delete/nodes/`

**Описание**: Удалить узлы по указанным ID.

**Пример запроса**:
```bash
curl -X DELETE "http://127.0.0.1:8000/delete/nodes/" -H "Authorization: Bearer token" -H "Content-Type: application/json" -d "["1", "2", "3"]"
```
