from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('nova/', views.nova_transacao, name='nova_transacao'),
    path('nova-meta/', views.nova_meta, name='nova_meta'),
    path('editar/<int:id>/', views.editar_transacao, name='editar_transacao'),   # Nova
    path('excluir/<int:id>/', views.excluir_transacao, name='excluir_transacao'), 
    path('categoria/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('perfil/', views.perfil, name='perfil')
]