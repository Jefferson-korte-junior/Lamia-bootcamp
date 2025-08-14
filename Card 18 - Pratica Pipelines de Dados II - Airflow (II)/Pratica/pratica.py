from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime

# Argumentos da DAG
default_args = {
    'start_date': datetime(2025, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

with DAG(dag_id='pratica_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:

    # Task inicial
    tarefa_inicio = DummyOperator(task_id='inicio')

    # Tasks de processamento simples
    processar_dados_1 = BashOperator(
        task_id='processar_dados_1',
        bash_command='echo "Processando dataset 1..."'
    )

    processar_dados_2 = BashOperator(
        task_id='processar_dados_2',
        bash_command='echo "Processando dataset 2..."'
    )

    # Task com queue específica
    tarefa_intensiva = BashOperator(
        task_id='tarefa_intensiva',
        bash_command='echo "Executando computação intensiva..."',
        queue='worker_cpu'
    )

    # Task de agregação
    agregar_resultados = BashOperator(
        task_id='agregar_resultados',
        bash_command='echo "Agregando todos os resultados..."'
    )

    # Task final
    tarefa_fim = DummyOperator(task_id='fim')

    # Definindo as dependências
    tarefa_inicio >> [processar_dados_1, processar_dados_2]
    [processar_dados_1, processar_dados_2] >> tarefa_intensiva
    tarefa_intensiva >> agregar_resultados
    agregar_resultados >> tarefa_fim
