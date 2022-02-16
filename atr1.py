# Import modules
import turtle
import time
import threading
import random
import math
import asyncio
import socket
import multiprocessing
from multiprocessing import Process
from datetime import datetime


statusTiro = 0
pause = 'jogando'
status = 0
invaders_tiros = 5
player_dx = 15
libera_tiro = threading.Semaphore()
invaders_tiro = threading.Semaphore(invaders_tiros)
register_dead = ""
inicio = time.time()
fim_jogo = True
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

def acertou_nave(t1, t2):
    if math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2)) <= 15 and t1.isvisible:
        return True
    else:
        return False



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

#criando vetor dos tiros do invasor:
tiros_inv = []
for i in range(invaders_tiros):
    tiros_inv.append(turtle.Turtle())
for tiro_inv in tiros_inv:
    tiro_inv.hideturtle()
    tiro_inv.shape("circle")
    tiro_inv.color("red")
    tiro_inv.shapesize(0.5, 0.5)
    tiro_inv.speed(0)
    tiro_inv.up()
    tiro_inv.setheading(270)

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

def sair_jogo():
    janela.bye()

def pausar_jogo():
    global pause
    global invaders
    if pause == 'jogando':
        pause = 'pausado'
    else:
        pause.clear()
        pontos_pen.clear()
        nave.showturtle()
        tiro.showturtle()
        down_line.showturtle()
        for invader in invaders:
            invader.showturtle()
        time.sleep(2)
        pause= 'jogando'


        


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
    global invaders_tiros
    global status
    global pause
    while True:
        if pause == 'pausado':
            pause = turtle.Turtle()
            pause.color('#FFD700')
            pause.up()
            pause.hideturtle()
            nave.hideturtle()
            tiro.hideturtle()
            tiros_inv.clear()
            down_line.hideturtle()
            for invader in invaders:
                invader.hideturtle()
            pause.write("PAUSE", move=True, align='center',
                            font=('Arial', 40, 'normal'))
            pontos_pen.setposition(0, -30)
            pontos_pen.write('Score Atual: %s' % pontos, align='center',
                                font=('Arial', 18, 'normal'))
        else:
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
                #sortear disparo de invasor acontece ou não
                disparo = random.randint(0,100)
                if (disparo%11) == 0:
                    if invaders_tiros > 0 and invader.isvisible() and not tiros_inv[invaders_tiros-1].isvisible():
                        invaders_tiro.acquire()
                        x, y = invader.xcor(), invader.ycor() - 10
                        tiros_inv[invaders_tiros - 1].setpos(x, y)
                        tiros_inv[invaders_tiros - 1].showturtle()
                        invaders_tiros -= 1
                            # Movimentando tiros_inv inimigos e verificando colisão com o jogador ou saida da tela de jogo
                    for n in range(len(tiros_inv)):
                        if tiros_inv[n].isvisible():
                            tiros_inv[n].forward(15)
                            if tiros_inv[n].ycor() <= -210:
                                invaders_tiros += 1
                                tiros_inv[n].hideturtle()
                                invaders_tiro.release()
                            elif acertou_nave(tiros_inv[n], nave):
                                tiros_inv[n].hideturtle()
                                down_line.hideturtle()
                                invaders_tiro.release()
                                invaders_tiros += 1
                                status = 1
                                break
        if status == 1:
            tela(invader)
            break    



# Mostra quando jogador perde ou ganha, atualiza a tela
def tela(invader):
    global status
    global fim_jogo
    while True:
        if (invader.ycor() < -120 and invader.isvisible()) or status == 1:
            gameOver = turtle.Turtle()
            gameOver.color('#FF3333')
            gameOver.up()
            gameOver.hideturtle()
            nave.hideturtle()
            tiro.hideturtle()
            tiros_inv.clear()
            down_line.hideturtle()
            for invader in invaders:
                invader.hideturtle()
            gameOver.write("Game over", move=True, align='center',
                           font=('Arial', 40, 'normal'))
            pontos_pen.setposition(0, -30)
            pontos_pen.write('Score Final: %s' % pontos, align='center',
                             font=('Arial', 18, 'normal'))
            register_dead = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            fim_jogo = False
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
            fim_jogo = False                 
            break

def menu():
    turtle.onkey(sair_jogo, 'e')
    turtle.onkey(pausar_jogo, 'p')

class init(Process):
    def __init__(self, host, port, log):
        super().__init__()
        self.address = (host, port)
        self.log = log.value.decode()

        

class cloud_process(init):   
    def run(self):
        f=open("info.txt","a")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.address)
        self.s.listen(1)
        conn, addr = self.s.accept()

        while True:
            data_hora_min = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dados = conn.recv(1024)
            if not dados:
                break
            elif dados.decode() == "kill":
                print(f"[{data_hora_min}] Jogo Finalizado",file=f)
                f.close()
                self.s.close()
            else:
                print(dados.decode(),file=f)

def LoggerProcess(host,port):
    global pontos
    global register_dead
    global fim_jogo
    soketinho = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soketinho.connect((host,port))
    while True:
        time.sleep(5)
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tempo_de_vida = time.time() - inicio
        if register_dead != "":
            text = "["+data +"] Pontuação: "+str(pontos)+" Tempo de game: "+ str(tempo_de_vida)+ " segundos " + " Você morreu em: "+ register_dead 
        else:
            text = "["+data +"] Pontuação: "+str(pontos)+" Tempo de game: "+ str(tempo_de_vida)+ " segundos " 
        if fim_jogo and register_dead != "":
            text = "["+data +"] Pontuação: "+str(pontos)+" Tempo de game: "+ str(tempo_de_vida)+ " segundos " + " Você morreu em: "+ register_dead 
            envia = text.encode()
            time.sleep(1)
            soketinho.send(envia)
            text = "kill"
            envia = text.encode()
            time.sleep(1)
            soketinho.send(envia)
            soketinho.close()
        elif fim_jogo:
            text = "kill"
            envia = text.encode()
            time.sleep(1)
            soketinho.send(envia)
            soketinho.close()
        envia = text.encode()
        time.sleep(1)
        soketinho.send(envia)

host = 'localhost'
port = 8008

horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log = "["+horario+"] Game started"
logMP = multiprocessing.Array('c', log.encode())
    
cloud = cloud_process(host, port,logMP)
cloud.start()

thread1 = threading.Thread(target=trajetoria_tiros)
thread1.start()

thread2 = threading.Thread(target=invaders_move)
thread2.start()

thread3 = threading.Thread(target=tela)
thread3.start()

thread4 = threading.Thread(target=menu)
thread4.start()

thread5 = threading.Thread(target=LoggerProcess, args=(host,port))
thread5.start()


janela.mainloop()
