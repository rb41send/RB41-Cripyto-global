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

    total_poder_de_hash = sum(c.poder_de_hash for c in carteiras)

    for c in carteiras:
        if c.endereco == carteira_mineradora:
            percentagem_contribuicao = c.poder_de_hash / total_poder_de_hash

            # Convert recompensa to float
            recompensa = float(recompensa)

            recompensa_minerador = recompensa * percentagem_contribuicao
            c.saldo += recompensa_minerador
            contador_blocos += 100  # Increment the counter of mined blocks
            print(f"Bloco Minerado {contador_blocos}: Recompensa {recompensa_minerador} {nome_da_moeda}")

# Função para simular o tempo de mineração de um minerador
def tempo_de_mineracao():


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


# Função para salvar carteiras e saldos em um arquivo JSON
def salvar_carteiras_e_saldos():


# Função para carregar carteiras e saldos de um arquivo JSON
def carregar_carteiras_e_saldos():
