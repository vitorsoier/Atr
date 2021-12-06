# Import modules
import turtle
import threading
import time


player_dx = 15
# mover para esquerda


def esquerda():
    x = nave.xcor() - player_dx
    if x < -210:
        x = -210
    nave.setx(x)

# mover direita


def direita():
    x = nave.xcor() + player_dx
    if x > 200:
        x = 200
    nave.setx(x)

# tiros que a nave vai disparar


def tiros_nave():
    x = nave.xcor()
    y = nave.ycor()
    tiro.setposition(x, y+30)
    tiro.showturtle()

# detectar colisão entre tiros e personagens


def acertou(t1, t2):
    if abs(t1.xcor() - t2.xcor()) < 15 and abs(t1.ycor() - t2.ycor()) < 15:
        return True
    else:
        return False

# detectar se os invader chegaram até o fim da tela de jogo


        # definindo o tamanho da janela
janela = turtle.Screen()
janela.setup(height=560, width=560)
janela.bgcolor('#000124')
janela.title('Space Invaders By:Vitor Soier')

# definindo linha abaixo da nave
down_line = turtle.Turtle()
down_line.speed(0)
down_line.color('#00fd24')
down_line.up()
down_line.setposition(-220, -200)
down_line.down()
down_line.pensize(3.5)
down_line.forward(430)
down_line.hideturtle()

# definindo a pontuação
pontos = 0
pontos_pen = turtle.Turtle()
pontos_pen.speed(0)
pontos_pen.color('white')
pontos_pen.up()
pontos_pen.setposition(-220, -220)
pontos_pen.write('Score: %s' % pontos)
pontos_pen.hideturtle()


# definindo estilo para nave
turtle.register_shape('imagens/nave.gif')
turtle.register_shape('imagens/invaders1.gif')

nave = turtle.Turtle()
nave.shape('imagens/nave.gif')
nave.speed(0)
nave.up()
nave.setposition(0, -170)
nave.setheading(90)

# criando tiros da nave
tiro = turtle.Turtle()
tiro.speed(0)
tiro.color('white')
tiro.shape('circle')
tiro.up()
tiro.setheading(90)
tiro.shapesize(0.5, 0.5)
tiro.setposition(-400, -400)
# tiro.hideturtle()
velocidade_tiro = 15

invaders = []
# Add enemies to the list
for i in range(5):
    # Create the enemy
    invaders.append(turtle.Turtle())

count = 0
for invader in invaders:
    invader.color("red")
    invader.shape("circle")
    invader.penup()
    invader.speed(0)
    if count == 0:
        x = -210
        y = 220
    else:
        x += 100
    invader.setposition(x, y)
    count += 1

velocidade_invader = 5


def trajetoria_tiros():
    global pontos
    while True:
        tiro.forward(velocidade_tiro)

        # esperando os inputs acionarem as funcoes, utilizarei para criar a thread de movimentação
        turtle.listen()
        turtle.onkey(direita, 'Right')
        turtle.onkey(esquerda, 'Left')
        turtle.onkey(tiros_nave, 'space')

        for invader in invaders:
            if acertou(tiro, invader):
                tiro.hideturtle()
                invader.hideturtle()
                pontos += 50
                pontos_pen.clear()
                pontos_pen.write('Score: %s' % pontos)


def invaders_move():
    global velocidade_invader
    while True:
        for invader in invaders:
            localizacao_x = invader.xcor()
            localizacao_x += velocidade_invader
            invader.setx(localizacao_x)

            if (invader.xcor() > 220 or invader.xcor() < -220) and invader.isvisible():
                for inv in invaders:
                    y = inv.ycor()
                    y -= 10
                    inv.sety(y)
                velocidade_invader *= -1


thread1 = threading.Thread(target=trajetoria_tiros)
thread1.start()

thread2 = threading.Thread(target=invaders_move)
thread2.start()


janela.mainloop()
