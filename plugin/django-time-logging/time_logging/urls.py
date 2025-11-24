from django.urls import path
from . import views

urlpatterns = [
    path("", views.TimeLogListView, name="time_logging"),
]
