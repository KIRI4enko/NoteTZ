import pytest
from .models import Note, Tag

@pytest.mark.django_db
class TestNoteService:

    def test_create_note_creates_tags_correctly(self, note_service):
        """
        Проверяем базовый сценарий создания заметки.
        Новые теги должны создаться, а заметка должна связаться с ними.
        """
       
        note = note_service.create_note(
            title="Изучаем Django Ninja",
            text="Это быстрый фреймворк на базе Pydantic",
            tag_names=["Python", "DjangO", "ninja"]
        )

        assert Note.objects.count() == 1
        assert Tag.objects.count() == 3
        
        assert note.title == "Изучаем Django Ninja"
        assert note.tags.count() == 3

        tag_names = list(note.tags.values_list('name', flat=True))
        assert "python" in tag_names
        assert "django" in tag_names

    def test_create_note_reuses_existing_tags(self, note_service):
        """
        Проверяем требование ТЗ: если тег уже существует — использовать его,
        не создавать дубликаты тегов в базе.
        """
        
        existing_tag = Tag.objects.create(name="python")

        note = note_service.create_note(
            title="Еще одна заметка",
            text="Текст",
            tag_names=[" PYTHON ", "django"]  
        )

        assert Tag.objects.count() == 2 
        assert note.tags.count() == 2
        
        assert note.tags.filter(id=existing_tag.id).exists()

    def test_get_notes_list_filtering_by_tag(self, note_service):
        """Проверяем фильтрацию списка заметок по тегу."""

        note_python = note_service.create_note("Title 1", "Text 1", ["python"])
        note_js = note_service.create_note("Title 2", "Text 2", ["javascript"])

        filtered_notes = note_service.get_notes_list(tag="python")

        assert len(filtered_notes) == 1
        assert note_python in filtered_notes
        assert note_js not in filtered_notes

    def test_get_notes_list_searching_by_text(self, note_service):
        """Проверяем текстовый поиск"""
        # Arrange
        note_1 = note_service.create_note("Помидоры", "Купить в магазине", ["shopping"])
        note_2 = note_service.create_note("Купить молоко", "Свежее в магазине", ["shopping"])
        note_3 = note_service.create_note("Планы на вечер", "Погулять", ["chill"])

        results_title = note_service.get_notes_list(search="молоко")
        assert len(results_title) == 1
        assert note_2 in results_title

        results_text = note_service.get_notes_list(search="магазине")
        assert len(results_text) == 2
        assert note_1 in results_text

        results_shared = note_service.get_notes_list(search="куп")
        assert len(results_shared) == 2
        assert note_1 in results_shared
        assert note_2 in results_shared

    def test_get_notes_list_combined_filters(self, note_service):
        """Проверяем фильтрации по тегу и тексту"""
        note_1 = note_service.create_note("Купить хлеб", "Белый", ["fastfood"])
        note_2 = note_service.create_note("Купить бургер", "Очень вкусный", ["fastfood"])
        note_3 = note_service.create_note("Купить бургер", "Домашний", ["healthy"])

        results = note_service.get_notes_list(tag="fastfood", search="бургер")

        assert len(results) == 1
        assert note_2 in results

    def test_get_note_by_id_returns_none_if_not_exists(self, note_service):
        """Проверяем, что запрос несуществующей заметки возвращает None (для дальнейшей обработки в 404)."""
        note = note_service.get_note(note_id=999)

        assert note is None