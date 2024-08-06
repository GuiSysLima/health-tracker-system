import threading
import time
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import SmartwatchForm
from .models import Smartwatch, SmartwatchHistory
from datetime import datetime


def cadastrar_smartwatch(request):
    if request.method == 'POST':
        form = SmartwatchForm(request.POST)
        if form.is_valid():
            porta_url = f"http://127.0.0.1:{form.cleaned_data['porta_url']}/data"
            funcionario = form.cleaned_data['funcionario']
            try:
                response = requests.get(porta_url)
                response.raise_for_status()
                data = response.json()

                imei = data.get('imei')
                if Smartwatch.objects.filter(imei=imei).exists():
                    messages.error(request, f'IMEI já existe no banco de dados.')
                    return

                data_obj = datetime.strptime(data.get('date'), "%A, %d/%m/%Y").strftime("%Y-%m-%d")

                Smartwatch.objects.create(
                    imei=imei,
                    data=data_obj,
                    hora=data.get('time'),
                    bpm=data.get('bpm'),
                    mmhg=data.get('mmhg'),
                    temperatura_corporal=data.get('temperature'),
                    funcionario=funcionario
                )
                messages.success(request, 'Smartwatch adicionado com sucesso!')
                return redirect('listar_smartwatches')

            except requests.RequestException as e:
                messages.error(request, f'Erro ao adicionar o smartwatch: {str(e)}, porta não disponível')
                return
            except ValueError as e:
                messages.error(request, f'Erro no formulário. {str(e)} Verifique os dados e tente novamente.')
                return
    else:
        form = SmartwatchForm()

    return render(request, 'smartwatches/cadastrar_smartwatch.html', {'form': form})


def atualizar_smartwatch(smartwatch, porta_inicial, porta_final):
    for porta in range(porta_inicial, porta_final + 1):
        try:
            response = requests.get(f"http://localhost:{porta}/data")
            response.raise_for_status()
            data = response.json()

            imei = data.get('imei')
            if Smartwatch.objects.filter(imei=imei).exists() and smartwatch.imei == imei:
                data_obj = datetime.strptime(data.get('date'), "%A, %d/%m/%Y").strftime("%Y-%m-%d")
                SmartwatchHistory.objects.create(
                    smartwatch=smartwatch,
                    data=data_obj,
                    hora=data.get('time'),
                    bpm=data.get('bpm'),
                    mmhg=data.get('mmhg'),
                    temperatura_corporal=data.get('temperature'),
                )

                smartwatch.data = data_obj
                smartwatch.hora = data.get('time')
                smartwatch.bpm = data.get('bpm')
                smartwatch.mmhg = data.get('mmhg')
                smartwatch.temperatura_corporal = data.get('temperature')
                smartwatch.save()
                print(f'Atualizando smartwatch {smartwatch.imei} pela porta {porta}')
                break
        except requests.RequestException as e:
            print(f"Erro ao conectar ao smartwatch {smartwatch.imei}: {e}")


def atualizar_todos_smartwatches(porta_inicial, porta_final):
    while True:
        smartwatches = Smartwatch.objects.all()
        for smartwatch in smartwatches:
            atualizar_smartwatch(smartwatch, porta_inicial, porta_final)

def buscar_smartwatch(request, imei):
    smartwatch = get_object_or_404(Smartwatch, imei=imei)
    historico = SmartwatchHistory.objects.filter(smartwatch=smartwatch).order_by('-data')
    return render(request, 'smartwatches/historico_smartwatch.html', {'smartwatch': smartwatch, 'historico': historico})

def listar_smartwatches(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        smartwatches = list(
            Smartwatch.objects.all().values('imei', 'bpm', 'data', 'mmhg', 'temperatura_corporal', 'hora', 'funcionario'))
        return JsonResponse({'smartwatches': smartwatches})

    smartwatches = Smartwatch.objects.all()
    return render(request, 'smartwatches/listar_smartwatches.html', {'smartwatches': smartwatches})

def historico_smartwatch_json(request, imei):
    registros = SmartwatchHistory.objects.filter(smartwatch__imei=imei).values('data', 'bpm', 'mmhg', 'temperatura_corporal')
    return JsonResponse({'registros': list(registros)})
