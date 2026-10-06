from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto1 TEXT NOT NULL,
                produto2 TEXT NOT NULL,
                status TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Mapeamento completo baseado no documento Alma Lavada
REACOES = {
    # PODE (Seguro)
    frozenset(["agua", "cloro"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "cloro_gel"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "sabao_po"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "multiuso"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "sabao_liquido"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "desengordurante"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "limpa_vidro"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "detergente"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "bicarbonato"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "vinagre"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "agua_oxigenada"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "alcool"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "agua_sanitaria"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "lysoform"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "desinfetante"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "sabao_barra"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua", "pasta_panela"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_barra", "sabao_po"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_barra", "multiuso"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_barra", "sabao_liquido"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_barra", "desengordurante"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_barra", "detergente"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_barra", "bicarbonato"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_barra", "agua_sanitaria"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_barra", "cloro"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_barra", "amaciante"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["detergente", "sabao_po"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["detergente", "amaciante"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["detergente", "sabao_liquido"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["detergente", "desengordurante"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["detergente", "bicarbonato"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["detergente", "pasta_panela"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["bicarbonato", "sabao_po"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["bicarbonato", "sabao_liquido"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["bicarbonato", "desengordurante"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["bicarbonato", "pasta_panela"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_liquido", "sabao_po"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_liquido", "amaciante"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_liquido", "multiuso"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["desengordurante", "sabao_po"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["desengordurante", "pasta_panela"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["pasta_panela", "sabao_barra"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["pasta_panela", "vinagre"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["pasta_panela", "soda_caustica"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["multiuso", "pasta_panela"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["agua_sanitaria", "cloro"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["alcool", "bicarbonato"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["limpa_vidro", "sabao_liquido"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["limpa_vidro", "detergente"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["limpa_vidro", "bicarbonato"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["vinagre", "sabao_liquido"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["vinagre", "detergente"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["sabao_po", "amaciante"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["soda_caustica", "sabao_barra"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},
    frozenset(["cera_piso", "lustra_moveis"]): {"status": "PODE", "mensagem": "Mistura segura. Pode utilizar."},

    # CUIDADO (Usar com precaução)
    frozenset(["alcool", "sabao_po"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["alcool", "amaciante"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["alcool", "sabao_liquido"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["alcool", "detergente"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["alcool", "vinagre"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["alcool", "agua_oxigenada"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["alcool", "desinfetante"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["alcool", "sabao_barra"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["alcool", "pasta_panela"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["cloro", "sabao_po"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["cloro", "sabao_liquido"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["cloro", "detergente"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["cloro", "cloro_gel"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["cloro_gel", "sabao_liquido"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["cloro_gel", "detergente"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["bicarbonato", "multiuso"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["bicarbonato", "vinagre"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},
    frozenset(["bicarbonato", "agua_oxigenada"]): {"status": "CUIDADO", "mensagem": "Pode utilizar, mas com cuidado."},

    # INIBE (Um anula o efeito do outro)
    frozenset(["vinagre", "amaciante"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["vinagre", "desengordurante"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["vinagre", "limpa_vidro"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["vinagre", "cera_piso"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["vinagre", "soda_caustica"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["vinagre", "desinfetante"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["vinagre", "amonia"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["vinagre", "sabao_barra"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["bicarbonato", "cloro"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["bicarbonato", "amaciante"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["bicarbonato", "cloro_gel"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["bicarbonato", "agua_sanitaria"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."},
    frozenset(["bicarbonato", "desinfetante"]): {"status": "INIBE", "mensagem": "Esta mistura inibe a ação dos produtos."}
}

PRODUTOS_NOMES = {
    "cloro": "Cloro",
    "cloro_gel": "Cloro em Gel",
    "sabao_po": "Sabão em Pó",
    "multiuso": "Multiuso",
    "amaciante": "Amaciante",
    "lustra_moveis": "Lustra Móveis",
    "sabao_liquido": "Sabão Líquido",
    "desengordurante": "Desengordurante",
    "limpa_vidro": "Limpa Vidro",
    "cera_piso": "Cera de Piso",
    "inseticida": "Inseticida Doméstico",
    "soda_caustica": "Soda Cáustica",
    "detergente": "Detergente",
    "agua": "Água",
    "bicarbonato": "Bicarbonato de Sódio",
    "vinagre": "Vinagre",
    "removedor": "Removedor",
    "agua_oxigenada": "Água Oxigenada",
    "alcool": "Álcool",
    "agua_sanitaria": "Água Sanitária",
    "lysoform": "Lysoform",
    "solupan": "Solupan (Roxinho)",
    "desengraxante": "Desengraxante",
    "desinfetante": "Desinfetante",
    "amonia": "Amônia",
    "sabao_barra": "Sabão em Barra",
    "pasta_panela": "Pasta de Lavar Panela"
}

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT produto1, produto2, status, mensagem FROM historico ORDER BY id DESC')
        historico_db = cursor.fetchall()
    return render_template('index.html', historico=historico_db)

@app.route('/api/misturar', methods=['POST'])
def misturar():
    data = request.get_json()
    p1 = data.get('produto1')
    p2 = data.get('produto2')

    if not p1 or not p2:
        return jsonify({"erro": "Selecione dois produtos"}), 400

    par = frozenset([p1, p2])
    
    # Se a combinação não estiver explicitamente mapeada como PODE, CUIDADO ou INIBE, é NAO_PODE por padrão
    resultado = REACOES.get(par, {
        "status": "NAO_PODE",
        "mensagem": "Não pode misturar! Risco de reação química perigosa ou tóxica."
    })

    nome_p1 = PRODUTOS_NOMES.get(p1, p1)
    nome_p2 = PRODUTOS_NOMES.get(p2, p2)

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO historico (produto1, produto2, status, mensagem) VALUES (?, ?, ?, ?)',
            (nome_p1, nome_p2, resultado['status'], resultado['mensagem'])
        )
        conn.commit()

    return jsonify({
        "produto1": nome_p1,
        "produto2": nome_p2,
        "status": resultado['status'],
        "mensagem": resultado['mensagem']
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)