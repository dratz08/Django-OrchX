import django
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """Manager para criar usuários e superusuários com email"""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("O campo email é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name="E-mail"
    )
    name = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Define que o login será feito com email
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []  # Nenhum campo obrigatório além do email

    objects = CustomUserManager()

    def __str__(self):
        return str(self.id)


class Bot(models.Model):
    TIPO = (
        ('robot', 'robot'),
        ('python', 'python')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    nome = models.CharField(max_length=100, blank=False)
    id_cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zip = models.FileField(blank=False, upload_to="bots_zip/")
    entrypoint = models.CharField(blank=False)
    tipo = models.CharField(max_length=6, choices=TIPO, blank=False, default='robot')
    diretorio = models.CharField(blank=False, default="abc")
    log_timeout = models.IntegerField(blank=False)

    # Cria uma relação de unicidade para os nomes de um mesmo id
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["id", "nome"], name="unique_id_nome_bot")
        ]

    def __str__(self):
        return self.id


class Automacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    nome = models.CharField(max_length=100, blank=False)
    id_cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField()
    descricao = models.CharField(max_length=800)

    # Cria uma relação de unicidade para os nomes de um mesmo id
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["id", "nome"], name="unique_id_nome_automacao")
        ]

    def __str__(self):
        return self.id


class PassoAutomacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    ordem = models.IntegerField(auto_created=True)
    id_automacao = models.ForeignKey(Automacao, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_bot = models.ForeignKey(Bot, null=True, on_delete=models.PROTECT)
    status = models.CharField()

    # Cria uma relação de unicidade para a ordem de uma mesma automacao
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["id_automacao", "ordem"], name="unique_id_ordem_passo")
        ]

    def __str__(self):
        return self.id


class LogRobot(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    id_cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_automacao = models.ForeignKey(Automacao, on_delete=models.CASCADE)
    id_bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    data_hora = models.DateField(default=django.utils.timezone.now)

    tasks_falhas = models.IntegerField()
    tasks_completas = models.IntegerField()
    tasks_puladas = models.IntegerField()
    duracao = models.IntegerField()
    link = models.CharField()

    def __str__(self):
        return self.id


class Agendamento(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    nome = models.CharField(max_length=255)
    id_automacao = models.ForeignKey(Automacao, on_delete=models.CASCADE)
    cron = models.CharField(max_length=40, blank=False)
    ativo = models.BooleanField(blank=False)
    id_cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Cria uma relação de unicidade para os nomes de um mesmo id
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["id", "nome"], name="unique_id_nome_agendamento")
        ]


    def __str__(self):
        return self.id
