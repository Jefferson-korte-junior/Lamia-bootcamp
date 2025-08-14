# Este código foi escrito com base em versões antigas do Airflow.
# Alguns operadores, como BashOperator e PythonOperator, foram movidos em versões mais recentes.

from process_logs import process_logs_func
import sys
import airflow
# DAG + macros (como ts_nodash)
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator        # Executa comandos bash
from airflow.operators.python_operator import PythonOperator    # Executa funções Python
# (não usado neste código)
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta


# Adiciona o diretório de scripts ao PATH para importar funções externas
sys.path.insert(1, '/usr/local/airflow/dags/scripts')

# Importa a função Python que será usada na DAG


# Template para o caminho onde os logs serão salvos
# Usa variáveis do Airflow + macro para formatar timestamp no nome da pasta
TEMPLATED_LOG_DIR = """{{ var.value.source_path }}/data/{{ macros.ds_format(ts_nodash, "%Y%m%dT%H%M%S", "%Y-%m-%d-%H-%M") }}/"""


# Argumentos padrão para a DAG
default_args = {
    "owner": "Airflow",
    "start_date": airflow.utils.dates.days_ago(1),  # Começa há 1 dia
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "youremail@host.com",
    "retries": 1
}


# Define a DAG que roda diariamente
with DAG(dag_id="template_dag", schedule_interval="@daily", default_args=default_args) as dag:

    # Apenas imprime a data formatada para debug/registro
    t0 = BashOperator(
        task_id="t0",
        bash_command="echo {{ ts_nodash }} - {{ macros.ds_format(ts_nodash, '%Y%m%dT%H%M%S', '%Y-%m-%d-%H-%M') }}"
    )

    # Executa script shell que gera o arquivo de log
    t1 = BashOperator(
        task_id="generate_new_logs",
        bash_command="./scripts/generate_new_logs.sh",
        params={'filename': 'log.csv'}
    )

    # Verifica se o arquivo de log foi criado com sucesso no caminho esperado
    t2 = BashOperator(
        task_id="logs_exist",
        bash_command="test -f " + TEMPLATED_LOG_DIR + "log.csv"
    )

    # Processa os logs usando função Python externa
    t3 = PythonOperator(
        task_id="process_logs",
        python_callable=process_logs_func,          # Função importada do script
        provide_context=True,                       # Permite acessar contexto do Airflow
        # Passa o caminho do log como template
        templates_dict={'log_dir': TEMPLATED_LOG_DIR},
        params={'filename': 'log.csv'}
    )

    # Define a ordem de execução: t0 → t1 → t2 → t3
    t0 >> t1 >> t2 >> t3
