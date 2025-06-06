# mariobros/models/Hongo.py
from .ObjetoBeneficioso import ObjetoBeneficioso
from utils.Constants import MUSHROOM_APPEAR_TIME_MS

class Hongo(ObjetoBeneficioso):
    def __init__(self, x, y, tipo_hongo, fijo=False, oculto_inicialmente=False): # tipo_hongo: "crecimiento" or "vida" [cite: 4]
        super().__init__(x, y, f"hongo_{tipo_hongo}")
        self.tipo_hongo = tipo_hongo
        self.fijo = fijo # Is this one of the fixed, hidden mushrooms?
        self.oculto = oculto_inicialmente
        self.tiempo_visible_restante = 0
        if self.oculto:
            self.visible = False

    def aplicar_efecto(self, jugador, game):
        if self.tipo_hongo == "crecimiento":
            jugador.crecer() # [cite: 4]
        elif self.tipo_hongo == "vida":
            jugador.ganar_vida() # [cite: 4]
        print(f"Efecto de hongo {self.tipo_hongo} aplicado.")

    def revelar(self):
        """Reveals a hidden mushroom for a limited time."""
        if self.oculto and not self.visible: # [cite: 5]
            self.visible = True
            self.tiempo_visible_restante = MUSHROOM_APPEAR_TIME_MS # [cite: 5]
            print(f"Hongo {self.tipo_hongo} revelado en ({self.posicionX}, {self.posicionY})")
            return True
        return False

    def actualizar_visibilidad(self, delta_tiempo_ms, game):
        if self.fijo and self.visible and self.tiempo_visible_restante > 0:
            self.tiempo_visible_restante -= delta_tiempo_ms
            if self.tiempo_visible_restante <= 0:
                self.visible = False
                self.oculto = True # Reset to hidden state
                self.tiempo_visible_restante = 0
                print(f"Hongo {self.tipo_hongo} en ({self.posicionX}, {self.posicionY}) se ocultó.")
                # Update canvas (Game class should handle this)
                if self.canvas_id and game.canvas:
                    game.canvas.itemconfig(self.canvas_id, state='hidden')