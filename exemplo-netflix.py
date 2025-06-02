import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt


class NoFilme:
    def __init__(self, titulo, nota):
        self.titulo = titulo
        self.nota = nota
        self.esquerda = None
        self.direita = None

class ArvoreFilmes:
    def __init__(self):
        self.raiz = None

    def inserir(self, titulo, nota):
        self.raiz = self._inserir_recursivo(self.raiz, titulo, nota)

    def _inserir_recursivo(self, no, titulo, nota):
        if no is None:
            return NoFilme(titulo, nota)
        if nota < no.nota:
            no.esquerda = self._inserir_recursivo(no.esquerda, titulo, nota)
        else:
            no.direita = self._inserir_recursivo(no.direita, titulo, nota)
        return no

    def em_ordem_decrescente(self):
        filmes = []
        self._em_ordem_decrescente(self.raiz, filmes)
        return filmes

    def _em_ordem_decrescente(self, no, filmes):
        if no:
            self._em_ordem_decrescente(no.direita, filmes)
            filmes.append((no.titulo, no.nota))
            self._em_ordem_decrescente(no.esquerda, filmes)

biblioteca_filmes = {
    "Ação": [("John Wick", 9), ("Gladiador", 8), ("Mad Max", 9)],
    "Drama": [("Titanic", 8), ("Forrest Gump", 9), ("Clube da Luta", 9)],
    "Ficção": [("Matrix", 9), ("Interestelar", 10), ("A Origem", 9)],
    "Musical": [("La La Land", 8), ("O Rei do Show", 7), ("Chicago", 8)],
    "Suspense": [("Seven", 9), ("Garota Exemplar", 8), ("O Silêncio dos Inocentes", 9)],
    "Romance": [("Orgulho e Preconceito", 8), ("Simplesmente Amor", 7), ("Questão de Tempo", 8)]
}

grafo_generos = {
    "Ação": ["Ficção", "Suspense"],
    "Drama": ["Romance", "Musical"],
    "Ficção": ["Ação", "Suspense"],
    "Musical": ["Drama"],
    "Suspense": ["Ação", "Ficção"],
    "Romance": ["Drama"]
}

def obter_generos_relacionados(genero):
    return grafo_generos.get(genero, [])

def mostrar_grafo_generos():
    G = nx.Graph()
    for genero, vizinhos in grafo_generos.items():
        for n in vizinhos:
            G.add_edge(genero, n)
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000,
            font_size=12, font_weight='bold', edge_color='gray')
    plt.title("Grafo de Gêneros Relacionados")
    plt.show()

class AppFilmes:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Pobreflix")
        self.nome_usuario = ""
        self.tela_nome()

    def limpar_tela(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

    def tela_nome(self):
        self.limpar_tela()
        ttk.Label(self.janela, text="Bem-vindo! Qual é o seu nome?").pack(pady=10)
        self.entrada_nome = ttk.Entry(self.janela, width=30)
        self.entrada_nome.pack(pady=5)
        ttk.Button(self.janela, text="Continuar", command=self.salvar_nome_ir).pack(pady=10)

    def salvar_nome_ir(self):
        nome = self.entrada_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome.")
            return
        self.nome_usuario = nome
        self.mostrar_generos()

    def mostrar_generos(self):
        self.limpar_tela()
        ttk.Label(self.janela, text=f"Olá, {self.nome_usuario}! Escolha um gênero:").pack(pady=10)

        for genero in biblioteca_filmes.keys():
            ttk.Button(self.janela, text=genero, width=20,
                       command=lambda g=genero: self.mostrar_catalogo(g)).pack(pady=5)

        ttk.Separator(self.janela, orient='horizontal').pack(fill='x', pady=10)
        ttk.Button(self.janela, text="Mostrar Grafo de Gêneros", command=mostrar_grafo_generos).pack()

    def mostrar_catalogo(self, genero):
        self.limpar_tela()
        ttk.Label(self.janela, text=f"{self.nome_usuario}, aqui estão os filmes de {genero}:").pack(pady=10)

        arvore = ArvoreFilmes()
        for titulo, nota in biblioteca_filmes[genero]:
            arvore.inserir(titulo, nota)
        filmes_ordenados = arvore.em_ordem_decrescente()

        for filme, nota in filmes_ordenados:
            quadro = ttk.Frame(self.janela, borderwidth=1, relief="solid", padding=10)
            ttk.Label(quadro, text=f"{filme}", font=("Arial", 12, "bold")).pack(anchor="w")
            ttk.Label(quadro, text=f"Nota: {nota}/10").pack(anchor="w")
            quadro.pack(padx=10, pady=5, fill="x")

        generos_relacionados = obter_generos_relacionados(genero)
        if generos_relacionados:
            ttk.Label(self.janela, text="Também pode gostar de:").pack(pady=10)
            for rel in generos_relacionados:
                ttk.Button(self.janela, text=rel, width=20,
                           command=lambda g=rel: self.mostrar_catalogo(g)).pack(pady=2)

        ttk.Button(self.janela, text="Voltar aos Gêneros", command=self.mostrar_generos).pack(pady=10)
        ttk.Button(self.janela, text="Sair", command=self.janela.quit).pack(pady=5)


janela = tk.Tk()
estilo = ttk.Style(janela)
estilo.theme_use('clam')

app = AppFilmes(janela)
janela.mainloop()
