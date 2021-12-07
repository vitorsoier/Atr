# Import modules
import turtle
import threading
import time

statusTiro = 0
player_dx = 15
libera_tiro = threading.Semaphore()
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

# definindo status do tiro:


def status_tiro():
    global statusTiro
    statusTiro = 1
    return (statusTiro)


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

# detectar o game over


'''def game_over():
    gameOver = turtle.Turtle()
    gameOver.color('#FF3333')
    gameOver.up()
    gameOver.hideturtle()
    nave.hideturtle()
    tiro.hideturtle()
    down_line.hideturtle()
    for invader in invaders:
        invader.hideturtle()
    gameOver.write("Game over", move=True, align='center',
                   font=('Arial', 40, 'normal'))
    pontos_pen.setposition(0, -30)
    pontos_pen.write('Score Final: %s' % pontos, align='center',
                     font=('Arial', 18, 'normal'))
'''
# detectar vitória


'''def win():
    vitoria = turtle.Turtle()
    vitoria.color('#52FF6A')
    vitoria.up()
    vitoria.hideturtle()
    nave.hideturtle()
    tiro.hideturtle()
    down_line.hideturtle()
    for invader in invaders:
        invader.hideturtle()
    vitoria.write("Você venceu!", move=True, align='center',
                  font=('Arial', 40, 'normal'))
    pontos_pen.setposition(0, -30)
    pontos_pen.write('Score Final: %s' % pontos, align='center',
                     font=('Arial', 18, 'normal'))
'''

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
    invader.shape('imagens/invaders1.gif')
    invader.penup()
    invader.speed(0)
    if count == 0:
        x = -210
        y = 220
    else:
        x += 100
    invader.setposition(x, y)
    count += 1

velocidade_invader = 2


def trajetoria_tiros():
    global pontos
    global statusTiro
    while True:
        # Função feita pra limitar a quantidade de tirosm contar pontos e ocultar tiro assim que passar da tela ou atingir um inimigo
        turtle.listen()
        turtle.onkey(direita, 'Right')
        turtle.onkey(esquerda, 'Left')
        turtle.onkey(status_tiro, 'space')
        if statusTiro == 1:
            libera_tiro.acquire()
            statusTiro = 0
            tiros_nave()
            while True:
                tiro.forward(velocidade_tiro)
                for invader in invaders:
                    if acertou(tiro, invader) and invader.isvisible():
                        tiro.hideturtle()
                        invader.hideturtle()
                        pontos += 50
                        pontos_pen.clear()
                        pontos_pen.write('Score: %s' % pontos)
                        libera_tiro.release()
                        statusTiro = 0
                        break
                if tiro.ycor() > 220:
                    tiro.hideturtle()
                    libera_tiro.release()
                    statusTiro = 0
                    break

# função para movimentar os invaders e chamar a função atualiza a tela


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
            if invader.ycor() < -120 and invader.isvisible():
                tela(invader)
                break
            if pontos == 250:
                tela(invader)
                break

# Mostra quando jogador perde ou ganha, atualiza a tela


def tela(invader):
    while True:
        if invader.ycor() < -120 and invader.isvisible():
            gameOver = turtle.Turtle()
            gameOver.color('#FF3333')
            gameOver.up()
            gameOver.hideturtle()
            nave.hideturtle()
            tiro.hideturtle()
            down_line.hideturtle()
            for invader in invaders:
                invader.hideturtle()
            gameOver.write("Game over", move=True, align='center',
                           font=('Arial', 40, 'normal'))
            pontos_pen.setposition(0, -30)
            pontos_pen.write('Score Final: %s' % pontos, align='center',
                             font=('Arial', 18, 'normal'))
            break
        if pontos == 250:
            vitoria = turtle.Turtle()
            vitoria.color('#52FF6A')
            vitoria.up()
            vitoria.hideturtle()
            nave.hideturtle()
            tiro.hideturtle()
            down_line.hideturtle()
            for invader in invaders:
                invader.hideturtle()
            vitoria.write("Você venceu!", move=True, align='center',
                          font=('Arial', 40, 'normal'))
            pontos_pen.setposition(0, -30)
            pontos_pen.write('Score Final: %s' % pontos, align='center',
                             font=('Arial', 18, 'normal'))
            break


thread1 = threading.Thread(target=trajetoria_tiros)
thread1.start()

thread2 = threading.Thread(target=invaders_move)
thread2.start()

thread3 = threading.Thread(target=tela)
thread3.start()


janela.mainloop()
