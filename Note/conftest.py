import pytest
from .services import NoteService

@pytest.fixture
def note_service():
    return NoteService()