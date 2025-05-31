import requests

def verificar_professor(professor_id):
    url = f'http://sistema-gerenciamento:5000/professores/{professor_id}'
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
