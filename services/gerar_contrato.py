from docxtpl import DocxTemplate
import os

def gerar_contrato(dados):
    # caminho do template
    template_path = "contrato_template.docx"

    # nome do arquivo final
    nome_arquivo = f"contrato_{dados['locatario_nome']}.docx"

    # carrega o modelo
    doc = DocxTemplate(template_path)

    # substitui os {{campos}} pelos dados
    doc.render(dados)

    # salva o contrato pronto
    doc.save(nome_arquivo)

    return nome_arquivo