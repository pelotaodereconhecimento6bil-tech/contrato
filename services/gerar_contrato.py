from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def gerar_contrato(dados):
    pdf = f"contrato_{dados['locatario_nome']}.pdf"

    c = canvas.Canvas(pdf, pagesize=A4)

    texto = c.beginText(40, 800)
    texto.setFont("Helvetica", 11)

    linhas = [
        "CONTRATO DE LOCAÇÃO DE VEÍCULO",
        "",
        f"Locatário: {dados['locatario_nome']}",
        f"CPF: {dados['locatario_cpf']}",
        f"RG: {dados['locatario_rg']}",
        f"Endereço: {dados['locatario_endereco']}",
        "",
        f"Veículo: {dados['veiculo_modelo']}",
        f"Placa: {dados['veiculo_placa']}",
        "",
        f"Valor: R$ {dados['valor']} ({dados['valor_extenso']})",
        f"Duração: {dados['duracao']}",
        "",
        f"Início: {dados['data_inicio']}",
        f"Fim: {dados['data_fim']}",
        "",
        f"Data: {dados['data_assinatura_extenso']}",
    ]

    for linha in linhas:
        texto.textLine(linha)

    c.drawText(texto)
    c.save()

    return pdf