# mariobros/models/Moneda.py
from .ObjetoBeneficioso import ObjetoBeneficioso

class Moneda(ObjetoBeneficioso):
    def __init__(self, x, y):
        super().__init__(x, y, "moneda")

    def aplicar_efecto(self, jugador, game):
        jugador.recoger_moneda() # [cite: 3]
        print(f"Moneda recogida. Total monedas: {jugador.monedas_recogidas}")
        # The game will check if all 10 are collected to give a life [cite: 3]