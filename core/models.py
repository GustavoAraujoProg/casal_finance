from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Tipos de transação
TIPO_CHOICES = (
    ('receita', 'Receita'),
    ('despesa', 'Despesa'),
)

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    icone = models.CharField(max_length=20, help_text="Classe do ícone (ex: fa-home)")
    cor = models.CharField(max_length=7, default="#3B82F6", help_text="Código Hex da cor")
    # --- NOVO CAMPO AQUI ---
    limite_mensal = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Quanto você pretende gastar por mês?")
    
    def __str__(self):
        return self.nome
    

class Conta(models.Model):
    """ Ex: Nubank Dele, Itaú Dela, Carteira, VR """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo = models.CharField(max_length=20, choices=[('banco', 'Banco'), ('carteira', 'Dinheiro'), ('vr', 'Vale Refeição')])

    def __str__(self):
        return f"{self.nome} - {self.usuario.username}"

class Meta(models.Model):
    """ Ex: Viagem para Europa, Reserva de Emergência """
    titulo = models.CharField(max_length=100)
    valor_alvo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_limite = models.DateField()
    concluida = models.BooleanField(default=False)

    def progresso(self):
        # Retorna porcentagem para a barra de progresso
        return int((self.valor_atual / self.valor_alvo) * 100)

class Transacao(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=date.today)
    
    # Relacionamentos
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE) # De onde saiu o dinheiro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Quem gastou
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    
    # Lógica de Casal
    compartilhado = models.BooleanField(default=False, help_text="Se marcado, divide o custo nas estatísticas ou conta como gasto do casal")
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"