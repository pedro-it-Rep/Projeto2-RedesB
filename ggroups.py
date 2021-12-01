from tkinter import Tk, Toplevel, Label, CENTER, Entry, Button, Text, Scrollbar,\
    DISABLED, END, NORMAL, LEFT, RIGHT, StringVar, BOTTOM

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
        self.login.resizable(width=True,
                             height=True)
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
        self.buttonPos = 0
        self.Window.mainloop()

    def goAhead(self, name):

        self.layout(name)

    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("XasUP APP")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=800,
                              height=500,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=0.7)
        self.buttonMsg1234 = Button(self.Window,
                                 text="Add Group",
                                 font="Helvetica 8 bold",
                                 width=20,
                                 bg="#ABB2B9",
                                    command=lambda : self.creategroup())

        self.buttonMsg1234.place(relx=0.7,
                              #rely=0.05,
                              relheight=0.1,
                              relwidth=0.1)

        self.buttonMsg12345 = Button(self.Window,
                                    text="Add Contato",
                                    font="Helvetica 8 bold",
                                    width=20,
                                    bg="#ABB2B9",
                                     command=lambda:self.personContact())

        self.buttonMsg12345.place(relx=0.8,
                                 #rely=0.05,
                                 relheight=0.1,
                                 relwidth=0.1)

        self.buttonMsg12346 = Button(self.Window,
                                    text="Bloquear",
                                    font="Helvetica 8 bold",
                                    width=20,
                                    bg="#ABB2B9")

        self.buttonMsg12346.place(relx=0.9,
                                 #rely=0.05,
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
                             font="Helvetica 14",
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
                                bg="#ABB2B9")

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


        self.buttonMsg1 = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9")

        self.buttonMsg1.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        # function to basically start the thread for sending messages

    def creategroup(self):
        groupname = StringVar()
        top = Toplevel(self.Window)
        label1 = Label(top, text="Insira nome do grupo")
        label1.pack(side=LEFT)
        entry = Entry(top, bd=5)
        entry.pack(side=LEFT)
        button = Button(top,text="Confirmar", command=lambda : groupname.set(entry.get()))
        button.pack(side=LEFT)
        button.wait_variable(groupname)
        print(groupname.get())
        top.destroy()
        self.createButtonGroup(groupname.get())

    def personContact(self):
        personname = StringVar()
        top = Toplevel(self.Window)
        label1 = Label(top, text="Insira nome do grupo")
        label1.pack(side=LEFT)
        entry = Entry(top, bd=5)
        entry.pack(side=LEFT)
        button = Button(top, text="Confirmar", command=lambda: personname.set(entry.get()))
        button.pack(side=LEFT)
        button.wait_variable(personname)
        print(personname.get())
        top.destroy()
        self.createPersonContact(personname.get())

    def createButtonGroup(self, groupname):
        self.buttonPos += 0.1
        self.buttonMsg12347 = Button(self.Window,
                                     text=groupname,
                                     font="Helvetica 8 bold",
                                     width=20,
                                     bg="#ABB2B9")

        self.buttonMsg12347.place(relx=0.7,
                                  rely= self.buttonPos,
                                  relheight=0.1,
                                  relwidth=0.3)

    def createPersonContact(self,nameperson):
        self.buttonPos += 0.1
        self.buttonMsg12347 = Button(self.Window,
                                     text=nameperson,
                                     font="Helvetica 8 bold",
                                     width=20,
                                     bg="#ABB2B9")

        self.buttonMsg12347.place(relx=0.7,
                                  rely=self.buttonPos,
                                  relheight=0.1,
                                  relwidth=0.3)


i = interface()


