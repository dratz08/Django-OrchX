from orchestrator.environment import criar_diretorio_robo
from orchestrator.models import Bot, Automacao, PassoAutomacao, Agendamento
from orchestrator.serializers import (BotSerializers, AutomacaoSerializers, PassoAutomacaoSerializers,
                                      AgendamentoSerializers)
from orchestrator.throttles import RegisterAnonRateThrottle, BotCreateUserRateThrottle, UserRateThrottle
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


class BotViewSet(viewsets.ModelViewSet):
    serializer_class = BotSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Bot.objects.filter(id_cliente=str(self.request.user.id))
        return queryset

    def perform_create(self, serializer):
        with transaction.atomic():
            bot = serializer.save(id_cliente=self.request.user.id)
            criar_diretorio_robo(bot.id, self.request.user.id, bot.zip.path)


# class ListaBots(generics.ListAPIView):
#     def get_queryset(self):
#         queryset = Bot.objects.filter(id=self.kwargs['pk'], id_cliente=str(self.request.user.id))
#         return queryset
#
#     serializer_class = ListaBotSerializers


class AutomacaoViewSet(viewsets.ModelViewSet):
    queryset = Automacao.objects.all()
    serializer_class = AutomacaoSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra as automações para o usuário logado
        return Automacao.objects.filter(id_cliente=self.request.user)

    def perform_create(self, serializer):
        # Define o usuário logado como dono do bot
        serializer.save(id_cliente=self.request.user)
#
#
# class BotCreateView(generics.CreateAPIView):
#     queryset = Automacao.objects.all()
#     serializer_class = BotSerializers
#
#     def perform_create(self, serializer):
#         with transaction.atomic():
#             # Define o usuário logado como dono do bot
#             bot = serializer.save(id_cliente=self.request.user)
#             validar_arquivo_zip(bot.zip.path)
#             criar_diretorio_robo(bot.id, bot.id_cliente.id, bot.zip.path)
#
#
# class ListaAutomacoes(generics.ListAPIView):
#     def get_queryset(self):
#         queryset = Automacao.objects.filter(id_automacao=self.kwargs['pk'], id_cliente=self.request.user.id)
#         return queryset
#
#     serializer_class = ListaAutomacaoSerializers


class PassoAutomacaoViewSet(viewsets.ModelViewSet):
    queryset = PassoAutomacao.objects.all()
    serializer_class = PassoAutomacaoSerializers
    permission_classes = [IsAuthenticated]


class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializers
    permission_classes = [IsAuthenticated]