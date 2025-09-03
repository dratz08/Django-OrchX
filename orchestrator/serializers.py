from rest_framework import serializers
from orchestrator.models import Bot, Automacao, PassoAutomacao, CustomUser
from rest_framework.validators import ValidationError
from orchestrator.zip_validator import validar_arquivo_zip
import re


class BotSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['nome', 'entrypoint', 'zip', 'tipo', 'log_timeout']
        read_only_fields = ["id_cliente"]

    def validate(self, dados):
        padrao_nome = r"^[a-zA-Z_]{3,30}$"
        padrao_entrypoint = r"^[a-zA-Z0-9_]{4,240}\.(py|robot)$"

        if not re.fullmatch(padrao_nome, dados['nome']):
            raise ValidationError({
                'nome': 'O nome deve conter: De 3 a 30 caracteres; Letras e/ou _'
            })

        if not re.fullmatch(padrao_entrypoint, dados['entrypoint']):
            raise ValidationError({
                'entrypoint': 'O entrypoint não deve possuir caracteres inválidos e deve ser do tipo .robot ou .py'
            })

    def validate_zip(self, zip):
        print(self.context["request"].user.id)
        return validar_arquivo_zip(zip)

    def create(self, validated_data):
        validated_data["id_cliente"] = self.context["request"].user
        return super().create(validated_data)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, dados):
        padrao_nome = r"^[a-zA-Z_ ]{3,40}$"
        padrao_senha = r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){8,50}$'

        if not re.fullmatch(padrao_nome, dados['nome']):
            raise ValidationError({
                'nome': 'O nome deve conter: De 3 a 40 caracteres; Letras, _ e/ou espaços'
            })

        if not re.fullmatch(padrao_senha, dados['senha']):
            raise ValidationError({
                "senha": "A senha deve conter: De 8 a 50 caracteres; 1 número 1 letra maiúscula ; "
                        "1 letra minúscula; 1 caractere especial"})
        return dados


class AutomacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Automacao
        fields = ['nome', 'descricao']

    def validate_nome(self, nome):
        padrao = r"^[a-zA-Z_]{3,30}$"
        if not re.fullmatch(padrao, nome):
            raise ValidationError('O nome deve conter: De 3 a 30 caracteres; Letras e/ou _')
        return nome


class PassoAutomacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = PassoAutomacao
        fields = ['id_automacao', 'id_bot']


class ListaBotSerializers(serializers.ListSerializer):
    class Meta:
        model = Bot
        fields = "__all__"


class ListaAutomacaoSerializers(serializers.ListSerializer):
    class Meta:
        model = Automacao
        fields = ['nome', 'descricao']
