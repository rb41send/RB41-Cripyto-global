# Conet-P2P.exe no Ubuntu

Este repositório contém instruções para instalar e executar o Conet-P2P.exe no Ubuntu usando o Wine.

## Requisitos

- **Wine:** Certifique-se de ter o Wine instalado. Se não estiver, use estes comandos no terminal:

    ```bash
    sudo dpkg --add-architecture i386
    sudo apt-get update
    sudo apt-get install -y wine64 wine32
    ```

- **Acesso à Internet:** Garanta acesso à internet para baixar o [Conet-P2P.exe](https://github.com/rb41send/RB41-Cripyto-global/tree/main/blockchain/Conet-P2P.exe).

## Instalação

1. **Baixe o Conet-P2P.exe:**

    Faça o download [aqui](https://github.com/rb41send/RB41-Cripyto-global/tree/main/blockchain/Conet-P2P.exe) e salve-o em um diretório de sua escolha.

2. **Instale o Conet-P2P.exe com o Wine:**

    No terminal, vá ao diretório do arquivo e execute:

    ```bash
    wine Conet-P2P.exe
    ```

    Siga as instruções na tela para concluir a instalação.

3. **Inicie o Conet-P2P:**

    Após a instalação, inicie o Conet-P2P.exe com o comando:

    ```bash
    wine ~/.wine/drive_c/caminho/do/Conet-P2P.exe
    ```

    Substitua `caminho/do/Conet-P2P.exe` pelo caminho real onde o Conet-P2P.exe foi instalado.

## Notas Importantes

- Certifique-se de ter as permissões adequadas para executar o script de instalação e o Conet-P2P.exe.
- Este procedimento utiliza o Wine, um emulador de Windows, para executar programas .exe no Ubuntu.

## Problemas Conhecidos

- Se encontrar problemas, consulte a [documentação do Wine](https://www.winehq.org/documentation) ou os [fóruns de suporte](https://forum.winehq.org/).

## Contribuindo

Abra uma [issue](https://github.com/seu-usuario/seu-repositorio/issues) se encontrar problemas ou tiver sugestões.

**Divirta-se minerando com o Conet-P2P!**

Depois de tudo feito abra seu navegado com seu http://ip:2083