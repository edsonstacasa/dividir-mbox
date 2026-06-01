import email.utils
import mailbox
import queue
import threading
import tkinter as tk
from collections import defaultdict
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


def obter_periodo(msg, modo_divisao):
    try:
        data = msg.get("Date")
        if not data:
            return "sem_data"

        dt = email.utils.parsedate_to_datetime(data)
        if modo_divisao == "ano_mes":
            return f"{dt.year:04d}-{dt.month:02d}"

        return f"{dt.year:04d}"
    except Exception:
        return "erro_data"


def obter_caminho_saida(caminho_entrada, periodo):
    sufixo = caminho_entrada.suffix
    nome_base = caminho_entrada.stem if sufixo else caminho_entrada.name
    return caminho_entrada.with_name(f"{nome_base}_{periodo}{sufixo}")


def dividir_mbox(caminho_entrada, modo_divisao, enviar_evento):
    arquivos = {}
    contadores = defaultdict(int)
    mbox = mailbox.mbox(str(caminho_entrada), create=False)

    try:
        enviar_evento("log", f"Abrindo mbox: {caminho_entrada}")

        for i, msg in enumerate(mbox, start=1):
            periodo = obter_periodo(msg, modo_divisao)

            if periodo not in arquivos:
                caminho_saida = obter_caminho_saida(caminho_entrada, periodo)
                arquivos[periodo] = mailbox.mbox(str(caminho_saida))
                arquivos[periodo].lock()
                enviar_evento("log", f"Criando saida: {caminho_saida}")

            arquivos[periodo].add(msg)
            contadores[periodo] += 1

            if i % 100 == 0:
                enviar_evento("progresso", f"{i} mensagens processadas...")

        enviar_evento("log", "")
        enviar_evento("log", "Resumo:")
        for periodo in sorted(contadores):
            enviar_evento("log", f"{periodo}: {contadores[periodo]} mensagens")

        enviar_evento("concluido", "Concluido.")
    finally:
        for arq in arquivos.values():
            arq.flush()
            arq.unlock()
            arq.close()

        mbox.close()


class DividirMboxApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Dividir mbox")
        self.geometry("760x520")
        self.minsize(680, 460)

        self.caminho_var = tk.StringVar()
        self.modo_var = tk.StringVar(value="ano")
        self.status_var = tk.StringVar(value="Selecione um arquivo mbox.")
        self.eventos = queue.Queue()
        self.thread_processamento = None

        self._criar_interface()
        self.after(100, self._processar_eventos)

    def _criar_interface(self):
        raiz = ttk.Frame(self, padding=16)
        raiz.pack(fill=tk.BOTH, expand=True)

        arquivo_frame = ttk.LabelFrame(raiz, text="Arquivo")
        arquivo_frame.pack(fill=tk.X)

        entrada = ttk.Entry(arquivo_frame, textvariable=self.caminho_var)
        entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(12, 8), pady=12)

        self.botao_selecionar = ttk.Button(
            arquivo_frame,
            text="Selecionar",
            command=self._selecionar_arquivo,
        )
        self.botao_selecionar.pack(side=tk.RIGHT, padx=(0, 12), pady=12)

        modo_frame = ttk.LabelFrame(raiz, text="Divisao")
        modo_frame.pack(fill=tk.X, pady=(12, 0))

        ttk.Radiobutton(
            modo_frame,
            text="Por ano",
            variable=self.modo_var,
            value="ano",
        ).pack(side=tk.LEFT, padx=(12, 24), pady=12)

        ttk.Radiobutton(
            modo_frame,
            text="Por ano-mes",
            variable=self.modo_var,
            value="ano_mes",
        ).pack(side=tk.LEFT, padx=(0, 12), pady=12)

        acoes_frame = ttk.Frame(raiz)
        acoes_frame.pack(fill=tk.X, pady=(12, 0))

        self.botao_iniciar = ttk.Button(
            acoes_frame,
            text="Dividir mbox",
            command=self._iniciar_processamento,
        )
        self.botao_iniciar.pack(side=tk.LEFT)

        ttk.Label(acoes_frame, textvariable=self.status_var).pack(
            side=tk.LEFT,
            padx=(12, 0),
        )

        log_frame = ttk.LabelFrame(raiz, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

        self.log_texto = tk.Text(log_frame, height=16, wrap=tk.WORD, state=tk.DISABLED)
        self.log_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12, 0), pady=12)

        rolagem = ttk.Scrollbar(log_frame, command=self.log_texto.yview)
        rolagem.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 12), pady=12)
        self.log_texto.configure(yscrollcommand=rolagem.set)

    def _selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo mbox",
            filetypes=[
                ("Arquivos mbox", "*.mbox *"),
                ("Todos os arquivos", "*.*"),
            ],
        )
        if caminho:
            self.caminho_var.set(caminho)
            self.status_var.set("Arquivo selecionado.")

    def _iniciar_processamento(self):
        caminho = Path(self.caminho_var.get().strip().strip('"')).expanduser()
        if not caminho.is_file():
            messagebox.showerror("Arquivo invalido", "Selecione um arquivo mbox existente.")
            return

        self._limpar_log()
        self._definir_processando(True)
        self.status_var.set("Processando...")

        self.thread_processamento = threading.Thread(
            target=self._executar_processamento,
            args=(caminho, self.modo_var.get()),
            daemon=True,
        )
        self.thread_processamento.start()

    def _executar_processamento(self, caminho, modo_divisao):
        try:
            dividir_mbox(caminho, modo_divisao, self._enviar_evento)
        except Exception as exc:
            self._enviar_evento("erro", str(exc))

    def _enviar_evento(self, tipo, mensagem):
        self.eventos.put((tipo, mensagem))

    def _processar_eventos(self):
        while True:
            try:
                tipo, mensagem = self.eventos.get_nowait()
            except queue.Empty:
                break

            if tipo == "log":
                self._adicionar_log(mensagem)
            elif tipo == "progresso":
                self.status_var.set(mensagem)
                self._adicionar_log(mensagem)
            elif tipo == "concluido":
                self.status_var.set(mensagem)
                self._adicionar_log(mensagem)
                self._definir_processando(False)
                messagebox.showinfo("Concluido", mensagem)
            elif tipo == "erro":
                self.status_var.set("Erro.")
                self._adicionar_log(f"Erro: {mensagem}")
                self._definir_processando(False)
                messagebox.showerror("Erro", mensagem)

        self.after(100, self._processar_eventos)

    def _adicionar_log(self, mensagem):
        self.log_texto.configure(state=tk.NORMAL)
        self.log_texto.insert(tk.END, f"{mensagem}\n")
        self.log_texto.see(tk.END)
        self.log_texto.configure(state=tk.DISABLED)

    def _limpar_log(self):
        self.log_texto.configure(state=tk.NORMAL)
        self.log_texto.delete("1.0", tk.END)
        self.log_texto.configure(state=tk.DISABLED)

    def _definir_processando(self, processando):
        estado = tk.DISABLED if processando else tk.NORMAL
        self.botao_selecionar.configure(state=estado)
        self.botao_iniciar.configure(state=estado)


def main():
    app = DividirMboxApp()
    app.mainloop()


if __name__ == "__main__":
    main()
