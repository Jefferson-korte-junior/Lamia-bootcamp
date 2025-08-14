import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# A DAG simula um pipeline de processamento de dados com múltiplas fontes, tratamento de erros e notificações condicionais.

args_padrao = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
}

# Simulando diferentes fontes de dados
FONTES_DADOS = {
    'database_a': 'postgres://localhost/db_a',
    'database_b': 'postgres://localhost/db_b',
    'api_externa': 'https://api.exemplo.com/dados'
}


def verificar_fonte_disponivel():
    # Verifica qual fonte de dados está disponível
    print("Verificando fontes de dados disponíveis...")
    # Simulação de verificação - em um cenário real verificaria conectividade
    # Simula que database_b está indisponível
    fontes_disponiveis = ['database_a', 'api_externa']

    if fontes_disponiveis:
        print(f"Fontes disponíveis: {fontes_disponiveis}")
        return fontes_disponiveis[0]  # Retorna a primeira fonte disponível
    else:
        print("Nenhuma fonte disponível")
        return 'nenhuma_fonte'


def processar_dados_db_a():
    print("Processando dados do Database A...")
    return "dados_db_a_processados"


def processar_dados_db_b():
    print("Processando dados do Database B...")
    return "dados_db_b_processados"


def processar_dados_api():
    print("Processando dados da API externa...")
    return "dados_api_processados"


def falha_processamento():
    print("Erro: Falha no processamento dos dados")


def sucesso_processamento():
    print("Sucesso: Dados processados com êxito")


def validar_resultados():
    print("Validando resultados finais...")


def notificar_sucesso():
    print("Notificação: Operação concluída com sucesso")


def notificar_falha():
    print("Notificação: Operação falhou")


with DAG(dag_id='experimento_dag',
         default_args=args_padrao,
         schedule_interval="@daily",
         catchup=False) as dag:

    # Tarefa inicial de verificação com BranchPythonOperator
    verificar_fonte = BranchPythonOperator(
        task_id='verificar_fonte',
        python_callable=verificar_fonte_disponivel
    )

    # Tarefas de processamento para cada fonte de dados
    processar_db_a = PythonOperator(
        task_id='database_a',
        python_callable=processar_dados_db_a,
        trigger_rule="all_success"
    )

    processar_db_b = PythonOperator(
        task_id='database_b',
        python_callable=processar_dados_db_b,
        trigger_rule="all_success"
    )

    processar_api = PythonOperator(
        task_id='api_externa',
        python_callable=processar_dados_api,
        trigger_rule="all_success"
    )

    # Tarefa para quando nenhuma fonte está disponível
    nenhuma_fonte = DummyOperator(
        task_id='nenhuma_fonte'
    )

    # Tarefas condicionais baseadas no resultado do processamento
    falha_dados = PythonOperator(
        task_id='falha_dados',
        python_callable=falha_processamento,
        trigger_rule="all_failed"
    )

    sucesso_dados = PythonOperator(
        task_id='sucesso_dados',
        python_callable=sucesso_processamento,
        trigger_rule="all_success"
    )

    # Tarefa de validação que roda independente do resultado anterior
    validar = PythonOperator(
        task_id='validar',
        python_callable=validar_resultados,
        trigger_rule="one_success"
    )

    # Tarefas de notificação com diferentes trigger rules
    notif_sucesso = PythonOperator(
        task_id='notif_sucesso',
        python_callable=notificar_sucesso,
        trigger_rule="none_failed"
    )

    notif_falha = PythonOperator(
        task_id='notif_falha',
        python_callable=notificar_falha,
        trigger_rule="one_failed"
    )

    # Tarefa com template usando macros do Airflow
    gerar_relatorio = BashOperator(
        task_id='gerar_relatorio',
        bash_command='echo "Relatório gerado em {{ ds }} para execução {{ ts_nodash }}"',
        trigger_rule="none_failed"
    )

    # Definindo as dependências
    verificar_fonte >> [processar_db_a,
                        processar_db_b, processar_api, nenhuma_fonte]

    # Fluxo de processamento
    [processar_db_a, processar_db_b, processar_api] >> [falha_dados, sucesso_dados]
    [falha_dados, sucesso_dados] >> validar

    # Fluxo de notificações
    validar >> [notif_sucesso, notif_falha]

    # Geração de relatório final
    [notif_sucesso, notif_falha] >> gerar_relatorio

    # Fluxo alternativo quando nenhuma fonte está disponível
    nenhuma_fonte >> notif_falha
