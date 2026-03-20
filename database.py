import sqlite3

def conectar():
    return sqlite3.connect("data/contratos.db", check_same_thread=False)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contratos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cpf TEXT,
        veiculo TEXT,
        valor REAL,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()

def salvar_contrato(nome, cpf, veiculo, valor, data):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO contratos (nome, cpf, veiculo, valor, data)
    VALUES (?, ?, ?, ?, ?)
    """, (nome, cpf, veiculo, valor, data))

    conn.commit()
    conn.close()

def listar_contratos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contratos ORDER BY id DESC")
    dados = cursor.fetchall()

    conn.close()
    return dados