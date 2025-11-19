# Importa o módulo tkinter e dá a ele o apelido "tk"
# Esse módulo é o que permite criar janelas, botões, campos de texto, etc.
import tkinter as tk


# Define uma classe chamada "Calculadora" que herda de "tk.Tk"
# "tk.Tk" é a janela principal de um programa feito com Tkinter.
class Calculadora(tk.Tk):
    # Método inicializador da classe (chamado quando criamos um objeto Calculadora)
    def __init__(self):
        # Chama o inicializador da classe pai (tk.Tk)
        super().__init__()

        # Define o título da janela (aparece na barra superior)
        self.title("Calculadora")
        # Impede que a janela seja redimensionada (não aumenta/diminui arrastando)
        self.resizable(False, False)

        # Chama o método que cria todos os elementos da interface (campo de texto, botões, etc.)
        self._criar_widgets()
        # Chama o método que configura os eventos do teclado (o que acontece ao apertar teclas)
        self._configurar_eventos()

    # ----------------- UI (interface gráfica) -----------------
    # Método para criar os widgets (componentes visuais) da calculadora
    def _criar_widgets(self):
        # Cria o campo de exibição (onde aparecem os números e resultados)
        # tk.Entry é um campo de texto de uma linha.
        self.display = tk.Entry(
            self,
            font=("Segoe UI", 20),   # Fonte e tamanho do texto
            borderwidth=2,           # Espessura da borda
            relief="solid",          # Estilo da borda
            justify="right"          # Alinhamento do texto à direita (como em calculadoras)
        )
        # Coloca o campo de texto na grade (layout em tabela)
        # row=0 (linha 0), column=0 (coluna 0), columnspan=4 (ocupa 4 colunas)
        # padx e pady são espaçamentos externos; ipady aumenta a altura interna
        # sticky="we" faz ele "esticar" na direção oeste-leste (esquerda-direita)
        self.display.grid(row=0, column=0, columnspan=4,
                          padx=10, pady=10, ipady=10, sticky="we")

        # Cria uma lista com as informações de cada botão:
        # (texto do botão, linha na grade, coluna na grade)
        botoes = [
            ("C",  1, 0), ("←", 1, 1), ("/", 1, 2), ("*", 1, 3),
            ("7",  2, 0), ("8", 2, 1), ("9", 2, 2), ("-", 2, 3),
            ("4",  3, 0), ("5", 3, 1), ("6", 3, 2), ("+", 3, 3),
            ("1",  4, 0), ("2", 4, 1), ("3", 4, 2), ("=", 4, 3),
            ("0",  5, 0), (".", 5, 1),
        ]

        # Percorre a lista de botões, criando cada um deles
        for (texto, linha, coluna) in botoes:
            # Cria um botão
            botao = tk.Button(
                self,                 # A janela principal é o "pai" do botão
                text=texto,           # Texto que aparece no botão
                font=("Segoe UI", 14),
                width=5,              # Largura do botão em "caracteres"
                height=2,             # Altura do botão em "linhas de texto"
                # command define a função chamada quando o botão é clicado
                # usamos "lambda" para passar o texto do botão como parâmetro
                command=lambda t=texto: self._ao_clicar_botao(t)
            )
            # Posiciona o botão na grade
            botao.grid(row=linha, column=coluna,
                       padx=5, pady=5, sticky="nsew")   # "nsew" → norte, sul, leste, oeste (preenche o espaço)

        # Configura todas as 4 colunas para crescerem proporcionalmente,
        # caso a janela fosse redimensionada (apesar de estar desativado)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        # Configura as linhas de 1 a 5 da mesma forma
        for i in range(1, 6):
            self.grid_rowconfigure(i, weight=1)

    # Método que configura os eventos do teclado
    def _configurar_eventos(self):
        # Liga o evento de qualquer tecla pressionada ("<Key>") ao método _ao_digitar
        self.bind("<Key>", self._ao_digitar)

        # Liga a tecla Enter ("<Return>") à função de calcular
        self.bind("<Return>", lambda e: self._calcular())
        # Liga o Enter do teclado numérico ("<KP_Enter>") também à função de calcular
        self.bind("<KP_Enter>", lambda e: self._calcular())
        # Liga a tecla Backspace à função que apaga o último caractere
        self.bind("<BackSpace>", lambda e: self._backspace())
        # Liga a tecla Esc (Escape) à função que limpa o display
        self.bind("<Escape>", lambda e: self._limpar())

    # ----------------- Lógica dos botões -----------------
    # Método chamado quando qualquer botão da calculadora é clicado
    def _ao_clicar_botao(self, char: str):
        # Se o caractere for um número ou ponto, apenas adiciona ao display
        if char in "0123456789.":
            # tk.END indica "fim do texto atual"
            self.display.insert(tk.END, char)
        # Se for um operador matemático, também adicionamos no display
        elif char in "+-*/":
            self.display.insert(tk.END, char)
        # Se for "C", chamamos a função que limpa o display
        elif char == "C":
            self._limpar()
        # Se for "←", chamamos a função que remove o último caractere
        elif char == "←":
            self._backspace()
        # Se for "=", chamamos a função que calcula o resultado
        elif char == "=":
            self._calcular()

    # ----------------- Lógica do teclado -----------------
    # Método chamado quando o usuário digita alguma tecla
    def _ao_digitar(self, event):
        # event.char é o caractere correspondente à tecla pressionada
        char = event.char

        # Se for número, ponto ou operador, colocamos no display
        if char in "0123456789.+-*/":
            self.display.insert(tk.END, char)
        # Outras teclas especiais (Enter, Backspace, Esc) já estão tratadas nos binds
        # em _configurar_eventos, então não precisamos tratar aqui.

    # ----------------- Ações -----------------
    # Limpa todo o conteúdo do display
    def _limpar(self):
        # delete(início, fim) → apaga do índice 0 até o fim
        self.display.delete(0, tk.END)

    # Apaga o último caractere do display (backspace)
    def _backspace(self):
        # Pega o texto atual do display
        texto = self.display.get()
        # Se tiver algo escrito...
        if texto:
            # Apaga o último caractere: do índice len(texto) - 1 até o fim
            self.display.delete(len(texto) - 1, tk.END)

    # Verifica se a expressão tem apenas caracteres permitidos
    def _expressao_valida(self, expr: str) -> bool:
        # Define uma string com todos os caracteres que consideramos seguros
        permitidos = "0123456789+-*/(). "
        # Retorna True se TODOS os caracteres da expressão estiverem em "permitidos"
        return all(c in permitidos for c in expr)

    # Faz o cálculo baseado no que estiver escrito no display
    def _calcular(self):
        # Lê o texto do display (a expressão matemática)
        expr = self.display.get()
        # Se estiver vazio, não faz nada
        if not expr:
            return

        try:
            # Primeiro, verifica se a expressão contém apenas caracteres permitidos
            if not self._expressao_valida(expr):
                # Se tiver caractere estranho, lança um erro proposital
                raise ValueError("Expressão inválida")

            # Usa eval para avaliar a expressão matemática como código Python.
            # IMPORTANTE: usamos um "ambiente" vazio para não permitir acesso a funções perigosas.
            resultado = eval(expr, {"__builtins__": None}, {})
            # Limpa o display
            self.display.delete(0, tk.END)
            # Mostra o resultado no display
            self.display.insert(tk.END, str(resultado))
        except Exception:
            # Se der qualquer erro (divisão por zero, expressão inválida etc.),
            # limpamos o display e mostramos "Erro"
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Erro")


# Esse bloco garante que o código abaixo só será executado
# se o arquivo for rodado diretamente (python calculadora.py)
# e não quando ele for importado como módulo em outro arquivo.
if __name__ == "__main__":
    # Cria uma instância (objeto) da classe Calculadora
    app = Calculadora()
    # Inicia o "loop" principal da interface gráfica.
    # Esse loop mantém a janela aberta e cuidando dos eventos (cliques, teclas, etc.)
    app.mainloop()
