from num2words import num2words
import requests

def buscar_cep(cep):
    cep = cep.replace("-", "").strip()

    if len(cep) != 8:
        return None

    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException:
        return None

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

# 🔥 NOVA FUNÇÃO (ADICIONAR AQUI)
def formatar_moeda(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 🔥 FUNÇÃO MELHORADA (SUBSTITUIR ESSA)
def valor_por_extenso(valor):
    inteiro = int(valor)
    centavos = int(round((valor - inteiro) * 100))

    extenso = num2words(inteiro, lang='pt_BR').upper() + " REAIS"

    if centavos > 0:
        extenso += f" E {num2words(centavos, lang='pt_BR').upper()} CENTAVOS"

    return extenso

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