import platform
import os
from tkinter import *
from tkinter import ttk
import psutil
import customtkinter
from time import sleep
import cpuinfo
from datetime import datetime
import threading


# Conversão em Bytes
def get_size(bytes, sufixo="B"):
    fator = 1024
    for unidade in ["", "K", "M", "G", "T", "P"]:
        if bytes < fator:
            return f"{bytes:.2f}{unidade}{sufixo}"
        bytes /= fator


# Customização da aparência da interface
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# Definição do tamanho da janela
largura = 800
altura = 500

janela = customtkinter.CTk()  # Criação da janela
janela.resizable(False, False)  # Define se é possível redimensionar a janela
janela.minsize(800, 500)  # Tamanho mínimo da janela
janela.maxsize(1200, 800)  # Tamanho máximo da janela
janela.title("Dashboard")  # Nome da janela

# Resolução do sistema
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
# Posição da janela
posx = largura_tela / 2 - largura / 2
posy = altura_tela / 2 - altura / 2
# Definição do tamanho e posição inicial da janela
janela.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))

# janela.iconbitmap("Imagens/dashboard.ico") # Ícone do aplicativo
# img = ImageTk.PhotoImage(Image.open("airplay.png"))
# myLabel = Label(image=img)
# myLabel.pack()
# myLabel.grid(column=0, row=0)

# Definição das fontes
fonte_titulo = customtkinter.CTkFont(size=30)
fonte_padrao = customtkinter.CTkFont(size=18)

# Variáveis das informações do Sistema
nome_sistema = platform.node()
sistema_operacional = platform.system()
versao_so = platform.version()
arquitetura_cpu = platform.machine()
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)

# Variáveis das informações da CPU
processador = cpuinfo.get_cpu_info()['brand_raw']
nucleos_fisicos = psutil.cpu_count(logical=False)
nucleos_logicos = psutil.cpu_count(logical=True)
freq_min_cpu = psutil.cpu_freq().min
freq_max_cpu = psutil.cpu_freq().max

# Variáveis da Memória RAM e da SWAP
ram_total = get_size(psutil.virtual_memory().total)
swap_total = get_size(psutil.swap_memory().total)

# Variáveis das informações do Disco Rígido
num_discos = len(psutil.disk_partitions())
nome_discos = []
armazenamento_total = []
armazenamento_disponivel = []
armazenamento_utilizado = []
armazenamento_usado_percentual = []
for i in range(num_discos):
    disco = psutil.disk_partitions()[i][1]
    nome_discos.append(psutil.disk_partitions()[i][0])
    armazenamento_total.append(get_size(psutil.disk_usage(disco).total))
    armazenamento_disponivel.append(get_size(psutil.disk_usage(disco).free))
    armazenamento_utilizado.append(get_size(psutil.disk_usage(disco).used))
    armazenamento_usado_percentual.append(psutil.disk_usage(disco).percent)

# Textos dos botões
texto_botao_sistema = "Mostrar informações gerais do Sistema"
texto_botao_cpu = "Mostrar informações da CPU"
texto_botao_ram = "Mostrar informações da Memória RAM"
texto_botao_hd = "Mostrar informações do Disco Rígido"
texto_botao_processos = "Mostrar Processos"
texto_botao_grafico_cpu = "Mostrar o Gráfico do Uso da CPU"
texto_botao_grafico_ram = "Mostrar o Gráfico do Uso da RAM"
texto_botao_terminal = "Abrir o Terminal de Comandos"

# Todos os textos que serão utilizados
texto0 = StringVar()
texto1 = StringVar()
texto2 = StringVar()
texto3 = StringVar()
texto4 = StringVar()
texto5 = StringVar()
texto6 = StringVar()
texto_botao0 = StringVar()
texto_botao1 = StringVar()
texto_botao2 = StringVar()
texto_botao3 = StringVar()
texto_botao4 = StringVar()
texto_botao5 = StringVar()
texto_botao6 = StringVar()

# Inicialização de flags
janela_atual = -1
janela_anterior = -1
encerrar = 0
flag_tabela = 0


# Informações gerais do Sistema
def infoSistema():
    global janela_atual
    global janela_anterior
    if janela_atual != 0:
        texto0.set("\nInformações Gerais do Sistema")
        texto1.set(f"Nome do Sistema: {nome_sistema}")
        texto2.set(f"Sistema Operacional: {sistema_operacional}")
        texto3.set(f"Versão do Sistema Operacional: {versao_so}")
        texto4.set(f"Arquitetura do Processador: {arquitetura_cpu}")
        texto5.set(
            f"Horário do Boot do Sistema: {bt.day}/{bt.month}/{bt.year} {bt.hour:02}:{bt.minute:02}:{bt.second:02}")
        texto6.set("")
        janela_atual = 0
        if janela_anterior == 1:
            percentual_cpu.configure(text="")
            percentual_por_cpu.configure(text="")
        elif janela_anterior == 2:
            percentual_uso_ram.configure(text="")
            percentual_disponivel_ram.configure(text="")
            percentual_disponivel_swap.configure(text="")
            percentual_uso_swap.configure(text="")


# Inicializa o texto sobre o uso da CPU
percentual_cpu = customtkinter.CTkLabel(janela, text=f"\rUso da CPU: {psutil.cpu_percent()}%", font=fonte_padrao)
percentual_por_cpu = customtkinter.CTkLabel(janela,
                                            text=f"Uso de cada núcleo da CPU: "
                                                 f"{psutil.cpu_percent(interval=1, percpu=True)}")


# Atualização do uso da CPU
def atualiza_cpu():
    while janela_atual == 1:
        percentual_cpu.configure(text=f"\rUso da CPU: {psutil.cpu_percent()}%")
        sleep(0.5)
        if encerrar == 1:
            break


# Atualização do uso por CPU
def atualiza_por_cpu():
    while janela_atual == 1:
        percentual_por_cpu.configure(
            text=f"Uso de cada núcleo da CPU: {psutil.cpu_percent(interval=0, percpu=True)}")
        sleep(0.5)
        if encerrar == 1:
            break


# Informações sobre a CPU
def infoCPU():
    t0 = threading.Thread(target=atualiza_cpu)
    t1 = threading.Thread(target=atualiza_por_cpu)
    global janela_atual
    global janela_anterior
    if janela_atual != 1:
        texto0.set("\nInformações do Processador")
        texto1.set(f"Processador: {processador}")
        texto2.set(f"Núcleos Físicos: {nucleos_fisicos}")
        texto3.set(f"Núcleos Lógicos: {nucleos_logicos}")
        texto4.set(f"Frequência mínima da CPU: {freq_min_cpu}")
        texto5.set(f"Frequência máxima da CPU: {freq_max_cpu}")
        texto6.set("")
        janela_atual = 1
        percentual_cpu.grid(column=0, row=7)
        t0.start()
        percentual_por_cpu.grid(column=0, row=8)
        t1.start()
        if janela_anterior == 2:
            percentual_uso_ram.configure(text="")
            percentual_disponivel_ram.configure(text="")
            percentual_disponivel_swap.configure(text="")
            percentual_uso_swap.configure(text="")


# Inicializa o texto sobre o uso da RAM
percentual_uso_ram = customtkinter.CTkLabel(janela,
                                            text=f"\rUso de RAM: {get_size(psutil.virtual_memory().used)} "
                                                 f"({psutil.virtual_memory().percent}%)",
                                            font=fonte_padrao)
percentual_disponivel_ram = customtkinter.CTkLabel(janela, text=f"\rUso de RAM: {psutil.virtual_memory().available}%",
                                                   font=fonte_padrao)


# Atualização do uso da RAM
def atualiza_uso_ram():
    while janela_atual == 2:
        percentual_uso_ram.configure(
            text=f"\rUso de RAM: {get_size(psutil.virtual_memory().used)} ({psutil.virtual_memory().percent}%)")
        sleep(0.1)
        if encerrar == 1:
            break


# Atualização da disponibilidade da RAM
def atualiza_disponivel_ram():
    while janela_atual == 2:
        percentual_disponivel_ram.configure(text=f"\rRAM disponível: {get_size(psutil.virtual_memory().available)}")
        sleep(0.1)
        if encerrar == 1:
            break


# Inicializa o texto sobre o uso da SWAP
percentual_uso_swap = customtkinter.CTkLabel(janela,
                                             text=f"\rUso de Memória SWAP: {get_size(psutil.swap_memory().used)} "
                                                  f"({psutil.swap_memory().percent}%)",
                                             font=fonte_padrao)
percentual_disponivel_swap = customtkinter.CTkLabel(janela,
                                                    text=f"\rMemória SWAP disponível: {psutil.swap_memory().free}",
                                                    font=fonte_padrao)


# Atualização do uso da SWAP
def atualiza_uso_swap():
    while janela_atual == 2:
        percentual_uso_swap.configure(
            text=f"\rUso de Memória SWAP: {get_size(psutil.swap_memory().used)} ({psutil.swap_memory().percent}%)")
        sleep(0.1)
        if encerrar == 1:
            break


# Atualização da disponibilidade da SWAP
def atualiza_disponivel_swap():
    while janela_atual == 2:
        percentual_disponivel_swap.configure(text=f"\rMemória SWAP disponível: {get_size(psutil.swap_memory().free)}")
        sleep(0.1)
        if encerrar == 1:
            break


# Informações sobre a Memória RAM e a SWAP
def infoRAM():
    t2 = threading.Thread(target=atualiza_uso_ram)
    t3 = threading.Thread(target=atualiza_disponivel_ram)
    t4 = threading.Thread(target=atualiza_uso_swap)
    t5 = threading.Thread(target=atualiza_disponivel_swap)
    global janela_atual
    global janela_anterior
    if janela_atual != 2:
        texto0.set("\nInformações de RAM e SWAP")
        texto1.set(f"Total de RAM: {ram_total}")
        texto2.set(f"Total de Memória SWAP: {swap_total}")
        texto3.set("")
        texto4.set("")
        texto5.set("")
        texto6.set("")
        janela_atual = 2
        info6 = customtkinter.CTkLabel(janela, textvariable=texto6)
        info6.grid(column=0, row=3)
        percentual_uso_ram.grid(column=0, row=7)
        t2.start()
        percentual_disponivel_ram.grid(column=0, row=8)
        t3.start()
        percentual_uso_swap.grid(column=0, row=9)
        t4.start()
        percentual_disponivel_swap.grid(column=0, row=10)
        t5.start()
        if janela_anterior == 1:
            percentual_cpu.configure(text="")
            percentual_por_cpu.configure(text="")


# Informações sobre o HD
def infoHD():
    global janela_atual
    global janela_anterior
    if janela_atual != 3:
        texto0.set("\nInformações do Disco Rígido")
        if num_discos > 1:
            texto1.set(f"Foram encontrados {num_discos} discos de armazenamento no sistema")
        else:
            texto1.set(f"Foi encontrado {num_discos} disco de armazenamento no sistema")
        texto2.set(f"Armazenamento total: {', '.join(nome_discos)} [{', '.join(armazenamento_total)}]")
        texto3.set(f"Armazenamento livre: {', '.join(nome_discos)} [{', '.join(armazenamento_disponivel)}]")
        texto4.set(
            f"Armazenamento utilizado: {', '.join(nome_discos)} [{', '.join(armazenamento_utilizado)}] "
            f"({armazenamento_usado_percentual}%)")
        texto5.set("")
        texto6.set("")
        janela_atual = 3
        if janela_anterior == 1:
            percentual_cpu.configure(text="")
            percentual_por_cpu.configure(text="")
        elif janela_anterior == 2:
            percentual_uso_ram.configure(text="")
            percentual_disponivel_ram.configure(text="")
            percentual_disponivel_swap.configure(text="")
            percentual_uso_swap.configure(text="")


def sort():
    rows = [(int(meus_processos.set(item, 'pid')), int(item)) for item in meus_processos.get_children('')]
    rows.sort()

    for index, (values, item) in enumerate(rows):
        meus_processos.move(str(item), '', index)
        if flag_tabela == 0:
            break


def atualiza_processos():
    global linha
    mudou = 0
    while flag_tabela == 1:
        for proc in psutil.process_iter(['username', 'name', 'pid']):
            if not meus_processos.exists(str(proc.pid)) and flag_tabela == 1:
                try:
                    meus_processos.insert(parent='', index='end', iid=str(proc.pid), text='',
                                          values=(proc.pid, proc.name(), proc.username()))
                except:
                    meus_processos.insert(parent='', index='end', iid=str(proc.pid), text='',
                                          values=(proc.pid, proc.name(), "SISTEMA"))
                linha = linha + 1
                mudou = 1
        for processo in meus_processos.get_children():
            if not psutil.pid_exists(int(processo)) and flag_tabela == 1:
                meus_processos.delete(processo)
                linha = linha - 1
                mudou = 1
        if mudou == 1 and flag_tabela == 1:
            sort()
            mudou = 0
        sleep(2)


# Informações sobre os Processos
def infoProcessos():
    global flag_tabela
    global janela_processos
    global meus_processos
    global tabela_processos
    if flag_tabela == 0:
        t6 = threading.Thread(target=atualiza_processos)
        janela_processos = customtkinter.CTkToplevel(janela)
        janela_processos.geometry("800x300")
        janela_processos.resizable(False, False)
        janela_processos.title("Processos")
        tabela_processos = Frame(janela_processos)
        tabela_processos.pack()

        tabela_scroll = Scrollbar(tabela_processos, orient='vertical')
        tabela_scroll.pack(side=RIGHT, fill=Y)

        # tabela_scroll = Scrollbar(tabela_processos, orient='horizontal')
        # tabela_scroll.pack(side=BOTTOM, fill=X)

        meus_processos = ttk.Treeview(tabela_processos, yscrollcommand=tabela_scroll.set,
                                      xscrollcommand=tabela_scroll.set)
        meus_processos.pack()

        tabela_scroll.config(command=meus_processos.yview)
        # tabela_scroll.config(command=meus_processos.xview)

        meus_processos['columns'] = ('pid', 'nome', 'usuário')

        meus_processos.column("#0", width=0, stretch=NO)
        meus_processos.column("pid", anchor=CENTER, width=200)
        meus_processos.column("nome", anchor=CENTER, width=200)
        meus_processos.column("usuário", anchor=CENTER, width=200)

        meus_processos.heading("#0", text="", anchor=CENTER)
        meus_processos.heading("pid", text="PID", anchor=CENTER)
        meus_processos.heading("nome", text="Nome", anchor=CENTER)
        meus_processos.heading("usuário", text="Usuário", anchor=CENTER)

        global linha
        linha = 0
        for proc in psutil.process_iter(['username', 'name', 'pid']):
            try:
                meus_processos.insert(parent='', index='end', iid=str(proc.pid), text='',
                                      values=(proc.pid, proc.name(), proc.username()))
            except:
                meus_processos.insert(parent='', index='end', iid=str(proc.pid), text='',
                                      values=(proc.pid, proc.name(), "SISTEMA"))
            linha = linha + 1
        meus_processos.pack()

        flag_tabela = 1
        t6.start()


        def fechar_janela_processos():
            global flag_tabela
            flag_tabela = 0
            tabela_processos.destroy()
            janela_processos.destroy()

        janela_processos.protocol("WM_DELETE_WINDOW", fechar_janela_processos)


# Inicialização das informações principais
infoSistema()
texto_botao0.set(texto_botao_sistema)
texto_botao1.set(texto_botao_cpu)
texto_botao2.set(texto_botao_ram)
texto_botao3.set(texto_botao_hd)
texto_botao4.set(texto_botao_processos)
texto_botao5.set(texto_botao_terminal)
texto_botao6.set(texto_botao_grafico_cpu)

info0 = customtkinter.CTkLabel(janela, textvariable=texto0, font=fonte_titulo)
info0.grid(column=0, row=0, ipadx=90, ipady=10)

info1 = customtkinter.CTkLabel(janela, textvariable=texto1, font=fonte_padrao)
info1.grid(column=0, row=1)

info2 = customtkinter.CTkLabel(janela, textvariable=texto2, font=fonte_padrao)
info2.grid(column=0, row=2)

info3 = customtkinter.CTkLabel(janela, textvariable=texto3, font=fonte_padrao)
info3.grid(column=0, row=3)

info4 = customtkinter.CTkLabel(janela, textvariable=texto4, font=fonte_padrao)
info4.grid(column=0, row=4)

info5 = customtkinter.CTkLabel(janela, textvariable=texto5, font=fonte_padrao)
info5.grid(column=0, row=5)


# Funções dos botões
def funcao_botao0():
    global janela_anterior
    global janela_atual
    janela_anterior = janela_atual
    infoSistema()


def funcao_botao1():
    global janela_anterior
    global janela_atual
    janela_anterior = janela_atual
    infoCPU()


def funcao_botao2():
    global janela_anterior
    global janela_atual
    janela_anterior = janela_atual
    infoRAM()


def funcao_botao3():
    global janela_anterior
    global janela_atual
    janela_anterior = janela_atual
    infoHD()


def funcao_botao4():
    infoProcessos()


def funcao_botao5():
    if sistema_operacional == "Windows":
        os.startfile('C:\WINDOWS\system32\cmd.exe')


# def funcao_botao6():
#     print("ABRIR GRAFICO")


# Inicialização dos botões
botao0 = customtkinter.CTkButton(janela, textvariable=texto_botao0, command=lambda: funcao_botao0())
botao0.place(relx=0.85, rely=0.15, anchor=CENTER)

botao1 = customtkinter.CTkButton(janela, textvariable=texto_botao1, command=lambda: funcao_botao1())
botao1.place(relx=0.85, rely=0.25, anchor=CENTER)

botao2 = customtkinter.CTkButton(janela, textvariable=texto_botao2, command=lambda: funcao_botao2())
botao2.place(relx=0.85, rely=0.35, anchor=CENTER)

botao3 = customtkinter.CTkButton(janela, textvariable=texto_botao3, command=lambda: funcao_botao3())
botao3.place(relx=0.85, rely=0.45, anchor=CENTER)

botao4 = customtkinter.CTkButton(janela, textvariable=texto_botao4, command=lambda: funcao_botao4())
botao4.place(relx=0.85, rely=0.55, anchor=CENTER)

botao5 = customtkinter.CTkButton(janela, textvariable=texto_botao5, command=lambda: funcao_botao5())
botao5.place(relx=0.85, rely=0.65, anchor=CENTER)


# botao6 = customtkinter.CTkButton(janela, textvariable=texto_botao6, command=lambda: funcao_botao6())
# botao6.place(relx=0.85, rely=0.75, anchor=CENTER)


# Finalização do programa/Fechar a janela
def fechar_janela():
    global encerrar
    global flag_tabela
    global tabela_processos
    encerrar = 1
    if flag_tabela == 1:
        flag_tabela = 0
        tabela_processos.destroy()
        janela_processos.destroy()
    botao0.destroy()
    botao1.destroy()
    botao2.destroy()
    botao3.destroy()
    botao4.destroy()
    botao5.destroy()
    # botao6.destroy()
    janela.destroy()


janela.protocol("WM_DELETE_WINDOW", fechar_janela)

janela.mainloop()
