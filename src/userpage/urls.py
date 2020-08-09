from django.urls import path
from .views import my_profile,u_profile
urlpatterns = [
    path('my-profile',my_profile),
    path('<str:slug>',u_profile),
]