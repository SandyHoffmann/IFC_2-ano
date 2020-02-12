from objetos.objeto import Objeto
import random

class Bola(Objeto):

    def __init__(self, center_x=0, center_y=0,vetor_x=0):
        imagem = 'jogo/bola/imagens/bola.png'
        dimensao_imagem = 0.25
        self.vetor_y = 10
        self.vetor_x = vetor_x
        super().__init__(imagem, dimensao_imagem, center_x, center_y)

    def moverbola(self):
        self.center_x += self.vetor_x
        self.center_y += self.vetor_y


