from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from Note.api import router

api = NinjaAPI(title="Notes API")

api.add_router("/notes", router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api.urls),  
]