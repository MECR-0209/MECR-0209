import os
import requests

# Função para obter as estatísticas do WakaTime
def get_wakatime_stats(api_key):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get('https://wakatime.com/api/v1/users/current/stats/last_7_days', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
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
    with open('README.md', 'a') as readme:
        readme.write('\n\n## Wakatime Stats\n\n')
        readme.write(stats)

# Obter a chave da API do WakaTime do Secret do GitHub
api_key = os.getenv('WAKATIME_API_KEY')

# Obter as estatísticas do WakaTime
stats = get_wakatime_stats(api_key)

# Formatar as estatísticas
formatted_stats = format_stats(stats)

# Atualizar o README.md com as estatísticas
update_readme(formatted_stats)
