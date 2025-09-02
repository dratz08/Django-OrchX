from orchestrator.models import Bot, Automacao, PassoAutomacao
from orchestrator.serializers import BotSerializers, AutomacaoSerializers, PassoAutomacaoSerializers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class BotViewSet(viewsets.ModelViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSerializers
    permission_classes = [IsAuthenticated]


# class UsuarioViewSet(viewsets.ModelViewSet):
#     queryset = Usuario.objects.all()
#     serializer_class = UsuarioSerializers
#     permission_classes = [IsAuthenticated]


class AutomacaoViewSet(viewsets.ModelViewSet):
    queryset = Automacao.objects.all()
    serializer_class = AutomacaoSerializers
    permission_classes = [IsAuthenticated]


class PassoAutomacaoViewSet(viewsets.ModelViewSet):
    queryset = PassoAutomacao.objects.all()
    serializer_class = PassoAutomacaoSerializers
    permission_classes = [IsAuthenticated]