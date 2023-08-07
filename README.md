# Projeto-Infracom

Projeto da disciplina de Infraestrutura de Comunicação, que consiste em um chat em grupo utilizando UDP.

## Como rodar

1. Certifique-se de ter o Python instalado em sua máquina.
2. Abra o terminal ou prompt de comando e navegue até a pasta src do projeto.
3. Execute o servidor UDP digitando o seguinte comando no terminal:

        python server.py

4. Em seguida, ainda na pasta src do projeto. Execute o cliente UDP digitando o seguinte comando no terminal:

        python client.py

## Funcionamento

O servidor roda em loop aguardando pacotes de até 1024 bytes enviados pelos clientes. Quando recebe um pacote do cliente, ele salva as informações na pasta "server" e, em seguida, envia esse arquivo de volta ao cliente. O cliente, por sua vez, salva o novo arquivo na pasta "client/receivedFiles".

Para escolher qual arquivo será enviado ao servidor, você pode editar a linha 9 do arquivo "src/client.py" e alterar o caminho para o arquivo desejado.