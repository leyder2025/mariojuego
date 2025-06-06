# mariobros/models/Estrella.py
from .ObjetoBeneficioso import ObjetoBeneficioso

class Estrella(ObjetoBeneficioso):
    def __init__(self, x, y):
        super().__init__(x, y, "estrella")

    def aplicar_efecto(self, jugador, game):
        jugador.activar_inmunidad() # [cite: 6]