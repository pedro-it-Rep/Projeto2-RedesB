 > :construction: Este é um projeto de Redes de Computadores, feito na linguagem Python, onde o objetivo é explorar o protocolo MQTT e seu funcionamento junto da api Kafka :construction:

# :stop_sign: Introdução

Em um planeta muiiiito muiiiiiiito distante, chamado Xastre Planet, os xastráqueos elevaram o nível de comunicação usando um sistema de comunicação que ficou bastante popular o XasUp APP.

Esse sistema é bastante simples, pois possibilita aos xastráqueos trocarem xassagens entre eles.

Ficou curiosos para saber como voce pode participar deste sistema de comunicação? 
Basta seguir os passos descritos neste documento e voce terá acesso.


# :warning: Pré Requisitos

Para rodar o XasUp APP é necessario ter instalado o broker mqtt Mosquitto, o ZooKeeper e a api Kafka, além da linguagem de programação python.

👨‍🦱 Poxa como faço para instalar esses recursos?

### :desktop_computer: Windows

<p> • Python </p>
  Primeiro verifique se já tem a linguagem de programação instalada, com o comando
  
    which python OU which python3
    
 Se o comando retornar um caminho para um diretorio então não é necessario fazer nada. Agora caso o comando tenha retornado "NO PYTHON IN", voce pode fazer o download pelo comando 
 
    sudo apt-get install python3
    
<p> • <a href= "https://mosquitto.org/download/"/> Mosquitto</a>: Basta fazer o download e seguir os passos indicados no site oficial do broker </p>
<p> • <a href= "https://zookeeper.apache.org/releases.html"/> ZooKeeper</a>: É possivel fazer o download no site oficial da API </p>
<p> • <a href= "https://kafka.apache.org/quickstart"/> Kafka</a>: É possivel fazer o download no site oficial da API </p>

<p> OBS: É possivel fazer o download apenas do Kafka, pois o ZooKeeper já esta incluso no pacote, porém durante o desenvolvimento alguns integrantes do grupo tiveram alguns problemas, sendo apenas solucionados ao baixar diretamente a API. </p>

### :desktop_computer: Ubuntu

• Python: Caso esteja utilizando um desktop Windows, não é necessario instalar o python.
<p> • <a href= "https://mosquitto.org/download/"/> Mosquitto</a> </p>
 <p> É necessario baixar o repositório: </p>
 
    sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
    
 <p> E depois obter a versão mais recente: </p>
 
    sudo apt-get update

    
<p> • <a href= "https://zookeeper.apache.org/releases.html"/> ZooKeeper</a>: É possivel fazer o download no site oficial da API </p>
<p> Após fazer o download é necessario descompactar o arquivo .tar. Isso pode ser feito com o seguinte comando: </p>

    tar -zxf zookeeper-3.4.6.tar.gz

• <a href= "https://kafka.apache.org/quickstart"/> Kafka</a>: É possivel fazer o download no site oficial da API

OBS: É possivel fazer o download apenas do Kafka, pois o ZooKeeper já esta incluso no pacote, porém durante o desenvolvimento alguns integrantes do grupo tiveram alguns problemas, sendo apenas solucionados ao baixar diretamente a API.

# :scroll: Instruções de Uso:

### :desktop_computer: Windows e Ubuntu

1.Baixe o código fonte do projeto usando o comando:

        
    git clone https://github.com/pedro-it-Rep/RedesB.git ou Apenas fazendo o download do arquivo de release
        
2.Descompacte o arquivo.

3.Vá para o repositório do projeto.

        
    cd Projeto2-RedesB

# :keyboard: Run Code:

### :desktop_computer: Windows e Ubuntu

Antes de iniciar o chat, é necessário iniciar o broker e a API do Kafka.

• Inicializando o Broker Mosquitto

Para inicializar com as configurações default, só rodar o comando:

    mosquitto -v

Para iniciar com alguma configuração personalizada, é necessario criar um arquivo mosquitto.conf.
Voce pode ver mais sobre isso no site: https://mosquitto.org/man/mosquitto-conf-5.html
 <p> Já tendo criado o arquivo, só rodar o comando </p>

    mosquitto -c mosquitto.conf
    
• Inicializando o ZooKeeper

Apenas rodar o comando

    bin/zkServer.sh start
    
• Inicializando o Kafka

Criar o topico no Kafka

    kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic geral

Depois apenas rodar o comando

    kafka-console-consumer.bat --boostrap-server localhost:9092 --topic geral --from-beginning

• Inicializando o cliente

Após iniciar todos os serviços necessário, precisamos apenas iniciar nosso cliente, rodando o seguinte comando em um terminal

    python KafkaCli.py

- E veja  a mágica acontecer

• Ficou com curiosidade do que se pode fazer com o nosso chat?
<p> Veja no video uma demostração do sistema funcionando: LINK DO VIDEO </p>

# Contribuidores
| Name | Git account |
|------|-------------|
| Pedro Ignácio Trevisan| [https://github.com/pedro-it-Rep] | 
| Fabricio Silva Cardoso| [https://github.com/Fabricio-Silva-Cardoso1]|
| Cesar Marrote Manzano| [https://github.com/cesarmmanzano]|
