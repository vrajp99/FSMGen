from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("submit/", views.submit, name='submit'),
    path("file_upload/", views.file_upload, name='upload'),
    path("seq_det/", views.seq_det, name="seq_det"),
]

urlpatterns += staticfiles_urlpatterns()
