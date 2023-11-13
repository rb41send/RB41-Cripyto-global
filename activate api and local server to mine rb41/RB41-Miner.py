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
import sys
import tkinter as tk
import socket
import socket
import time

# Obtém o endereço IP do roteador
def obter_endereco_ip_do_roteador():
    try:
        # Conecta-se a um serviço externo para obter o endereço IP público
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        endereco_ip = s.getsockname()[0]
        s.close()
        return endereco_ip
    except Exception as e:
        print(f"Erro ao obter endereço IP do roteador: {e}")
        return None

# Constrói as URLs com o IP do roteador e a porta 2083
endereco_ip_roteador = obter_endereco_ip_do_roteador()
if endereco_ip_roteador:
    MINING_SERVER_URLS = [f'http://{endereco_ip_roteador}:2083/api']
    SEND_BALANCE_SERVER_URLS = [f'http://{endereco_ip_roteador}:2083/api/enviar_saldo']

    # Escolha uma URL aleatoriamente da lista de URLs de envio de saldo
    selected_balance_server_url = random.choice(SEND_BALANCE_SERVER_URLS)

    # Inicialize o iterator para as URLs de mineração
    url_iterator = itertools.cycle(MINING_SERVER_URLS)

    # Aguarde 15 segundos
    print("Aguarde... Coletando informações do Peer-to-peer.")
    for _ in range(15):
        time.sleep(1)
        print(".", end="", flush=True)  # Exibe uma barra de carregamento simples
    print("\n\nInformações do Peer-to-peer coletadas com sucesso:")
    print(f"Iniciado Peer-to-peer: {endereco_ip_roteador}")
    print(f"Porta: 2083")
else:
    print("Não foi possível obter o endereço IP do roteador.")
    
# Adicione o nome da moeda como uma variável global
nome_da_moeda = "RB41"




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
   


def mineracao_gpu(carteira_mineradora, last_proof, difficulty, gpu_limit=None):  # Adicione um argumento padrão para gpu_limit


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
    global contador_blocos  # Access the global variable contador_blocos

# Função para simular o tempo de mineração de um minerador
def tempo_de_mineracao():
    # Simule o tempo de mineração com valores aleatórios entre 300 e 600 segundos (5 a 10 minutos)
    return random.randint(300, 600)

def minerar(carteira):


# Função para enviar saldo de uma carteira para outra no servidor
def enviar_saldo(carteira_origem, carteira_destino, valor, send_balance_server_urls):
    senha_origem = input("Digite a senha da carteira de origem: ")
    dados = {
        'carteira_origem': carteira_origem,
        'carteira_destino': carteira_destino,
        'valor': valor,
        'senha_origem': senha_origem
    }


# Função para salvar carteiras e saldos em um arquivo JSON
def salvar_carteiras_e_saldos():



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
        
                # Definindo poder_de_hash como 1 para novas carteiras
                poder_de_hash = 1.0
        
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