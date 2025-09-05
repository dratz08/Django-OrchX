from django.contrib import admin
from orchestrator.models import Bot, Automacao, PassoAutomacao, Agendamento


class Bots(admin.ModelAdmin):
    list_display = ('id', 'nome', 'entrypoint', 'tipo', 'diretorio', 'log_timeout')
    list_display_links = ('id', 'nome', 'entrypoint', 'tipo', 'diretorio', 'log_timeout')
    list_per_page = 10
    search_fields = ('id', 'nome')


class Automacoes(admin.ModelAdmin):
    list_display = ('id', 'nome', 'id_cliente', 'descricao')
    list_display_links = ('id', 'nome', 'id_cliente', 'descricao')
    list_per_page = 10
    search_fields = ('nome',)


class PassosAutomacoes(admin.ModelAdmin):
    list_display = ('id', 'ordem', 'id_automacao', 'id_bot', 'id_cliente')
    list_display_links = ('id', 'ordem', 'id_automacao', 'id_bot', 'id_cliente')
    list_per_page = 10
    search_fields = ('id_automacao', 'id_bot', 'id_cliente')


class Agendamentos(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cron', 'id_automacao', 'id_cliente', 'ativo')
    list_display_links = ('id', 'nome', 'cron', 'id_automacao', 'id_cliente', 'ativo')
    list_per_page = 10
    search_fields = ('nome', 'id_automacao', 'id_cliente')


admin.site.register(Bot, Bots)
admin.site.register(Automacao, Automacoes)
admin.site.register(Agendamento, Agendamentos)
admin.site.register(PassoAutomacao, PassosAutomacoes)