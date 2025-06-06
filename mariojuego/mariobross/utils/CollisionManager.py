# mariobros/utils/CollisionManager.py

class CollisionManager:
    def __init__(self, game):
        self.game = game # Reference to the main game instance

    def check_aabb_collision(self, item1, item2):
        """
        Checks for Axis-Aligned Bounding Box collision.
        Assumes items have get_bbox() method returning [x1, y1, x2, y2].
        """
        if not item1 or not item2: # one of the items might be None
            return False
        
        # Ensure canvas_id exists and items are active/visible on canvas for item1
        # (especially if it's a player or enemy that could be removed)
        # For item2 (like a collectible), ensure it's visible if it has such a property
        if hasattr(item1, 'canvas_id') and not item1.canvas_id: return False
        if hasattr(item2, 'canvas_id') and not item2.canvas_id: return False
        if hasattr(item2, 'visible') and not item2.visible: return False


        # Use canvas bbox for more accurate collision with Tkinter items if available
        # and the item is drawn on canvas. Otherwise, use logical bbox.
        try:
            if item1.canvas_id and self.game.canvas:
                bbox1 = self.game.canvas.bbox(item1.canvas_id)
            else:
                bbox1 = item1.get_bbox()

            if item2.canvas_id and self.game.canvas:
                bbox2 = self.game.canvas.bbox(item2.canvas_id)
            else:
                bbox2 = item2.get_bbox()
            
            if not bbox1 or not bbox2: # Bbox might be None if item not on canvas
                return False

        except Exception: # Item might have been deleted from canvas
            return False


        # bbox1: [x1_1, y1_1, x2_1, y2_1]
        # bbox2: [x1_2, y1_2, x2_2, y2_2]
        # Check for overlap
        overlap_x = bbox1[0] < bbox2[2] and bbox1[2] > bbox2[0]
        overlap_y = bbox1[1] < bbox2[3] and bbox1[3] > bbox2[1]
        
        return overlap_x and overlap_y

    def handle_player_enemy_collision(self, jugador, enemigo):
        # Player-enemy collision logic based on PDF [cite: 14, 15, 16, 17]
        # This is now mostly handled in Jugador.interactuar_con_goomba
        # This method can be a wrapper or be removed if logic is fully in Jugador
        print(f"Collision check between {jugador.nombre} and {enemigo.nombre}")
        if jugador.interactuar_con_goomba(self.game):
            # Game over was triggered
            pass

    def handle_player_objeto_collision(self, jugador, objeto):
        print(f"Collision check between {jugador.nombre} and {objeto.tipo}")
        objeto.aplicar_efecto(jugador, self.game)
        # Game class will handle removing the object from screen and list