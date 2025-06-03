import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
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

imagens_capas = {
    "John Wick": "capas/john_wick.jpg",
    "Gladiador": "capas/gladiador.jpg",
    "Mad Max": "capas/mad_max.jpg",
    "Titanic": "capas/titanic.jpg",
    "Forrest Gump": "capas/forrest_gump.jpg",
    "Clube da Luta": "capas/clube_da_luta.jpg",
    "Matrix": "capas/matrix.jpg",
    "Interestelar": "capas/interestelar.jpg",
    "A Origem": "capas/a_origem.jpg",
    "La La Land": "capas/la_la_land.jpg",
    "O Rei do Show": "capas/o_rei_do_show.jpg",
    "Chicago": "capas/chicago.jpg",
    "Seven": "capas/seven.jpg",
    "Garota Exemplar": "capas/garota_exemplar.jpg",
    "O Silêncio dos Inocentes": "capas/o_silencio_dos_inocentes.jpg",
    "Orgulho e Preconceito": "capas/orgulho_e_preconceito.jpg",
    "Simplesmente Amor": "capas/simplesmente_amor.jpg",
    "Questão de Tempo": "capas/questao_de_tempo.jpg"
}

class AppFilmes:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Pobreflix")
        self.janela.geometry("900x700")
        self.janela.configure(bg="#141414")
        self.nome_usuario = ""
        self.imagens_cache = {}  
        self.tela_nome()

    def limpar_tela(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

    def criar_botao(self, texto, comando):
        return tk.Button(self.janela, text=texto, font=("Helvetica", 11, "bold"),
                         bg="#E50914", fg="white", activebackground="#B20710",
                         relief="flat", padx=10, pady=6, command=comando)

    def tela_nome(self):
        self.limpar_tela()
        tk.Label(self.janela, text="Pobreflix", font=("Helvetica", 30, "bold"),
                 fg="#E50914", bg="#141414").pack(pady=40)
        tk.Label(self.janela, text="Qual é o seu nome?", font=("Helvetica", 16),
                 fg="white", bg="#141414").pack(pady=10)
        self.entrada_nome = tk.Entry(self.janela, font=("Helvetica", 14), width=30)
        self.entrada_nome.pack(pady=10)
        self.criar_botao("Continuar", self.salvar_nome_ir).pack(pady=20)

    def salvar_nome_ir(self):
        nome = self.entrada_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome.")
            return
        self.nome_usuario = nome
        self.mostrar_generos()

    def mostrar_generos(self):
        self.limpar_tela()
        tk.Label(self.janela, text=f"Olá, {self.nome_usuario}!",
                 font=("Helvetica", 24, "bold"), fg="white", bg="#141414").pack(pady=20)
        tk.Label(self.janela, text="Escolha um gênero:",
                 font=("Helvetica", 18), fg="white", bg="#141414").pack(pady=10)

        for genero in biblioteca_filmes.keys():
            self.criar_botao(genero, lambda g=genero: self.mostrar_catalogo(g)).pack(pady=8)

        tk.Label(self.janela, text="", bg="#141414").pack(pady=10)
        self.criar_botao("🎞 Ver grafo de gêneros", mostrar_grafo_generos).pack(pady=10)

    def mostrar_catalogo(self, genero):
        self.limpar_tela()
        tk.Label(self.janela, text=f"Filmes de {genero}",
                 font=("Helvetica", 24, "bold"), fg="white", bg="#141414").pack(pady=20)

        arvore = ArvoreFilmes()
        for titulo, nota in biblioteca_filmes[genero]:
            arvore.inserir(titulo, nota)

        filmes_ordenados = arvore.em_ordem_decrescente()

        frame_cards = tk.Frame(self.janela, bg="#141414")
        frame_cards.pack(fill="both", expand=True, padx=20)

        colunas = 3
        for i, (filme, nota) in enumerate(filmes_ordenados):
            card = tk.Frame(frame_cards, bg="#222", bd=0, relief="flat", width=160, height=280)
            card.grid(row=i//colunas, column=i%colunas, padx=15, pady=15)
            card.pack_propagate(False)

            caminho_imagem = imagens_capas.get(filme, None)
            if caminho_imagem:
                try:
                    img = Image.open(caminho_imagem)
                    img = img.resize((160, 220)) 
                    foto = ImageTk.PhotoImage(img)
                    label_img = tk.Label(card, image=foto, bg="#222")
                    label_img.image = foto  
                    label_img.pack()
                except Exception as e:
                    
                    label_img = tk.Label(card, text="🎬", bg="#444", fg="white", font=("Helvetica", 48))
                    label_img.pack(fill="both", expand=True)
            else:
                label_img = tk.Label(card, text="🎬", bg="#444", fg="white", font=("Helvetica", 48))
                label_img.pack(fill="both", expand=True)

            
            titulo_label = tk.Label(card, text=filme, font=("Helvetica", 12, "bold"),
                                    fg="white", bg="#222", wraplength=150, justify="center")
            titulo_label.pack(pady=(5,0))
            nota_label = tk.Label(card, text=f"Nota: {nota}/10", font=("Helvetica", 11),
                                  fg="#ccc", bg="#222")
            nota_label.pack()

        relacionados = obter_generos_relacionados(genero)
        if relacionados:
            tk.Label(self.janela, text="Você também pode gostar de:",
                     font=("Helvetica", 16), fg="white", bg="#141414").pack(pady=15)
            for rel in relacionados:
                self.criar_botao(rel, lambda g=rel: self.mostrar_catalogo(g)).pack(pady=5)

        self.criar_botao("⬅ Voltar", self.mostrar_generos).pack(pady=25)
        self.criar_botao("❌ Sair", self.janela.quit).pack()

janela = tk.Tk()
app = AppFilmes(janela)
janela.mainloop()
