import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# =========================================================
#  USER MODEL CUSTOMIZADO
# =========================================================

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa de um endereço de email.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        # Melhoria: validação mais segura
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True.")
        if not password:
            raise ValueError("Superuser precisa ter uma senha.")
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.id)


# =========================================================
#  STATUS PADRONIZADOS (REUTILIZÁVEL)
# =========================================================

class Status(models.TextChoices):
    PARADO = "parado", "Parado"
    RODANDO = "rodando", "Rodando"
    FALHA = "falha", "Falha"
    SUCESSO = "sucesso", "Sucesso"


# =========================================================
#  BOT MODEL
# =========================================================

class Bot(models.Model):
    TIPO = (
        ('python', 'python'),
        ('robot', 'robot')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bots")
    nome = models.CharField(max_length=255)
    tipo = models.CharField(choices=TIPO, blank=False, null=False, default='python')
    zip = models.FileField(upload_to="bots_zip/", blank=True, null=True)
    diretorio = models.CharField(max_length=500)
    entrypoint = models.CharField(max_length=255)

    class Meta:
        constraints = [
            # Garantir que cada cliente só possa ter bots com nomes únicos
            models.UniqueConstraint(fields=["id_cliente", "nome"], name="unique_nome_por_cliente")
        ]

    def __str__(self):
        dados = {
            'nome': self.nome
        }
        return str(dados)


# =========================================================
#  AUTOMAÇÃO
# =========================================================

class Automacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="automacoes")
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PARADO)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["id_cliente", "nome"], name="unique_automacao_por_cliente")
        ]

    def __str__(self):
        dados = {
            'nome': self.nome
        }
        return str(dados)


# =========================================================
#  PASSOS DA AUTOMAÇÃO
# =========================================================

class PassoAutomacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="passos")
    id_automacao = models.ForeignKey(Automacao, on_delete=models.CASCADE, related_name="passos")
    id_bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="passos")
    nome = models.CharField(max_length=255)
    ordem = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PARADO)

    class Meta:
        constraints = [
            # Impede duas etapas com mesma ordem dentro da mesma automação
            models.UniqueConstraint(fields=["id_automacao", "ordem"], name="unique_ordem_por_automacao")
        ]

    def __str__(self):
        return str(self.id)


# =========================================================
#  LOG DE EXECUÇÃO DE ROBÔS
# =========================================================

class LogRobot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="logs")
    id_automacao = models.ForeignKey(Automacao, on_delete=models.CASCADE, related_name="logs")
    id_bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="logs")
    data_hora = models.DateTimeField(default=timezone.now)
    link = models.URLField(max_length=500)

    def __str__(self):
        return str(self.id)


# =========================================================
#  AGENDAMENTO DE AUTOMAÇÕES
# =========================================================

class Agendamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="agendamentos")
    id_automacao = models.ForeignKey(Automacao, on_delete=models.CASCADE, related_name="agendamentos")
    nome = models.CharField(max_length=255)
    ativo = models.BooleanField(default=False)
    cron = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["id_cliente", "nome"], name="unique_agendamento_por_cliente")
        ]

    def __str__(self):
        return self.nome
