import os
import requests

# Linhas especiais para identificar onde as estatísticas do WakaTime devem ser inseridas no README.md
START_SECTION = "<!--START_SECTION:waka-->"
END_SECTION = "<!--END_SECTION:waka-->"

# Função para obter as estatísticas do WakaTime
def get_wakatime_stats(api_key):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get('https://wakatime.com/api/v1/users/current/stats/last_7_days', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch Wakatime stats:", response.status_code)
        return None

# Função para formatar as estatísticas
def format_stats(stats):
    formatted_stats = ""
    if stats:
        for data in stats['data']:
            formatted_stats += f"{data['range']['text']}: {data['total']['text']}\n"
            for language in data['languages']:
                formatted_stats += f"{language['name']}: {language['text']}\n"
            formatted_stats += "\n"
    return formatted_stats

# Função para atualizar o README.md com as estatísticas
def update_readme(stats):
    with open('README.md', 'r+') as readme:
        readme_content = readme.read()
        # Encontrar a posição onde as estatísticas do WakaTime devem ser inseridas
        start_index = readme_content.find(START_SECTION) + len(START_SECTION)
        end_index = readme_content.find(END_SECTION)
        # Substituir as estatísticas do WakaTime na seção do README.md
        updated_readme_content = (
            readme_content[:start_index]
            + "\n\n## Wakatime Stats\n\n"  # Adiciona um cabeçalho antes das estatísticas
            + stats
            + readme_content[end_index:]
        )
        # Voltar ao início do arquivo e escrever o conteúdo atualizado
        readme.seek(0)
        readme.write(updated_readme_content)
        readme.truncate()

# Adicione instruções de log para indicar o início da execução do script
print("Starting script execution...")

# Obter a chave da API do WakaTime do Secret do GitHub
api_key = os.getenv('WAKATIME_API_KEY')

# Obter as estatísticas do WakaTime
stats = get_wakatime_stats(api_key)

# Verifique se as estatísticas foram obtidas corretamente
if stats:
    # Adicione instruções de log para exibir as estatísticas obtidas do Wakatime
    print("Wakatime stats obtained successfully:")
    print(stats)

    # Formatar as estatísticas
    formatted_stats = format_stats(stats)

    # Atualizar o README.md com as estatísticas
    update_readme(formatted_stats)

    # Adicione uma instrução de log para indicar o final bem-sucedido da execução do script
    print("Script execution completed successfully!")
else:
    # Adicione uma instrução de log para indicar que houve um erro ao obter as estatísticas do Wakatime
    print("Failed to obtain Wakatime stats. Script execution failed!")
