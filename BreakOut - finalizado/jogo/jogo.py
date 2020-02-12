import arcade
import math
import random
from bola.bola import Bola
from player.player import Player
from fases.fase import Fase
from fases.menu import Menu
from objetos.powerup import Powerup


#Aqui estão as variaveis consideradas constantes.
LARGURA_TELA = 800
ALTURA_TELA = 800
TITULO_TELA = "BreakOUT"
AJUDA = -2
GAME_OVER = -1
MENU = 0
FASE1 = 1
FASE2 = 2
FASE3 = 3
FASE4 = 4
FASE5 = 5
TELA_FINAL = 6
FONTE = "jogo/font/breakOUT.ttf"
SIMBOLO = "jogo/font/Wingding.ttf"

class Jogo(arcade.Window):

    #Metodo init para inicializar a janela do jogo e alguns metodos necessários
    def __init__(self, largura, altura, titulo):
        super().__init__(largura, altura, title=titulo)
        #O estado do jogo é o que vai definir como o jogo irá funcionar de acordo com determinadas situações
        #Ele fica setado inicialmente pro Menu, mas apos isso ele vai se alterando dependendo das escolhas do jogador, alem da sua capacidade de passar de fase, etc.
        self.estado_jogo = MENU
        arcade.set_background_color((0,0,0))
        #O modo de jogo dirá com quantos players o jogo ira funcionar, sendo posto como 0 no iniciar do jogo.
        self.modo_de_jogo = 0
        #Vidas dos jogadores.
        self.vidas = 0
        #Pontuação dos players
        self.pontuacao = 0
    """
    A função setup inicializa metodos e atributos quando chamado.
    É uma função do python arcade.   
    """
    def setup(self):
        #O jogo se inicia pausado, afim de faciliar para o jogador na hora da passagem de fase, dando a opção de lançar a bola.
        self.jogo_pausado = True
        #Para que a bola permaneça pausada no inicio de cada fase, colocamos esse atributo especifico para essa tarefa.
        self.pausa_bola = 0
        #Aqui se encontram as listas do jogo, onde ficarão os sprites.
        self.lista_bola = arcade.SpriteList()
        self.lista_blocos = arcade.SpriteList()
        self.lista_power_up = arcade.SpriteList()
        self.lista_jogador = arcade.SpriteList()
        self.lista_jogador2 = arcade.SpriteList()
        #O aleatorio_powerup é um atributo que determinara os power_ups aleatoriamentes, quando um bloco power_up for quebrado.
        self.aleatorio_powerup = 0
        #Ambos os contadores de colisao_paredes servem para garantir que a bola não saia do campo de visão do jogador.
        self.contador_colisao_paredes_vertical = 0
        self.contador_colisao_paredes_horizontal = 0
        #O bloco delay serve para amenizar o contato da bola com os blocos, afim de que minimize os bugs de colisão.
        self.bloco_delay =-1
        #Para pôr tempo nos power_ups escolhemos manualmente fazer os contadores, sendo o contador_tempo o tempo total do power_up
        #e o contador variador o qual ira zerar o tempo do powerup. Temos dois de cada, pois há a opção de dois players.
        self.contador_tempo_power_up_1 = 600
        self.contador_variador_1 = 0
        self.contador_tempo_power_up_2 = 600
        self.contador_variador_2 = 0
        #A função run serve para realizar ações dependendo do estado do jogo.
        self.run(self.estado_jogo)
        #Se o modo de jogo for 1, ira ser posto apenas 1 player, se for dois, dois players.
        if self.modo_de_jogo == 1:
            self.lista_jogador.append(Player('jogo/player/imagens/barra_normal.png',1,8,arcade.key.LEFT,arcade.key.RIGHT,LARGURA_TELA/2,64 ))
        if self.modo_de_jogo == 2:
            self.lista_jogador.append(Player('jogo/player/imagens/barra_normal.png',1,8,arcade.key.LEFT,arcade.key.RIGHT,64,64 ))
            self.lista_jogador2.append(Player('jogo/player/imagens/barra_normal.png',1,8,arcade.key.A,arcade.key.D,LARGURA_TELA-64,64 ))
        #Se o jogo não estiver no menu,game_over,tela de ajuda, ou tela final haverá a bola no jogo.
        if self.estado_jogo!=MENU and self.estado_jogo!=GAME_OVER and self.estado_jogo!=AJUDA and self.estado_jogo!=TELA_FINAL:
            for player in self.lista_jogador:
                self.lista_bola.append(Bola(player.center_x+player.width/4,96))
                break
        #Cada nova fase ira iniciar com 3 vidas.
        self.set_vida(3)

    #Seta a vida dos jogadores
    def set_vida(self,vida):
        self.vidas = vida
    #Retorna o quanto de vida os jogadores possuem
    def get_vida(self):
        return self.vidas
    #Adiciona vida ao player, esse adicionar pode tbm ser negativo se assim for o objetivo
    def adicionar_vida(self,vida):
        self.vidas+=vida
    #Seta a pontuação dos jogadores
    def set_pontuacao(self,pontuacao):
        self.pontuacao = pontuacao
    #Retorna o quanto de pontos os jogadores possuem
    def get_pontuacao(self):
        return self.pontuacao
    #Adiciona pontuação dependendo do tanto de blocos que os jogadores eliminam
    def adicionar_pontuacao(self,pontuacao):
        self.pontuacao+=pontuacao
    """
        Como dito antes, a função run irá organizar as fases dependendo do estado do jogo, chamando a clase fase, que irá dar o mapa
    correto a cada circunstância.
    """
    def run(self,situacao_atual_jogo):
        fase = Fase()

        if situacao_atual_jogo ==FASE1:
            fase.determinar_fase(1)
            self.lista_blocos = fase.get_fase() 
            self.lista_power_up = fase.get_power_up() 

        if situacao_atual_jogo ==FASE2:
            fase.determinar_fase(2)
            self.lista_power_up = fase.get_power_up() 
            self.lista_blocos= fase.get_fase() 

        if situacao_atual_jogo ==FASE3:
            fase.determinar_fase(3)
            self.lista_power_up = fase.get_power_up() 
            self.lista_blocos= fase.get_fase() 

        if situacao_atual_jogo ==FASE4:
            fase.determinar_fase(4)
            self.lista_power_up = fase.get_power_up() 
            self.lista_blocos= fase.get_fase()

        if situacao_atual_jogo ==FASE5:
            fase.determinar_fase(5)
            self.lista_power_up = fase.get_power_up() 
            self.lista_blocos= fase.get_fase()

    """
    On_key_press é uma função do arcade que permite que ao clicar de uma tecla se realize determinado tipo de ação.
    Aqui ocorre o movimento dos jogadores, alem da mudança do estado do jogo na parte do menu, tela final, ajuda e game over.
    """
    def on_key_press(self, key, modifiers):
        for player in self.lista_jogador:
            player.on_key_press(key, modifiers)
        for player in self.lista_jogador2:
            player.on_key_press(key, modifiers)
        if self.estado_jogo == 0:
            if key == arcade.key.NUM_1:
                self.estado_jogo +=1
                self.modo_de_jogo = 1
                self.setup()
            if key == arcade.key.NUM_2:
                self.estado_jogo +=1
                self.modo_de_jogo = 2
                self.setup()
            if key == arcade.key.NUM_3:
                self.estado_jogo = AJUDA
                self.modo_de_jogo = 0
                self.setup()
        if self.estado_jogo == AJUDA:
            if key == arcade.key.NUM_4:
                self.estado_jogo = MENU
                self.setup()
        if self.estado_jogo == TELA_FINAL:
            if key == arcade.key.ENTER:
                self.estado_jogo = MENU
                self.setup()
        if self.estado_jogo == GAME_OVER:
            if key == arcade.key.ENTER:
                self.estado_jogo = MENU
                self.setup()
    """
    No on_key_release irá ocorrer as ações apos que voce solte determinada tecla. 
    Nessa parte, ficara o sistema de pause do jogo.
    """
    def on_key_release(self, key, modifiers):

        for player in self.lista_jogador:
            player.on_key_release(key, modifiers)
        
        for player in self.lista_jogador2:
            player.on_key_release(key, modifiers)

        if self.estado_jogo>0 and self.estado_jogo!=6:
            if key == arcade.key.ENTER :
                if self.jogo_pausado == False:
                    self.jogo_pausado= True 
                    self.pausa_bola = 1      
                else:
                    self.jogo_pausado = False
                    self.pausa_bola =0
                
    """
    A função on_draw pertence ao arcade e serve para basicamente desenhar as coisas na tela.
    E por causa dessa função que as fases, os blocos, as telas, os players, enfim, pratimante o jogo todo fica visivel.
    Vale ressaltar que dependendo do estado de jogo coisas diferentes serão desenhadas na tela.
    """
    def on_draw(self):
        arcade.start_render() 
        self.lista_bola.draw()
        self.lista_jogador.draw() 
        self.lista_jogador2.draw()
        blocos_sobrando = f"{len(self.lista_blocos)}"
        vidas = f"{self.get_vida()}"
        arcade.draw_text("Vidas: "+str(vidas), LARGURA_TELA-128, 0,
                         arcade.color.WHITE, 20,font_name=FONTE)
        arcade.draw_text("Blocos: "+blocos_sobrando, 0, 0,
                         arcade.color.WHITE, 20,font_name=FONTE)  
        if self.estado_jogo == FASE1:                              
            self.lista_blocos.draw()
            self.lista_power_up.draw()
            arcade.draw_text("-Fase 1-", LARGURA_TELA/2-60, 0,
                         arcade.color.WHITE, 20,font_name=FONTE)
        if self.estado_jogo == FASE2:                              
            self.lista_blocos.draw()
            self.lista_power_up.draw()
            arcade.draw_text("-Fase 2-", LARGURA_TELA/2-60, 0,
                         arcade.color.WHITE, 20,font_name=FONTE)
        if self.estado_jogo == FASE3:                              
            self.lista_blocos.draw()
            self.lista_power_up.draw()
            arcade.draw_text("-Fase 3-", LARGURA_TELA/2-60, 0,
                         arcade.color.WHITE, 20,font_name=FONTE)
        if self.estado_jogo == FASE4:                              
            self.lista_blocos.draw()
            self.lista_power_up.draw()
            arcade.draw_text("-Fase 4-", LARGURA_TELA/2-60, 0,
                         arcade.color.WHITE, 20,font_name=FONTE)
        if self.estado_jogo == FASE5:                              
            self.lista_blocos.draw()
            self.lista_power_up.draw()
            arcade.draw_text("-Fase 5-", LARGURA_TELA/2-60, 0,
                         arcade.color.WHITE, 20,font_name=FONTE)
        pontuacao = f"{self.get_pontuacao()}"
        arcade.draw_text("Pontuação: "+pontuacao, 2, ALTURA_TELA-64,
                         arcade.color.PINK_SHERBET, 20,font_name=FONTE)
        arcade.draw_text("Pontuação: "+pontuacao, 0, ALTURA_TELA-64,
                         arcade.color.WHITE, 20,font_name=FONTE)
        if self.jogo_pausado == True and (self.estado_jogo!=0 and self.estado_jogo!=-1) and self.pausa_bola ==1:
            menu = Menu()
            menu.desenhar_pause(FONTE,SIMBOLO)
        if self.estado_jogo == TELA_FINAL:
            menu = Menu()
            menu.desenhar_tela_agradecimento(FONTE,SIMBOLO)
        if self.estado_jogo == AJUDA:
            menu = Menu()
            menu.desenhar_tela_ajuda(FONTE,SIMBOLO)
        if self.estado_jogo == GAME_OVER:
            menu = Menu()
            menu.desenhar_game_over(FONTE,SIMBOLO)
        if self.estado_jogo == MENU:
            menu = Menu()
            menu.desenhar_tela_menu(FONTE,SIMBOLO)

    """
    Aqui obtemos a colisão entre a parede e a bola, assegurando que a bola não escape da tela.
    """
    def colisao_parede_bola(self):
        #Se a bola tentar aflingir os limites de largura da parede, ela ira para o lado oposto.
        for bola in self.lista_bola:
            if (bola.center_x+32 > LARGURA_TELA or bola.center_x < 32) and self.contador_colisao_paredes_vertical <= 0 :
                bola.center_x += -bola.vetor_x
                bola.center_y += -bola.vetor_y
                bola.vetor_x = - bola.vetor_x
                som = arcade.Sound('jogo/sons/somparede.wav')
                som.play()
                self.contador_colisao_paredes_vertical = 1
        #Se a bola tentar chegar ao teto ela será mandada ao lado oposto.
            if (bola.center_y+32 > ALTURA_TELA) and self.contador_colisao_paredes_horizontal <= 0:
                bola.center_x += -bola.vetor_x
                bola.center_y += -bola.vetor_y
                bola.vetor_y = - bola.vetor_y
                som = arcade.Sound('jogo/sons/somparede.wav')
                som.play()
                self.contador_colisao_paredes_horizontal = 1
        #Se a bola sair do limite e cair da tela no canto inferior ela irá ser removida da lista de bolas e jogador perderá uma vida.
        #Em seguida ela sera posta ao jogo novamente até que a vida dos jogadores chegue a zero.
            if bola.center_y<32:
                bola.kill()
                self.adicionar_vida(-1)
                for player in self.lista_jogador:
                    self.lista_bola.append(Bola(player.center_x+player.width/4,96))
                    break
                break

    """
    Aqui é onde conferimos a colisão da bola com os blocos basicamente.
    """
    def colisao_blocos_bola(self):
        #Se a bola bater no bloco, o bloco é eliminado da lista
        for bloco in self.lista_blocos:
            for bola in self.lista_bola:
                batida = arcade.check_for_collision_with_list(bloco,self.lista_bola)
                if (len(batida)>0) and (self.bloco_delay<=0):
                    if abs(bola.center_x - bloco.center_x) < abs(bola.center_y- bloco.center_y):
                        bola.vetor_y = -bola.vetor_y
                    if abs(bola.center_y- bloco.center_y) < abs(bola.center_x - bloco.center_x):
                        bola.center_x += -bola.vetor_x
                        bola.center_y += bola.vetor_y
                        bola.vetor_x = -bola.vetor_x
                    som = arcade.Sound('jogo/sons/sombloco.wav')
                    self.bloco_delay =2
                    self.adicionar_pontuacao(1)
                    som.play()
                    bloco.kill()
                    break

        #Se a bola bater em um bloco que é power_up, o bloco é eliminado da lista, e um novo power up é lançado para que o jogador possa pegar.
        for powerup in self.lista_power_up:
            for bola in self.lista_bola:
                batida = arcade.check_for_collision_with_list(powerup,self.lista_bola)
                if len(batida)>0: 
                    som = arcade.Sound('jogo/sons/sombloco.wav')
                    som.play()
                    self.lista_power_up.append(Powerup('jogo/objetos/imagens/powerup.png',powerup.center_x,powerup.center_y,10))
                    powerup.kill()
                    self.adicionar_pontuacao(1)
                    self.lista_power_up.draw()
                    break
    #Aqui se detecta a colisão de ambos os players com a bola. Se isso ocorrer ela é rebatida.
    def colisao_players_bola(self):
        for bola in self.lista_bola:
            for player in self.lista_jogador:
                batida = arcade.check_for_collision_with_list(bola, self.lista_jogador)
                diferenca = player.center_x-bola.center_x
                if  len(batida) >0:
                    bola.vetor_x = (math.cos(math.pi/2+diferenca/256*(math.pi))*10)
                    bola.vetor_y = (math.sin(math.pi/2+diferenca/256*(math.pi))*10)
                    som = arcade.Sound('jogo/sons/somplayer.wav')
                    som.play()
                    break

        for bola in self.lista_bola:
            for player in self.lista_jogador2:
                batida = arcade.check_for_collision_with_list(bola, self.lista_jogador2)
                diferenca = player.center_x-bola.center_x
                if  len(batida) >0:
                    bola.vetor_x = (math.cos(math.pi/2+diferenca/256*(math.pi))*10)
                    bola.vetor_y = (math.sin(math.pi/2+diferenca/256*(math.pi))*10)
                    som = arcade.Sound('jogo/sons/somplayer.wav')
                    som.play()
                    break
    """Aqui se detecta a colisão de ambos os players com o power_up. Se for detectada, será sorteado um numero aleatorio que determinará
       qual tipo de power_up o player pegará, com auxilio da função power_up.
    """               
    def colisao_players_power_up(self):
        for power in self.lista_power_up:
            for player in self.lista_jogador:
                batida = arcade.check_for_collision_with_list(power, self.lista_jogador)
                if  len(batida) >0:
                    power.kill()
                    self.aleatorio_powerup = random.randint(1, 6)
                    self.funcao_powerup(self.aleatorio_powerup,1)
                    som = arcade.Sound('jogo/sons/somplayer.wav')
                    som.play()
                    break
        for power in self.lista_power_up:
            for player in self.lista_jogador2:
                batida = arcade.check_for_collision_with_list(power, self.lista_jogador2)
                if  len(batida) >0:
                    power.kill()
                    self.aleatorio_powerup = random.randint(1, 5)
                    self.funcao_powerup(self.aleatorio_powerup,2)                 
                    som = arcade.Sound('jogo/sons/somplayer.wav')
                    som.play()
                    break
    """Aqui se detecta a colisão de ambos os players com as paredes. Essa função não deixara que os jogadores saiam dos limites da tela.
        Se percebe que dependendo do modo do jogo(1 ou 2 players), a colisao é alterada, pois no dois players, os jogadores so poderao
        ir ate metade da tela, dependendo de seu lado inicial.
    """               
    def colisao_players_parede(self):
        if self.modo_de_jogo == 1:
            for player in self.lista_jogador:
                if player.center_x+player.width/2> LARGURA_TELA:
                    player.center_x = LARGURA_TELA - player.width/2
                if player.center_x < player.width/2:
                    player.center_x = player.width/2
        if self.modo_de_jogo == 2:
            for player in self.lista_jogador:
                if player.center_x+player.width/2> LARGURA_TELA:
                    player.center_x = LARGURA_TELA - player.width/2
                if player.center_x < player.width/2:
                    player.center_x = player.width/2
                if player.center_x+player.width/2> LARGURA_TELA/2:
                    player.center_x = LARGURA_TELA/2 -player.width//2
            for player in self.lista_jogador2:
                if player.center_x+player.width/2> LARGURA_TELA:
                    player.center_x = LARGURA_TELA - player.width/2
                if player.center_x < player.width/2:
                    player.center_x = player.width/2
                if player.center_x+player.width/2< LARGURA_TELA/2+player.width:
                    player.center_x = LARGURA_TELA/2 + player.width/2
    """
    O fim powerup serve para acabar com o efeito do powerup se o tempo do contador chegar em zero.
    """
    def fim_powerup(self):
        for player in self.lista_jogador:
            if self.contador_tempo_power_up_1 < 0:
                self.lista_jogador.append(Player('jogo/player/imagens/barra_normal.png',1,8,arcade.key.LEFT,arcade.key.RIGHT,player.center_x,64 ))
                player.kill()
                self.contador_variador_1 = 0
                self.contador_tempo_power_up_1 = 600


        for player in self.lista_jogador2:
            if self.contador_tempo_power_up_2 < 0:
                self.lista_jogador2.append(Player('jogo/player/imagens/barra_normal.png',1,8,arcade.key.A,arcade.key.D,player.center_x,64 ))
                player.kill()
                self.contador_variador_2 = 0
                self.contador_tempo_power_up_2 = 600

    """
    A função powerup ira determinar de acordo com o numero recebido com a obtenção do power_up, qual será o efeito sobre o jogador.
    Observasse que pode ser um efeito bom ou ruim.
    """
    def funcao_powerup(self,numero_recbido,jogador):
        if jogador == 1:
            for player in self.lista_jogador:
                if (numero_recbido==1):
                    self.lista_jogador.append(Player('jogo/player/imagens/barra_pequena.png',1,8,arcade.key.LEFT,arcade.key.RIGHT,player.center_x,64 ))
                    player.kill()
                    numero_recbido = 0
                    self.contador_tempo_power_up_1 = 600
                    self.contador_variador_1 = -1
                elif (numero_recbido==2):
                    self.lista_jogador.append(Player('jogo/player/imagens/barra_grande.png',1,8,arcade.key.LEFT,arcade.key.RIGHT,player.center_x,64 ))
                    player.kill()
                    numero_recbido = 0
                    self.contador_tempo_power_up_1 = 600
                    self.contador_variador_1 = -1
                elif (numero_recbido==3):
                    self.lista_jogador.append(Player('jogo/player/imagens/barra_inversa.png',1,8,arcade.key.RIGHT,arcade.key.LEFT,player.center_x,64 ))
                    player.kill()
                    numero_recbido = 0
                    self.contador_tempo_power_up_1 = 600
                    self.contador_variador_1 = -1
                elif (numero_recbido==4):
                    self.lista_jogador.append(Player('jogo/player/imagens/barra_rapida.png',1,16,arcade.key.LEFT,arcade.key.RIGHT,player.center_x,64 ))
                    player.kill()
                    numero_recbido = 0
                    self.contador_tempo_power_up_1 = 600
                    self.contador_variador_1 = -1
                elif (numero_recbido==5):
                    self.adicionar_vida(1)
                    numero_recbido = 0

        if jogador == 2:   
            for player in self.lista_jogador2:
                if (numero_recbido==1):
                    self.lista_jogador2.append(Player('jogo/player/imagens/barra_pequena.png',1,8,arcade.key.A,arcade.key.D,player.center_x,64 ))
                    player.kill()
                    numero_recbido = 0
                    self.contador_tempo_power_up_2 = 600
                    self.contador_variador_2 = -1
                elif (numero_recbido==2):
                    self.lista_jogador2.append(Player('jogo/player/imagens/barra_grande.png',1,8,arcade.key.A,arcade.key.D,player.center_x,64 ))
                    player.kill()
                    numero_recbido = 0
                    self.contador_tempo_power_up_2 = 600
                    self.contador_variador_2 = -1
                elif (numero_recbido==3):
                    self.lista_jogador2.append(Player('jogo/player/imagens/barra_inversa.png',1,8,arcade.key.D,arcade.key.A,player.center_x,64 ))
                    player.kill()
                    numero_recbido = 0
                    self.contador_tempo_power_up_2 = 600
                    self.contador_variador_2 = -1
                elif (numero_recbido==4):
                    self.lista_jogador2.append(Player('jogo/player/imagens/barra_rapida.png',1,16,arcade.key.A,arcade.key.D,player.center_x,64 ))
                    player.kill()
                    numero_recbido = 0
                    self.contador_tempo_power_up_2 = 600
                    self.contador_variador_2 = -1
                elif (numero_recbido==5):
                    self.adicionar_vida(1)
                    numero_recbido = 0
    """
    A função update é pertencente ao arcade e serve para sempre atualizar as funções e atributos do jogo.
    Ela irá funcionar se o jogo não estiver pausado, e não estiver em uma tela de menu (ajuda,game_over,menu inicial ou tela final de agradecimento).
    """
    def update(self, delta_time):
        if (self.estado_jogo!=MENU and self.estado_jogo!=GAME_OVER and self.estado_jogo!=TELA_FINAL and self.estado_jogo!=AJUDA) and (self.jogo_pausado==False):
            self.lista_jogador.update()
            self.lista_jogador2.update()
            self.lista_blocos.update()
            self.lista_jogador.update_animation()
            self.lista_jogador2.update_animation()
            self.bloco_delay += (-1)
            self.colisao_parede_bola()
            self.colisao_players_parede()
            self.colisao_players_bola()
            self.colisao_players_power_up()
            self.colisao_blocos_bola()
            self.contador_tempo_power_up_1 += self.contador_variador_1
            self.contador_tempo_power_up_2 += self.contador_variador_2
            self.contador_colisao_paredes_horizontal+=(-1)
            self.contador_colisao_paredes_vertical+=(-1)
            self.fim_powerup()
            if self.get_vida() <0:
                self.estado_jogo = GAME_OVER
                self.set_pontuacao(0)
                self.setup()
            if self.estado_jogo>0:
                if len(self.lista_blocos) == 0 and self.estado_jogo!=6:
                    self.estado_jogo += 1
                    self.setup()
            for power in self.lista_power_up:
                power.moverpowerup()
            for bola in self.lista_bola:
                bola.moverbola()
        
def main():
    window = Jogo(LARGURA_TELA, ALTURA_TELA, TITULO_TELA)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()