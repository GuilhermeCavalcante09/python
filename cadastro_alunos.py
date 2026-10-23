import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "alunos.db"


class CadastroAlunos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão Acadêmica | Cadastro de Alunos")
        self.root.geometry("1120x720")
        self.root.minsize(960, 620)
        self.root.configure(bg="#f3f5f8")

        self.selected_id = None
        self.photo_path = ""
        self.vars = {
            "nome": tk.StringVar(),
            "email": tk.StringVar(),
            "telefone": tk.StringVar(),
            "sexo": tk.StringVar(value="Não informado"),
            "nascimento": tk.StringVar(),
            "cpf": tk.StringVar(),
            "curso": tk.StringVar(value="Técnico em Informática"),
            "busca": tk.StringVar(),
        }

        self.configure_styles()
        self.create_database()
        self.build_interface()
        self.load_students()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", fieldbackground="white",
                        foreground="#263247", rowheight=29, borderwidth=0)
        style.configure("Treeview.Heading", background="#e8edf4",
                        foreground="#263247", font=("Segoe UI", 9, "bold"), padding=8)
        style.map("Treeview", background=[("selected", "#dbeafe")],
                  foreground=[("selected", "#172554")])
        style.configure("TCombobox", padding=6)
        style.configure("TEntry", padding=7)

    def create_database(self):
        with sqlite3.connect(DB_PATH) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefone TEXT,
                    sexo TEXT,
                    nascimento TEXT,
                    cpf TEXT,
                    curso TEXT,
                    foto TEXT,
                    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def build_interface(self):
        header = tk.Frame(self.root, bg="#172b4d", height=82)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="GESTÃO ACADÊMICA", bg="#172b4d", fg="#9fc5ff",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=24, pady=(14, 0))
        tk.Label(header, text="Cadastro de alunos", bg="#172b4d", fg="white",
                 font=("Segoe UI", 21, "bold")).pack(anchor="w", padx=24)

        main = tk.Frame(self.root, bg="#f3f5f8")
        main.pack(fill="both", expand=True, padx=20, pady=18)

        form_card = tk.Frame(main, bg="white", highlightbackground="#dce3ec",
                             highlightthickness=1)
        form_card.pack(fill="x", pady=(0, 14))

        tk.Label(form_card, text="DADOS DO ESTUDANTE", bg="white", fg="#52627a",
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=6,
                                                      sticky="w", padx=18, pady=(16, 10))

        self.add_field(form_card, "Nome completo *", "nome", 1, 0, 2)
        self.add_field(form_card, "E-mail *", "email", 1, 2, 2)
        self.add_field(form_card, "Telefone", "telefone", 1, 4, 2)
        self.add_field(form_card, "Data de nascimento (DD/MM/AAAA)", "nascimento", 3, 0, 2)
        self.add_field(form_card, "CPF", "cpf", 3, 2, 2)

        tk.Label(form_card, text="Sexo", bg="white", fg="#34445c",
                 font=("Segoe UI", 9, "bold")).grid(row=3, column=4, sticky="w",
                                                    padx=(12, 8), pady=(10, 4))
        ttk.Combobox(form_card, textvariable=self.vars["sexo"],
                     values=["Não informado", "Feminino", "Masculino", "Outro"],
                     state="readonly").grid(row=4, column=4, columnspan=2,
                                            sticky="ew", padx=(12, 18), pady=(0, 10))

        tk.Label(form_card, text="Curso / turma", bg="white", fg="#34445c",
                 font=("Segoe UI", 9, "bold")).grid(row=5, column=0, sticky="w",
                                                    padx=(18, 8), pady=(4, 4))
        ttk.Combobox(form_card, textvariable=self.vars["curso"],
                     values=["Técnico em Informática", "Desenvolvimento de Sistemas",
                             "Redes de Computadores", "Administração", "Outro"]).grid(
                         row=6, column=0, columnspan=2, sticky="ew",
                         padx=(18, 8), pady=(0, 16))

        photo_box = tk.Frame(form_card, bg="#f3f6fa", highlightbackground="#dce3ec",
                             highlightthickness=1)
        photo_box.grid(row=5, column=2, rowspan=2, columnspan=2, sticky="nsew",
                       padx=10, pady=(4, 16))
        tk.Label(photo_box, text="FOTO DO ALUNO", bg="#f3f6fa", fg="#64748b",
                 font=("Segoe UI", 9, "bold")).pack(pady=(10, 4))
        self.photo_label = tk.Label(photo_box, text="Nenhuma foto selecionada",
                                    bg="#f3f6fa", fg="#64748b",
                                    font=("Segoe UI", 9), wraplength=180)
        self.photo_label.pack(pady=2)
        tk.Button(photo_box, text="Selecionar arquivo", command=self.choose_photo,
                  bg="#e1e9f5", fg="#172b4d", relief="flat", padx=10,
                  cursor="hand2").pack(pady=(5, 10))

        actions = tk.Frame(form_card, bg="white")
        actions.grid(row=5, column=4, rowspan=2, columnspan=2, sticky="nsew",
                     padx=(8, 18), pady=(4, 16))
        self.action_button(actions, "Novo cadastro", self.clear_form, "#e8edf4", "#263247")
        self.action_button(actions, "Salvar aluno", self.save_student, "#176b55", "white")
        self.action_button(actions, "Atualizar selecionado", self.update_student, "#2459a9", "white")
        self.action_button(actions, "Excluir selecionado", self.delete_student, "#a63838", "white")

        for c in range(6):
            form_card.grid_columnconfigure(c, weight=1)

        list_card = tk.Frame(main, bg="white", highlightbackground="#dce3ec",
                             highlightthickness=1)
        list_card.pack(fill="both", expand=True)

        top = tk.Frame(list_card, bg="white")
        top.pack(fill="x", padx=16, pady=14)
        tk.Label(top, text="Alunos cadastrados", bg="white", fg="#172b4d",
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        tk.Label(top, text="Pesquisar:", bg="white", fg="#52627a",
                 font=("Segoe UI", 9)).pack(side="left", padx=(22, 6))
        search = ttk.Entry(top, textvariable=self.vars["busca"], width=28)
        search.pack(side="left")
        search.bind("<KeyRelease>", lambda _e: self.load_students())
        tk.Button(top, text="Limpar busca", command=self.clear_search,
                  bg="#e8edf4", fg="#263247", relief="flat", padx=10,
                  cursor="hand2").pack(side="left", padx=7)
        tk.Button(top, text="Ver selecionado", command=self.view_student,
                  bg="#172b4d", fg="white", relief="flat", padx=12,
                  cursor="hand2").pack(side="right")

        table_frame = tk.Frame(list_card, bg="white")
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        columns = ("id", "nome", "email", "telefone", "sexo", "nascimento", "cpf", "curso")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        headings = {"id": "ID", "nome": "Nome", "email": "E-mail", "telefone": "Telefone",
                    "sexo": "Sexo", "nascimento": "Nascimento", "cpf": "CPF", "curso": "Curso / turma"}
        widths = {"id": 48, "nome": 170, "email": 190, "telefone": 105, "sexo": 95,
                  "nascimento": 110, "cpf": 125, "curso": 190}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], minwidth=60,
                             anchor="w" if col not in ("id",) else "center")
        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", lambda _e: self.view_student())

        self.status = tk.Label(self.root, text="Pronto", anchor="w", bg="#e8edf4",
                               fg="#52627a", padx=20, pady=7, font=("Segoe UI", 9))
        self.status.pack(fill="x", side="bottom")

    def add_field(self, parent, label, key, row, col, span):
        tk.Label(parent, text=label, bg="white", fg="#34445c",
                 font=("Segoe UI", 9, "bold")).grid(row=row, column=col, columnspan=span,
                                                    sticky="w", padx=(18 if col == 0 else 10, 8),
                                                    pady=(10, 4))
        entry = ttk.Entry(parent, textvariable=self.vars[key])
        entry.grid(row=row + 1, column=col, columnspan=span, sticky="ew",
                   padx=(18 if col == 0 else 10, 8), pady=(0, 8))

    def action_button(self, parent, text, command, bg, fg):
        tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                  activebackground=bg, activeforeground=fg, relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=8, pady=7,
                  cursor="hand2").pack(fill="x", pady=3)

    def choose_photo(self):
        path = filedialog.askopenfilename(
            title="Selecionar foto",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos os arquivos", "*.*")]
        )
        if path:
            self.photo_path = path
            self.photo_label.config(text=Path(path).name)
            self.status.config(text="Foto selecionada: " + Path(path).name)

    def form_data(self):
        data = {key: self.vars[key].get().strip()
                for key in ("nome", "email", "telefone", "sexo", "nascimento", "cpf", "curso")}
        data["foto"] = self.photo_path
        if not data["nome"] or not data["email"]:
            messagebox.showwarning("Campos obrigatórios", "Preencha nome completo e e-mail.")
            return None
        if "@" not in data["email"] or "." not in data["email"].split("@")[-1]:
            messagebox.showwarning("E-mail inválido", "Informe um endereço de e-mail válido.")
            return None
        if data["nascimento"]:
            try:
                datetime.strptime(data["nascimento"], "%d/%m/%Y")
            except ValueError:
                messagebox.showwarning("Data inválida", "Use o formato DD/MM/AAAA.")
                return None
        return data

    def save_student(self):
        data = self.form_data()
        if not data:
            return
        with sqlite3.connect(DB_PATH) as con:
            con.execute("""INSERT INTO alunos
                (nome,email,telefone,sexo,nascimento,cpf,curso,foto)
                VALUES (?,?,?,?,?,?,?,?)""",
                tuple(data[k] for k in ("nome","email","telefone","sexo","nascimento","cpf","curso","foto")))
        self.load_students()
        self.clear_form()
        self.status.config(text="Aluno cadastrado com sucesso.")

    def update_student(self):
        if not self.selected_id:
            messagebox.showinfo("Selecionar aluno", "Selecione um aluno na tabela para atualizar.")
            return
        data = self.form_data()
        if not data:
            return
        with sqlite3.connect(DB_PATH) as con:
            con.execute("""UPDATE alunos SET nome=?,email=?,telefone=?,sexo=?,nascimento=?,
                cpf=?,curso=?,foto=? WHERE id=?""",
                tuple(data[k] for k in ("nome","email","telefone","sexo","nascimento","cpf","curso","foto"))
                + (self.selected_id,))
        self.load_students()
        self.status.config(text="Cadastro atualizado.")

    def delete_student(self):
        if not self.selected_id:
            messagebox.showinfo("Selecionar aluno", "Selecione um aluno na tabela para excluir.")
            return
        if not messagebox.askyesno("Confirmar exclusão", "Deseja excluir o aluno selecionado?"):
            return
        with sqlite3.connect(DB_PATH) as con:
            con.execute("DELETE FROM alunos WHERE id=?", (self.selected_id,))
        self.clear_form()
        self.load_students()
        self.status.config(text="Cadastro excluído.")

    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        term = self.vars["busca"].get().strip()
        with sqlite3.connect(DB_PATH) as con:
            if term:
                rows = con.execute("""SELECT id,nome,email,telefone,sexo,nascimento,cpf,curso
                    FROM alunos WHERE nome LIKE ? OR email LIKE ? OR cpf LIKE ? OR curso LIKE ?
                    ORDER BY id DESC""", tuple(f"%{term}%" for _ in range(4))).fetchall()
            else:
                rows = con.execute("""SELECT id,nome,email,telefone,sexo,nascimento,cpf,curso
                    FROM alunos ORDER BY id DESC""").fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.status.config(text=f"{len(rows)} aluno(s) exibido(s).")

    def on_select(self, _event=None):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0], "values")
        self.selected_id = int(values[0])
        with sqlite3.connect(DB_PATH) as con:
            row = con.execute("SELECT nome,email,telefone,sexo,nascimento,cpf,curso,foto FROM alunos WHERE id=?",
                              (self.selected_id,)).fetchone()
        if row:
            for key, value in zip(("nome","email","telefone","sexo","nascimento","cpf","curso"), row[:7]):
                self.vars[key].set(value or "")
            self.photo_path = row[7] or ""
            self.photo_label.config(text=Path(self.photo_path).name if self.photo_path else "Nenhuma foto selecionada")

    def view_student(self):
        if not self.selected_id:
            messagebox.showinfo("Selecionar aluno", "Selecione um aluno na tabela.")
            return
        with sqlite3.connect(DB_PATH) as con:
            row = con.execute("""SELECT id,nome,email,telefone,sexo,nascimento,cpf,curso
                                 FROM alunos WHERE id=?""", (self.selected_id,)).fetchone()
        if row:
            labels = ["ID", "Nome", "E-mail", "Telefone", "Sexo", "Nascimento", "CPF", "Curso / turma"]
            details = "\n".join(f"{label}: {value or '—'}" for label, value in zip(labels, row))
            messagebox.showinfo("Ficha do aluno", details)

    def clear_form(self):
        self.selected_id = None
        self.photo_path = ""
        for key in ("nome","email","telefone","nascimento","cpf"):
            self.vars[key].set("")
        self.vars["sexo"].set("Não informado")
        self.vars["curso"].set("Técnico em Informática")
        self.photo_label.config(text="Nenhuma foto selecionada")
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        self.status.config(text="Formulário pronto para um novo cadastro.")

    def clear_search(self):
        self.vars["busca"].set("")
        self.load_students()


if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroAlunos(root)
    root.mainloop()
