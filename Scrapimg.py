import json
import os
import sys
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("API Ligada")

@sio.event
def disconnect():
    print("API Desligada")
    sys.exit()
    
script_dir = os.path.dirname(os.path.abspath(__file__))

dados_usuario_arquivo = os.path.join(script_dir, 'data_user.json')
def carregar_dados_usuario():
    if os.path.exists(dados_usuario_arquivo):
        with open(dados_usuario_arquivo, 'r') as file:
            return json.load(file)
    return None

def salvar_dados_usuario(cpf, senha):
    dados = {
        "cpf": cpf,
        "senha": senha
    }
    with open(dados_usuario_arquivo, 'w') as file:
        json.dump(dados, file)

script_dir = os.path.dirname(os.path.abspath(__file__))

json_files = {
    'Baccara_A': 'Baccara_A.json',
    'Baccara_Results': 'Results_Baccara_Evolution.json'
}

json_paths = {key: os.path.join(script_dir, f'{value}') for key, value in json_files.items()}

last_counts = {key: {} for key in json_files.keys()}

def save_data_to_json(key, data):
    try:
       
        try:
            with open(json_paths[key], 'r') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            existing_data = {}

        for item_key, value in data.items():
            if item_key in existing_data:
                if value['count'] != last_counts[key].get(item_key, None):
                    existing_data[item_key] = value
                    last_counts[key][item_key] = value['count']
            else:
                existing_data[item_key] = value
                last_counts[key][item_key] = value['count']

        with open(json_paths[key], 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

    except Exception as e:
        print(f"Erro ao salvar os dados para {key}: {e}")

@sio.on("Baccara_A")
def handle_bacaras(data):
    save_data_to_json('Baccara_A', data)

@sio.on("Baccara_Results")
def handle_bacaras1(data):
    save_data_to_json('Baccara_Results', data)

@sio.on("autenticacao_sucesso")
def handle_autenticacao_sucesso(data):
    try:
        token = data['token']
        print("Autenticação bem-sucedida! API On")
        sio.emit('connect_token', {'token': token})
    except KeyError:
        pass

@sio.on("autenticacao_falha")
def handle_autenticacao_falha(data):
    print("Falha na autenticação:", data['message'])

def autenticar(cpf, senha):
    sio.emit("autenticar", {"cpf": cpf, "senha": senha})

if __name__ == "__main__":
    try:
        dados_usuario = carregar_dados_usuario()
        if dados_usuario:
            cpf = dados_usuario['cpf']
            senha = dados_usuario['senha']
        else:
            cpf = input("Digite o CPF: ").lstrip('0') 
            senha = input("Digite a senha: ")
            salvar_dados_usuario(cpf, senha)

        sio.connect("wss://apiafobada.com.br")  
        autenticar(cpf, senha)  
        sio.wait() 
        
    except Exception as e:
        print(f"Erro ao conectar: {e}")
