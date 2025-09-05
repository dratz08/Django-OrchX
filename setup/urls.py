from django.contrib import admin
from django.urls import path, include
from orchestrator.views import (BotViewSet, AutomacaoViewSet, PassoAutomacaoViewSet, AgendamentoViewSet)
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
router.register('bots', BotViewSet, 'Bots')
router.register('automacoes', AutomacaoViewSet, 'Automações')
router.register('passos', PassoAutomacaoViewSet, 'Passos')
router.register('agendamentos', AgendamentoViewSet, 'Agendamentos')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
