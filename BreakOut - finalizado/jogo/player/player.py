import arcade
from objetos.objeto import Objeto

class Player(Objeto):

    def __init__(self, imagem, zoom , vetor_x, esquerda , direita , x , y ):
        super().__init__(imagem, zoom)
        self.vetor_x = vetor_x
        self.esquerda = esquerda
        self.direita = direita
        self.center_x = x
        self.center_y = y

    def load_images(self, imagem, zoom):
        self.andar = []
        self.andar.append(arcade.load_texture('jogo/player/imagens/barra_normal.png'))

    def on_key_press(self, key, modifiers):
        if key == self.direita:
            self.change_x = self.vetor_x
        elif key == self.esquerda:
            self.change_x = -self.vetor_x
    def on_key_release(self, key, modifiers):
        if key == self.direita or key == self.esquerda:
            self.change_x = 0
