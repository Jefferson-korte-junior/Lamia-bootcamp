# Importa a classe DAG, que é usada para definir um fluxo de tarefas (Directed Acyclic Graph)
from airflow.models import DAG

# Importa uma função utilitária que retorna uma data relativa (n dias atrás)
from airflow.utils.dates import days_ago

# Importa um operador vazio, usado apenas para criar tarefas de controle ou marcação
from airflow.operators.empty import EmptyOperator

# Importa um operador que permite executar comandos de terminal (bash)
from airflow.operators.bash_operator import BashOperator

# Define o contexto da DAG com suas configurações básicas
with DAG(
    'meu_primeiro_dag',  # Nome da DAG (identificador único no Airflow)
    start_date=days_ago(2),  # Data de início: 1 dia atrás em relação à data atual
    schedule_interval='@daily'  # Intervalo de agendamento: executa 1 vez por dia
) as dag:

    # Define a primeira tarefa (vazia), que inicia o fluxo
    tarefa_1 = EmptyOperator(task_id='tarefa_1')

    # Define outras duas tarefas vazias, que dependem da tarefa_1
    tarefa_2 = EmptyOperator(task_id='tarefa_2')
    tarefa_3 = EmptyOperator(task_id='tarefa_3')

    # Define uma tarefa que executa um comando bash para criar uma pasta no sistema
    tarefa_4 = BashOperator(
        task_id='cria_pasta',
        # Cria uma pasta com o nome baseado na data final do intervalo da execução (data_interval_end).
        bash_command='mkdir -p "/home/jeffinho345/Documents/airflowalura/pasta={{data_interval_end}}"'
    )

    # Define as dependências entre as tarefas:
    # tarefa_1 → (tarefa_2 e tarefa_3) → tarefa_4 (apenas vindo de tarefa_3)
    tarefa_1 >> [tarefa_2, tarefa_3]
    tarefa_3 >> tarefa_4
