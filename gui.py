#gui.py
import tkinter as tk
import music_controller  
import threading # Allows running gesture control in background (allows running 2 things at same time (mulitithreading))

# Global variables for UI elements
root = None #main window
song_label = None #will show current song name
btn_pause = None #pause/resume button

def update_song_label():
    #Update the song name label
    if music_controller.songs and 0 <= music_controller.current_index < len(music_controller.songs):
        song_name = music_controller.songs[music_controller.current_index][0]  # Get the name part of the tuple
        song_label.config(text=song_name)
    else:
        song_label.config(text="No Song Playing")

def update_pause_button():
    #Update pause button icon
    if btn_pause:
        btn_pause.config(text="⏸️" if not music_controller.is_paused else "▶️")

def force_update_ui():
    """Update all UI elements"""
    update_song_label()
    update_pause_button()

def play_current_song():
    music_controller.playMusic()
    force_update_ui()

def toggle_pause_resume():
    music_controller.pause()
    force_update_ui()

def next_song():
    music_controller.play_next()
    force_update_ui()

def prev_song():
    music_controller.play_previous()
    force_update_ui()

def pause_or_resume():
    toggle_pause_resume()
    force_update_ui()

def start_gesture_control():
    #Runs gesture control in a separate thread
    def run_gesture():
        import gesture_control
        gesture_control.GestureController().run()
    
    gesture_thread = threading.Thread(target=run_gesture, daemon=True) #Start new thread (parallel running) for gesture control so that music player doesn't freeze
    gesture_thread.start()

def start_app():
    global root, song_label, btn_pause

    # Initialize window
    root = tk.Tk() #create the main window
    root.title("🎵 Music Player")
    root.geometry("800x600")
    root.configure(bg="#121212") #dark grey

    # Song display
    song_label = tk.Label(root, text="No Song Playing", 
                         font=("Arial", 24), fg="white", bg="#121212")
    song_label.pack(pady=50)

    # Control buttons
    controls_frame = tk.Frame(root, bg="#121212")
    controls_frame.pack() #keep all control buttons together

    #creating 4 buttons inside frame
    # Previous button
    btn_prev = tk.Button(controls_frame, text="⏮", font=("Arial", 30), 
                        fg="white", bg="#1DB954", bd=0,
                        command=prev_song)

    # Play button
    btn_play = tk.Button(controls_frame, text="▶", font=("Arial", 30),
                        fg="white", bg="#1DB954", bd=0,
                        command=play_current_song)

    # Pause/Resume button
    btn_pause = tk.Button(controls_frame, text="⏸️", font=("Arial", 30),
                         fg="white", bg="#1DB954", bd=0,
                         command=pause_or_resume)

    # Next button
    btn_next = tk.Button(controls_frame, text="⏭", font=("Arial", 30),
                        fg="white", bg="#1DB954", bd=0,
                        command=next_song)

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
    status_label = tk.Label(root, text=f"🎵 {len(music_controller.songs)} songs loaded",
                           font=("Arial", 12), fg="grey", bg="#121212")
    status_label.pack(side="bottom", pady=10)
    
    def update_ui():
        update_song_label()
        update_pause_button()
        root.after(100, update_ui)  # Updates every 100ms

    update_ui()  # Start the auto-update loop
    # play_current_song()  # <- Added this to directly play song when you run 
    root.mainloop() #This keeps the window open forever until you close it manually

if __name__ == "__main__":
    start_app()
