from django.shortcuts import render, redirect, get_object_or_404
from .forms import FuncionarioForm
from .models import Funcionario

def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_funcionarios')
    else:
        form = FuncionarioForm()
    return render(request, 'funcionarios/cadastrar_funcionario.html', {'form': form})

def listar_funcionarios(request):
    search_query = request.GET.get('search', '')
    search_type = request.GET.get('searchType', 'nome')

    #Lógica de busca de funcionarios
    if search_query:
        if search_type == 'nome':
            funcionarios = Funcionario.objects.filter(nome_completo__icontains=search_query)
        elif search_type == 'email':
            funcionarios = Funcionario.objects.filter(email__icontains=search_query)
        elif search_type == 'idade':
            try:
                idade = int(search_query)
                funcionarios = Funcionario.objects.filter(idade=idade)
            except ValueError:
                funcionarios = Funcionario.objects.none()  # Se a idade não for um número, não retorna resultados.
        elif search_type == 'altura':
            try:
                altura = float(search_query)
                funcionarios = Funcionario.objects.filter(altura=altura)
            except ValueError:
                funcionarios = Funcionario.objects.none()  # Se a altura não for um número, não retorna resultados.
        elif search_type == 'peso':
            try:
                peso = float(search_query)
                funcionarios = Funcionario.objects.filter(peso=peso)
            except ValueError:
                funcionarios = Funcionario.objects.none()  # Se o peso não for um número, não retorna resultados.
    else:
        funcionarios = Funcionario.objects.all()

    return render(request, 'funcionarios/listar_funcionarios.html', {'funcionarios': funcionarios})

def perfil_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    return render(request, 'funcionarios/perfil_funcionario.html', {'funcionario': funcionario})