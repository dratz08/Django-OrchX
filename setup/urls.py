from django.contrib import admin
from django.urls import path, include
from orchestrator.views import BotCreateView, ListaBots, AutomacaoCreateView, ListaAutomacoes
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('bots/<uuid:pk>/', ListaBots.as_view()),
    path('bots/create/', BotCreateView.as_view()),
    path('automacoes/<uuid:pk>/', ListaAutomacoes.as_view()),
    path('automacoes/create/', AutomacaoCreateView.as_view()),
]
