import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from orchestrator.models import CustomUser, Bot
from rest_framework.validators import ValidationError
from orchestrator.environment import criar_diretorios_usuario, deletar_diretorio, criar_diretorio_robo

DIRETORIO_USUARIOS = os.getenv("DIRETORIO_USUARIOS_ORCHX")


@receiver(post_save, sender=CustomUser)
def criar_env_user(sender, instance, created, **kwargs):
    """
    Cria automaticamente o ambiente do usuário
    """
    if created:
        criar_diretorios_usuario(instance.id)


@receiver(post_save, sender=Bot)
def criar_robo_dir(sender, instance, created, **kwargs):
    """
    Cria automaticamente o diretório de um robô
    """
    if created:
        try:
            criar_diretorio_robo(instance.id, instance.id_cliente, instance.zip)
        except Exception as e:
            os.remove(str(instance.zip))
            print(f"Não foi possível criar o diretório do robô: {e}")