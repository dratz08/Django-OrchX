from rest_framework import serializers
from orchestrator.models import Bot, Automacao, PassoAutomacao, Agendamento, CustomUser
from rest_framework.validators import ValidationError
from orchestrator.zip_validator import validar_arquivo_zip
from orchestrator.utils import validar_cron
import re


class BotSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['nome', 'entrypoint', 'zip', 'tipo']

    def validate(self, dados):
        padrao_nome = r"^[a-zA-Z_]{3,30}$"
        padrao_entrypoint = r"^[a-zA-Z0-9_]{1,240}\.(py|robot)$"

        # Valida as restrições do campo nome, bem como sua duplicidade
        if not re.fullmatch(padrao_nome, dados['nome']):
            raise ValidationError({
                'nome': 'O nome deve conter: De 3 a 30 caracteres; Letras e/ou _'
            })
        user = self.context["request"].user
        if Bot.objects.filter(id_cliente=user, nome=dados['nome']).exists():
            raise serializers.ValidationError({"nome": "Você já possui um bot com este nome."})

        # Valida as restrições do campo entrypoint
        if not re.fullmatch(padrao_entrypoint, dados['entrypoint']):
            raise ValidationError({
                'entrypoint': 'O entrypoint não deve possuir caracteres inválidos e deve ser do tipo .robot ou .py'
            })

        # Varre o arquivo zip em busca de inconsistencias
        validar_arquivo_zip(dados['zip'])

        return dados

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
    id_bot = serializers.SlugRelatedField(
        slug_field="nome",
        queryset=Bot.objects.none()
    )
    id_automacao = serializers.SlugRelatedField(
        slug_field="nome",
        queryset=Automacao.objects.none()
    )

    class Meta:
        model = PassoAutomacao
        fields = ['id_automacao', 'id_bot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and hasattr(request, "user"):
            self.fields["id_bot"].queryset = Bot.objects.filter(id_cliente=request.user)
            self.fields["id_automacao"].queryset = Automacao.objects.filter(id_cliente=request.user)

    def create(self, validated_data: dict):
        user = self.context.get("request").user
        id_automacao = Automacao.objects.filter(id_cliente=user, nome=validated_data['id_automacao'])[0].id
        id_bot = Automacao.objects.filter(id_cliente=user, nome=validated_data['id_bot'])[0].id
        validated_data["id_automacao"] = id_automacao
        validated_data["id_bot"] = id_bot
        validated_data["id_cliente"] = user
        return validated_data


class AgendamentoSerializers(serializers.ModelSerializer):
    automacao = serializers.SlugRelatedField(
        slug_field='nome',
        queryset= Automacao.objects.none()
    )

    class Meta:
        model = Agendamento
        fields = ['nome', 'automacao', 'cron', 'ativo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            self.fields["automacao"].queryset = Automacao.objects.filter(id_cliente=request.user)

    def validate_nome(self, nome):
        padrao = r"^[a-zA-Z_]{3,50}$"
        if not re.fullmatch(padrao, nome):
            raise ValidationError('O nome deve conter: De 3 a 50 caracteres; Letras e/ou _')
        return nome

    def validate_cron(self, cron):
        check = validar_cron(cron)
        if not check:
            raise ValidationError('Expressão cron inválida')
        return cron
#
#
# class ListaBotSerializers(serializers.ListSerializer):
#     class Meta:
#         model = Bot
#         fields = "__all__"
#
#
# class ListaAutomacaoSerializers(serializers.ListSerializer):
#     class Meta:
#         model = Automacao
#         fields = ['nome', 'descricao']
