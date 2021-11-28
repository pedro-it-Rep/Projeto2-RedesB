from tkinter import Tk, Toplevel, Label, CENTER, Entry, Button, Text, Scrollbar, DISABLED, END, NORMAL

from Client import *

client = ''
username = ''
topic = "geral"  # Topico onde os clientes irão se conectar
broker = "localhost"
port = 1883


class interface:

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
        self.login.configure(width=400,
                             height=300)
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
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        global textCons

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
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

        # function to basically start the thread for sending messages

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=on_publish())
        snd.start()

    def printMsg(self, msg):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg)

        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def on_message(self, client, userdata, message):
        flag = 0
        # Verifica se é uma mensagem para um grupo ou não
        # Divide a mensagem para tratar ela de forma correta
        msg = message.payload.decode("utf-8").split(
            ".")  # Necessario converter para utf-8, caso contrario a mensagem estará em binário
        # Verifica se é uma mensagem para um grupo ou não
        if str(msg[3]) == '0':
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
                    aux = "{}: {}\n\n".format(str(msg[1]), str(msg[2]))
                    interface.printMsg(self, aux)

            else:
                print("Msg n é para mim")
        else:
            for i in range(len(groups)):
                if msg[0] == groups[i]:
                    # print("{} -> {}: {}".format(str(msg[0]), str(msg[1]), str(msg[2])))
                    aux = "Grupo {}- > {}: {} \n\n".format(str(msg[0]), str(msg[1]), str(msg[2]))
                    interface.printMsg(self, aux)
                    flag = 1
                i += 1
            if flag == 0:
                for i in range(len(msg[3])):
                    if msg[3][i] == username:
                        print("Adicionado em um novo grupo -> {}".format(str(msg[0])))
                        groups.append(msg[0])
                        # print("Grupo {}- > {}: {}".format(str(msg[0]), str(msg[1]), str(msg[2])))
                        aux = "Grupo {}- > {}: {}\n\n".format(str(msg[0]), str(msg[1]), str(msg[2]))
                        interface.printMsg(self, aux)
                    else:
                        print("Nao estou no grupo")
                    i += 1


# Necessario alterar a logica para um melhor funcionamento no front end
def on_publish():
    flag = 0
    message = input("Digite MSG, Group ou Block: \n")
    # Verifica se a mensagem será enviada para um unico cliente ou para um grupo
    if message == "msg":
        dst = input("Para quem deseja mandar a mensagem? \n")
        message = input("Digite sua mensagem: \n")
        # Monta a estrutura da mensagem, onde irá conter [Destino, Source, Mensagem, Se é para um grupo ou não]
        msg = "{}.{}.{}.0".format(dst, username, message)
        client.publish(topic, msg)  # Publica a mensagem no topico desejado

    elif message == "group":
        grpName = input("Digite o nome do grupo: \n")
        for i in range(len(groups)):
            if grpName == groups[i]:
                message = input("Digite sua mensagem: \n")
                # Monta a estrutura da mensagem quando é um grupo -> [Destino, Source, Mensagem, Se é para um grupo ou não]
                msg = "{}.{}.{}.1".format(grpName, username, message)  # Destino será o nome do grupo
                flag = 1
                client.publish(topic, msg)
            i += 1
        if flag == 0:
            # Caso o nome do grupo não exista, é necessario criar o novo grupo
            groups.append(grpName)
            print("Para criar o grupo digite 'create' ")
            entry = input("Digite quem vc deseja add no grupo > \n")
            while entry != 'create':
                entry = input("Digite quem vc deseja add no grupo > \n")
                # Add people in group
                if entry != 'create':
                    grpUsers.append(entry)
            message = input("Digite sua mensagem: \n")
            msg = "{}.{}.{}.{}".format(grpName, username, message, grpUsers)  # Destino será o nome do grupo
            client.publish("geral", str(msg))

    elif message == "block":
        dst = input("Quem deseja bloquear? \n")
        block.append(dst)


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
