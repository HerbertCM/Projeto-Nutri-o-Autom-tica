import os
import pandas as pd

caminho = "data/"

if not os.path.exists(caminho):
    os.makedirs(caminho)

if not os.path.exists(caminho + "aluno.csv"):
    aluno = {
        "aluno_id": [],
        "Nome": [],
        "Idade": [],
        "Altura": [],
        "Peso": [],
        "Objetivo": []
    }
    df_aluno = pd.DataFrame(aluno)
    df_aluno.to_csv(caminho + "aluno.csv", index=False)
    print("DataFrame aluno criado!")
else:
    df_aluno = pd.read_csv(caminho + "aluno.csv")
    print("DataFrame aluno Carregado!")

if not os.path.exists(caminho + "dieta.csv"):
    dieta = {
        "aluno_id": [],
        "Café da Manhã": [],
        "Lanche da Manhã": [],
        "Almoço": [],
        "Lanche da Tarde": [],
        "Jantar": [],
        "Ceia": [],
        "Pré-Treino": [],
        "Caloria": [],
    }
    df_dieta = pd.DataFrame(dieta)
    df_dieta.to_csv(caminho + "dieta.csv", index=False)
    print("DataFrame dieta criado!")
else:
    df_dieta = pd.read_csv(caminho + "dieta.csv")
    print("DataFrame dieta Carregado!")