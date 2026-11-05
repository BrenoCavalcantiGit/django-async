import asyncio

from django.http import HttpResponse

STEP_DELAY = 1


async def run_step(name):
    """Simula uma tarefa demorada, sem travar o servidor."""
    print(f'{name}: iniciando')
    await asyncio.sleep(STEP_DELAY)
    print(f'{name}: concluido')
    return name


async def async_view(request):
    print('Requisicao recebida')

    # "await chain": cada passo espera o anterior terminar
    first = await run_step('Passo 1')
    second = await run_step('Passo 2')
    third = await run_step('Passo 3')

    print('Resposta enviada')
    return HttpResponse(f'Await chain concluida: {first} -> {second} -> {third}')
