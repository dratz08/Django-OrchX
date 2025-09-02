from rest_framework import serializers
from orchestrator.models import Bot, Usuario, Automacao, PassoAutomacao
from rest_framework.validators import ValidationError
from orchestrator.zip_validator import validar_arquivo_zip
import re


class BotSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['nome', 'entrypoint', 'zip', 'tipo', 'log_timeout']

    def validate_nome(self, nome):
        padrao = r"^[a-zA-Z_]{3,30}$"
        if not re.fullmatch(padrao, nome):
            raise ValidationError('O nome deve conter: De 3 a 30 caracteres; Letras e/ou _')
        return nome

    def validate_entrypoint(self, entrypoint):
        padrao = r"^[a-zA-Z0-9_]{4,240}\.(py|robot)$"
        if not re.fullmatch(padrao, entrypoint):
            raise ValidationError('O entrypoint não deve possuir caracteres inválidos e deve ser do tipo .robot ou .py')
        return entrypoint

    def validate_zip(self, zip):
        print(self.context["request"].user.id)
        return validar_arquivo_zip(zip)


class UsuarioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def validate_nome(self, nome):
        padrao = r"^[a-zA-Z_ ]{3,40}$"
        if not re.fullmatch(padrao, nome):
            raise ValidationError('O nome deve conter: De 3 a 40 caracteres; Letras, _ e/ou espaços')
        return nome

    def validate_senha(self, senha):
        padrao = r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){8,50}$'
        if not re.fullmatch(padrao, senha):
            raise ValidationError("A senha deve conter: De 8 a 50 caracteres; 1 número"
                                  "1 letra maiúscula ; 1 letra minúscula; 1 caractere especial")
        return senha


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