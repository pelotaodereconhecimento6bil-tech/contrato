from docxtpl import DocxTemplate
import os
import re

def gerar_contrato(dados):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # caminho do template
    template_path = os.path.join(BASE_DIR, "..", "contrato_template.docx")

    # =========================
    # LIMPAR NOME DO ARQUIVO
    # =========================
    nome_limpo = dados['locatario_nome']

    # remove caracteres especiais
    nome_limpo = re.sub(r"[^\w\s]", "", nome_limpo)

    # substitui espaços por _
    nome_limpo = nome_limpo.replace(" ", "_")

    # nome final do arquivo
    nome_arquivo = f"contrato_{nome_limpo}.docx"

    # =========================
    # GERAR DOCUMENTO
    # =========================
    doc = DocxTemplate(template_path)
    doc.render(dados)
    doc.save(nome_arquivo)

    return nome_arquivo