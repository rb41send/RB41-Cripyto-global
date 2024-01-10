| Passo 1: Registro no No-IP |
|----------------------------------------------------------------------------------------------------------------------|
| 1. Acesse o site do No-IP em [No-IP](https://www.noip.com/). |
| 2. Crie uma conta ou faça login se já tiver uma. |
| 3. Após fazer o login, navegue até a seção “DNS Dinâmico” e clique em “Adicionar um Host”. |
| 4. Escolha um nome de host (que será usado para acessar seu computador remotamente) e selecione o domínio desejado |
|    (por exemplo, no-ip.org). |
| 5. Selecione o horário de renovação do seu nome de host (intervalo em que seu IP será atualizado automaticamente). |
| 6. Clique em "Adicionar Host" para salvar as configurações. |

| Etapa 2: Baixe e instale o software No-IP |
|----------------------------------------------------------------------------------------------------------------------|
| 1. Baixe o cliente No-IP DUC (Dynamic Update Client) em [Download No-IP](https://www.noip.com/download). |
| 2. Instale o software seguindo as instruções na tela. |
| 3. Durante a instalação, faça login com sua conta No-IP. |
| 4. Escolha os hosts que deseja associar ao seu IP dinâmico. |

| Etapa 3: Configuração do roteador (encaminhamento de porta) |
|----------------------------------------------------------------------------------------------------------------------|
| Para acessar seu computador remotamente, configure o encaminhamento de porta em seu roteador. Os detalhes exatos variam de |
| acordo com o modelo de roteador, mas geralmente envolvem: |
| 1. Acesse as configurações do seu roteador através de um navegador digitando o endereço IP do roteador (consulte o |
|    manual para obter informações sobre o endereço IP padrão). |
| 2. Localize a seção encaminhamento de porta ou "Encaminhamento de porta". |
| 3. Adicione uma regra para encaminhar conexões na porta desejada (por exemplo, porta 80 para acesso HTTP) ao seu |
|    endereço IP local do computador. |

| Etapa 4: Verificação |
|----------------------------------------------------------------------------------------------------------------------|
| 1. Abra o software No-IP DUC em seu computador. |
| 2. O DUC detectará automaticamente seu IP público e atualizará o host no No-IP com esse IP. |
| 3. Acesse seu computador remotamente usando o nome de host configurado no No-IP. |
