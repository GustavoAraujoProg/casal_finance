from django.contrib import admin
from .models import Categoria, Conta, Meta, Transacao, Perfil

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'icone', 'cor')
    search_fields = ('nome',)

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'tipo', 'saldo_inicial')
    list_filter = ('usuario', 'tipo')

@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'valor_alvo', 'valor_atual', 'data_limite', 'concluida')
    list_filter = ('concluida', 'data_limite')

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    # Colunas que aparecerão na tabela
    list_display = ('descricao', 'valor', 'tipo', 'data', 'conta', 'usuario', 'compartilhado')
    
    # Filtros laterais (MUITO útil para ver gastos só de um ou do outro)
    list_filter = ('tipo', 'usuario', 'compartilhado', 'data', 'categoria')
    
    # Barra de pesquisa
    search_fields = ('descricao',)
    
    # Ordenação padrão no admin
    ordering = ('-data',)

admin.site.register(Perfil)