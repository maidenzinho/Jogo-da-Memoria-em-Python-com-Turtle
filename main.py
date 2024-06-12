import random
from time import sleep
import turtle

# Classe para representar o jogo da memória
class JogoMemoria:
    def __init__(self):
        self.mat = []
        self.mat_exib = []
        self.primeira_pos = None
        self.segunda_pos = None
        self.tentativas = 0
        self.erros = 0
        self.acertos = 0
        self.revelacoes_restantes = 2
        self.dificuldade = None
        self.ranking_file = "ranking.txt"

    # Método para criar a matriz de jogo
    def criar_matriz(self, dificuldade):
        emojis = [
            "😀", "😎", "😂", "🥳", "😜", "🤖", "🐱", "🌻",
            "🍕", "🚀", "🎉", "🍔", "🌈", "🎸", "🍑", "📚",
            "🦄", "🐼", "🍩", "🎈", "🍭", "🌟", "💡", "🍆",
            "🍉", "🚗", "🎨", "🐳", "🍦", "🎵", "🧩", "🎳",
            "🍇", "🚲", "🎻", "🐶", "🍰", "🎬", "🎮", "📖",
            "🍓", "🛵", "🎤", "🐯", "🍪", "🎭", "🎲", "📕"
        ]

        mat_length = 4
        if dificuldade == "2":
            mat_length = 6
        elif dificuldade == "3":
            mat_length = 8

        # Inicializa a matriz e escolhe os emojis de forma aleatória
        total_celulas = mat_length * mat_length
        selecionados = []
        while len(selecionados) < total_celulas // 2:
            emoji = emojis[random.randint(0, len(emojis) - 1)]
            if emoji not in selecionados:
                selecionados.append(emoji)

        # Duplica os emojis selecionados e embaralha
        selecionados *= 2
        random.shuffle(selecionados)

        self.mat = [selecionados[i * mat_length:(i + 1) * mat_length] for i in range(mat_length)]
        self.mat_exib = [['#' for _ in range(mat_length)] for _ in range(mat_length)]

    # Método para desenhar a matriz de jogo
    def desenhar_matriz(self):
        turtle.clear()
        turtle.speed(0)
        turtle.hideturtle()
        tamanho = len(self.mat_exib)
        lado = 40

        for i in range(tamanho):
            for j in range(tamanho):
                x = j * lado - (tamanho * lado) / 2
                y = i * lado - (tamanho * lado) / 2
                self.desenhar_celula(x, y, self.mat_exib[i][j])

        self.atualizar_contadores()
        turtle.update()

    # Método para desenhar uma célula da matriz
    def desenhar_celula(self, x, y, simbolo):
        lado = 40
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.setheading(0)

        if simbolo == '#':
            turtle.fillcolor("lightgrey")
        else:
            turtle.fillcolor("white")

        turtle.begin_fill()
        for _ in range(4):
            turtle.forward(lado)
            turtle.left(90)
        turtle.end_fill()

        if simbolo != '#':
            turtle.penup()
            turtle.goto(x + lado / 2, y + lado / 2 - 10)
            turtle.pendown()
            turtle.color("black")
            turtle.write(simbolo, align="center", font=("Arial", 16, "normal"))
        turtle.color("black")

    # Método para atualizar os contadores de erros e acertos
    def atualizar_contadores(self):
        turtle.penup()
        turtle.goto(-150, 200)
        turtle.pendown()
        turtle.color("red")
        turtle.write(f"Erros: {self.erros}", align="center", font=("Arial", 16, "normal"))

        turtle.penup()
        turtle.goto(-5, 170)
        turtle.pendown()
        turtle.color("blue")
        turtle.write(f"Revelações restantes: {self.revelacoes_restantes}", align="center", font=("Arial", 16, "normal"))

        turtle.penup()
        turtle.goto(150, 200)
        turtle.pendown()
        turtle.color("green")
        turtle.write(f"Acertos: {self.acertos}", align="center", font=("Arial", 16, "normal"))

    # Método chamado quando o jogador clica em uma célula da matriz
    def on_click(self, x, y):
        tamanho = len(self.mat_exib)
        lado = 40
        coluna = int((x + (tamanho * lado) / 2) // lado)
        linha = int((y + (tamanho * lado) / 2) // lado)

        if 0 <= linha < tamanho and 0 <= coluna < tamanho:
            self.revelar_posicao(linha, coluna)

    # Método para revelar o símbolo de uma posição da matriz
    def revelar_posicao(self, linha, coluna):
        if self.mat_exib[linha][coluna] == '#':
            if not self.primeira_pos:
                self.primeira_pos = (linha, coluna)
                self.mat_exib[linha][coluna] = self.mat[linha][coluna]
            elif not self.segunda_pos:
                self.segunda_pos = (linha, coluna)
                self.mat_exib[linha][coluna] = self.mat[linha][coluna]

                self.desenhar_matriz()
                turtle.update()
                self.tentativas += 1
                sleep(1)

                if self.mat[self.primeira_pos[0]][self.primeira_pos[1]] != self.mat[self.segunda_pos[0]][self.segunda_pos[1]]:
                    self.mat_exib[self.primeira_pos[0]][self.primeira_pos[1]] = '#'
                    self.mat_exib[self.segunda_pos[0]][self.segunda_pos[1]] = '#'
                    self.erros += 1
                else:
                    self.acertos += 1

                self.primeira_pos = None
                self.segunda_pos = None

            self.desenhar_matriz()

            # Verifica se todas as posições foram reveladas
            if all(self.mat_exib[i][j] == self.mat[i][j] for i in range(len(self.mat)) for j in range(len(self.mat[i]))):
                # Exibe o resultado final
                self.exibir_resultado_final()

    # Método para exibir o resultado final e perguntar ao jogador se deseja jogar novamente
    def exibir_resultado_final(self):
        turtle.penup()
        turtle.goto(0, -270)
        turtle.pendown()
        turtle.color("blue")
        turtle.write(f"Parabéns! Você completou o jogo em {self.tentativas} tentativas.", align="center", font=("Arial", 16, "normal"))
        turtle.penup()
        turtle.goto(0, -290)
        turtle.pendown()
        turtle.color("blue")
        turtle.write(f"Erros: {self.erros}, Acertos: {self.acertos}", align="center", font=("Arial", 16, "normal"))
        turtle.update()
        self.registrar_ranking()

        # Perguntar se deseja jogar novamente
        resposta = turtle.textinput("Jogar Novamente", "Deseja jogar novamente? (sim ou não)")
        if resposta and resposta.lower() == "sim":
            self.jogo_da_memoria()
        else:
            turtle.clear()
            turtle.penup()
            turtle.goto(0, 0)
            turtle.pendown()
            turtle.color("blue")
            turtle.write("Obrigado por jogar!", align="center", font=("Arial", 24, "normal"))
            turtle.update()
            sleep(2)
            print("Obrigado por jogar!")
            turtle.bye()

    # Método para registrar o ranking do jogador
    def registrar_ranking(self):
        iniciais = turtle.textinput("Ranking", "Insira suas iniciais (3 caracteres):")
        if iniciais and len(iniciais) == 3:
            dificuldade_texto = {
                "1": "Fácil",
                "2": "Médio",
                "3": "Difícil"
            }.get(self.dificuldade, "Desconhecida")

            # Adicionar novo registro
            with open(self.ranking_file, "a") as f:
                f.write(f"{iniciais.upper()} - Dificuldade: {dificuldade_texto}, Tentativas: {self.tentativas}, Erros: {self.erros}, Acertos: {self.acertos}\n")

            self.mostrar_ranking()

    # Método para mostrar o ranking dos jogadores
    def mostrar_ranking(self):
        turtle.clear()
        turtle.penup()
        turtle.goto(0, 100)
        turtle.color("black")
        turtle.write("Ranking", align="center", font=("Arial", 24, "normal"))
        turtle.update()
        with open(self.ranking_file, "r") as f:
            linhas = f.readlines()

        # Ordena o ranking pelo número de tentativas (em ordem crescente)
        linhas = sorted(linhas, key=lambda x: int(x.split(",")[1].split(":")[1].strip()))

        turtle.goto(0, 50)
        for linha in linhas[:10]:  # Mostra os primeiros 10 registros (os melhores)
            turtle.write(linha.strip(), align="center", font=("Arial", 16, "normal"))
            turtle.goto(0, turtle.ycor() - 30)

        turtle.update()
        self.jogar_novamente()

    # Método para escolher a dificuldade do jogo
    def escolher_dificuldade(self):
        tela = turtle.Screen()
        tela.title("Escolha a Dificuldade")
        turtle.hideturtle()
        turtle.penup()
        turtle.goto(0, 100)
        turtle.color("black")
        turtle.write("Escolha a Dificuldade", align="center", font=("Arial", 24, "normal"))
        turtle.goto(0, 50)
        turtle.color("green")
        turtle.write("1 - Fácil", align="center", font=("Arial", 18, "normal"))
        turtle.goto(0, 0)
        turtle.color("yellow")
        turtle.write("2 - Médio", align="center", font=("Arial", 18, "normal"))
        turtle.goto(0, -50)
        turtle.color("red")
        turtle.write("3 - Difícil", align="center", font=("Arial", 18, "normal"))
        turtle.update()
        dificuldade = turtle.textinput("Dificuldade", "Escolha a dificuldade (1, 2, 3):")
        tela.clear()
        return dificuldade

    # Método para perguntar ao jogador se deseja jogar novamente
    def jogar_novamente(self):
        resposta = turtle.textinput("Jogar Novamente", "Deseja jogar novamente? (sim ou não)")
        if resposta and resposta.lower() == "sim":
            self.jogo_da_memoria()
        else:
            turtle.clear()
            turtle.penup()
            turtle.goto(0, 0)
            turtle.pendown()
            turtle.color("blue")
            turtle.write("Obrigado por jogar!", align="center", font=("Arial", 24, "normal"))
            turtle.update()
            sleep(2)
            print("Obrigado por jogar!")
            turtle.bye()

    # Método principal do jogo
    def jogo_da_memoria(self):
        # Escolha da dificuldade
        self.dificuldade = self.escolher_dificuldade()
        if self.dificuldade not in ["1", "2", "3"]:
            print("Dificuldade inválida!")
            return

        # Inicialização das variáveis do jogo
        self.criar_matriz(self.dificuldade)
        self.primeira_pos = None
        self.segunda_pos = None
        self.tentativas = 0
        self.erros = 0
        self.acertos = 0
        self.revelacoes_restantes = 2

        # Configurações da tela do Turtle
        tela = turtle.Screen()
        tela.title("Jogo da Memória")
        turtle.hideturtle()
        turtle.penup()

        # Desenhar a matriz inicial
        turtle.tracer(0)
        self.desenhar_matriz()
        turtle.update()

        # Criação dos botões
        self.criar_botao("Revelar", -100, -200, self.revelar_jogo, cor_texto="purple")  # Cor do texto roxa
        self.criar_botao("Desistir", 100, -200, self.desistir, cor_texto="red")  # Cor do texto vermelha

        # Eventos do Turtle
        turtle.onscreenclick(self.on_click)
        turtle.done()

    # Método para criar um botão
    def criar_botao(self, texto, x, y, funcao, cor_texto="white"):
        botao = turtle.Turtle()
        botao.speed(0)
        botao.penup()
        botao.goto(x, y)
        botao.color(cor_texto)  # Cor do texto definida aqui
        botao.write(texto, align="center", font=("Arial", 16, "normal"))
        botao.goto(x, y - 20)
        botao.shape("square")
        botao.shapesize(stretch_wid=1.5, stretch_len=3)
        botao.fillcolor("blue")
        botao.onclick(funcao)
        return botao

    # Método para desistir do jogo
    def desistir(self, x, y):
        print("Você desistiu do jogo.")
        turtle.bye()

    # Método para revelar todas as células do jogo por 5 segundos
    def revelar_jogo(self, x, y):
        if self.revelacoes_restantes > 0:
            self.revelacoes_restantes -= 1
            celulas_nao_reveladas = [(i, j) for i in range(len(self.mat_exib)) for j in range(len(self.mat_exib[i])) if self.mat_exib[i][j] == '#']

            for i, j in celulas_nao_reveladas:
                self.mat_exib[i][j] = self.mat[i][j]

            self.desenhar_matriz()
            turtle.update()
            sleep(5)

            for i, j in celulas_nao_reveladas:
                self.mat_exib[i][j] = '#'

            self.desenhar_matriz()

# Instanciando e iniciando o jogo
if __name__ == "__main__":
    jogo = JogoMemoria()
    jogo.jogo_da_memoria()
