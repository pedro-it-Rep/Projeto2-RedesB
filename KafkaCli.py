import time
from tkinter import Tk, Toplevel, Label, CENTER, Entry, Button, Text, Scrollbar, \
    DISABLED, END, NORMAL, LEFT, RIGHT, StringVar, BOTTOM, IntVar
import paho.mqtt.client as paho
# import time
import threading

# Variaveis relacionadas ao MQTT
client = ''
username = ''
topic = "geral"  # Topico onde os clientes irão se conectar
broker = "localhost"
port = 1883

# Variaveis utilizadas
flag = 0  # Usada apenas para algumas verificações
msg = []  # [Destino, Source, Mensagem, isGroup]
message = ""  # Mensagem que deseja ser enviada
block = []  # Lista de bloqueados
grpName = ""  # Nome do grupo
groups = []  # Lista de grupos que fui inserido
etry = ""
msgToSend = 0
newMessages = []

LOGIN_WIDTH = 400
LOGIN_HEIGHT = 300

CHAT_WIDTH = 800
CHAT_HEIGHT = 500


class interface:
    dst = []  # Destino da mensagem
    msgToSend = 0

    def __init__(self):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=LOGIN_WIDTH,
                             height=LOGIN_HEIGHT)
        # create a Label
        self.pls = Label(self.login,
                         text="Por Favor Digite seu Nome",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Username: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        # set the focus of the cursor
        self.entryName.focus()

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="Login",
                         font="Helvetica 14",
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.55)
        self.buttonPos = 0
        self.listContacts = [] # Usado para adicionar pessoas nos grupos
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        global username
        global client
        username = name
        client = paho.Client(username)
        client.on_subscribe = on_subscribe
        client.on_unsubscribe = on_unsubscribe
        client.on_connect = on_connect
        client.on_message = self.on_message
        client.connect(broker, port)
        client.loop_start()
        client.subscribe(topic)

        self.layout(name)

    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("XasUP APP")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=CHAT_WIDTH,
                              height=CHAT_HEIGHT,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=0.7)
        self.buttonMsgAddGroup = Button(self.Window,
                                        text="Add Group",
                                        font="Helvetica 8 bold",
                                        width=20,
                                        bg="#ABB2B9",
                                        command=lambda: self.creategroup())

        self.buttonMsgAddGroup.place(relx=0.7,
                                     # rely=0.05,
                                     relheight=0.1,
                                     relwidth=0.1)

        self.buttonMsgAddContact = Button(self.Window,
                                          text="Add Contato",
                                          font="Helvetica 8 bold",
                                          width=20,
                                          bg="#ABB2B9",
                                          command=lambda: self.personContact())

        self.buttonMsgAddContact.place(relx=0.8,
                                       # rely=0.05,
                                       relheight=0.1,
                                       relwidth=0.1)

        self.buttonMsgBlockContat = Button(self.Window,
                                           text="Bloquear",
                                           font="Helvetica 8 bold",
                                           width=20,
                                           bg="#ABB2B9",
                                           command=lambda: self.getContact(self.dst, 2))

        self.buttonMsgBlockContat.place(relx=0.9,
                                        # rely=0.05,
                                        relheight=0.1,
                                        relwidth=0.1)

        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=0.7,
                        rely=0.07,
                        relheight=0.012)

        global textCons

        self.textCons = Text(self.Window,
                             width=10,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 10",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=0.7,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=0.7,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def creategroup(self):
        groupname = StringVar()
        top = Toplevel(self.Window)
        label1 = Label(top, text="Insira nome do grupo")
        label1.pack(side=LEFT)
        entry = Entry(top, bd=5)
        entry.pack(side=LEFT)
        button = Button(top, text="Confirmar",
                        command=lambda: groupname.set(entry.get()))
        button.pack(side=LEFT)
        button.wait_variable(groupname)
        print(groupname.get())
        top.destroy()
        self.addContactGroup()
        self.createButtonGroup(groupname.get())

    def addContactGroup(self):
        exit = IntVar()
        top = Toplevel(self.Window)
        label1 = Label(top, text="Digite um contato para inserir no grupo")
        label1.pack(side=LEFT)
        entry = Entry(top, bd=5)
        entry.pack(side=LEFT)
        button1 = Button(top, text="Adicionar",
                         command=lambda: self.checkContact(entry.get()))
        button1.pack(side=LEFT)

        button2 = Button(top, text="Sair",
                         command=lambda: exit.set(1))
        button2.pack(side=LEFT)
        button2.wait_variable(exit)
        top.destroy()

    def checkContact(self, contact):
        print(self.listContacts)
        if not self.listContacts:
            print("Criação de um grupo invalido! Crie um contato.")
        else:
            for i in self.listContacts:
                if contact == i:
                    print("Nome cadastrado")
                else:
                    print("Contato não existente")

    def personContact(self):
        personname = StringVar()
        top = Toplevel(self.Window)
        label1 = Label(top, text="Insira nome do contato")
        label1.pack(side=LEFT)
        entry = Entry(top, bd=5)
        entry.pack(side=LEFT)
        button = Button(top, text="Confirmar",
                        command=lambda: personname.set(entry.get()))
        button.pack(side=LEFT)
        button.wait_variable(personname)
        self.listContacts.append(personname.get())
        top.destroy()
        self.createPersonContact(personname.get())

    def createButtonGroup(self, groupname):
        self.buttonPos += 0.1
        self.buttonMsg12347 = Button(self.Window,
                                     text="Grupo " + groupname,
                                     font="Helvetica 8 bold",
                                     width=20,
                                     bg="#ABB2B9",
                                     command=lambda: self.getContact(groupname, 1))

        self.buttonMsg12347.place(relx=0.7,
                                  rely=self.buttonPos,
                                  relheight=0.1,
                                  relwidth=0.3)

    def createPersonContact(self, nameperson):
        self.buttonPos += 0.1
        self.buttonMsg12347 = Button(self.Window,
                                     text=nameperson,
                                     font="Helvetica 8 bold",
                                     width=20,
                                     bg="#ABB2B9",
                                     command=lambda: self.getContact(nameperson, 0))

        self.buttonMsg12347.place(relx=0.7,
                                  rely=self.buttonPos,
                                  relheight=0.1,
                                  relwidth=0.3)

    def getContact(self, nameperson, isGrp):
        flag = 0
        self.textCons.config(state=NORMAL)
        self.textCons.delete(1.0, END)
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

        if newMessages:
            x = 0
            for i in range(len(newMessages)):
                if nameperson == newMessages[i][0]:
                    auxMsg = "{}: {}\n".format(newMessages[i][0], newMessages[i][1])
                    self.printMsg(auxMsg)
                    x += 1

            self.buttonMsg12347.configure(text=f'{nameperson}')
            for i in range(x):
                newMessages.pop(0)

        if isGrp == 0:
            self.dst = nameperson
            self.msgToSend = 0
            print("is person")
        elif isGrp == 1:
            self.dst = nameperson
            self.msgToSend = 1
            print("is group")
        elif isGrp == 2:
            for i in range(len(block)):
                if self.dst == block[i]:
                    block.remove(self.dst)
                    flag = 1
            if flag == 0:
                block.append(nameperson)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.on_publish())
        snd.start()

    def printMsg(self, msg):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg)

        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def on_message(self, client, userdata, message):
        flag = 0
        aux = 0
        # Verifica se é uma mensagem para um grupo ou não
        # Divide a mensagem para tratar ela de forma correta
        msg = message.payload.decode("utf-8").split(
            ".")  # Necessario converter para utf-8, caso contrario a mensagem estará em binário
        # Verifica se é uma mensagem para um grupo ou não
        if str(msg[1]) != username:
            if str(msg[3]) == '0':
                # Verifica se a mensagem é diretamente para meu username
                if str(msg[0]) == username:
                    # Verifico se o usuario está bloqueado ou não
                    for i in range(len(block)):
                        # Caso esteja, não recebo a mensagem, apenas ignoro
                        if block[i] == str(msg[1]):
                            print("Quem enviou esta na lista de bloqueados")
                            flag = 1
                            break
                        i += 1
                    if flag == 0:
                        if self.dst != str(msg[1]):  # Se mensagem != destino selecionado -> Envia apenas recebida
                            for i in range(len(newMessages)):
                                if str(msg[1]) == newMessages[i][0]:
                                    aux += 1
                            newMessages.append([str(msg[1]), str(msg[2]), aux])
                            self.buttonMsg12347.configure(text=f'{str(msg[1])} \t {aux+1}')
                            # Usar um vetor com as mensagens recebidas -> Manda um lida e tira as mensagens do vetor
                        else:
                            aux = "{}: {}\n".format(str(msg[1]), str(msg[2]))
                            interface.printMsg(self, aux)

                else:
                    print("Msg n é para mim")
            else:
                for i in range(len(groups)):
                    if str(msg[0]) == groups[i]:
                        aux = "Grupo {}- > {}: {} \n\n".format(
                            str(msg[0]), str(msg[1]), str(msg[2]))
                        interface.printMsg(self, aux)
                        flag = 1
                    i += 1
                if flag == 0:
                    x = []
                    aux = ""
                    # Recebemos do MQTT o vetor como string, é necessario repassar para vetor novamente
                    for i in msg[3]:
                        # Indicativos de string
                        if i == '[' or i == "'" or i == " ":
                            pass
                        else:
                            # Final do "vetor" e de um novo nome, então podemos adicionar ao novo vetor auxiliar
                            if i == "," or i == "]":
                                x.append(aux)
                                aux = ""
                            else:
                                aux += i
                                print(aux)
                    print(x)
                    for i in x:
                        if i == username:
                            groups.append(str(msg[0]))
                            aux = "Adicionado em um novo grupo -> {} \n".format(str(msg[0]))
                            interface.printMsg(self, aux)
                            self.createButtonGroup(str(msg[0]))

                        else:
                            print("Nao estou no grupo")

    # Necessario alterar a logica para um melhor funcionamento no front end

    def on_publish(self):
        flag = 0
        # Verifica se a mensagem será enviada para um unico cliente ou para um grupo
        # Flag para verificar se é grupo ou não
        if self.msgToSend == 0:
            message = self.msg
            # Monta a estrutura da mensagem, onde irá conter [Destino, Source, Mensagem, Se é para um grupo ou não]
            aux = "You: {} \n".format(message)
            interface.printMsg(self, aux)
            msg = "{}.{}.{}.0".format(self.dst, username, message)
            client.publish(topic, msg)  # Publica a mensagem no topico desejado
            aux = str(time.strftime("Mensagem Recebida: " + '%B %d, %Y' + ' at ' + '%I:%M %p \n'))
            interface.printMsg(self, aux)
            aux = str(time.strftime("Mensagem Lida: " + '%B %d, %Y' + ' at ' + '%I:%M %p \n'))
            interface.printMsg(self, aux)

        elif self.msgToSend == 1:
            grpName = self.dst  # Nome do grupo que está selecionado
            for i in range(len(groups)):
                if grpName == groups[i]:
                    message = self.msg
                    # Monta a estrutura da mensagem quando é um grupo -> [Destino, Source, Mensagem, Se é para um grupo ou não]
                    aux = "You: {} \n".format(message)
                    interface.printMsg(self, aux)
                    # Destino será o nome do grupo
                    msg = "{}.{}.{}.1".format(grpName, username, message)
                    flag = 1
                    client.publish(topic, msg)
                i += 1
            if flag == 0:
                # Caso o nome do grupo não exista, é necessario criar o novo grupo
                groups.append(grpName)
                message = self.msg
                aux = "You: {} \n".format(message)
                interface.printMsg(self, aux)
                # Destino será o nome do grupo
                msg = "{}.{}.{}.{}".format(
                    grpName, username, message, self.listContacts)
                client.publish("geral", str(msg))


def on_connect(client, userdata, message, rc):
    print("Connected - rc: ", rc)


def on_subscribe(client, userdata, mid, granted_qos):
    # Verificar envio de pacote para todos conectados
    # append quando alguem se conectar
    print("{} se conectou".format(username))


def on_unsubscribe():
    # Necessario alterar a lista de conectados
    print("{} se desconectou".format(username))


i = interface()
