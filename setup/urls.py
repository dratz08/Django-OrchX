from django.contrib import admin
from django.urls import path, include
from orchestrator.views import (bots_view, ListaBots, AutomacaoCreateView, ListaAutomacoes,
                                login_page, register_page, dashboard_page, dashboard_data)
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path("bots/", bots_view, name="bots"),
    path('automacoes/<uuid:pk>/', ListaAutomacoes.as_view()),
    path('automacoes/create/', AutomacaoCreateView.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path("login/", login_page, name="login-page"),
    path("register/", register_page, name="register-page"),
    path("dashboard/", dashboard_page, name="dashboard-page"),
    path("api/dashboard-data/", dashboard_data, name="dashboard_data"),
]
