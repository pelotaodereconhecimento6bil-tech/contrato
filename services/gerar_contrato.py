from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_contrato(dados):
    nome_pdf = f"contrato_{dados['locatario_nome']}.pdf"

    c = canvas.Canvas(nome_pdf, pagesize=A4)
    texto = c.beginText(40, 800)
    texto.setFont("Helvetica", 10)

    linhas = [
        "CONTRATO DE LOCAÇÃO DE VEÍCULO",
        "",
        f"LOCATÁRIO: {dados['locatario_nome']}",
        f"CPF: {dados['locatario_cpf']}",
        "",
        "CLÁUSULA 1ª - DO OBJETO",
        f"Veículo: {dados['veiculo_modelo']} - {dados['veiculo_placa']}",
        "",
        f"Valor: R$ {dados['valor']} ({dados['valor_extenso']})",
        "",
        f"Período: {dados['data_inicio']} até {dados['data_fim']}",
        "",
        "Demais cláusulas conforme contrato padrão.",
    ]

    for linha in linhas:
        texto.textLine(linha)

    c.drawText(texto)
    c.save()

    return nome_pdf