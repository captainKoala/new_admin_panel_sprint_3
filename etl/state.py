import abc
import json
from json.decoder import JSONDecodeError
from typing import Any, Optional
from datetime import date, datetime


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        return {}


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path) as f:
                data = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            data = {}
        return data

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as f:
            f.write(json.dumps(state))


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        data = self.storage.retrieve_state()
        print(key, value, flush=True)
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        data[key] = value
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        data = self.storage.retrieve_state()
        return data.get(key)

    def is_state(self, key: str, value: Any) -> bool:
        """Проверяет, равно ли состояние по ключу key значению value."""
        saved_value = self.get_state(key)
        return saved_value is not None and value == saved_value
