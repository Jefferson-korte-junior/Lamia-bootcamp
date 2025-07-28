# Importa a classe DAG para criar e configurar uma DAG
from airflow import DAG

# Importa uma função utilitária para definir datas relativas (ex: 1 dia atrás)
from airflow.utils.dates import days_ago

# Importa o operador PythonOperator, que permite executar funções Python como tarefas
from airflow.operators.python_operator import PythonOperator

# Define uma função simples que será usada como tarefa no Airflow
def tarefa_exemplo():
    print("Executando tarefa!")

# Criação do contexto da DAG utilizando o gerenciador de contexto 'with'
with DAG(
    'atividade_aula_4',            # ID da DAG
    start_date=days_ago(1),        # Data de início da DAG (1 dia atrás a partir da data atual)
    schedule_interval='@daily'     # Intervalo de agendamento da DAG (diariamente)
) as dag:

    # Define a função que será chamada pela tarefa
    def cumprimentos():
        print("Boas vindas ao airflow!")

    # Cria uma tarefa do tipo PythonOperator
    tarefa = PythonOperator(
        task_id='cumprimentos',        # Identificador único da tarefa dentro da DAG
        python_callable=cumprimentos   # Função Python que será executada quando a tarefa rodar
    )
