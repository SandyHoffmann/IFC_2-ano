from objetos.objeto import Objeto
import random

class Powerup(Objeto):

    def __init__(self, imagem,center_x=0, center_y=0, vetor_y = 0):
        dimensao_imagem = 1
        self.vetor_y = vetor_y
        

        super().__init__(imagem, dimensao_imagem, center_x, center_y)

    def moverpowerup(self):
        self.center_y -= self.vetor_y