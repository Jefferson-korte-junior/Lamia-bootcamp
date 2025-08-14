# Este código segue a estrutura de um curso antigo de Airflow.
# Alguns operadores foram reorganizados em versões mais recentes.


import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator


# Argumentos padrão para a DAG
default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}


# Links de três APIs públicas de geolocalização por IP
IP_GEOLOCATION_APIS = {
    'ip-api': 'http://ip-api.com/json/',
    'ipstack': 'https://api.ipstack.com/',
    'ipinfo': 'https://ipinfo.io/json'
}


# Tenta acessar cada API e verifica se a resposta tem o campo 'country'
# Retorna uma lista com o nome das APIs válidas ou 'none' se nenhuma funcionar
def check_api():
    apis = []
    for api, link in IP_GEOLOCATION_APIS.items():
        r = requests.get(link)
        try:
            data = r.json()
            if data and 'country' in data and len(data['country']):
                apis.append(api)
        except ValueError:
            pass
    return apis if len(apis) > 0 else 'none'


# Define a DAG que roda uma vez
with DAG(dag_id='branch_dag', default_args=default_args, schedule_interval="@once") as dag:

    # Tarefa que decide para onde seguir, com base no retorno da função check_api
    check_api = BranchPythonOperator(
        task_id='check_api',
        python_callable=check_api
    )

    # Executada se nenhuma API funcionar
    none = DummyOperator(task_id='none')

    # Tarefa final que será executada depois da válida (ou do 'none')
    save = DummyOperator(task_id='save', trigger_rule='one_success')

    # Encadeamento caso nenhuma API funcione
    check_api >> none >> save

    # Para cada API, cria uma tarefa que será chamada se a respectiva API for válida
    for api in IP_GEOLOCATION_APIS:
        process = DummyOperator(task_id=api)
        check_api >> process >> save
