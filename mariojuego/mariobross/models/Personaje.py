# mariobros/models/Personaje.py
class Personaje:
    def __init__(self, id_char, nombre, x, y, estado="Vivo"):
        self.id = id_char
        self.nombre = nombre
        self.posicionX = x
        self.posicionY = y
        self.estado = estado  # "Vivo", "Muerto"
        self.canvas_id = None # For Tkinter canvas item ID
        self.width = 0
        self.height = 0

    def mover(self, dx=0, dy=0):
        self.posicionX += dx
        self.posicionY += dy

    def get_bbox(self):
        """Returns the bounding box [x1, y1, x2, y2] for the character."""
        half_width = self.width / 2
        half_height = self.height / 2
        return [
            self.posicionX - half_width,
            self.posicionY - half_height,
            self.posicionX + half_width,
            self.posicionY + half_height
        ]