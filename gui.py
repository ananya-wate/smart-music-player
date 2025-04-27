#gui.py
import tkinter as tk
from music_controller import *
import os
import subprocess
import threading

# Global variables for UI elements
root = None
song_label = None
btn_pause = None

def update_song_label():
    """Update the song name label"""
    if songs and 0 <= current_index < len(songs):
        song_name = songs[current_index][0]  # Get the name part of the tuple
        song_label.config(text=song_name)
    else:
        song_label.config(text="No Song Playing")

def update_pause_button():
    """Update pause button icon"""
    if btn_pause:
        btn_pause.config(text="⏸️" if not is_paused else "▶️")

def force_update_ui():
    """Update all UI elements"""
    update_song_label()
    update_pause_button()
    root.update()

def play_current_song():
    playMusic()
    force_update_ui()

def toggle_pause_resume():
    pause()
    force_update_ui()

def start_gesture_control():
    """Runs gesture control in a separate thread."""
    def run_gesture():
        import gesture_control
        gesture_control.GestureController().run()
    
    gesture_thread = threading.Thread(target=run_gesture, daemon=True)
    gesture_thread.start()

def start_app():
    global root, song_label, btn_pause

    # Initialize window
    root = tk.Tk()
    root.title("🎵 Pro Music Player")
    root.geometry("800x600")
    root.configure(bg="#121212")

    # Song display
    song_label = tk.Label(root, text="No Song Playing", 
                         font=("Arial", 24), fg="white", bg="#121212")
    song_label.pack(pady=50)

    # Control buttons
    controls_frame = tk.Frame(root, bg="#121212")
    controls_frame.pack()

    # Previous button
    btn_prev = tk.Button(controls_frame, text="⏮", font=("Arial", 30), 
                        fg="white", bg="#1DB954", bd=0,
                        command=lambda: [play_previous(), force_update_ui()])

    # Play button
    btn_play = tk.Button(controls_frame, text="▶", font=("Arial", 30),
                        fg="white", bg="#1DB954", bd=0,
                        command=play_current_song)

    # Pause/Resume button
    btn_pause = tk.Button(controls_frame, text="⏸️", font=("Arial", 30),
                         fg="white", bg="#1DB954", bd=0,
                         command=toggle_pause_resume)

    # Next button
    btn_next = tk.Button(controls_frame, text="⏭", font=("Arial", 30),
                        fg="white", bg="#1DB954", bd=0,
                        command=lambda: [play_next(), force_update_ui()])

    # Layout buttons
    btn_prev.grid(row=0, column=0, padx=20)
    btn_play.grid(row=0, column=1, padx=20)
    btn_pause.grid(row=0, column=2, padx=20)
    btn_next.grid(row=0, column=3, padx=20)

    # Gesture control button
    btn_gesture = tk.Button(controls_frame, text="👆 Gesture Control",
                           font=("Arial", 14), fg="white", bg="#1DB954",
                           command=start_gesture_control)
    btn_gesture.grid(row=1, columnspan=4, pady=20)

    # Status bar
    status_label = tk.Label(root, text=f"🎵 {len(songs)} songs loaded",
                           font=("Arial", 12), fg="grey", bg="#121212")
    status_label.pack(side="bottom", pady=10)
    def update_ui():
        update_song_label()
        update_pause_button()
        root.after(100, update_ui)  # Updates every 100ms

    update_ui()  # Start the auto-update loop
    root.mainloop()

if __name__ == "__main__":
    start_app()