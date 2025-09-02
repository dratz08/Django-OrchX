from orchestrator.models import Bot, Automacao, PassoAutomacao
from orchestrator.serializers import (BotSerializers, AutomacaoSerializers, PassoAutomacaoSerializers,
                                      ListaBotSerializers, ListaAutomacaoSerializers)
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from orchestrator.environment import criar_diretorio_robo, deletar_diretorio


class BotCreateView(generics.CreateAPIView):
    queryset = Bot.objects.all()
    serializer_class = BotSerializers
    permission_classes = [IsAuthenticated]

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
