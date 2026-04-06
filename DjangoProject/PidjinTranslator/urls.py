from django.urls import path

from . import views

app_name = 'pidjin_translator'

urlpatterns = [
    path("api/lexer/analyze", views.analyze, name="lexer_analyze"),
]
