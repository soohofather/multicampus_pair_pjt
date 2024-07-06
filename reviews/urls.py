from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("detail/<int:pk>", views.detail, name="detail"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path("update/<int:pk>", views.update, name="update"),
    path("<int:pk>/c_create", views.c_create, name="c_create"),
    path("<int:a_pk>/<int:c_pk>/c_delete", views.c_delete, name="c_delete"),
    path("like/<int:pk>", views.like, name="like"),
]
