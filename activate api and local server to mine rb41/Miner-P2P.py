import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from cryptography.fernet import Fernet
from flask import Flask

# Chave de criptografia (gerada uma vez e compartilhada entre pares)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

app = Flask(__name__)

@app.route('/api')
def hello():
    return "Hello, Flask!"

def handle_client(client_socket, shutdown_event, server_ip, server_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as flask_socket:
            flask_socket.connect((server_ip, server_port))

            while not shutdown_event.is_set():
                data = client_socket.recv(1024)
                if not data:
                    break

                flask_socket.send(data)

                response = b""
                while True:
                    chunk = flask_socket.recv(1024)
                    if not chunk:
                        break
                    response += chunk

                client_socket.send(response)
    except Exception as e:
        print(f"Erro na comunicação: {e}")
    finally:
        client_socket.close()

def start_p2p_server(shutdown_event, server_ip, server_port):
    p2p_port = 2083
    server_p2p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_p2p.bind(('0.0.0.0', p2p_port))
    server_p2p.listen()

    print(f"P2P server on")

    max_threads = 5
    with ThreadPoolExecutor(max_threads) as executor:
        while not shutdown_event.is_set():
            client_socket, _ = server_p2p.accept()
            executor.submit(handle_client, client_socket, shutdown_event, server_ip, server_port)

def start_flask_server():
    try:
        app.run(host='0.0.0.0', port=2096, threaded=True)
    except Exception as e:
        print(f"Erro ao iniciar o servidor Flask: {e}")
        print(f"O endereço IP associado a '{dominio}' é: {target_ip}")

