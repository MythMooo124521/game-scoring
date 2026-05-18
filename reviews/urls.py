from django.urls import path

from reviews import views

urlpatterns = [
    path("add/<slug:slug>/review/", views.add_review, name="add_review"),
]
