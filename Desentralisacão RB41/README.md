# RB41 - LEIA-ME

## Visão geral

RB41 é um projeto de criptomoeda descentralizado que enfatiza a comunicação ponto a ponto (P2P) para mineração e interação entre nós. Este README fornece uma visão geral da implementação da rede P2P no projeto RB41.

## Manipulação de conexão P2P

### Inicialização do nó

A rede RB41 utiliza um modelo de conexão P2P onde cada nó atua como cliente e servidor. Os principais componentes da configuração P2P incluem:

- `connected_clients`: Um dicionário para rastrear clientes conectados na rede.
- `server`: Representa o nó do servidor que gerencia conexões P2P.
- `first_client_addr`: Armazena as informações de endereço do primeiro cliente conectado.
- `data_from_server`: Container para dados recebidos do servidor Flask.

### Função de conexão P2P

A função `handle_p2p_connection` é crucial para gerenciar conexões P2P. Ele lida com conexões de clientes de entrada e gerencia a comunicação entre clientes e o servidor. A função segue estas etapas:

1. **Inicialização:**
    - Quando uma nova conexão P2P é estabelecida, a função imprime informações sobre a conexão.

2. **Configuração do servidor:**
    - Se for o primeiro cliente a se conectar, o servidor é inicializado e a conexão com o servidor Flask é estabelecida.

3. **Troca de dados:**
    - Os dados recebidos do servidor Flask são retransmitidos para clientes conectados.
    - Os dados recebidos dos clientes são retransmitidos para o servidor Flask.

4. **Tratamento de erros:**
    - A função inclui tratamento de erros para gerenciar problemas inesperados durante a comunicação P2P.

5. **Encerramento de conexão:**
    - Após a conclusão da comunicação ou se ocorrer um erro, a conexão é encerrada e as entradas relevantes são removidas.

## Uso

1. **Inicialização do nó:**
    - Antes de executar a conexão P2P, certifique-se de que as variáveis necessárias (`connected_clients`, `server`, `first_client_addr`, `data_from_server`) estejam configuradas corretamente.

2. **Manuseio de conexão P2P:**
    - Chame a função `handle_p2p_connection`, passando o soquete do cliente e o endereço do cliente como parâmetros.

3. **Interação Servidor-Cliente:**
    - Os clientes se comunicam entre si e com o servidor Flask através da conexão P2P.

4. **Gerenciamento de erros:**
    - A função inclui mecanismos para lidar com erros normalmente.

5. **Encerramento de conexão:**
    - As conexões são fechadas adequadamente após a conclusão da comunicação ou quando ocorrem erros.

## Notas

- A rede P2P RB41 foi projetada para facilitar a comunicação descentralizada entre os nós.
- Certifique-se de que as configurações de rede necessárias estejam em vigor para uma comunicação P2P bem-sucedida.

Sinta-se à vontade para explorar mais o projeto RB41 para obter uma compreensão mais profunda de sua arquitetura descentralizada e recursos de rede ponto a ponto.

## Contribuição

Se você encontrar problemas ou tiver sugestões, abra um problema. Contribuições são bem-vindas!

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).