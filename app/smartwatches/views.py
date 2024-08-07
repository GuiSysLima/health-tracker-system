import time
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from funcionarios.models import Funcionario
from .forms import SmartwatchForm
from .models import Smartwatch, SmartwatchHistory
from datetime import datetime
from smartwatches.search_smartwatchs import search
import asyncio

def cadastrar_smartwatch(request):
    if request.method == 'POST':
        form = SmartwatchForm(request.POST)
        if form.is_valid():
            funcionario = form.cleaned_data['funcionario']
            try:
                imei = form.cleaned_data['imei']
                if Smartwatch.objects.filter(imei=imei).exists():
                    messages.error(request, f'IMEI já existe no banco de dados.')
                    return

                Smartwatch.objects.create(
                    imei=imei,
                    funcionario=funcionario
                )
                messages.success(request, 'Smartwatch adicionado com sucesso!')
                return redirect('listar_smartwatches')
            except ValueError as e:
                messages.error(request, f'Erro no formulário. {str(e)} Verifique os dados e tente novamente.')
                return
            except Exception as e:
                messages.error(request, f'Erro {str(e)}')
    else:
        form = SmartwatchForm()

    return render(request, 'smartwatches/cadastrar_smartwatch.html', {'form': form})


def atualizar_smartwatch(smartwatch):
    try:
        data_obj = datetime.strptime(smartwatch['date'], "%A, %d/%m/%Y").strftime("%Y-%m-%d")
        sw = Smartwatch.objects.get(pk=int(smartwatch['imei']))
        SmartwatchHistory.objects.create(
            smartwatch=sw,
            data=data_obj,
            hora=smartwatch['time'],
            bpm=smartwatch['bpm'],
            mmhg=smartwatch['mmhg'],
            temperatura_corporal=smartwatch['temperature'],
        )
        print(f'Atualizando smartwatch {smartwatch['imei']} pela porta {smartwatch["port"]}')
    except Smartwatch.DoesNotExist:
        print(f'Smartwatch {smartwatch.imei} não encontrado.')


def atualizar_todos_smartwatches(porta_inicial, porta_final):
    while True:
        sws_imeis = list(Smartwatch.objects.values_list("imei", flat=True))
        sws_on = asyncio.run(search(porta_inicial, porta_final-porta_inicial, "http://127.0.0.1"))
        for smartwatch in [sw for sw in sws_on if sw['imei'] in sws_imeis]:
            atualizar_smartwatch(smartwatch)
        time.sleep(10)

def buscar_smartwatch(request, imei):
    smartwatch = get_object_or_404(Smartwatch, imei=imei)
    historico = SmartwatchHistory.objects.filter(smartwatch=smartwatch).order_by('-timestamp')
    return render(request, 'smartwatches/historico_smartwatch.html', {'smartwatch': smartwatch, 'historico': historico})

def listar_smartwatches(request):
    sws_on = [x['imei'] for x in asyncio.run(search(5000, 10, "http://127.0.0.1"))]
    smartwatches = [vars(x) for x in Smartwatch.objects.all()]
    for sw in smartwatches:
        sw['status'] = "on" if sw['imei'] in sws_on else "off"
        sw['funcionario'] = Funcionario.objects.get(pk=sw['funcionario_id']).nome_completo
        del sw['_state']
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'smartwatches': smartwatches})
    return render(request, 'smartwatches/listar_smartwatches.html', {'smartwatches': smartwatches})


def search_smartwatches(request):
    smartwatches = asyncio.run(search(5000, 21, "http://127.0.0.1"))
    is_a_json_request = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    for watch in smartwatches:
        try:
            sw = Smartwatch.objects.get(pk=int(watch['imei']))
            watch['funcionario_nome'] = sw.funcionario.nome_completo
            watch['funcionario_id'] = sw.funcionario.id
        except Smartwatch.DoesNotExist:
            watch['funcionario_nome'] = "Sem vinculo"
            watch['funcionario_id'] = 0
    smartwatches.sort(key=lambda x: x["port"])
    print(smartwatches)
    if is_a_json_request:
        return JsonResponse({'smartwatches': smartwatches})
    return render(request, 'smartwatches/search_smartwatches.html', {'smartwatches': smartwatches})

def historico_smartwatch_json(request, imei):
    registros = SmartwatchHistory.objects.filter(smartwatch__imei=imei).values('data', 'bpm', 'mmhg', 'hora', 'temperatura_corporal')
    return JsonResponse({'registros': list(registros)})