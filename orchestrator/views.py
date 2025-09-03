import os
from orchestrator.models import Bot, Automacao, PassoAutomacao
from orchestrator.serializers import (BotSerializers, AutomacaoSerializers, PassoAutomacaoSerializers,
                                      ListaBotSerializers, ListaAutomacaoSerializers, CustomUserSerializer)
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from orchestrator.environment import criar_diretorio_robo, DIRETORIO_USUARIOS
from django.shortcuts import render
from orchestrator.throttles import RegisterAnonRateThrottle, BotCreateUserRateThrottle, UserRateThrottle
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def dashboard_data(request):
    # Simulação de dados, depois podemos integrar com o banco
    mock_data = {
        "24h": {"success": 80, "fail": 20},
        "7d": {"success": 450, "fail": 100},
        "30d": {"success": 1500, "fail": 400},
    }

    period = request.GET.get("period", "24h")
    data = mock_data.get(period, {"success": 0, "fail": 0})

    return JsonResponse(data)


class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    # Personalizar o limite de acesso a essa rota
    throttle_classes = [UserRateThrottle, RegisterAnonRateThrottle]

    def perform_create(self, serializer):
        with transaction.atomic():
            user = serializer.save()
            os.makedirs(f"{DIRETORIO_USUARIOS}/{user.id}/Bots", exist_ok=True)


@login_required
def bots_view(request):
    # Obtém todos os bots do usuário logado
    bots = Bot.objects.filter(usuario=request.user)

    context = {
        "bots": bots
    }
    return render(request, "orchestrator/bots.html", context)


class ListaBots(generics.ListAPIView):
    def get_queryset(self):
        queryset = Bot.objects.filter(id=self.kwargs['pk'], id_cliente=str(self.request.user.id))
        return queryset

    serializer_class = ListaBotSerializers


class AutomacaoCreateView(generics.CreateAPIView):
    queryset = Automacao.objects.all()
    serializer_class = AutomacaoSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Define o usuário logado como dono do bot
        serializer.save(id_cliente=self.request.user)


class ListaAutomacoes(generics.ListAPIView):
    def get_queryset(self):
        queryset = Automacao.objects.filter(id_automacao=self.kwargs['pk'], id_cliente=self.request.user.id)
        return queryset

    serializer_class = ListaAutomacaoSerializers


class PassoAutomacaoViewSet(viewsets.ModelViewSet):
    queryset = PassoAutomacao.objects.all()
    serializer_class = PassoAutomacaoSerializers
    permission_classes = [IsAuthenticated]


def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def dashboard_page(request):
    return render(request, "dashboard.html")
