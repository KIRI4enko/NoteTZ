from django.db.models import Q, QuerySet
from .models import Note, Tag

class TagRepository:
    @staticmethod
    def get_or_create_tags(tag_names: list[str]) -> list[Tag]:
        """
        Принимает список названий тегов, находит существующие 
        и создает недостающие. Избегает дубликатов.
        """
        # Убираем пробелы, приводим к нижнему регистру и удаляем дубликаты из самого запроса
        cleaned_names = list(set(name.strip().lower() for name in tag_names if name.strip()))
        
        tags = []
        for name in cleaned_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        return tags


class NoteRepository:
    @staticmethod
    def create(title: str, text: str) -> Note:
        """Создает "голую" заметку без тегов."""
        return Note.objects.create(title=title, text=text)

    @staticmethod
    def add_tags(note: Note, tags: list[Tag]) -> None:
        """Связывает теги с заметкой (Many-to-Many)."""
        note.tags.add(*tags)

    @staticmethod
    def get_by_id(note_id: int) -> Note | None:
        """Возвращает заметку по ID вместе с предзагруженными тегами (оптимизация)."""
        try:
            return Note.objects.prefetch_related('tags').get(id=note_id)
        except Note.DoesNotExist:
            return None

    @staticmethod
    def list(tag_filter: str | None = None, search_query: str | None = None) -> QuerySet[Note]:
        """Возвращает список заметок с поддержкой фильтрации и поиска."""
        queryset = Note.objects.prefetch_related('tags').order_by('-created_at')

        # Фильтрация по тегу
        if tag_filter:
            queryset = queryset.filter(tags__name__iexact=tag_filter.strip())

        # Фильтрация по заголовку или тексту
        if search_query:
            q = search_query.strip()
            by_title = queryset.filter(title__icontains=q)
            by_text = queryset.filter(text__icontains=q)
            
            queryset = by_title | by_text  

        return queryset