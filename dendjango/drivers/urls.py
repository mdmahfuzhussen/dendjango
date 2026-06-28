from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('reviews/submit/', views.submit_review, name='submit_review'),
    path('signup/', views.signup_view, name='signup'),
]