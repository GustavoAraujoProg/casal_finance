from django import forms
from .models import Transacao, Meta, Categoria


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data', 'categoria', 'conta', 'tipo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Supermercado'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'conta': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class MetaForm(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['titulo', 'valor_alvo', 'data_limite']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Viagem para Europa'}),
            'valor_alvo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quanto precisa juntar?'}),
            'data_limite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'icone', 'cor', 'limite_mensal']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'icone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: fa-utensils'}),
            'cor': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}), # Type color abre o seletor de cores!
            'limite_mensal': forms.NumberInput(attrs={'class': 'form-control'}),
        }