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


class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    # Personalizar o limite de acesso a essa rota
    throttle_classes = [UserRateThrottle, RegisterAnonRateThrottle]

    def perform_create(self, serializer):
        with transaction.atomic():
            user = serializer.save()
            os.makedirs(f"{DIRETORIO_USUARIOS}/{user.id}/Bots", exist_ok=True)


class BotCreateView(generics.CreateAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializers
    permission_classes = [IsAuthenticated]
    # Personalizar o limite de acesso a essa rota
    throttle_classes = [BotCreateUserRateThrottle]

    def perform_create(self, serializer):
        with transaction.atomic():
            # Salva o bot, mas ainda não confirma no banco
            bot = serializer.save(id_cliente=self.request.user)

            # Monta o caminho dos diretórios
            criar_diretorio_robo(str(bot.id), str(bot.id_cliente.id), bot.zip.path)


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
