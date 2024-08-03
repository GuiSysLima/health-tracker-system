from django.shortcuts import render, redirect
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
    funcionarios = Funcionario.objects.all()
    return render(request, 'funcionarios/listar_funcionarios.html', {'funcionarios': funcionarios})
