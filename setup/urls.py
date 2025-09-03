from django.contrib import admin
from django.urls import path, include
from orchestrator.views import (BotCreateView, ListaBots, AutomacaoCreateView, ListaAutomacoes,
                                login_page, register_page, dashboard_page)
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('bots/<uuid:pk>/', ListaBots.as_view()),
    path('bots/create/', BotCreateView.as_view()),
    path('automacoes/<uuid:pk>/', ListaAutomacoes.as_view()),
    path('automacoes/create/', AutomacaoCreateView.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path("login/", login_page, name="login-page"),
    path("register/", register_page, name="register-page"),
    path("dashboard/", dashboard_page, name="dashboard-page"),
]
