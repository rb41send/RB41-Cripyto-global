import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
import nmap

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

def search_for_peer():
    nm = nmap.PortScanner()

    # Intervalo de endereços IP para varredura
    ip_range = '0.0.0.0'  # Exemplo: altere conforme necessário para o seu ambiente de rede

    # Porta para verificar a disponibilidade
    target_port = 2096

    nm.scan(hosts=ip_range, arguments=f'-p {target_port}')

    for host in nm.all_hosts():
        if nm[host]['tcp'][target_port]['state'] == 'open':
            print(f'Par encontrado em {host}:{target_port}')

if __name__ == "__main__":
    search_for_peer()

