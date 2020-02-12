from objetos.objeto import Objeto

class Bloco(Objeto):
    def __init__(self,center_x=0, center_y=0,direcao=0,imagem = 'jogo/objetos/imagens/bloco.png'):
        dimensao_imagem =1
        super().__init__(imagem, dimensao_imagem, center_x, center_y)

