import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator


# Parâmetros padrão da DAG
default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
}


def download_website_a():
    print("download_website_a")
    # raise ValueError("error")  # Descomente para simular erro


def download_website_b():
    print("download_website_b")


def download_failed():
    print("download_failed")


def download_succeed():
    print("download_succeed")


def process():
    print("process")


def notif_a():
    print("notif_a")


def notif_b():
    print("notif_b")


# DAG executa diariamente
with DAG(dag_id='trigger_rule_dag', default_args=default_args, schedule_interval="@daily") as dag:

    # Tarefas principais: downloads de dois sites
    download_website_a_task = PythonOperator(
        task_id='download_website_a',
        python_callable=download_website_a,
        trigger_rule="all_success"  # Executa se tarefas anteriores forem bem-sucedidas
    )

    download_website_b_task = PythonOperator(
        task_id='download_website_b',
        python_callable=download_website_b,
        trigger_rule="all_success"
    )

    # Executada apenas se TODAS as tarefas anteriores falharem
    download_failed_task = PythonOperator(
        task_id='download_failed',
        python_callable=download_failed,
        trigger_rule="all_failed"
    )

    # Executada apenas se TODAS tiverem sucesso
    download_succeed_task = PythonOperator(
        task_id='download_succeed',
        python_callable=download_succeed,
        trigger_rule="all_success"
    )

    # Executada se PELO MENOS UMA tarefa anterior tiver sucesso
    process_task = PythonOperator(
        task_id='process',
        python_callable=process,
        trigger_rule="one_success"
    )

    # Executada se NENHUMA tarefa anterior falhar
    notif_a_task = PythonOperator(
        task_id='notif_a',
        python_callable=notif_a,
        trigger_rule="none_failed"
    )

    # Executada se PELO MENOS UMA tarefa anterior falhar
    notif_b_task = PythonOperator(
        task_id='notif_b',
        python_callable=notif_b,
        trigger_rule="one_failed"
    )

    # As tarefas de sucesso e falha dependem dos dois downloads
    [download_website_a_task, download_website_b_task] >> download_failed_task
    [download_website_a_task, download_website_b_task] >> download_succeed_task

    # A tarefa de processamento depende das duas (falha e sucesso)
    [download_failed_task, download_succeed_task] >> process_task

    # As notificações são executadas depois do processamento
    process_task >> [notif_a_task, notif_b_task]
