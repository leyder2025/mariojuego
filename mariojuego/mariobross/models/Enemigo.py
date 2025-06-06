# mariobros/models/Enemigo.py
import random
from .Personaje import Personaje # Using Personaje for position and canvas_id
from utils.Constants import GOOMBA_SPEED, GOOMBA_SIZE

class Enemigo(Personaje): # [cite: 7]
    def __init__(self, id_char, x, y, tipo_visual=None): # tipo_visual: "café" or "negro" [cite: 8]
        # For Goombas, nombre would be "Goomba"
        super().__init__(id_char, "Goomba", x, y)
        if tipo_visual is None:
            self.tipo_visual = random.choice(["café", "negro"]) # [cite: 9]
        else:
            self.tipo_visual = tipo_visual
        self.velocidad = GOOMBA_SPEED
        self.width, self.height = GOOMBA_SIZE

    def mover(self):
        super().mover(dx=-self.velocidad) # Se desplazan hacia la izquierda [cite: 10]

    def ha_llegado_al_borde_izquierdo(self):
        # Check based on its right edge, or center, depending on spawn logic
        # Assuming posicionX is center, and width is known
        return self.posicionX + (self.width / 2) < 0 # [cite: 11]