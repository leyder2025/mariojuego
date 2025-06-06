# mariobros/models/Jugador.py
from .Personaje import Personaje
from utils.Constants import PLAYER_INITIAL_LIVES, STAR_DURATION_MS, PLAYER_SMALL_SIZE, PLAYER_BIG_SIZE

class Jugador(Personaje):
    def __init__(self, id_char, nombre, x=0, y=0):
        super().__init__(id_char, nombre, x, y)
        self.vidas = PLAYER_INITIAL_LIVES
        self.monedas_recogidas = 0
        self.puntos = 0 # Not specified in PDF, but exists in base.
        self.tiempo = 300 # Not specified in PDF, but exists in base.
        self.tamano = 'pequeño'  # 'pequeño' or 'grande'
        self.estado_inmunidad = False
        self.tiempo_inmunidad_restante = 0 # in milliseconds
        self.is_jumping = False
        self.jump_velocity = 0
        self.on_ground = True # True if player is on a surface
        self.facing_direction = "derecha" # "izquierda" o "derecha"
        self.update_size()

    def update_size(self):
        if self.tamano == 'grande':
            self.width, self.height = PLAYER_BIG_SIZE
        else: # pequeño or any other state
            self.width, self.height = PLAYER_SMALL_SIZE

    def recoger_moneda(self):
        self.monedas_recogidas += 1
        # Logic for extra life if all coins collected is handled in Game.py [cite: 3]

    def crecer(self):
        if self.tamano == 'pequeño':
            self.tamano = 'grande'
            self.update_size()
            print("Jugador crece a grande") # For debugging
            return True # Indicates change happened
        return False

    def encoger(self):
        if self.tamano == 'grande':
            self.tamano = 'pequeño'
            self.update_size()
            print("Jugador encoge a pequeño") # For debugging
            return True # Indicates change happened
        # If already small, no change in size, but might lose life or game over
        return False

    def activar_inmunidad(self):
        self.estado_inmunidad = True
        self.tiempo_inmunidad_restante = STAR_DURATION_MS
        print("Jugador obtiene inmunidad") # For debugging

    def actualizar_inmunidad(self, delta_tiempo_ms):
        if self.estado_inmunidad:
            self.tiempo_inmunidad_restante -= delta_tiempo_ms
            if self.tiempo_inmunidad_restante <= 0:
                self.estado_inmunidad = False
                self.tiempo_inmunidad_restante = 0
                print("Inmunidad del jugador terminada") # For debugging
                return True # Immunity ended
        return False # Immunity continues or was not active

    def perder_vida(self):
        self.vidas -= 1
        print(f"Jugador pierde una vida. Vidas restantes: {self.vidas}") # For debugging
        if self.vidas <= 0:
            self.estado = "Muerto" # Or handle game over
            return True # Player is out of lives
        return False # Player still has lives

    def ganar_vida(self):
        self.vidas += 1
        print(f"Jugador gana una vida. Vidas totales: {self.vidas}")

    def interactuar_con_goomba(self, game):
        if self.estado_inmunidad:
            print("Jugador inmune choca con Goomba, sin efecto.") # [cite: 17]
            return False # No game over

        if self.encoger(): # Player was big, now small [cite: 14]
            pass # Size changed, no life lost yet
        else: # Player was already small
            if self.vidas == 1: # Was small and only one life
                print("Jugador pequeño con 1 vida choca con Goomba. Game Over.") # [cite: 15]
                self.perder_vida() # This will set lives to 0
                game.game_over() # Notify game to end
                return True # Game Over
            else: # Was small, more than one life
                self.perder_vida() # [cite: 16]
        return False # Game not over from this interaction