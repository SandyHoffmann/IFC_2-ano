import arcade

class Objeto(arcade.Sprite):
    
    def __init__(self, imagem, dimensao_imagem, center_x=0, center_y=0):
        super().__init__(imagem, dimensao_imagem)
        self.center_x = center_x
        self.center_y = center_y