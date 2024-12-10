from bs4 import BeautifulSoup
# Importa a classe BeautifulSoup da biblioteca bs4 para analisar documentos HTML e XML.

import requests
# Importa a biblioteca requests para fazer requisições HTTP.

import time
# Importa a biblioteca time para manipular operações relacionadas ao tempo, como adicionar atrasos.

print('Put some skill that are not familiar with')
# Exibe uma mensagem solicitando que o usuário insira uma habilidade com a qual não está familiarizado.

unfamiliar_skill = input('>')
# Captura a entrada do usuário e armazena na variável unfamiliar_skill.

print(f'Filtering out {unfamiliar_skill}')
# Imprime uma mensagem confirmando a habilidade que será filtrada.

def find_jobs():
    # Define uma função chamada find_jobs que irá procurar por vagas de emprego.

    html_text = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=Python&txtKeywords=Python&txtLocation=").text
    # Faz uma requisição GET para a URL especificada e armazena o conteúdo HTML da página em html_text.

    soup = BeautifulSoup(html_text, 'lxml')
    # Usa BeautifulSoup com o parser lxml para analisar o HTML recebido e armazena o resultado em soup.

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    # Encontra todas as tags <li> com a classe clearfix job-bx wht-shd-bx e armazena os resultados em jobs.

    for job in jobs:
        # Inicia um loop para iterar sobre cada item em jobs.

        published_date = job.find('span', class_='sim-posted').span.text
        # Encontra a data de publicação dentro da tag <span> com a classe sim-posted e armazena o texto na variável published_date.

        if 'few' in published_date:
            # Verifica se a palavra 'few' está presente na data de publicação, indicando que a vaga foi publicada recentemente.

            company_name = job.find('h3', class_='joblist-comp-name').text.replace('', '')
            # Encontra o nome da empresa dentro da tag <h3> com a classe joblist-comp-name e remove espaços em branco extras.

            skills = job.find('span', class_='srp-skills').text.replace('', '')
            # Encontra as habilidades requeridas dentro da tag <span> com a classe srp-skills e remove espaços em branco extras.

            more_info = job.header.h2.a['href']
            # Encontra o link para mais informações sobre a vaga dentro da tag <a> aninhada em <header><h2> e armazena o valor do atributo href.

            if unfamiliar_skill not in skills:
                # Verifica se a habilidade desconhecida não está presente nas habilidades requeridas.

                print(f"Company name : {company_name.strip()}")
                # Imprime o nome da empresa.

                print(f"Required Skills: {skills.strip()}")
                # Imprime as habilidades requeridas.

                print(f'More info: {more_info}')
                # Imprime o link para mais informações sobre a vaga.

                print('')
                # Adiciona uma linha em branco para separar visualmente as vagas de emprego.

if __name__ == '__main__':
    # Verifica se o script está sendo executado como o programa principal.

    while True:
        # Inicia um loop infinito para repetir a busca por vagas de emprego periodicamente.

        find_jobs()
        # Chama a função find_jobs para procurar por vagas de emprego.

        time_wait = 10
        # Define o tempo de espera em 10 minutos.

        print(f'Waiting {time_wait} seconds')
        # Imprime uma mensagem indicando o tempo de espera.

        time.sleep(time_wait * 60)
        # Pausa a execução do programa por time_wait minutos (convertido para segundos).