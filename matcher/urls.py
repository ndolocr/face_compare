from django.urls import path
from .views import compare_faces

urlpatterns = [
    path("compare/", compare_faces, name="compare_faces"),
]