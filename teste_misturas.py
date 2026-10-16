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
    ("cloro", "detergente", "CUIDADO"),
    ("sabao_po", "bicarbonato", "CUIDADO"),
    ("vinagre", "agua_oxigenada", "CUIDADO"),
    ("vinagre", "alcool", "NAO PODE"),

    # Categoria: INIBE A AÇÃO (NEUTRALIZA)
    ("cloro", "bicarbonato", "INIBE"),
    ("vinagre", "bicarbonato", "NAO PODE"),
    ("soda_caustica", "bicarbonato", "INIBE"),

    # Categoria: PODE (SEGURA)
    ("agua_sanitaria", "cloro", "PODE"),
    ("vinagre", "detergente", "NAO PODE"),
    ("vinagre", "sabao_liquido", "INIBE"),
    ("vinagre", "agua", "NAO PODE"),
    ("alcool", "detergente", "NAO PODE"),
    ("alcool", "sabao_po", "NAO PODE"),
    ("alcool", "desinfetante", "NAO PODE"),
    ("alcool", "bicarbonato", "INIBE"),
    ("alcool", "agua", "INIBE"),
    ("bicarbonato", "detergente", "INIBE"),
    ("bicarbonato", "sabao_po", "CUIDADO"),
    ("bicarbonato", "desinfetante", "NAO PODE"),
    ("bicarbonato", "agua", "CUIDADO"),
    ("detergente", "sabao_po", "NAO PODE"),
    ("detergente", "desinfetante", "NAO PODE"),
    ("detergente", "agua", "PODE"),
    ("sabao_po", "desinfetante", "NAO PODE"),
    ("sabao_po", "agua", "PODE"),
    ("desinfetante", "agua", "CUIDADO"),
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
