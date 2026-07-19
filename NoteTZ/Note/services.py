from django.db import transaction
from django.db.models import QuerySet
from .repositories import NoteRepository, TagRepository
from .models import Note

class NoteService:
    def __init__(self):
        self.note_repo = NoteRepository()
        self.tag_repo = TagRepository()

    def create_note(self, title: str, text: str, tag_names: list[str]) -> Note:
        """
        1. Найти или создать теги.
        2. Создать саму заметку.
        3. Связать их.
        """
        with transaction.atomic():
            # 1. Работаем с тегами
            tags = self.tag_repo.get_or_create_tags(tag_names)
            
            # 2. Создаем заметку
            note = self.note_repo.create(title=title, text=text)
            
            # 3. Привязываем теги к созданной заметке
            if tags:
                self.note_repo.add_tags(note, tags)
                
            return note

    def get_note(self, note_id: int) -> Note | None:
        """Получить одну заметку."""
        return self.note_repo.get_by_id(note_id)

    def get_notes_list(self, tag: str | None = None, search: str | None = None) -> QuerySet[Note]:
        """Получить список заметок с фильтрами."""
        return self.note_repo.list(tag_filter=tag, search_query=search)