from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Transacao, Meta, Categoria, Perfil
from .forms import TransacaoForm, MetaForm, CategoriaForm
import json
from datetime import datetime, timedelta



def home(request):
    # --- 1. Filtro de Data (Máquina do Tempo) ---
    hoje = datetime.now()
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))
    data_filtro = datetime(ano, mes, 1)

    # Filtra transações apenas deste mês/ano
    transacoes = Transacao.objects.filter(data__month=mes, data__year=ano).order_by('-data')
    
    # Metas são globais (não dependem do mês)
    metas = Meta.objects.filter(concluida=False)

    # --- 2. Cálculos de Totais ---
    total_receitas = transacoes.filter(tipo='receita').aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = transacoes.filter(tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_total = total_receitas - total_despesas

    # --- 3. Lógica de Orçamento (Limites Mensais) ---
    orcamentos = []
    categorias = Categoria.objects.all()
    
    for cat in categorias:
        if cat.limite_mensal > 0: # Só processa se tiver limite definido no Admin
            # Quanto gastou nesta categoria NESTE mês específico
            gasto_cat = transacoes.filter(tipo='despesa', categoria=cat).aggregate(Sum('valor'))['valor__sum'] or 0
            
            # Cálculo da porcentagem
            porcentagem = int((gasto_cat / cat.limite_mensal) * 100)
            
            # Define cor e aviso
            cor_barra = "bg-success" # Verde (Padrão)
            aviso = ""
            
            if porcentagem >= 80 and porcentagem < 100:
                cor_barra = "bg-warning" # Amarelo
                aviso = "⚠️ Atenção"
            elif porcentagem >= 100:
                cor_barra = "bg-danger"  # Vermelho
                aviso = "🚨 Estourou!"

            orcamentos.append({
                'id': cat.id,
                'nome': cat.nome,
                'icone': cat.icone,
                'limite': cat.limite_mensal,
                'gasto': gasto_cat,
                'porcentagem': min(porcentagem, 100), # Trava visualmente em 100%
                'porcentagem_real': porcentagem,      # Número real para mostrar no texto
                'cor': cor_barra,
                'aviso': aviso
            })

    # --- 4. Dados para o Gráfico (Donut) ---
    gastos_por_categoria = transacoes.filter(tipo='despesa').values('categoria__nome', 'categoria__cor').annotate(total=Sum('valor'))
    labels = [item['categoria__nome'] for item in gastos_por_categoria]
    data = [float(item['total']) for item in gastos_por_categoria]
    colors = [item['categoria__cor'] for item in gastos_por_categoria]

    # --- 5. Navegação Próximo/Anterior ---
    data_anterior = data_filtro - timedelta(days=1)
    mes_anterior = data_anterior.month
    ano_anterior = data_anterior.year
    
    data_proxima = data_filtro + timedelta(days=32)
    mes_proximo = data_proxima.month
    ano_proximo = data_proxima.year

    nomes_meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

    return render(request, 'home.html', {
        'transacoes': transacoes,
        'metas': metas,
        'orcamentos': orcamentos, # <--- Enviando orçamentos para o HTML
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo_total': saldo_total,
        'grafico_labels': json.dumps(labels),
        'grafico_data': json.dumps(data),
        'grafico_colors': json.dumps(colors),
        'mes_atual': mes,
        'ano_atual': ano,
        'nome_mes': nomes_meses[mes],
        'mes_anterior': mes_anterior,
        'ano_anterior': ano_anterior,
        'mes_proximo': mes_proximo,
        'ano_proximo': ano_proximo,
    })

def nova_transacao(request):
    form = TransacaoForm(request.POST or None)
    if form.is_valid():
        transacao = form.save(commit=False)
        transacao.usuario = request.user
        transacao.save()
        return redirect('home')
    return render(request, 'form_transacao.html', {'form': form})

def nova_meta(request):
    form = MetaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'form_meta.html', {'form': form})

def editar_transacao(request, id):
    transacao = get_object_or_404(Transacao, id=id)
    form = TransacaoForm(request.POST or None, instance=transacao)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'form_transacao.html', {'form': form})

def excluir_transacao(request, id):
    transacao = get_object_or_404(Transacao, id=id)
    if request.method == 'POST':
        transacao.delete()
        return redirect('home')
    return render(request, 'confirmar_exclusao.html', {'transacao': transacao})

def perfil(request):
    usuarios = User.objects.all()
    dados_usuarios = []
    total_geral = 0
    
    for u in usuarios:
        total_gasto = Transacao.objects.filter(usuario=u, tipo='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
        try:
            foto = u.perfil.foto.url
        except:
            foto = None
        dados_usuarios.append({'nome': u.first_name or u.username, 'total': total_gasto, 'foto': foto})
        total_geral += total_gasto
    
    for item in dados_usuarios:
        if total_geral > 0:
            item['porcentagem'] = int((item['total'] / total_geral) * 100)
        else:
            item['porcentagem'] = 0

    return render(request, 'perfil.html', {'dados': dados_usuarios})

def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    
    if form.is_valid():
        form.save()
        return redirect('home')
        
    return render(request, 'form_categoria.html', {'form': form})