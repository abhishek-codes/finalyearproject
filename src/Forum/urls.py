from django.urls import path
from .views import (
    delete_post_view,
    detail_post_view,
    edit_post_view,
    list_post_view,
)

urlpatterns = [
    path('',list_post_view),
    path('<str:slug>',detail_post_view),
    path('<str:slug>/edit',edit_post_view),
    path('<str:slug>/delete',delete_post_view),
]