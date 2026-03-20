from num2words import num2words
import requests

def buscar_cep(cep):
    cep = cep.replace("-", "").strip()

    if len(cep) != 8:
        return None

    url = f"https://viacep.com.br/ws/{cep}/json/"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    dados = response.json()

    if "erro" in dados:
        return None

    return {
        "endereco": dados.get("logradouro"),
        "cidade": dados.get("localidade"),
        "estado": dados.get("uf")
    }

def valor_por_extenso(valor):
    return num2words(valor, lang='pt_BR').upper()

def data_por_extenso(data):
    meses = [
        "janeiro", "fevereiro", "março", "abril",
        "maio", "junho", "julho", "agosto",
        "setembro", "outubro", "novembro", "dezembro"
    ]

    dia = data.day
    mes = meses[data.month - 1].capitalize()
    ano = data.year

    return f"{dia} de {mes} de {ano}"