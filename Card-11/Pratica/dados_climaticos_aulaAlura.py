# Importações necessárias para criar a DAG e operadores do Airflow
from airflow import DAG
import pendulum
from airflow.operators.bash_operator import BashOperator  # Executa comandos bash
from airflow.operators.python import PythonOperator       # Executa funções Python
from airflow.macros import ds_add                         # Macro para manipular datas
from os.path import join 
import pandas as pd
import os

# Definição da DAG: executa semanalmente às segundas-feiras a partir de 26/05/2025
with DAG(
    "dados_climaticos",
    start_date=pendulum.datetime(2025, 5, 26, tz="UTC"),
    schedule_interval='0 0 * * 1',  # Toda segunda-feira à meia-noite
    catchup=False
) as dag: 

    # Tarefa 1: Cria uma pasta baseada na data de execução
    tarefa_1 = BashOperator(
        task_id='cria_pasta',
        bash_command='mkdir -p "/home/jeffinho345/Documents/airflowalura/semana={{ data_interval_end.strftime("%Y-%m-%d") }}/"'
    )

    # Função para extrair dados climáticos da API da Visual Crossing
    def extrai_dados(data_interval_end):
        city = "boston" 
        key = "FCEBUQSX974B4B58F2X9QFMLW"

        # Monta a URL da API com intervalo de 7 dias
        url = (
            f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
            f"{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={key}&contentType=csv"
        )

        # Define o caminho da pasta onde os arquivos serão salvos
        file_path = f"/home/jeffinho345/Documents/airflowalura/semana={data_interval_end}/"
        os.makedirs(file_path, exist_ok=True)

        # Lê os dados da URL
        dados = pd.read_csv(url)

        # Salva os dados brutos e filtrados em CSVs separados
        dados.to_csv(file_path + "dados_bruto.csv")
        dados[["datetime", "tempmin", "temp", "tempmax"]].to_csv(file_path + "temperatura.csv", index=False)
        dados[["datetime", "description", "icon"]].to_csv(file_path + "condicoes.csv", index=False)

    # Tarefa 2: Executa a função de extração de dados
    tarefa_2 = PythonOperator(
        task_id='extrai_dados',
        python_callable=extrai_dados,
        op_kwargs={'data_interval_end': '{{ data_interval_end.strftime("%Y-%m-%d") }}'}
    )

    # Define a ordem de execução: tarefa_1 → tarefa_2
    tarefa_1 >> tarefa_2
