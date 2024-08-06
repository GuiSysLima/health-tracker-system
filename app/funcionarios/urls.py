from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('listar/', views.listar_funcionarios, name='listar_funcionarios'),
    path('excluir/<int:funcionario_id>/', views.excluir_funcionario, name='excluir_funcionario'),
    path('perfil/<int:funcionario_id>/', views.perfil_funcionario, name='perfil_funcionario'),
]