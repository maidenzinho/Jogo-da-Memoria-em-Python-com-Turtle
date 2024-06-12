# Jogo da Memória em Python com Turtle
### Turtle é uma interface gráfica para Python, criada pelo próprio time do Python, para entender melhor leia a documentação do Turtle no site do python.org
### No código é possível notar que o Turtle está espalhado pelo código base, pois com Turtle é necessário colocar certos parametros
# Um exemplo do que foi dito acima:
```
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
```
