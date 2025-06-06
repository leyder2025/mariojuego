# mariobros/models/ObjetoBeneficioso.py
from .Personaje import Personaje # Using Personaje for position and canvas_id
from utils.Constants import ITEM_SIZE

class ObjetoBeneficioso:
    def __init__(self, x, y, tipo, visible=True):
        self.posicionX = x
        self.posicionY = y
        self.tipo = tipo # e.g., "moneda", "hongo_vida", "hongo_crecimiento", "estrella"
        self.visible = visible
        self.canvas_id = None
        self.width, self.height = ITEM_SIZE

    def aplicar_efecto(self, jugador, game):
        """Placeholder for applying effect. To be overridden by subclasses."""
        pass

    def get_bbox(self):
        """Returns the bounding box [x1, y1, x2, y2] for the object."""
        # Assuming posicionX, posicionY are center points
        half_width = self.width / 2
        half_height = self.height / 2
        return [
            self.posicionX - half_width,
            self.posicionY - half_height,
            self.posicionX + half_width,
            self.posicionY + half_height
        ]