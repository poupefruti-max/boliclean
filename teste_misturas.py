import pytest
# Substitui 'app' pelo nome do ficheiro onde está a tua API (ex: de 'main' import 'app')
from app import app 

@pytest.fixture
def client():
    # Cria um cliente de teste do Flask
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Matriz completa de testes conforme o projeto Alma Lavada
# Formato: (produto1, produto2, status_esperado)
CASOS_TESTE = [
    # Categoria: PERIGOSO / NAO PODE
    ("agua_sanitaria", "vinagre", "NAO PODE"),
    ("agua_sanitaria", "desinfetante", "NAO PODE"),
    ("agua_sanitaria", "alcool", "NAO PODE"),

    # Categoria: CUIDADO
    ("agua_sanitaria", "detergente", "CUIDADO"),
    ("agua_sanitaria", "sabao_em_po", "CUIDADO"),
    ("vinagre", "desinfetante", "CUIDADO"),
    ("vinagre", "alcool", "CUIDADO"),

    # Categoria: INIBE A AÇÃO (NEUTRALIZA)
    ("agua_sanitaria", "bicarbonato", "INIBE_ACAO"),
    ("vinagre", "bicarbonato", "INIBE_ACAO"),

    # Categoria: PODE (SEGURA)
    ("agua_sanitaria", "agua_cozedura", "PODE"),
    ("vinagre", "detergente", "PODE"),
    ("vinagre", "sabao_em_po", "PODE"),
    ("vinagre", "agua_cozedura", "PODE"),
    ("alcool", "detergente", "PODE"),
    ("alcool", "sabao_em_po", "PODE"),
    ("alcool", "desinfetante", "PODE"),
    ("alcool", "bicarbonato", "PODE"),
    ("alcool", "agua_cozedura", "PODE"),
    ("bicarbonato", "detergente", "PODE"),
    ("bicarbonato", "sabao_em_po", "PODE"),
    ("bicarbonato", "desinfetante", "PODE"),
    ("bicarbonato", "agua_cozedura", "PODE"),
    ("detergente", "sabao_em_po", "PODE"),
    ("detergente", "desinfetante", "PODE"),
    ("detergente", "agua_cozedura", "PODE"),
    ("sabao_em_po", "desinfetante", "PODE"),
    ("sabao_em_po", "agua_cozedura", "PODE"),
    ("desinfetante", "agua_cozedura", "PODE"),
]

@pytest.mark.parametrize("p1, p2, status_esperado", CASOS_TESTE)
def test_rota_misturar(client, p1, p2, status_esperado):
    # Envia a requisição POST com o JSON para a API
    response = client.post('/api/misturar', json={
        "produto1": p1,
        "produto2": p2
    })

    # Verifica se a API respondeu 200 OK
    assert response.status_code == 200

    # Valida o JSON de resposta
    data = response.get_json()
    assert data["status"] == status_esperado, f"Falha na mistura {p1} + {p2}. Retornou: {data['status']}"

def test_validacao_campos_ausentes(client):
    # Teste para garantir o retorno 400 caso o utilizador não envie os produtos
    response = client.post('/api/misturar', json={"produto1": "agua_sanitaria"})
    assert response.status_code == 400
    assert response.get_json()["erro"] == "Selecione dois produtos"