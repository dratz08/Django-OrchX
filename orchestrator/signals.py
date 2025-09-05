from django.db.models.signals import post_save
from django.dispatch import receiver
from orchestrator.models import CustomUser
from rest_framework.validators import ValidationError
from orchestrator.environment import criar_diretorios_usuario


@receiver(post_save, sender=CustomUser)
def criar_env_user(sender, instance, created, **kwargs):
    """
    Cria automaticamente o ambiente do usuário
    """
    if created:
        try:
            criar_diretorios_usuario(instance.id)
        except Exception as e:
            raise ValidationError(f"Erro ao criar diretório do usuário {e}")