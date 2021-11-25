import paho.mqtt.client as paho
import time

# TODO
# COnfigurar MQTT
# Como manter o vetor de clientes onlines atualizado?
# Configurações do MQTT -> Podem facilitar algo?
# Iniciar front end

topic = "geral"  # Topico onde os clientes irão se conectar
username = ""


# Variaveis utilizadas
flag = 0          # Usada apenas para algumas verificações
msg = []          # [Destino, Source, Mensagem, isGroup]
message = ""      # Mensagem que deseja ser enviada
dst = []          # Destino da mensagem
grpName = ""      # Nome do grupo
block = []        # Lista de bloqueados
groups = []       # Lista de grupos que fui inserido
grpUsers = []     # Usado para adicionar pessoas nos grupos


# Colocar thread
def on_publish():
    #global entry, flag, grpName, groups, block, grpUsers, message, msg, username, dst, entry
    flag = 0
    message = input("Digite MSG ou Group: ")
    # Verifica se a mensagem será enviada para um unico cliente ou para um grupo
    if message == "msg":
        dst = input("Para quem deseja mandar a mensagem? ")
        message = input("Digite sua mensagem: ")
        # Monta a estrutura da mensagem, onde irá conter [Destino, Source, Mensagem, Se é para um grupo ou não]
        msg = "{}.{}.{}.0".format(dst, username, message)
        client.publish(topic, msg)  # Publica a mensagem no topico desejado

    elif message == "group":
        grpName = input("Digite o nome do grupo: ")
        for i in range(len(groups)):
            if grpName == groups[i]:
                message = input("Digite sua mensagem: ")
                # Monta a estrutura da mensagem quando é um grupo -> [Destino, Source, Mensagem, Se é para um grupo ou não]
                msg = "{}.{}.{}.1".format(grpName, username, message)  # Destino será o nome do grupo
                flag = 1
                client.publish(topic, msg)
            i += 1
        if flag == 0:
            # Caso o nome do grupo não exista, é necessario criar o novo grupo
            groups.append(grpName)
            print("Para criar o grupo digite 'create' ")
            while entry != 'create':
                entry = input("Digite quem vc deseja add no grupo > ")
                # Add people in group
                grpUsers.append(entry)
            message = input("Digite sua mensagem: ")
            msg = "{}.{}.{}.{}".format(grpName, username, message, grpUsers)  # Destino será o nome do grupo
            client.publish("geral", str(msg))


def on_message(client, userdata, message):
    #global flag, msg
    flag = 0
    # Verifica se é uma mensagem para um grupo ou não
    # Divide a mensagem para tratar ela de forma correta
    msg = message.payload.decode("utf-8").split(
        ".")  # Necessario converter para utf-8, caso contrario a mensagem estará em binário
    # Verifica se é uma mensagem para um grupo ou não
    if int(msg[3]) == 0:
        # Verifica se a mensagem é diretamente para meu username
        if str(msg[0]) == username:
            # Verifico se o usuario está bloqueado ou não
            for i in range(len(block)):
                # Caso esteja, não recebo a mensagem, apenas ignoro
                if block[i] == str(msg[1]):
                    print("Quem enviou esta na lista de bloqueados")
                    flag = 1
                i += 1
            if flag == 0:
                print("{}: {}".format(str(msg[1]), str(msg[2])))
        else:
            print("Msg n é para mim")
    else:
        for i in range(len(groups)):
            if msg[0] == groups[i]:
                print("{}- > {}: {}".format(str(msg[0]), str(msg[1]), str(msg[2].payload.decode("utf-8"))))
                flag = 1
            i += 1
        if flag == 0:
            for i in range(len(msg[3])):
                if msg[3][i] == username:
                    print("Adicionado em um novo grupo -> {}".format(str(msg[0])))
                    groups.append(msg[0])
                    print("{}- > {}: {}".format(str(msg[0]), str(msg[1]), str(msg[2].payload.decode("utf-8"))))
                else:
                    print("Nao estou no grupo")
                i += 1


def on_connect(client, userdata, message, rc):
    print("Connected - rc: ", rc)


def on_subscribe(client, userdata, mid, granted_qos):
    # Verificar envio de pacote para todos conectados
    # append quando alguem se conectar
    print("{} se conectou".format(username))


def on_unsubscribe():
    # Necessario alterar a lista de conectados
    print("{} se desconectou".format(username))


broker = "localhost"
port = 1883

username = input("Digite seu username: ")
client = paho.Client(username)
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)

client.loop_start()
client.subscribe(topic)
time.sleep(1)

while True:
    if message == "stop" or message == "Stop":
        break
    on_publish()
client.disconnect()
client.loop_stop()
