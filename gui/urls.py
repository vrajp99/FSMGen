from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("submit/", views.submit, name='submit'),
    path("file_upload/", views.file_upload, name='upload'),
]

urlpatterns += staticfiles_urlpatterns()
