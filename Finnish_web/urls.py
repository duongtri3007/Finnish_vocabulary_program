"""
URL configuration for Finnish_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend import views as backend_views
from frontend import views as frontend_views

urlpatterns = [
    path('', frontend_views.main_menu, name='main_menu'),
    path('show_words', frontend_views.show_words, name='show_words'),
    path('add_words', frontend_views.add_word, name='add_word'),
    path('review/', frontend_views.review_options, name='review_options'),
    path('review/flashcards/', frontend_views.review_flashcards, name='review_flashcards'),
    path('review/quiz/', frontend_views.review_quiz, name='review_quiz'),
    path("server/", backend_views.backend),
]
