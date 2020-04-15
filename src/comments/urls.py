from django.urls import path
from .views import comment_delete,comment_cancel

urlpatterns = [
    path('<str:id>/delete',comment_delete),
    path('<str:id>/cancel',comment_cancel)
]