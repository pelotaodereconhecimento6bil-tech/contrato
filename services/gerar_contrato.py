from docxtpl import DocxTemplate
from docx2pdf import convert
import os
import pythoncom  # 👈 IMPORTANTE

def gerar_contrato(dados):
    pythoncom.CoInitialize()  # 👈 ESSENCIAL

    doc = DocxTemplate("templates/contrato_template.docx")
    doc.render(dados)

    docx = "contrato_temp.docx"
    pdf = f"contrato_{dados['locatario_nome']}.pdf"

    doc.save(docx)

    convert(docx, pdf)

    os.remove(docx)

    return pdf