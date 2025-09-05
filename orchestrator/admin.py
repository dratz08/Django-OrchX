from django.contrib import admin
from orchestrator.models import Bot, Automacao, PassoAutomacao, Agendamento


class Bots(admin.ModelAdmin):
    list_display = ('id', 'nome', 'entrypoint', 'tipo', 'diretorio')
    list_display_links = ('id', 'nome', 'entrypoint', 'tipo', 'diretorio')
    list_per_page = 10
    search_fields = ('id', 'nome')


class Automacoes(admin.ModelAdmin):
    list_display = ('id', 'nome', 'status', 'descricao')
    list_display_links = ('id', 'nome', 'status', 'descricao')
    list_per_page = 10
    search_fields = ('nome',)


class PassosAutomacoes(admin.ModelAdmin):
    list_display = ('id', 'ordem', 'id_automacao', 'id_bot')
    list_display_links = ('id', 'ordem', 'id_automacao', 'id_bot')
    list_per_page = 10
    search_fields = ('id_automacao', 'id_bot')


class Agendamentos(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cron', 'id_automacao', 'ativo')
    list_display_links = ('id', 'nome', 'cron', 'id_automacao', 'ativo')
    list_per_page = 10
    search_fields = ('nome', 'id_automacao')


admin.site.register(Bot, Bots)
admin.site.register(Automacao, Automacoes)
admin.site.register(Agendamento, Agendamentos)
admin.site.register(PassoAutomacao, PassosAutomacoes)