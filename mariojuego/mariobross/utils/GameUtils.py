# mariobros/utils/GameUtils.py
import tkinter as tk

class GameUtils:
    @staticmethod
    def show_game_over_message(canvas, game_instance):
        # Clear existing "Game Over" messages if any
        if hasattr(game_instance, 'game_over_text_id') and game_instance.game_over_text_id:
            canvas.delete(game_instance.game_over_text_id)
        if hasattr(game_instance, 'restart_button_id') and game_instance.restart_button_id:
            game_instance.restart_button_id.destroy()


        screen_width = canvas.winfo_width()
        screen_height = canvas.winfo_height()
        
        if screen_width <= 1 or screen_height <=1: # Canvas not ready
            canvas.after(100, lambda: GameUtils.show_game_over_message(canvas, game_instance))
            return

        text_id = canvas.create_text(
            screen_width / 2,
            screen_height / 2 - 30,
            text="¡Juego Terminado!", # [cite: 15]
            font=("Arial", 30, "bold"),
            fill="red",
            tags="game_over_message"
        )
        game_instance.game_over_text_id = text_id
        
        # Simple restart button (optional, or can be handled by main menu logic)
        # This example adds a Tkinter button on top of the canvas.
        # For better integration, one might draw a button-like rectangle on the canvas
        # and bind click events.
        
        # restart_btn = tk.Button(canvas.master, text="Reiniciar", command=game_instance.restart_game)
        # game_instance.restart_button_window_id = canvas.create_window(
        #     screen_width / 2,
        #     screen_height / 2 + 30,
        #     window=restart_btn
        # )
        # game_instance.restart_button_widget = restart_btn # Store to destroy later

        print("Mensaje de Game Over mostrado.")