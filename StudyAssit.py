import json
import os
import tkinter as tk

from tkinter import messagebox


ARQUIVO = "dados.json"

materias = {}

def carregar_dados():
    global materias
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO,"r",encoding="utf-8") as f:
            materias = json.load(f)
    else:
        materias = {}

def salvar_dados():
    with open(ARQUIVO,"w", encoding="utf-8") as f:
        json.dump(materias,f,indent=2,ensure_ascii=False) 

#INTERFACE ADICIONAR MATERIA 
def interface_salvar_mat():
    nova_janela = tk.Toplevel(janela)
    nova_janela.title("Adicionar Matéria")
    nova_janela.geometry("300x150")
    tk.Label(nova_janela,text="Nome da Matéria: ").pack(pady=5)
    
    entrada = tk.Entry(nova_janela, width= 30)
    entrada.pack(pady=5)

    def salvar_mat():
        nomeMat = entrada.get().strip()
        if not nomeMat:
            messagebox.showinfo("Aviso","Materia já existe")
        else:
            materias[nomeMat]= []
            salvar_dados()
            messagebox.showinfo("Sucesso",f"Materia {nomeMat} adicionada com sucesso")
            entrada.delete(0,tk.END)
    tk.Button(nova_janela, text="Adicionar",command=salvar_mat).pack(padx=10)


def interface_adicionar_taf():
    if not materias:
       messagebox.showwarning("Aviso","Você não possui matérias cadastradas")
       return
    
    nova_janela = tk.Toplevel(janela)
    nova_janela.title("Adicionar Tarefas")
    nova_janela.geometry("350x200")

    tk.Label(nova_janela,text="Escolha a matéria").pack(pady=5)

    materia_var =  tk.StringVar()
    materia_var.set(list(materias.keys())[0])

    menu_materias = tk.OptionMenu(nova_janela,materia_var,*materias.keys())
    menu_materias.pack(pady=5)

    tk.Label(nova_janela,text="Digite o nome da tarefa").pack(pady=5)
    entrada_tarefa= tk.Entry(nova_janela,width=30)
    entrada_tarefa.pack(pady=5)

    def salvar_taf():
        tarefa = entrada_tarefa.get().strip()
        meteria = materia_var.get()

        if not tarefa:
            messagebox.showwarning("Aviso","Digite o nome da tarefa")
            return
        materias[meteria].append({"Nome":tarefa,"concluida":False})
        salvar_dados()
        messagebox.showinfo("Sucesso",f"Tarefa adicionada na materia {meteria}!")
        entrada_tarefa.delete(0,tk.END)
    tk.Button(nova_janela,text="Adicionar Tarefa",command=salvar_taf).pack(pady=10)



def ver_taf():
    if not materias:
        messagebox.showwarning("Aviso", "Você não possui matérias cadastradas.")
        return

    janela_ver = tk.Toplevel(janela)
    janela_ver.title("Tarefas por Matérias")
    janela_ver.geometry("300x300")
    
    for mat, tarefas in materias.items():
        tk.Label(janela_ver, text=f"📘 {mat}", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        if tarefas:
            for t in tarefas:
                status = "✔️" if t["concluida"] else "❌"
                tk.Label(janela_ver, text=f"  {status} {t['Nome']}", anchor="w").pack(fill="x", padx=20)
        else:
            tk.Label(janela_ver, text="  Nenhuma tarefa", fg="gray").pack(anchor="w", padx=20)

def marcar_concluido():
    if not materias:
        messagebox.showwarning("Aviso", "Você não possui matérias cadastradas.")
        return

    janela_conc = tk.Toplevel(janela)
    janela_conc.title("Marcar Tarefa como Concluída")
    janela_conc.geometry("350x350")

    tk.Label(janela_conc, text="Selecione a matéria:").pack(pady=5)
    var_materia = tk.StringVar()
    var_materia.set(list(materias.keys())[0])
    tk.OptionMenu(janela_conc, var_materia, *materias.keys()).pack(pady=5)

    tarefas_listbox = tk.Listbox(janela_conc, width=40)
    tarefas_listbox.pack(pady=10)

    def atualizar_tarefas(*args):
        tarefas_listbox.delete(0, tk.END)
        mat = var_materia.get()
        for i, t in enumerate(materias[mat]):
            status = "✔️" if t["concluida"] else "❌"
            tarefas_listbox.insert(tk.END, f"{i + 1}. {status} {t['Nome']}")

    var_materia.trace("w", atualizar_tarefas)
    atualizar_tarefas()

    def marcar():
        mat = var_materia.get()
        selecao = tarefas_listbox.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma tarefa.")
            return
        indice = selecao[0]
        if materias[mat][indice]["concluida"]:
            messagebox.showinfo("Info", "Essa tarefa já está marcada como concluída.")
        else:
            materias[mat][indice]["concluida"] = True
            salvar_dados()
            messagebox.showinfo("Sucesso", "Tarefa marcada como concluída!")
            atualizar_tarefas()

    tk.Button(janela_conc, text="Marcar como concluída", command=marcar).pack(pady=5)

def menu():
    while True:
        print("\n=====- Gerenciador de estudos -=====")
        print("1. Adicionar uma nova matéria")
        print("2. Adicionar uma nova tarefa")
        print("3. Verificar tarefas")
        print("4. Marcar tarefa como concluída")
        print("5. Encerrar")
        
        opcao = input("Digite a opção que deseja executar: ")
        
        if opcao == "1":
            print("")
        elif opcao == "3":
            ver_taf()
        elif opcao == "4":
            marcar_concluido()
        elif opcao == "5":
            print("Saindo do gerenciador..")
            break
        else:
            print("Opção inexistente. Tente mais uma vez🤔")

carregar_dados()

#Janela principal

janela = tk.Tk()
janela.title("Study Assistant")
janela.geometry("400x400")
janela.configure(bg="#5B84C4")

#Titulo
titulo = tk.Label(janela,text= "Study Assistant 📚",font=("Impact",22))
titulo.pack(pady=45)

#Botoes
botao1 = tk.Button(janela,text="Adicionar Matéria",width=25,command=interface_salvar_mat)
botao1 .pack(pady=5)


botao2 = tk.Button(janela,text="Adicionar Tarefa",width=25,command=interface_adicionar_taf)
botao2.pack(pady=5)

botao3 = tk.Button(janela,text="Ver Tarefas",width=25,command=ver_taf)
botao3.pack(pady=5)

botao4 = tk.Button(janela,text="Marcar como concluída",width=25,command=marcar_concluido)
botao4.pack(pady=5)

#Botao de sair
botao5 = tk.Button(janela,text="Sair",width=25,bg="#F98125",fg="white",command=janela.destroy)
botao5.pack(pady=20)




janela.mainloop()