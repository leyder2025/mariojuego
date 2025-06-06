# mariobros/Game.py
import random
import tkinter as tk
from PIL import Image, ImageTk

from models import Jugador, Enemigo, Moneda, Hongo, Estrella # Using __init__.py
from utils import Constants
from utils.CollisionManager import CollisionManager
from utils.GameUtils import GameUtils

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Juego de Mario Extendido")

        self.game_state = Constants.GAME_STATE_MENU
        self.canvas = None
        self.menu_frame = None
        self.game_over_text_id = None
        self.restart_button_widget = None


        self.imgs = {}  # To store PhotoImage objects
        self.player = None
        self.stats_texts = {}

        self.goombas_en_pantalla = []
        self.objetos_beneficiosos = []
        self.monedas_activas = [] # Specifically for Moneda objects

        self.goombas_generados_total = 0
        self.monedas_creadas_total = 0
        
        self.special_mushrooms = [] # For the two fixed, hidden mushrooms

        self.collision_manager = CollisionManager(self)
        
        self.is_jumping = False
        self.jump_velocity = 0
        self.current_jump_step = 0
        self.gravity = 2 # Simple gravity effect

        self.setup_menu()
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release) # For smoother movement if needed
        self.keys_pressed = set()


    def load_images(self):
        try:
            # Player images
            self.imgs["player_small_r"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_SMALL_R}").resize(Constants.PLAYER_SMALL_SIZE))
            self.imgs["player_small_l"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_SMALL_L}").resize(Constants.PLAYER_SMALL_SIZE))
            self.imgs["player_move_r"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_MOVE_R}").resize(Constants.PLAYER_SMALL_SIZE))
            self.imgs["player_move_l"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_MOVE_L}").resize(Constants.PLAYER_SMALL_SIZE))
            
            # Try loading big mario images, fallback to small if specific ones not found or defined
            try:
                self.imgs["player_big_r"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_BIG_R}").resize(Constants.PLAYER_BIG_SIZE))
                # Assuming big left is similar or derived, add IMG_MARIO_BIG_L to Constants if specific
                self.imgs["player_big_l"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_BIG_L}").resize(Constants.PLAYER_BIG_SIZE)) if Constants.IMG_MARIO_BIG_L else self.imgs["player_big_r"]
            except FileNotFoundError:
                print(f"Warning: Big Mario images not found, using small as placeholder.")
                self.imgs["player_big_r"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_SMALL_R}").resize(Constants.PLAYER_BIG_SIZE))
                self.imgs["player_big_l"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_SMALL_L}").resize(Constants.PLAYER_BIG_SIZE))

            self.imgs["player_star"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_STAR}").resize(Constants.PLAYER_SMALL_SIZE)) # Or big size if star mario is big
            self.imgs["player_jump"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MARIO_JUMP}").resize(Constants.PLAYER_SMALL_SIZE))


            # Object images
            self.imgs["moneda"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_MONEDA}").resize(Constants.ITEM_SIZE))
            self.imgs["hongo_crecimiento"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_HONGO_ROJO}").resize(Constants.ITEM_SIZE))
            self.imgs["hongo_vida"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_HONGO_VERDE}").resize(Constants.ITEM_SIZE))
            self.imgs["estrella"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_ESTRELLA}").resize(Constants.ITEM_SIZE))

            # Enemy images
            self.imgs["goomba_café"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_GOOMBA_CAFE}").resize(Constants.GOOMBA_SIZE))
            self.imgs["goomba_negro"] = ImageTk.PhotoImage(Image.open(f"{Constants.ASSETS_DIR}{Constants.IMG_GOOMBA_NEGRO}").resize(Constants.GOOMBA_SIZE))
            print("Images loaded successfully.")
        except FileNotFoundError as e:
            print(f"Error loading images: {e}. Ensure all asset paths in Constants.py are correct and files exist.")
            self.root.destroy() # Can't run without images
            raise
        except Exception as e:
            print(f"An unexpected error occurred during image loading: {e}")
            self.root.destroy()
            raise


    def setup_menu(self):
        if self.canvas:
            self.canvas.destroy()
            self.canvas = None
        if self.menu_frame:
            self.menu_frame.destroy()

        self.game_state = Constants.GAME_STATE_MENU
        self.menu_frame = tk.Frame(self.root, bg="lightblue")
        tk.Label(self.menu_frame, text="Mario Bros Extendido", font=("Arial", 24), bg="lightblue").pack(pady=40)
        tk.Button(self.menu_frame, text="Iniciar Juego", command=self.start_game, font=("Arial", 16), width=20).pack(pady=20)
        tk.Button(self.menu_frame, text="Salir", command=self.root.quit, font=("Arial", 16), width=20).pack(pady=20)
        self.menu_frame.pack(fill="both", expand=True)

    def reset_game_state(self):
        # Clear lists
        for goom in self.goombas_en_pantalla:
            if goom.canvas_id and self.canvas: self.canvas.delete(goom.canvas_id)
        self.goombas_en_pantalla.clear()

        for obj in self.objetos_beneficiosos:
            if obj.canvas_id and self.canvas: self.canvas.delete(obj.canvas_id)
        self.objetos_beneficiosos.clear()
        
        for coin in self.monedas_activas:
            if coin.canvas_id and self.canvas: self.canvas.delete(coin.canvas_id)
        self.monedas_activas.clear()
        
        self.special_mushrooms.clear()


        # Reset counters
        self.goombas_generados_total = 0
        self.monedas_creadas_total = 0

        # Reset player
        if self.player:
            if self.player.canvas_id and self.canvas:
                 self.canvas.delete(self.player.canvas_id)
            self.player = None
        
        self.stats_texts.clear() # Will be recreated

        # Remove game over message if present
        if self.game_over_text_id and self.canvas:
            self.canvas.delete(self.game_over_text_id)
            self.game_over_text_id = None
        if self.restart_button_widget:
            self.restart_button_widget.destroy()
            self.restart_button_widget = None

        self.keys_pressed.clear()
        self.is_jumping = False
        self.jump_velocity = 0

    def start_game(self):
        self.reset_game_state()

        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = None

        if not self.canvas: # Create canvas if it doesn't exist
            self.canvas = tk.Canvas(self.root, width=Constants.SCREEN_WIDTH, height=Constants.SCREEN_HEIGHT, bg="skyblue")
        self.canvas.pack(pady=10) # Ensure it's packed
        self.canvas.focus_set() # For key bindings on canvas

        self.load_images() # Load images every time we start, in case of issues

        # Create Player
        player_start_x = Constants.SCREEN_WIDTH // 2
        player_start_y = Constants.OBJECT_FLOOR_Y_LIMIT - Constants.PLAYER_SMALL_SIZE[1] // 2 # Place on the floor
        self.player = Jugador(1, "Mario", player_start_x, player_start_y)
        self.player.on_ground = True # Start on ground
        self.add_player_to_canvas(self.player)
        self.update_player_sprite()

        # Initialize beneficial objects
        self.init_coins() # [cite: 2]
        self.init_special_mushrooms() # [cite: 5]
        # Could add random stars/other mushrooms here if desired, beyond the fixed ones

        self.game_state = Constants.GAME_STATE_RUNNING
        self.update_stats(self.player) # Initial stat display
        self.game_loop()


    def add_player_to_canvas(self, p):
        img = self.get_player_image_key()
        p.canvas_id = self.canvas.create_image(p.posicionX, p.posicionY, image=self.imgs[img], tags="player")
        self.update_player_sprite() # Ensure correct size on creation

        # Setup stats display
        self.stats_texts[p.id] = {}
        x0 = 10
        stat_attributes = ["Vidas", "Monedas", "Tamaño", "Inmunidad"]
        for i, attr_display_name in enumerate(stat_attributes):
            self.stats_texts[p.id][attr_display_name] = self.canvas.create_text(
                x0, 10 + i * 20, anchor="nw",
                text=f"{attr_display_name}: ...", font=("Arial", 10)
            )

    def get_player_image_key(self):
        p = self.player
        if p.estado_inmunidad:
            return "player_star"
        
        direction_suffix = "_l" if p.facing_direction == "izquierda" else "_r"
        
        if p.is_jumping and "player_jump" in self.imgs: # Add specific jump image if available
             return "player_jump" # Could also add direction to jump sprites

        # For moving, we might want specific move sprites if they differ from standing
        # For now, using small/big based on direction.
        # The original code had "inicial", "derecha", "izquierda"
        # Let's map current key presses to moving sprites
        if "Right" in self.keys_pressed or "Left" in self.keys_pressed:
             sprite_type = "player_move"
        else: # Standing still
             sprite_type = "player_small" if p.tamano == 'pequeño' else "player_big"


        if p.tamano == 'grande':
            return f"player_big{direction_suffix}" if f"player_big{direction_suffix}" in self.imgs else "player_big_r"
        else: # pequeño
            # If moving, use move sprites, otherwise use standing small sprites
            if "Right" in self.keys_pressed and f"player_move{direction_suffix}" in self.imgs:
                return f"player_move{direction_suffix}"
            if "Left" in self.keys_pressed and f"player_move{direction_suffix}" in self.imgs:
                return f"player_move{direction_suffix}"
            return f"player_small{direction_suffix}" if f"player_small{direction_suffix}" in self.imgs else "player_small_r"


    def update_player_sprite(self):
        if not self.player or not self.player.canvas_id or not self.canvas:
            return
        
        p = self.player
        p.update_size() # Update logical width/height based on tamano
        img_key = self.get_player_image_key()
        
        if img_key in self.imgs:
            try:
                self.canvas.itemconfig(p.canvas_id, image=self.imgs[img_key])
            except tk.TclError: # Canvas item might have been deleted
                print("Error updating player sprite: canvas item not found.")
                p.canvas_id = None # Mark as no longer on canvas
        else:
            print(f"Warning: Image key '{img_key}' not found in self.imgs.")


    def update_stats(self, p):
        if not self.canvas or not p or p.id not in self.stats_texts: return
        
        try:
            self.canvas.itemconfig(self.stats_texts[p.id]["Vidas"], text=f"Vidas: {p.vidas}")
            self.canvas.itemconfig(self.stats_texts[p.id]["Monedas"], text=f"Monedas: {p.monedas_recogidas}/{Constants.TOTAL_COINS}")
            self.canvas.itemconfig(self.stats_texts[p.id]["Tamaño"], text=f"Tamaño: {p.tamano.capitalize()}")
            inmunidad_status = "Activa" if p.estado_inmunidad else "No"
            if p.estado_inmunidad:
                inmunidad_status += f" ({p.tiempo_inmunidad_restante // 1000}s)"
            self.canvas.itemconfig(self.stats_texts[p.id]["Inmunidad"], text=f"Inmunidad: {inmunidad_status}")
        except tk.TclError:
            print("Error updating stats: Tkinter item likely deleted.")


    def init_coins(self): # [cite: 2]
        self.monedas_activas.clear() # Clear previous coins if any
        self.monedas_creadas_total = 0
        for _ in range(Constants.TOTAL_COINS):
            if self.monedas_creadas_total < Constants.TOTAL_COINS:
                # Ensure coins spawn above the floor limit [cite: 1]
                # And not on top of each other too much - simple random for now
                x = random.randint(Constants.ITEM_SIZE[0], Constants.SCREEN_WIDTH - Constants.ITEM_SIZE[0])
                y = random.randint(Constants.ITEM_SIZE[1], Constants.OBJECT_FLOOR_Y_LIMIT - Constants.ITEM_SIZE[1])
                
                nueva_moneda = Moneda(x, y)
                nueva_moneda.canvas_id = self.canvas.create_image(x, y, image=self.imgs["moneda"], tags="moneda")
                self.objetos_beneficiosos.append(nueva_moneda)
                self.monedas_activas.append(nueva_moneda)
                self.monedas_creadas_total +=1


    def init_special_mushrooms(self): # [cite: 5]
        self.special_mushrooms.clear()
        
        # Growth Mushroom (Red)
        hx_g, hy_g = Constants.FIXED_GROWTH_MUSHROOM_POS
        hongo_crecimiento = Hongo(hx_g, hy_g, "crecimiento", fijo=True, oculto_inicialmente=True)
        # Not drawn initially, drawn when revealed.
        self.objetos_beneficiosos.append(hongo_crecimiento)
        self.special_mushrooms.append(hongo_crecimiento)

        # Life Mushroom (Green)
        hx_l, hy_l = Constants.FIXED_LIFE_MUSHROOM_POS
        hongo_vida = Hongo(hx_l, hy_l, "vida", fijo=True, oculto_inicialmente=True)
        self.objetos_beneficiosos.append(hongo_vida)
        self.special_mushrooms.append(hongo_vida)

    def spawn_estrella_aleatoria(self):
        # Example: Randomly spawn a star if not too many items exist
        if len(self.objetos_beneficiosos) < (Constants.TOTAL_COINS + 3): # Limit total beneficial items
            x = random.randint(Constants.ITEM_SIZE[0], Constants.SCREEN_WIDTH - Constants.ITEM_SIZE[0])
            y = random.randint(Constants.ITEM_SIZE[1], Constants.OBJECT_FLOOR_Y_LIMIT - Constants.ITEM_SIZE[1]) # [cite: 1]
            estrella = Estrella(x,y)
            estrella.canvas_id = self.canvas.create_image(x,y, image=self.imgs["estrella"], tags="estrella")
            self.objetos_beneficiosos.append(estrella)


    def spawn_goomba(self):
        if len(self.goombas_en_pantalla) < Constants.MAX_GOOMBAS_ON_SCREEN and \
           self.goombas_generados_total < Constants.TOTAL_GOOMBAS_TO_SPAWN: # [cite: 12, 13]
            
            # Spawn on the right side, above floor [cite: 10]
            x = Constants.SCREEN_WIDTH + Constants.GOOMBA_SPAWN_X_OFFSET 
            y = Constants.OBJECT_FLOOR_Y_LIMIT - Constants.GOOMBA_SIZE[1] // 2 # Goomba's feet on floor
            
            nuevo_goomba = Enemigo(f"goomba_{self.goombas_generados_total}", x, y) # Visual type is random in Enemigo class [cite: 9]
            img_key = f"goomba_{nuevo_goomba.tipo_visual}"
            
            if img_key not in self.imgs: # Fallback if specific visual type image is missing
                print(f"Warning: Image for Goomba type '{nuevo_goomba.tipo_visual}' not found. Using cafe as default.")
                img_key = "goomba_café"

            nuevo_goomba.canvas_id = self.canvas.create_image(x, y, image=self.imgs[img_key], tags="enemigo")
            self.goombas_en_pantalla.append(nuevo_goomba)
            self.goombas_generados_total += 1


    def update_goombas(self):
        goombas_a_eliminar = []
        for goomba in self.goombas_en_pantalla:
            goomba.mover() # [cite: 10]
            if goomba.canvas_id and self.canvas:
                try:
                    self.canvas.coords(goomba.canvas_id, goomba.posicionX, goomba.posicionY)
                except tk.TclError: # Item might have been deleted
                    goomba.canvas_id = None # Mark as no longer on canvas

            if goomba.ha_llegado_al_borde_izquierdo(): # [cite: 11]
                goombas_a_eliminar.append(goomba)
        
        for goomba in goombas_a_eliminar:
            if goomba.canvas_id and self.canvas:
                try: self.canvas.delete(goomba.canvas_id)
                except tk.TclError: pass
            self.goombas_en_pantalla.remove(goomba)

    def update_special_mushrooms(self):
        for hongo in self.special_mushrooms:
            if isinstance(hongo, Hongo) and hongo.fijo:
                if hongo.oculto: # Check if player is "touching" the hidden spot
                    # A simpler check for "revealing" can be proximity to its fixed location
                    if self.collision_manager.check_aabb_collision(self.player, hongo): # Using hongo's logical bbox
                        if hongo.revelar(): # If it was successfully revealed (was hidden)
                            # Draw it on canvas if not already drawn or if state changed
                            img_key = f"hongo_{hongo.tipo_hongo}"
                            if hongo.canvas_id is None and self.canvas:
                                hongo.canvas_id = self.canvas.create_image(hongo.posicionX, hongo.posicionY, image=self.imgs[img_key], tags="hongo")
                            elif hongo.canvas_id and self.canvas:
                                self.canvas.itemconfig(hongo.canvas_id, state='normal', image=self.imgs[img_key])
                
                elif hongo.visible: # If revealed, update its timer
                     hongo.actualizar_visibilidad(Constants.GAME_UPDATE_INTERVAL, self)
                     # If it became hidden by the update, game.py will handle canvas item state via hongo.actualizar_visibilidad


    def apply_gravity_to_player(self):
        if not self.player or not self.canvas: return

        if not self.player.on_ground:
            self.player.posicionY += self.jump_velocity
            self.jump_velocity += self.gravity
        
        # Check for landing on the "floor"
        player_bottom_edge = self.player.posicionY + self.player.height / 2
        
        if player_bottom_edge >= Constants.OBJECT_FLOOR_Y_LIMIT:
            self.player.posicionY = Constants.OBJECT_FLOOR_Y_LIMIT - self.player.height / 2
            self.player.on_ground = True
            self.player.is_jumping = False
            self.jump_velocity = 0
            self.update_player_sprite() # Player landed, update sprite possibly from jump to standing

        if self.player.canvas_id:
            try:
                self.canvas.coords(self.player.canvas_id, self.player.posicionX, self.player.posicionY)
            except tk.TclError:
                self.player.canvas_id = None # Player removed from canvas somehow

    def game_loop(self):
        if self.game_state != Constants.GAME_STATE_RUNNING:
            return

        # Player movement from keys_pressed
        if "Left" in self.keys_pressed:
            self.move_player(-Constants.PLAYER_STEP_X, 0)
        if "Right" in self.keys_pressed:
            self.move_player(Constants.PLAYER_STEP_X, 0)
        
        # Apply gravity and update jump state
        self.apply_gravity_to_player()

        # Player immunity update
        if self.player.actualizar_inmunidad(Constants.GAME_UPDATE_INTERVAL):
             self.update_player_sprite() # Immunity ended, change sprite

        # Spawn enemies
        if random.random() < 0.02: # Probability to spawn goomba
            self.spawn_goomba()
        
        # Randomly spawn a star (example logic)
        if random.random() < 0.002:
            self.spawn_estrella_aleatoria()

        # Update game elements
        self.update_goombas()
        self.update_special_mushrooms()

        # Check collisions
        self.check_all_collisions()

        # Update displayed stats
        if self.player:
            self.update_stats(self.player)

        # Schedule next game loop iteration
        self.root.after(Constants.GAME_UPDATE_INTERVAL, self.game_loop)


    def on_key_press(self, event):
        if self.game_state != Constants.GAME_STATE_RUNNING or not self.player:
            return
        
        key = event.keysym
        self.keys_pressed.add(key) # Add key to set of pressed keys

        if key == "Up" and self.player.on_ground:
            self.player.is_jumping = True
            self.player.on_ground = False
            self.jump_velocity = -20 # Initial upward velocity (higher is smaller jump with this gravity)
            self.update_player_sprite() # Change to jump sprite
        
        elif key == "Left":
            self.player.facing_direction = "izquierda"
            self.update_player_sprite() # Change to moving left sprite
            # self.move_player(-Constants.PLAYER_STEP_X, 0) # Movement handled by game_loop from keys_pressed

        elif key == "Right":
            self.player.facing_direction = "derecha"
            self.update_player_sprite() # Change to moving right sprite
            # self.move_player(Constants.PLAYER_STEP_X, 0) # Movement handled by game_loop from keys_pressed
        
        # No direct move on key press, use flags in game_loop for continuous movement

    def on_key_release(self, event):
        if self.game_state != Constants.GAME_STATE_RUNNING or not self.player:
            return
        key = event.keysym
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        
        # Update sprite if movement key released and no other movement key is pressed
        if key in ["Left", "Right"] and not ("Left" in self.keys_pressed or "Right" in self.keys_pressed):
            self.update_player_sprite() # Change to standing sprite

    def move_player(self, dx, dy):
        if not self.player or not self.player.canvas_id or not self.canvas: return

        # Store old position for revert if collision with non-traversable
        old_x, old_y = self.player.posicionX, self.player.posicionY

        self.player.mover(dx, dy)

        # Boundary checks for screen edges
        player_half_width = self.player.width / 2
        if self.player.posicionX - player_half_width < 0:
            self.player.posicionX = player_half_width
        if self.player.posicionX + player_half_width > Constants.SCREEN_WIDTH:
            self.player.posicionX = Constants.SCREEN_WIDTH - player_half_width
        
        # Vertical boundaries (e.g. prevent going above screen, floor is handled by gravity)
        player_half_height = self.player.height / 2
        if self.player.posicionY - player_half_height < 0:
            self.player.posicionY = player_half_height
        # Max height/floor is handled by gravity and OBJECT_FLOOR_Y_LIMIT

        try:
            self.canvas.coords(self.player.canvas_id, self.player.posicionX, self.player.posicionY)
        except tk.TclError:
            self.player.canvas_id = None


    def check_all_collisions(self):
        if not self.player or not self.canvas: return

        # Player vs Enemies
        for goomba in list(self.goombas_en_pantalla): # Iterate over a copy for safe removal
            if goomba.canvas_id and self.collision_manager.check_aabb_collision(self.player, goomba):
                self.collision_manager.handle_player_enemy_collision(self.player, goomba)
                # Player.interact_con_goomba might trigger game over or remove goomba (e.g. if player jumps on it - not implemented)
                # For now, Goomba is not removed on collision unless player is star powered (future feature)
                if self.player.estado_inmunidad and goomba in self.goombas_en_pantalla: # Example: star player defeats goomba
                    if goomba.canvas_id: self.canvas.delete(goomba.canvas_id)
                    self.goombas_en_pantalla.remove(goomba)
                break # Process one goomba collision per frame to avoid multiple hits

        # Player vs Beneficial Objects
        collected_objects = []
        for objeto in self.objetos_beneficiosos:
            if objeto.visible and objeto.canvas_id and self.collision_manager.check_aabb_collision(self.player, objeto):
                self.collision_manager.handle_player_objeto_collision(self.player, objeto)
                collected_objects.append(objeto)
                
                # Specific logic after collection
                if isinstance(objeto, Moneda):
                    if self.player.monedas_recogidas % Constants.COIN_COUNT_FOR_EXTRA_LIFE == 0 and self.player.monedas_recogidas > 0:
                        # Check if all *initial* coins are collected
                        # This check might be better if we track total unique coins available
                        active_monedas = [m for m in self.objetos_beneficiosos if isinstance(m, Moneda) and m.visible]
                        if not active_monedas: # If this was the last coin
                             self.player.ganar_vida() # [cite: 3]
                             print("Todas las monedas recogidas! Vida extra!")
                             # Potentially respawn coins or end coin collection
                
                elif isinstance(objeto, Hongo):
                    self.update_player_sprite() # Mushroom might change player size
                
                elif isinstance(objeto, Estrella):
                    self.update_player_sprite() # Star changes player sprite

        for obj in collected_objects:
            if obj.canvas_id and self.canvas:
                try: self.canvas.delete(obj.canvas_id)
                except tk.TclError: pass
            if obj in self.objetos_beneficiosos: self.objetos_beneficiosos.remove(obj)
            if isinstance(obj, Moneda) and obj in self.monedas_activas: self.monedas_activas.remove(obj)
            if obj in self.special_mushrooms and not obj.oculto : # If it was a special mushroom that was collected
                obj.visible = False # It's gone
                # It won't respawn unless re-initialized

    def game_over(self):
        self.game_state = Constants.GAME_STATE_GAME_OVER
        print("GAME OVER triggered in Game class") # [cite: 15]
        if self.canvas:
            GameUtils.show_game_over_message(self.canvas, self)
            # Add a delay then go back to menu or show restart options
            self.root.after(3000, self.setup_menu) # Go back to menu after 3 seconds
        else: # Fallback if canvas is not available
            self.setup_menu()

    def run(self):
        self.root.mainloop()