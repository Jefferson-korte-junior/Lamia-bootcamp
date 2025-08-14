from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator  # Operador fictício para representar uma tarefa "vazia"
from airflow.operators.bash_operator import BashOperator    # Executa comandos no terminal/bash

from datetime import datetime

# Argumentos padrão para a DAG
default_args = {
    'start_date': datetime(2019, 1, 1),  # Data de início
    'owner': 'Airflow',                  # Dono da DAG (informativo)
    'email': 'owner@test.com'           # Email do dono (não utilizado aqui)
}

# Definição da DAG
with DAG(
    dag_id='queue_dag',                      # Nome da DAG
    schedule_interval='0 0 * * *',           # Executa diariamente à meia-noite
    default_args=default_args,
    catchup=False                            # Evita execuções retroativas
) as dag:
    
    # Tarefas I/O intensivas alocadas na fila 'worker_ssd'
    t_1_ssd = BashOperator(task_id='t_1_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')
    t_2_ssd = BashOperator(task_id='t_2_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')
    t_3_ssd = BashOperator(task_id='t_3_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')

    # Tarefas CPU intensivas alocadas na fila 'worker_cpu'
    t_4_cpu = BashOperator(task_id='t_4_cpu', bash_command='echo "CPU instensive task"', queue='worker_cpu')
    t_5_cpu = BashOperator(task_id='t_5_cpu', bash_command='echo "CPU instensive task"', queue='worker_cpu')

    # Tarefa com dependência Spark alocada na fila 'worker_spark'
    t_6_spark = BashOperator(task_id='t_6_spark', bash_command='echo "Spark dependency task"', queue='worker_spark')

    # Tarefa final fictícia usada como ponto de convergência
    task_7 = DummyOperator(task_id='task_7')

    # Todas as tarefas anteriores devem terminar antes de executar task_7
    [t_1_ssd, t_2_ssd, t_3_ssd, t_4_cpu, t_5_cpu, t_6_spark] >> task_7
