import arcade

"""
A classe menu serve para formar as telas de menu, como o menu principal, a tela de ajuda, o game over, pause e a tela final.
"""
class Menu:

    def desenhar_tela_menu(self,fonte,simbolo):
        arcade.start_render()
        self.imagem = arcade.load_texture('jogo/fases/imagens/menu.png')
        arcade.draw_texture_rectangle(800 // 2, 800 // 2,
                                      800, 800, self.imagem)   
        arcade.draw_text("1 jogador-aperte 1", 120, 800//2-64,
                         arcade.color.BLACK, 30,font_name=fonte)    
        arcade.draw_text("1 jogador-aperte 1", 125, 800//2-64,
                         arcade.color.WHITE, 30,font_name=fonte)
        arcade.draw_text("2 jogadores-aperte 2", 120, 800//2-64-64,
                         arcade.color.BLACK, 30,font_name=fonte)
        arcade.draw_text("2 jogadores-aperte 2", 125, 800//2-64-64,
                         arcade.color.WHITE, 30,font_name=fonte)
        arcade.draw_text("Controles - aperte 3", 120, 800//2-64-64-128,
                         arcade.color.PINK_SHERBET, 30,font_name=fonte)
        arcade.draw_text("Controles - aperte 3", 125, 800//2-64-64-128,
                         arcade.color.WHITE, 30,font_name=fonte)


    def desenhar_game_over(self,fonte,simbolo):
        arcade.draw_rectangle_filled(center_x = 800//2,center_y = 800//2 ,width=800, height = 800,color=arcade.color.BLACK)
        arcade.draw_text("GAME OVER", 140, 800//2,
                         arcade.color.SHOCKING_PINK, 64,font_name=fonte) 
        arcade.draw_text("GAME OVER", 150, 800//2,
                         arcade.color.WHITE, 64,font_name=fonte) 
        arcade.draw_text("Enter == Restart", 150+29, 800//2-74,
                         arcade.color.SHOCKING_PINK, 32,font_name=fonte)
        arcade.draw_text("Enter == Restart", 150+32, 800//2-74,
                         arcade.color.WHITE, 32,font_name=fonte)
        arcade.draw_text("U N U", 800//2-80, 800//2-(74*3),
                         arcade.color.WHITE, 64,font_name=simbolo)  


    def desenhar_pause(self,fonte,simbolo):
        arcade.draw_text("Pausado", 250-35, 800//2,
                         arcade.color.EGYPTIAN_BLUE	, 64,font_name=fonte) 
        arcade.draw_text("Pausado", 250-25, 800//2,
                         arcade.color.AMERICAN_ROSE, 64,font_name=fonte) 

        arcade.draw_text("Enter == continuar", 150+20, 800//2-74,
                         arcade.color.FLIRT, 32,font_name=fonte)
        arcade.draw_text("Enter == continuar", 150+25, 800//2-74,
                         arcade.color.HOT_PINK	, 32,font_name=fonte)

    def desenhar_tela_ajuda(self,fonte,simbolo):
        arcade.start_render()
        self.imagem = arcade.load_texture('jogo/fases/imagens/ajuda.png')
        arcade.draw_texture_rectangle(800 // 2, 800 // 2,
                                      800, 800, self.imagem)  
        arcade.draw_text("Jogador 1 - setinhas", 120, 550,
                         arcade.color.PURPLE_HEART,25,font_name=fonte)     
        arcade.draw_text("Jogador 1 - setinhas", 125, 550,
                         arcade.color.WHITE,25,font_name=fonte)
        arcade.draw_text("Jogador 2 - A e D", 120, 500,
                         arcade.color.PURPLE_HEART, 25,font_name=fonte)
        arcade.draw_text("Jogador 2 - A e D", 125, 500,
                         arcade.color.WHITE, 25,font_name=fonte)
        arcade.draw_text("Lançar bola - ENTER", 120, 450,
                         arcade.color.PURPLE_HEART, 25,font_name=fonte)
        arcade.draw_text("Lançar bola - ENTER", 125, 450,
                         arcade.color.WHITE, 25,font_name=fonte)
        arcade.draw_text("Pausar/Despausar - ENTER", 120, 400,
                         arcade.color.PURPLE_HEART, 25,font_name=fonte)
        arcade.draw_text("Pausar/Despausar - ENTER", 125, 400,
                         arcade.color.WHITE, 25,font_name=fonte)
        arcade.draw_text("Voltar - 4", 120, 150,
                         arcade.color.PURPLE_HEART, 25,font_name=fonte)
        arcade.draw_text("Voltar - 4", 125, 150,
                         arcade.color.WHITE, 25,font_name=fonte)


    def desenhar_tela_agradecimento(self,fonte,simbolo):
        arcade.start_render()
        self.imagem = arcade.load_texture('jogo/fases/imagens/agradecimento.png')
        arcade.draw_texture_rectangle(800 // 2, 800 // 2,
                                      800, 800, self.imagem)  
        arcade.draw_text("Jogo desenvolvido por: ", 120, 450,
                         arcade.color.PURPLE_HEART,25,font_name=fonte)     
        arcade.draw_text("Jogo desenvolvido por: ", 125, 450,
                         arcade.color.WHITE,25,font_name=fonte)
        arcade.draw_text("Eduardo Brandt", 180, 400,
                         arcade.color.PURPLE_HEART, 25,font_name=fonte)
        arcade.draw_text("Eduardo Brandt", 185, 400,
                         arcade.color.WHITE, 25,font_name=fonte)
        arcade.draw_text("Gabriel Harmel", 180, 350,
                         arcade.color.PURPLE_HEART, 25,font_name=fonte)
        arcade.draw_text("Gabriel Harmel", 185, 350,
                         arcade.color.WHITE, 25,font_name=fonte)
        arcade.draw_text("Matheus Caramuru", 180, 300,
                         arcade.color.PURPLE_HEART, 25,font_name=fonte)
        arcade.draw_text("Matheus Caramuru", 185, 300,
                         arcade.color.WHITE, 25,font_name=fonte)
        arcade.draw_text("Martin Lobe", 180, 250,
                         arcade.color.PURPLE_HEART, 25,font_name=fonte)
        arcade.draw_text("Martin Lobe", 185, 250,
                         arcade.color.WHITE, 25,font_name=fonte)
        arcade.draw_text("Sandy Hoffmann", 180, 200,
                         arcade.color.PURPLE_HEART, 25,font_name=fonte)
        arcade.draw_text("Sandy Hoffmann", 185, 200,
                         arcade.color.WHITE, 25,font_name=fonte)
        arcade.draw_text("Jogar Novamente - ENTER", 140, 50,
                         arcade.color.BARBIE_PINK, 25,font_name=fonte)
        arcade.draw_text("Jogar Novamente - ENTER", 145, 50,
                         arcade.color.WHITE, 25,font_name=fonte)
 