import inspect

from django.urls import reverse

from async_project import views


def test_async_view_is_a_coroutine_function():
    assert inspect.iscoroutinefunction(views.async_view)


def test_async_view_returns_all_steps(client, monkeypatch):
    monkeypatch.setattr(views, 'STEP_DELAY', 0)

    response = client.get(reverse('async'))

    content = response.content.decode()
    assert response.status_code == 200
    assert 'Passo 1' in content
    assert 'Passo 2' in content
    assert 'Passo 3' in content


def test_async_view_prints_await_chain_in_order(client, monkeypatch, capsys):
    monkeypatch.setattr(views, 'STEP_DELAY', 0)

    client.get(reverse('async'))

    output = capsys.readouterr().out
    assert 'Requisicao recebida' in output
    assert output.index('Passo 1: concluido') < output.index('Passo 2: iniciando')
    assert output.index('Passo 2: concluido') < output.index('Passo 3: iniciando')
    assert 'Resposta enviada' in output


def test_unknown_route_returns_404(client):
    response = client.get('/rota-que-nao-existe/')

    assert response.status_code == 404
