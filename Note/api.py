from ninja import Router
from ninja.errors import HttpError
from .schemas import NoteCreate, NoteOut
from .services import NoteService

router = Router()
note_service = NoteService()  

@router.post("/", response={201: NoteOut})
def create_note(request, data: NoteCreate):
    """Создание заметки по заголовку, тексту [и тегам]"""
    note = note_service.create_note(
        title=data.title, 
        text=data.text, 
        tag_names=data.tag_names
    )
    return 201, note

@router.get("/", response=list[NoteOut])
def list_notes(request, tag: str = None, search: str = None):
    """Получение заметок [с фильтром по тегам и словам]"""
    return note_service.get_notes_list(tag=tag, search=search) 

@router.get("/{note_id}", response=NoteOut)
def get_note(request, note_id: int):
    """Получение одной заметки по ID вместе с тегами."""
    note = note_service.get_note(note_id)
    
    if not note:
        raise HttpError(404, f"Заметка с id {note_id} не найдена")
        
    return note