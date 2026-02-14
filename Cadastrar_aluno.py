import streamlit as st
import pandas as pd
import time
import dataframe

df_aluno = pd.read_csv("data/aluno.csv")
df_dieta = pd.read_csv("data/dieta.csv")
objetivos = ["Emagrecimento", "Hipertrofia", "Definição"]

st.set_page_config(layout="wide")
st.title("Cadastro de Alunos")

abs1, abs2, abs3, abs4 = st.tabs(["Visualizar", "Cadastrar", "Editar", "Excluir"])

with abs1:
    st.markdown("<h3>Alunos Cadastrados:</h3>", unsafe_allow_html=True)
    st.dataframe(df_aluno)
with abs2:
    st.markdown("<h3>Cadastrar Aluno:</h3>", unsafe_allow_html=True)
    id = len(df_aluno) + 1
    nome = st.text_input("Nome:")
    idade = st.number_input("Idade:", min_value=1, step=1)
    altura = st.number_input("Altura (M):", min_value=0.0, step=0.01)
    peso = st.number_input("Peso (KG):", min_value=0.0, step=0.1)
    objetivo = st.selectbox("Objetivo", objetivos)

    if st.button("Salvar"):
        novo_aluno = {
            "aluno_id": len(df_aluno) + 1,
            "Nome": nome,
            "Idade": idade,
            "Altura": altura,
            "Peso": peso,
            "Objetivo": objetivo
        }
        df_aluno = pd.concat([df_aluno, pd.DataFrame([novo_aluno])], ignore_index=True)

        df_aluno.to_csv("data/aluno.csv", index=False)

        st.success("Aluno salvo com sucesso!")
        time.sleep(3)
        st.rerun()

with abs3:
    if len(df_aluno) != 0:
        st.markdown("<h3>Editar Aluno:</h3>", unsafe_allow_html=True)
        nome_selecionado = st.selectbox("Selecione o Aluno:", df_aluno["Nome"].to_list())
        df_aluno_selecionado = df_aluno[df_aluno["Nome"] == nome_selecionado]
        nome = st.text_input("Novo Nome:", value=nome_selecionado)
        idade = st.number_input("Nova Idade:", min_value=1, step=1, value=df_aluno_selecionado["Idade"].iloc[0])
        altura = st.number_input("Nova Altura (M):", min_value=0.0, step=0.01, value=df_aluno_selecionado["Altura"].iloc[0])
        peso = st.number_input("Novo Peso (KG):", min_value=0.0, step=0.1, value=df_aluno_selecionado["Peso"].iloc[0])
        
        objetivo_atual = df_aluno_selecionado["Objetivo"].iloc[0]
        objetivo_index = objetivos.index(objetivo_atual)
        objetivo = st.selectbox("Novo Objetivo", objetivos, index=objetivo_index)

        if st.button("Salvar Alterações"):
            index = df_aluno_selecionado.index[0]
            df_aluno.loc[index, "Nome"] = nome
            df_aluno.loc[index, "Idade"] = idade
            df_aluno.loc[index, "Altura"] = altura
            df_aluno.loc[index, "Peso"] = peso
            df_aluno.loc[index, "Objetivo"] = objetivo

            df_aluno.to_csv("data/aluno.csv", index=False)
            st.success("Dados atualizados com Sucesso!")
            time.sleep(3)
            st.rerun()
    else:
        st.warning("Cadastre Alunos!")

with abs4:
    if len(df_aluno) != 0:
        if "confirmar_exclusao" not in st.session_state:
            st.session_state.confirmar_exclusao = False

        nome_excluir = st.selectbox(
            "Selecione o Aluno",
            df_aluno["Nome"].to_list()
        )

        if st.button(f"Excluir {nome_excluir}"):
            st.session_state.confirmar_exclusao = True

        if st.session_state.confirmar_exclusao:
            st.warning(f"Todos os dados de {nome_excluir} serão apagados. Continuar?")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Sim, excluir"):
                    df_excluir = df_aluno[df_aluno["Nome"] != nome_excluir]
                    df_aluno_excluir = df_aluno[df_aluno["Nome"] == nome_selecionado]
                    df_dieta = df_dieta[df_dieta["aluno_id"] != df_aluno_excluir["aluno_id"].iloc[0]]
                    df_excluir.to_csv("data/aluno.csv", index=False)
                    df_dieta.to_csv("data/dieta.csv", index=False)

                    st.success(f"{nome_excluir} excluído com sucesso!")
                    st.session_state.confirmar_exclusao = False
                    time.sleep(2)
                    st.rerun()

            with col2:
                if st.button("Cancelar"):
                    st.session_state.confirmar_exclusao = False
                    st.rerun()
    else:
        st.warning("Cadastre Alunos!")