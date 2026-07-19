from datetime import datetime
from ninja import Schema

class TagOut(Schema):
    """Схема для вывода тега"""
    id: int
    name: str


class NoteOut(Schema):
    """Схема для отдачи заметки"""
    id: int
    title: str
    text: str
    created_at: datetime
    tags: list[TagOut]  


class NoteCreate(Schema):
    """Схема для создания заметки"""
    title: str
    text: str
    tag_names: list[str] | None = None  


class NoteUpdate(Schema):
    """Схема для частичного или полного обновления заметки."""
    title: str | None = None
    text: str | None = None
    tag_names: list[str] | None = None



class NoteFilterSchema(Schema):
    """Схема для параметров фильтров"""
    tag_filter: str | None = None
    search_query: str | None = None