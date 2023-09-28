# Projeto-Infracom

Projeto da disciplina de Infraestrutura de Comunicação, que consiste em um chat em grupo utilizando UDP.

## Como rodar

1. Certifique-se de ter o Python instalado em sua máquina.
2. Abra o terminal ou prompt de comando e navegue até a pasta src do projeto.

        cd src

3. Execute o servidor da sala de chat em grupo digitando o seguinte comando no terminal:

        python3 server.py

4. Em seguida, ainda na pasta src do projeto, execute o cliente UDP digitando o seguinte comando no terminal:

        python3 client.py
   
6. Para ter mais terminais de cliente que possam se comunicar entre si, execute mais instâncias do client.py
7. Nos terminais do cliente, a comunicação é feita através de comandos especiais, separados por ```/```. Os comandos disponíveis são:
   
| Comando  | Função |
| ------------- | ------------- |
| ```/hi <user_name>``` | Realiza o login com o nome de usuário inserido |
| ```/bye``` | Desconecta do servidor  |
| ```/list``` | Lista todos os usuários online no servidor no momento |
| ```/ml``` | Exibe a lista de amigos (online e offline) |
| ```/add <user_name>``` | Adiciona ```<user_name>``` na lista de amigos  |
| ```/rmv <user_name>``` | Remove ```<user_name>``` da lista de amigos |
| ```/ban <user_name>``` | Inicia uma votação para banir ```<user_name>``` |

## Funcionamento do Servidor

O servidor roda em loop aguardando pacotes enviados pelos clientes. Ao receber mensagens, ele processa a string para verificar se há algum comando e, caso haja, executa a função correspondente. Se não houver nenhum comando, a string é tratada como uma mensagem normal trocada entre usuários e faz broadcast delas para todos os outros usuários conectados.

## Funcionamento do cliente

As listas de amigos são guardadas no código de cada cliente e são, então, gerenciadas por eles. Os comandos ```/ml``` , ```/add``` e ```/rmv``` são primeiro interpretados do lado do cliente para realizar as ações na lista de amigos.
