import streamlit as st
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Image,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
import time

df_aluno = pd.read_csv("data/aluno.csv")
df_dieta = pd.read_csv("data/dieta.csv")
id_dieta = df_dieta["aluno_id"].to_list()
df_nomes_df = df_aluno[df_aluno["aluno_id"].isin(id_dieta)]
df_nomes = df_nomes_df["Nome"].to_list()
objetivos = ["Emagrecimento", "Hipertrofia", "Definição"]


st.set_page_config(layout="wide")
st.title("Gerar dieta em PDF")

abs1, abs2 = st.tabs(["Dietas Salvas", "Criar Dieta"])

with abs1:
    if len(df_dieta == 0):
        nome_selecionado = st.selectbox("Selecione o Aluno:", df_nomes, key="selecionar_pdf")
        linha_selecionada = df_aluno[df_aluno["Nome"] == nome_selecionado]
        id = linha_selecionada["aluno_id"].iloc[0]
        df_dietas_selecionadas = df_dieta[df_dieta["aluno_id"] == id]
        
        index=0
        if len(df_dietas_selecionadas) > 1:
            index = st.selectbox("Selecione a Dieta:", df_dietas_selecionadas.index.to_list())
        else:
            index = df_dietas_selecionadas.index[0]
        
        if st.button("Gerar PDF"):
            placeholder = st.empty()
            placeholder.info("⏳Aguarde! Gerando PDF...")
            doc = SimpleDocTemplate(
                f"dietas/dieta_{nome_selecionado}_{index}.pdf",
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(
                name="TituloRosa",
                parent=styles["Title"],
                textColor=HexColor("#C2185B"),  # rosa escuro
                alignment=1
            ))

            elements = []
            elements.append(Paragraph(
                f"<b>Dieta de</b><br/>{nome_selecionado}",
                styles["TituloRosa"]
            ))
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(
                f"<b>Idade</b>: {linha_selecionada["Idade"].iloc[0]} anos.<br/><br/>"
                f"<b>Altura</b>: {linha_selecionada["Altura"].iloc[0]} metros.<br/><br/>"
                f"<b>Peso</b>: {linha_selecionada["Peso"].iloc[0]} kg.<br/><br/>"
                f"<b>Objetivo</b>: {linha_selecionada["Objetivo"].iloc[0]}.",
                styles["Normal"]
            ))
            elements.append(Spacer(1, 20))

            elements.append(Paragraph(
                "<b>Dieta:</b>",
                styles["TituloRosa"]
            ))
            elements.append(Spacer(1, 20))

            elements.append(Paragraph(
                f"<b>Caloria</b>: {df_dieta.loc[index,"Caloria"]}<br/><br/>"
                f"<b>Pré-Treino</b>:<br/>{df_dieta.loc[index,"Pré-Treino"]}<br/><br/>"
                f"<b>Café da Manhã</b>:<br/>{df_dieta.loc[index,"Café da Manhã"]}<br/><br/>"
                f"<b>Lanche da Manhã</b>:<br/>{df_dieta.loc[index,"Lanche da Manhã"]}<br/><br/>"
                f"<b>Almoço</b>:<br/>{df_dieta.loc[index,"Almoço"]}.<br/><br/>"
                f"<b>Lanche da Tarde</b>:<br/>{df_dieta.loc[index,"Lanche da Tarde"]}<br/><br/>"
                f"<b>Jantar</b>:<br/>{df_dieta.loc[index,"Jantar"]}<br/><br/>"
                f"<b>Ceia</b>:<br/>{df_dieta.loc[index,"Ceia"]}"
            ))

            doc.build(elements)
            placeholder.empty()
            placeholder.success("✅ Dieta Gerada com Sucesso!")
            time.sleep(3)
            placeholder.empty()

            st.markdown("<br><h4>⬇️ Baixar PDF:</h4>", unsafe_allow_html=True)
            with open(f"dietas/dieta_{nome_selecionado}_{index}.pdf", "rb") as file: #Abre o arquivo em binario rb
                st.download_button(
                    label=" 📥Baixar Dieta", #Nome do botao
                    data=file, #Arquivo
                    file_name=f"dieta_{nome_selecionado}_{index}.pdf", #Nome que o usuário verá
                    mime="application/pdf" #Informar ao navegador que é pdf
                )
    else:
        st.warning("Cadastre Dietas!")
        
with abs2:
    st.markdown("<h3>Dados Pessoais:</h3>", unsafe_allow_html=True)
    nome = st.text_input("Nome:")
    idade = st.number_input("Idade:", min_value=1, step=1)
    altura = st.number_input("Altura (M):", min_value=0.01, step=0.01)
    peso = st.number_input("Peso (KG):", min_value=0.01, step=0.01)
    objetivo = st.selectbox("Objetivo:", objetivos)

    st.markdown("<h3>Dieta:</h3>", unsafe_allow_html=True)
    cm = st.text_input("Café da Manhã:")
    lm = st.text_input("Lanche da Manhã:")
    al = st.text_input("Almoço:")
    lt = st.text_input("Lanche da Tarde:")
    ja = st.text_input("Jantar:")
    ce = st.text_input("Ceia:")
    pt = st.text_input("Pré-treino:")
    caloria = st.number_input("Total de Calorias:", step=1)

    if st.button("Gerar PDF", key="gerar"):
        placeholder = st.empty()
        placeholder.info("⏳Aguarde! Gerando PDF...")
        doc = SimpleDocTemplate(
            f"dietas/dieta_{nome}.pdf",
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name="TituloRosa",
            parent=styles["Title"],
            textColor=HexColor("#C2185B"),  # rosa escuro
            alignment=1
        ))

        elements = []
        elements.append(Paragraph(
            f"<b>Dieta de</b><br/>{nome}",
            styles["TituloRosa"]
        ))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(
            f"<b>Idade</b>: {idade} anos.<br/><br/>"
            f"<b>Altura</b>: {altura} metros.<br/><br/>"
            f"<b>Peso</b>: {peso} kg.<br/><br/>"
            f"<b>Objetivo</b>: {objetivo}.",
            styles["Normal"]
        ))
        elements.append(Spacer(1, 20))

        elements.append(Paragraph(
            "<b>Dieta:</b>",
            styles["TituloRosa"]
        ))
        elements.append(Spacer(1, 20))

        elements.append(Paragraph(
            f"<b>Caloria</b>: {caloria}<br/><br/>"
            f"<b>Pré-Treino</b>:<br/>{pt}<br/><br/>"
            f"<b>Café da Manhã</b>:<br/>{cm}<br/><br/>"
            f"<b>Lanche da Manhã</b>:<br/>{lm}<br/><br/>"
            f"<b>Almoço</b>:<br/>{al}.<br/><br/>"
            f"<b>Lanche da Tarde</b>:<br/>{lt}<br/><br/>"
            f"<b>Jantar</b>:<br/>{ja}<br/><br/>"
            f"<b>Ceia</b>:<br/>{ce}"
        ))

        doc.build(elements)
        placeholder.empty()
        placeholder.success("✅ Dieta Gerada com Sucesso!")
        time.sleep(3)
        placeholder.empty()

        st.markdown("<br><h4>⬇️ Baixar PDF:</h4>", unsafe_allow_html=True)
        with open(f"dietas/dieta_{nome}.pdf", "rb") as file: #Abre o arquivo em binario rb
            st.download_button(
                label=" 📥Baixar Dieta", #Nome do botao
                data=file, #Arquivo
                file_name=f"dieta_{nome}.pdf", #Nome que o usuário verá
                mime="application/pdf" #Informar ao navegador que é pdf
            )