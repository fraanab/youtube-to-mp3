from django.urls import path

from . import views

urlpatterns = [
	path('', views.main, name="main"),
	path('convert/', views.download_video, name="convert"),
]
