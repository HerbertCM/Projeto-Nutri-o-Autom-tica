import streamlit as st
import pandas as pd
import time

if "confirmar_exclusao" not in st.session_state:
    st.session_state.confirmar_exclusao = False

df_aluno = pd.read_csv("data/aluno.csv")
df_dieta = pd.read_csv("data/dieta.csv")
st.set_page_config(layout="wide")
st.title("Cadastrar Dietas:")

id_dieta = df_dieta["aluno_id"].to_list()
df_nomes_df = df_aluno[df_aluno["aluno_id"].isin(id_dieta)]
df_nomes = df_nomes_df["Nome"].to_list()

abs1, abs2, abs3, abs4 = st.tabs(["Visualizar", "Cadastrar", "Editar", "Excluir"])

with abs1:
    st.dataframe(df_dieta)

with abs2:
    if len(df_aluno) != 0:
        aluno_selecionado = st.selectbox("Selecione o Aluno:", df_aluno["Nome"].to_list())
        df_selecionado = df_aluno[df_aluno["Nome"] == aluno_selecionado]
        
        id = df_selecionado["aluno_id"].iloc[0]
        cm = st.text_input("Café da Manhã:")
        lm = st.text_input("Lanche da Manhã:")
        al = st.text_input("Almoço:")
        lt = st.text_input("Lanche da Tarde:")
        ja = st.text_input("Jantar:")
        ce = st.text_input("Ceia:")
        pt = st.text_input("Pré-treino:")
        caloria = st.number_input("Total de Calorias:", min_value=1, step=1)

        if st.button("Salvar"):
            nova_dieta = {
                "aluno_id": id,
                "Café da Manhã": cm,
                "Lanche da Manhã": lm,
                "Almoço": al,
                "Lanche da Tarde": lt,
                "Jantar": ja,
                "Ceia": ce,
                "Pré-Treino": pt,
                "Caloria": caloria
            }
            df_dieta = pd.concat([df_dieta, pd.DataFrame([nova_dieta])], ignore_index=True)

            df_dieta.to_csv("data/dieta.csv", index=False)

            st.success("Dieta salva com sucesso!")
            time.sleep(3)
            st.rerun()
    else:
        st.warning("Cadastre Alunos!")

    with abs3:
        if len(df_dieta) != 0:
            col1, col2 = st.columns(2)
            with col1:
                aluno_selecionado = st.selectbox("Selecione o Aluno:", df_nomes, key="dieta")
                df_selecionado = df_aluno[df_aluno["Nome"] == aluno_selecionado]
                id = df_selecionado["aluno_id"].iloc[0]
                df_dietas_selecionas = df_dieta[df_dieta["aluno_id"] == id]

                index=0
                if len(df_dietas_selecionas) > 1:
                    index = st.selectbox("Selecione a Dieta:", df_dietas_selecionas.index.to_list(), key="index_dieta")
                else:
                    index = df_dietas_selecionas.index[0]
                
                cm = st.text_input("Novo Café da Manhã:", value=df_dietas_selecionas.loc[index, "Café da Manhã"])
                lm = st.text_input("Novo Lanche da Manhã:", value=df_dietas_selecionas.loc[index, "Lanche da Manhã"])
                al = st.text_input("Novo Almoço:", value=df_dietas_selecionas.loc[index, "Almoço"])
                lt = st.text_input("Novo Lanche da Tarde:", value=df_dietas_selecionas.loc[index, "Lanche da Tarde"])
                ja = st.text_input("Novo Jantar:", value=df_dietas_selecionas.loc[index, "Jantar"])
                ce = st.text_input("Nova Ceia:", value=df_dietas_selecionas.loc[index, "Ceia"])
                pt = st.text_input("Novo Pré-treino:", value=df_dietas_selecionas.loc[index, "Pré-Treino"])
                caloria = st.number_input("Novo Total de Calorias:", min_value=1, step=1, value=df_dietas_selecionas.loc[index, "Caloria"])

                if st.button("Salvar alterações"):
                    df_dieta.loc[index, "Café da Manhã"] = cm
                    df_dieta.loc[index, "Lanche da Manhã"] = lm
                    df_dieta.loc[index, "Almoço"] = al
                    df_dieta.loc[index, "Lanche da Tarde"] = lt
                    df_dieta.loc[index, "Jantar"] = ja
                    df_dieta.loc[index, "Ceia"] = ce
                    df_dieta.loc[index, "Pré-Treino"] = pt
                    df_dieta.loc[index, "Caloria"] = caloria

                    df_dieta.to_csv("data/dieta.csv", index=False)
                    st.success("Dados atualizados com Sucesso!")
                    time.sleep(3)
                    st.rerun()
            
                with col2:
                    st.dataframe(df_dietas_selecionas)
        else:
            st.warning("Cadastre Dietas!")

    with abs4:
        if len(df_dieta) != 0:
            aluno_selecionado = st.selectbox("Selecione o Aluno:", df_nomes, key="dieta_excluir")
            df_selecionado = df_aluno[df_aluno["Nome"] == aluno_selecionado]
            id = df_selecionado["aluno_id"].iloc[0]
            df_dietas_selecionas = df_dieta[df_dieta["aluno_id"] == id]

            if len(df_dietas_selecionas) > 1:
                index = st.selectbox("Selecione a Dieta:", df_dietas_selecionas.index.to_list())
            else:
                index = df_dietas_selecionas.index[0]

            if st.button(f"Excluir dieta de {aluno_selecionado}"):
                    st.session_state.confirmar_exclusao = True

            if st.session_state.confirmar_exclusao:
                st.warning(f"Continuar?")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Sim"):
                        df_dieta = df_dieta.drop(index)
                        df_dieta.to_csv("data/dieta.csv", index=False)

                        st.success("Dieta excluída com sucesso!")
                        st.session_state.confirmar_exclusao = False
                        time.sleep(2)
                        st.rerun()

                with col2:
                    if st.button("Cancelar"):
                        st.session_state.confirmar_exclusao = False
                        st.rerun()
        else:
            st.warning("Cadastre Dietas!")