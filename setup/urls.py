from django.contrib import admin
from django.urls import path, include
from orchestrator.views import UsuarioViewSet, BotViewSet, AutomacaoViewSet, PassoAutomacaoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('bots', BotViewSet, 'Bots')
router.register('usuarios', UsuarioViewSet, 'Usuarios')
router.register('automacoes', AutomacaoViewSet, 'Automações')
router.register('passo_automacoes', PassoAutomacaoViewSet, 'Passos da Automação')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
