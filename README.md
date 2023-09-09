# Projeto-Infracom

Projeto da disciplina de Infraestrutura de Comunicação, que consiste em um chat em grupo utilizando UDP.

## Como rodar

1. Certifique-se de ter o Python instalado em sua máquina.
2. Abra o terminal ou prompt de comando e navegue até a pasta src do projeto.

        cd src

3. Execute o servidor UDP digitando o seguinte comando no terminal:

        python3 server.py

4. Em seguida, ainda na pasta src do projeto, execute o cliente UDP e o arquivo escolhido para enviar que pode ser a imagem ou o texto, digitando o seguinte comando no terminal:

        para o txt: python3 client.py fileToSend.txt
        para o jpeg: python3 client.py imageToSend.jpeg

## Funcionamento

O servidor roda em loop aguardando pacotes de até 1024 bytes enviados pelos clientes. Quando recebe um pacote do cliente, ele salva as informações na pasta "server" e, em seguida, envia esse arquivo de volta ao cliente. O cliente, por sua vez, salva o novo arquivo na pasta "client/receivedFiles".

## Gerador de Perda de Pacotes

Foi assumido uma probabilidade fixa de 10% para o descarte de pacotes, simulando a perda real na rede.

## Fim de Comunicação

Além disso, situações onde o transmissor retransmite diversas vezes seguidas sem receber uma resposta do receptor ocasionarão no fim da comunicação, assume-se que todos os pacote foram transmitidos corretamente e o receptor fechou sua conexão.
