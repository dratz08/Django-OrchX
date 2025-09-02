import django
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=False, max_length=50, unique=True, validators=[EmailValidator])
    senha = models.CharField(blank=False)

    def __str__(self):
        return self.email


class Bot(models.Model):
    TIPO = (
        ('robot', 'robot'),
        ('python', 'python')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    nome = models.CharField(max_length=100, blank=False)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)
    zip = models.FileField(blank=False)
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
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
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
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_bot = models.ForeignKey(Bot, null=True, on_delete=models.PROTECT)

    # Cria uma relação de unicidade para a ordem de uma mesma automacao
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["id_automacao", "ordem"], name="unique_id_ordem_passo")
        ]

    def __str__(self):
        return self.id


class LogRobot(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
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
    id_automacao = models.ForeignKey(Automacao, on_delete=models.CASCADE)
    cron = models.CharField(max_length=40, blank=False)
    ativo = models.BooleanField(blank=False)
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
