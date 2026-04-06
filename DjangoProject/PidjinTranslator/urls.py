from django.urls import path

from . import views

urlpatterns = [
    path("api/lexer/analyze", views.analyze, name="lexer_analyze"),
]
