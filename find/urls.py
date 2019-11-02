from django.urls import path

from . import views

urlpatterns = [
    path('', views.find_fasta, name='find_fasta')
]