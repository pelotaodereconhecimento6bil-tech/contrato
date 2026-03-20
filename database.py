import sqlite3
import os

def conectar():
    # garante que a pasta existe
    os.makedirs("data", exist_ok=True)
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
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO contratos (nome, cpf, veiculo, valor, data)
        VALUES (?, ?, ?, ?, ?)
        """, (nome, cpf, veiculo, valor, data))

def listar_contratos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contratos ORDER BY id DESC")
    dados = cursor.fetchall()

    conn.close()
    return dados