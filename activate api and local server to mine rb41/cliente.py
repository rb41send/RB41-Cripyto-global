import random
import time
import psutil
import GPUtil
import pynvml
import threading
import requests
import itertools
import atexit
import os
import json
from cryptography.fernet import Fernet
import sys
import tkinter as tk

# Lista de URLs do servidor de mineração
MINING_SERVER_URLS = [
    'http://seuip:2083/api',
    # Adicione mais URLs conforme necessário
]

# Lista de URLs do servidor de envio de saldo (URLs dinâmicas)
SEND_BALANCE_SERVER_URLS = [
    'http://seuip:2083/api/enviar_saldo',
    # Adicione mais URLs conforme necessário
]

# Escolha uma URL aleatoriamente da lista de URLs de envio de saldo
selected_balance_server_url = random.choice(SEND_BALANCE_SERVER_URLS)

# Inicialize o iterator para as URLs de mineração
url_iterator = itertools.cycle(MINING_SERVER_URLS)

# Adicione o nome da moeda como uma variável global
nome_da_moeda = "RB41"

# Estrutura de dados para representar as carteiras dos mineradores
class Carteira:
    def __init__(self, endereco, saldo=0.0, poder_de_hash=1, senha=None):
        self.endereco = endereco
        self.saldo = saldo
        self.poder_de_hash = poder_de_hash
        self.senha = senha  # Adicionar uma senha à classe Carteira

# Lista de carteiras dos mineradores
carteiras = []

# Variável para contar os blocos minerados
contador_blocos = 0

# Função para criar uma nova carteira no servidor
def criar_carteira():
    senha = input("Digite a senha para a nova carteira: ")
    response = requests.post(next(url_iterator) + '/criar_carteira', json={'senha': senha}, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data["endereco"]
    else:
        return None

# Função para verificar o saldo de uma carteira
def verificar_saldo(carteira):
    response = requests.get(next(url_iterator) + '/verificar_saldo', params={'carteira': carteira})
    if response.status_code == 200:
        data = response.json()
        return data["saldo"]
    elif response.status_code == 404:
        print("A carteira não existe.")
        return None
    else:
        print("Erro ao verificar saldo.")
        return None

# Função para verificar o uso de memória da GPU
def verificar_uso_memoria_gpu():
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Use o primeiro dispositivo GPU
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    return (info.used / info.total) * 100

# Função para realizar a mineração de CPU
def mineracao_cpu(carteira_mineradora, last_proof, difficulty, cpu_limit):
    try:
        while True:
            print(f"Minerando com carteira (CPU): {carteira_mineradora}, last_proof: {last_proof}, difficulty: {difficulty}")

            # Defina o uso da CPU com base no limite definido pelo cliente
            cpu_percent = cpu_limit

            # Verifique o uso atual da CPU e ajuste para o limite da CPU
            cpu_current_percent = psutil.cpu_percent(interval=None)
            if cpu_current_percent > cpu_limit:
                cpu_percent = cpu_limit

            # Defina o uso da CPU
            psutil.cpu_percent(interval=None)

            # Fazer uma solicitação ao servidor para mineração
            response = requests.post(next(url_iterator) + '/minerar', json={
                'carteira': carteira_mineradora,
                'last_proof': last_proof,
                'difficulty': difficulty
            })

            if response.status_code == 200:
                data = response.json()
                recompensa = data.get("recompensa")
                bloco_minerado = data.get("bloco_minerado")

                if recompensa is not None:
                    if bloco_minerado is not None:
                        print(f"Mineração (CPU) concluída! Recompensa recebida em {nome_da_moeda}: {recompensa}")
                        print(f"Bloco minerado: {bloco_minerado}")

                        # Distribua a recompensa com base na potência de hash do minerador
                        distribuir_recompensa(carteira_mineradora, recompensa)
                    else:
                        print(f"Mineração (CPU) concluída! Recompensa recebida em {nome_da_moeda}: {recompensa}, mas nenhum bloco foi minerado.")
                else:
                    print("Erro ao iniciar a mineração (CPU).")
            else:
                print("Erro na solicitação de mineração (CPU)")

            # Aguarde um período de tempo (por exemplo, 60 segundos) antes de fazer a próxima solicitação
            time.sleep(60)  # Isso fará com que haja um atraso de 60 segundos entre as solicitações
    except Exception as e:
        print("Erro durante a mineração CPU:", str(e))
        time.sleep(15)  # Atraso de 60 segundos em caso de erro


def mineracao_gpu(carteira_mineradora, last_proof, difficulty, gpu_limit=None):  # Adicione um argumento padrão para gpu_limit
    while True:
        print(f"Minerando com carteira (GPU): {carteira_mineradora}, last_proof: {last_proof}, difficulty: {difficulty}")

        # Defina o uso da GPU com base no limite definido pelo cliente, ou 100% se gpu_limit for None
        if gpu_limit is None:
            gpu_percent = 100
        else:
            gpu_percent = gpu_limit

        # Verifique o uso atual da GPU e ajuste para o limite da GPU
        gpu_current_percent = GPUtil.getGPUs()[0].load * 100
        if gpu_current_percent > gpu_percent:
            gpu_percent = gpu_limit

        # Defina o uso da GPU
        GPUtil.showUtilization()

        # Fazer uma solicitação ao servidor para mineração
        response = requests.post(next(url_iterator) + '/minerar', json={
            'carteira': carteira_mineradora,
            'last_proof': last_proof,
            'difficulty': difficulty
        })

        if response.status_code == 200:
            data = response.json()
            recompensa = data.get("recompensa")
            bloco_minerado = data.get("bloco_minerado")

            if recompensa is not None:
                if bloco_minerado is not None:
                    print(f"Mineração (GPU) concluída! Recompensa recebida em {nome_da_moeda}: {recompensa}")
                    print(f"Bloco minerado: {bloco_minerado}")

                    # Distribua a recompensa com base na potência de hash do minerador
                    distribuir_recompensa(carteira_mineradora, recompensa)
                else:
                    print(f"Mineração (GPU) concluída! Recompensa recebida em {nome_da_moeda}: {recompensa}, mas nenhum bloco foi minerado.")
            else:
                print("Erro ao iniciar a mineração (GPU).")
        else:
            print("Erro na solicitação de mineração (GPU)")

        # Aguarde um período de tempo (por exemplo, 60 segundos) antes de fazer a próxima solicitação
        time.sleep(15)  # Isso fará com que haja um atraso de 60 segundos entre as solicitações

def registrar_cliente():
    senha = input("Digite a senha para a nova carteira: ")
    potencia_de_mineracao = float(input("Digite a potência de mineração (maior poder de mineração, maior recompensa): "))
    response = requests.post(next(url_iterator) + '/criar_carteira', json={'senha': senha, 'potencia_de_mineracao': potencia_de_mineracao})
    if response.status_code == 200:
        data = response.json()
        return data["endereco"]
    else:
        return None

# Função para distribuir a recompensa com base na potência de hash
def distribuir_recompensa(carteira_mineradora, recompensa):
    global contador_blocos  # Acessar a variável global contador_blocos

    total_poder_de_hash = sum(c.poder_de_hash for c in carteiras)

    for c in carteiras:
        if c.endereco == carteira_mineradora:
            percentagem_contribuicao = c.poder_de_hash / total_poder_de_hash
            recompensa_minerador = recompensa * percentagem_contribuicao
            c.saldo += recompensa_minerador
            contador_blocos += 100  # Incrementar o contador de blocos minerados
            print(f"Bloco Minerado {contador_blocos}: Recompensa {recompensa_minerador} {nome_da_moeda}")

# Função para simular o tempo de mineração de um minerador
def tempo_de_mineracao():
    # Simule o tempo de mineração com valores aleatórios entre 300 e 600 segundos (5 a 10 minutos)
    return random.randint(300, 600)

def minerar(carteira):
    # Simule a mineração aqui (pode envolver cálculos complexos)
    tempo = tempo_de_mineracao()  # Tempo de mineração simulado
    recompensa_base = 100.00 # Defina a recompensa base que o minerador receberá

    for c in carteiras:
        if c.endereco == carteira:
            # Calcule a recompensa com base no tempo de mineração em relação ao minerador mais rápido
            percentagem_recompensa = (tempo / tempo_de_mineracao())  # Calcula a porcentagem com base no tempo
            recompensa = recompensa_base * percentagem_recompensa
            c.saldo += recompensa
            return recompensa, f"Bloco Minerado em {tempo} segundos"  # Retorna ambos os valores

    return 0.0, None  # Retorna 0.0 para recompensa e None para bloco_minerado se a carteira não for encontrada

# Função para enviar saldo de uma carteira para outra no servidor
def enviar_saldo(carteira_origem, carteira_destino, valor, send_balance_server_urls):
    senha_origem = input("Digite a senha da carteira de origem: ")
    dados = {
        'carteira_origem': carteira_origem,
        'carteira_destino': carteira_destino,
        'valor': valor,
        'senha_origem': senha_origem
    }
    
    # Escolha uma URL aleatoriamente da lista de URLs de envio de saldo
    selected_balance_server_url = random.choice(send_balance_server_urls)

    response = requests.post(selected_balance_server_url, json=dados)
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("Saldo enviado com sucesso.")
        except json.decoder.JSONDecodeError:
            print("Erro: Resposta do servidor não contém dados JSON válidos.")
    else:
        print("Erro ao enviar saldo. Código de status:", response.status_code)

# Função para salvar carteiras e saldos em um arquivo JSON
def salvar_carteiras_e_saldos():
    data = {
        "carteiras": [{"endereco": c.endereco, "saldo": c.saldo, "poder_de_hash": c.poder_de_hash, "senha": c.senha} for c in carteiras],
        "contador_blocos": contador_blocos
    }

    with open("carteiras_saldos.json", "w") as json_file:
        json.dump(data, json_file)

# Função para carregar carteiras e saldos de um arquivo JSON
def carregar_carteiras_e_saldos():
    global carteiras, contador_blocos

    if os.path.exists("carteiras_saldos.json"):
        with open("carteiras_saldos.json", "r") as json_file:
            data = json.load(json_file)
            carteiras_data = data.get("carteiras", [])
            contador_blocos = data.get("contador_blocos", 0)

            carteiras = [Carteira(c["endereco"], c["saldo"], c["poder_de_hash"], c["senha"]) for c in carteiras_data]

# Carregar carteiras e saldos do arquivo JSON, se existir
carregar_carteiras_e_saldos()

if __name__ == "__main__":
    carteira_mineradora = None  # Inicialmente, não há carteira mineradora

    while True:
        print("Escolha uma opção:")
        print("1. Criar uma nova carteira")
        print("2. Verificar saldo de carteira")
        print("3. Iniciar Mineração Contínua")
        print("4. Enviar saldo para outra carteira")
        print("5. Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            endereco = criar_carteira()
            if endereco:
                print(f"Sua nova carteira foi criada com o endereço: {endereco}")
                poder_de_hash = float(input("Digite o poder de hash da carteira (maior poder de hash, maior recompensa): "))
                senha = input("Digite a senha da carteira: ")
                carteiras.append(Carteira(endereco, 0.0, poder_de_hash, senha))
                salvar_carteiras_e_saldos()
            else:
                print("Erro ao criar a carteira.")
        elif opcao == "2":
            carteira = input("Digite o endereço da carteira que deseja verificar: ")
            saldo = verificar_saldo(carteira)
            if saldo is not None:
                print(f"Saldo da carteira {carteira}: {saldo}")
            else:
                print("Carteira não encontrada ou senha incorreta.")
        elif opcao == "3":
            if carteira_mineradora:
                print(f"Mineração contínua já está ativa com a carteira {carteira_mineradora}...")
            else:
                carteira_mineradora = input("Digite o endereço da carteira para iniciar a mineração contínua: ")
                last_proof = 0  # Inicialize com um valor adequado
                difficulty = 4  # Defina a dificuldade desejada
                cpu_limit = float(input("Digite o limite de uso da CPU (0-100%): "))
                gpu_limit = float(input("Digite o limite de uso da GPU (0-100%): "))

                # Crie threads separadas para a mineração de CPU e GPU
                thread_cpu = threading.Thread(target=mineracao_cpu, args=(carteira_mineradora, last_proof, difficulty, cpu_limit))
                thread_gpu = threading.Thread(target=mineracao_gpu, args=(carteira_mineradora, last_proof, difficulty, gpu_limit))

                # Inicie as threads
                thread_cpu.start()
                thread_gpu.start()

                # Aguarde até que ambas as threads terminem (isso não acontecerá neste exemplo, pois são loops infinitos)
                # thread_cpu.join()
                # thread_gpu.join()
        elif opcao == "4":
            carteira_origem = input("Digite o endereço da carteira de origem: ")
            carteira_destino = input("Digite o endereço da carteira de destino: ")
            valor = float(input("Digite o valor a ser enviado: "))
            enviar_saldo(carteira_origem, carteira_destino, valor, SEND_BALANCE_SERVER_URLS)
            salvar_carteiras_e_saldos()

            for c in carteiras:
                if c.endereco == carteira_origem:
                    senha_origem = input("Digite a senha da carteira de origem: ")
                    if senha_origem == c.senha:
                        enviar_saldo(carteira_origem, carteira_destino, valor)
                        salvar_carteiras_e_saldos()
                    else:
                        print("Senha incorreta. Operação cancelada.")
                    break
            else:
                print("Carteira de origem não encontrada.")
        elif opcao == "5":
            sys.exit(0)
