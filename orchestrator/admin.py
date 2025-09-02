from django.contrib import admin
from orchestrator.models import Usuario, Bot


class Bots(admin.ModelAdmin):
    list_display = ('id', 'nome', 'entrypoint', 'tipo', 'diretorio', 'log_timeout')
    list_display_links = ('id', 'nome', 'entrypoint', 'tipo', 'diretorio', 'log_timeout')
    list_per_page = 10
    search_fields = ('id', 'nome')


admin.site.register(Bot, Bots)