# Este código utiliza operadores que estavam disponíveis em versões antigas do Airflow,
# os módulos http_operator e bash_operator foram movidos ou substituídos.

from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator  # Operador para chamadas HTTP
from airflow.operators.bash_operator import BashOperator        # Operador para rodar comandos no terminal

# Importa a classe datetime para definir a data de início da DAG
from datetime import datetime

# Parâmetros padrão para a DAG
default_args = {
    'start_date': datetime(2019, 1, 1),  # Data inicial da DAG 
    'owner': 'Airflow',                  # Dono da DAG 
    'email': 'owner@test.com'           # Email do dono 
}

# Definição da DAG principal
with DAG(
    dag_id='pool_dag',                      # Nome da DAG
    schedule_interval='0 0 * * *',          # Agendamento: todos os dias à meia-noite
    default_args=default_args,              # Parâmetros padrão definidos acima
    catchup=False                           # Evita executar DAGs antigas que não foram rodadas
) as dag:
    
    # Tarefa 1 - Faz requisição HTTP para buscar taxas de câmbio com base no euro (EUR)
    get_forex_rate_EUR = SimpleHttpOperator(
        task_id='get_forex_rate_EUR',           # Nome da tarefa
        method='GET',                           # Tipo de requisição HTTP
        priority_weight=1,                      # Peso de prioridade ao usar o pool
        pool='forex_api_pool',                  # Nome do pool para limitar concorrência
        http_conn_id='forex_api',               # ID da conexão definida no Airflow
        endpoint='/latest?base=EUR',            # Endpoint da API para base EUR
        xcom_push=True                          # Salva a resposta da API no XCom para uso posterior
    )
 
    # Tarefa 2 - Requisição com base no dólar (USD)
    get_forex_rate_USD = SimpleHttpOperator(
        task_id='get_forex_rate_USD',
        method='GET',
        priority_weight=2,
        pool='forex_api_pool',
        http_conn_id='forex_api',
        endpoint='/latest?base=USD',
        xcom_push=True
    )
 
    # Tarefa 3 - Requisição com base no iene japonês (JPY)
    get_forex_rate_JPY = SimpleHttpOperator(
        task_id='get_forex_rate_JPY',
        method='GET',
        priority_weight=3,
        pool='forex_api_pool',
        http_conn_id='forex_api',
        endpoint='/latest?base=JPY',
        xcom_push=True
    )
 

    # Comando bash que exibe o resultado das tarefas anteriores (valores puxados via XCom)
    bash_command = """
    {% for task in dag.task_ids %}
        echo "{{ task }}"
        echo "{{ ti.xcom_pull(task) }}"
    {% endfor %}
    """


    # Tarefa final - Executa o comando bash que imprime os dados das chamadas HTTP
    show_data = BashOperator(
        task_id='show_result',
        bash_command=bash_command
    )

    # Define a ordem das tarefas: todas as requisições devem rodar antes de mostrar os resultados
    [get_forex_rate_EUR, get_forex_rate_USD, get_forex_rate_JPY] >> show_data
