from ninja import NinjaAPI
from .schemas import NoteCreateSchema, NoteOutSchema
from .services import NoteService

api = NinjaAPI()
note_service = NoteService()  

@api.post("/notes", response={201: NoteOutSchema})
def create_note(request, data: NoteCreateSchema):
    note = note_service.create_note(
        title=data.title, 
        text=data.text, 
        tag_names=data.tags
    )
    return 201, note

@api.get("/notes", response=list[NoteOutSchema])
def list_notes(request, tag: str = None, search: str = None):
    return note_service.get_notes_list(tag=tag, search=search)