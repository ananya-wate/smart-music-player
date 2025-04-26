import pygame
import os

# Initialize mixer
pygame.mixer.init()

songs = [
    "songs/song1.mp3",
    "songs/song2.mp3",
    "songs/song3.mp3",
    "songs/song4.mp3"
]

current_index = 0
is_playing = False
is_paused = False

def setPlaylist(new_playlist):
    global songs
    songs = new_playlist

def playMusic():
    global is_playing, is_paused
    if is_paused:
        resumeMusic()  # If paused, resume instead of restarting
        return
    pygame.mixer.music.load(songs[current_index])
    pygame.mixer.music.play()
    is_playing = True
    is_paused = False  # Ensuring paused is False when playing
    print(f"Playing: {songs[current_index]}")
    

def pause():
    global is_playing, is_paused
    if is_playing and not is_paused:
        pygame.mixer.music.pause()
        is_paused = True
        print("Paused ⏸️")
    elif is_paused:  # If already paused, resume instead
        resumeMusic()

def resumeMusic():
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        print("Resumed ▶️")

def play_next():
    global current_index, is_playing, is_paused
    if current_index < len(songs) - 1:
        current_index += 1
        playMusic()
    else:
        print("Already at last song 🎵")

def play_previous():
    global current_index, is_playing, is_paused
    if current_index > 0:
        current_index -= 1
        playMusic()
    else:
        print("Already at first song 🎵")