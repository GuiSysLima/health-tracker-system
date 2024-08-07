from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_smartwatch, name='cadastrar_smartwatch'),
    path("<int:imei>", views.buscar_smartwatch, name='buscar_smartwatch'),
    path('search/', views.search_smartwatches, name='search_smartwatches'),
    path('listar/', views.listar_smartwatches, name='listar_smartwatches'),
    path('atualizar/', views.atualizar_todos_smartwatches, name='atualizar_todos_smartwatches'),
    path('<int:imei>/historico/json/', views.historico_smartwatch_json, name='historico_smartwatch_json'),
]
