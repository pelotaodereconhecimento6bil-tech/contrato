import streamlit as st
from datetime import date
from services.gerar_contrato import gerar_contrato
from database import criar_tabela, salvar_contrato, listar_contratos

from utils.formatacao import (
    valor_por_extenso,
    data_por_extenso,
    buscar_cep,
    formatar_nome,
    formatar_cpf,
    formatar_rg,
    formatar_moeda
)

criar_tabela()

st.set_page_config(layout="wide")
st.title("🚗 Sistema de Contratos")

menu = st.sidebar.selectbox("Menu", ["Novo Contrato", "Histórico"])

# =========================
# NOVO CONTRATO
# =========================
if menu == "Novo Contrato":

    st.markdown("## 📝 Novo Contrato")

    # =========================
    # DADOS DO LOCATÁRIO
    # =========================
    st.markdown("### 👤 Dados do Locatário")

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome completo")
        cpf = st.text_input("CPF")
        rg = st.text_input("RG")

    with col2:
        orgao_emissor = st.text_input("Órgão emissor (ex: SSP)")

        st.markdown("#### 📍 Endereço")

        cep = st.text_input("CEP")

        col_btn1, col_btn2 = st.columns([1, 3])

        with col_btn1:
            buscar = st.button("🔍 Buscar CEP")

        if "endereco_auto" not in st.session_state:
            st.session_state.endereco_auto = ""
            st.session_state.cidade_auto = ""
            st.session_state.estado_auto = ""

        if buscar:
            with st.spinner("Buscando CEP..."):
                dados_cep = buscar_cep(cep)

                if dados_cep:
                    st.session_state.endereco_auto = dados_cep["endereco"]
                    st.session_state.cidade_auto = dados_cep["cidade"]
                    st.session_state.estado_auto = dados_cep["estado"]
                    st.success("CEP encontrado!")
                else:
                    st.warning("CEP não encontrado!")

        endereco = st.text_input("Endereço", value=st.session_state.endereco_auto)

        col_end1, col_end2 = st.columns(2)

        with col_end1:
            numero = st.text_input("Número", placeholder="Ex: 123 ou S/N")

        with col_end2:
            complemento = st.text_input("Complemento (opcional)", placeholder="Apto, bloco...")

        cidade = st.text_input("Cidade", value=st.session_state.cidade_auto)
        estado = st.text_input("Estado", value=st.session_state.estado_auto)

        cep = st.text_input("CEP (final)", value=cep)

    st.divider()

    # =========================
    # VEÍCULO
    # =========================
    st.markdown("### 🚗 Dados do Veículo")

    col3, col4 = st.columns(2)

    with col3:
        veiculo = st.text_input("Modelo do veículo")
        placa = st.text_input("Placa")

    with col4:
        valor = st.number_input("Valor (R$)", min_value=0.0)
        data_inicio = st.date_input("Data início")
        data_fim = st.date_input("Data fim")

    st.divider()

    # =========================
    # VISTORIA
    # =========================
    st.markdown("### 🔍 Vistoria do Veículo")

    acessorios = st.text_area("Acessórios")
    estado_conservacao = st.text_area("Estado de conservação")
    pintura = st.text_input("Pintura")

    col5, col6 = st.columns(2)

    with col5:
        tipo_combustivel = st.selectbox("Combustível", ["Gasolina", "Etanol", "Flex", "Diesel"])

    with col6:
        nivel_combustivel = st.selectbox("Nível do tanque", ["Vazio", "1/4", "1/2", "3/4", "Cheio"])

    km_atual = st.number_input("KM atual", min_value=0)

    st.divider()

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

    with col_btn2:
        gerar = st.button("🚀 Gerar contrato", use_container_width=True)

    if gerar:

        if not nome or not cpf or not veiculo:
            st.error("Preencha todos os campos obrigatórios!")

        elif data_fim < data_inicio:
            st.error("Data final não pode ser menor que a inicial!")

        elif not numero:
            st.error("Informe o número do endereço!")

        else:
            # =========================
            # FORMATAÇÕES
            # =========================
            nome = formatar_nome(nome)
            cpf = formatar_cpf(cpf)
            rg = formatar_rg(rg)

            placa = placa.upper()
            estado = estado.upper()
            orgao_emissor = orgao_emissor.upper()

            endereco_completo = f"{endereco}, {numero}"
            if complemento:
                endereco_completo += f" - {complemento}"

            duracao = (data_fim - data_inicio).days
            valor_extenso = valor_por_extenso(valor)

            # =========================
            # DADOS DO CONTRATO
            # =========================
            dados = {
                "locatario_nome": nome,
                "locatario_cpf": cpf,
                "locatario_rg": rg,
                "orgao_emissor": orgao_emissor,
                "locatario_endereco": endereco_completo,
                "locatario_cidade": cidade,
                "locatario_estado": estado,
                "locatario_cep": cep,
                "veiculo_modelo": veiculo,
                "veiculo_placa": placa,
                "valor": formatar_moeda(valor),
                "valor_extenso": valor_extenso,
                "duracao": f"{duracao} dias",
                "data_inicio": data_inicio.strftime("%d/%m/%Y"),
                "data_fim": data_fim.strftime("%d/%m/%Y"),
                "data_assinatura_extenso": data_por_extenso(date.today()),
                "cidade": "São Paulo",
                "acessorios": acessorios,
                "estado_conservacao": estado_conservacao,
                "pintura": pintura,
                "tipo_combustivel": tipo_combustivel,
                "nivel_combustivel": nivel_combustivel,
                "km_atual": km_atual,
            }

            try:
                arquivo = gerar_contrato(dados)

                salvar_contrato(nome, cpf, veiculo, valor, str(date.today()))

                st.success("✅ Contrato gerado com sucesso!")

                with open(arquivo, "rb") as f:
                    st.download_button(
                        "📄 Baixar contrato (Word)",
                        f,
                        file_name=arquivo,
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"Erro: {e}")

# =========================
# HISTÓRICO
# =========================
elif menu == "Histórico":

    st.markdown("## 📄 Histórico de Contratos")

    busca = st.text_input("🔍 Buscar por nome")

    contratos = listar_contratos()

    if busca:
        contratos = [c for c in contratos if busca.lower() in c[1].lower()]

    if contratos:
        for c in contratos:
            with st.expander(f"📄 Contrato #{c[0]} - {c[1]}"):
                st.write(f"**CPF:** {c[2]}")
                st.write(f"**Veículo:** {c[3]}")
                st.write(f"**Valor:** R$ {c[4]}")
                st.write(f"**Data:** {c[5]}")
    else:
        st.info("Nenhum contrato encontrado.")